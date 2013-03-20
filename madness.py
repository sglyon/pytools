"""
Created Mar 16, 2013

Author: Spencer Lyon

File to gather/examine college basketball data for march madness

Playing style
-------------
offense (do these items per point to get relative weights)
    - Fast break (free throws, paint) [3, 2, 1, 4]
    - Pick and Roll (assists, paint) [4, 3, 2, 1]
    - 3 Point (pts. from 3s) [1, 2, 3, 4]
    - Paint (pts in paint, rebs, ft) [2, 4, 3, 1]

defense
    - Zone
    - press (steals)
    - Rebounds (off, def)
    - Man

Intangibles
-----------
- Playing style
- Current 12 game streak
- Previous meeting (favor loser)
- underdog factor (GB2 - McDonald Distribution)
- Average age (by class: freshman, sophomore)

Data
----
- RPI stats
    - SOS
    - RPI
    - W-L top 25 and 50
    - W-L below 100
    - Home/away/neutral (focus on away neutral)
    - Margin
- Box score
    - Player/Team stats per game (use team for playing style)
    - Previous meeting
    - AR(x) for continuation of winning streak
"""
import re
import shelve
from pprint import pformat
from urllib2 import urlopen
import pandas as pd
from pandas.io.parsers import TextParser
from lxml.html import parse

# Show wider columns!
pd.set_option('line_width', 180)


class Team(object):
    def __init__(self, name, team_id, rank, region):
        self.name = name
        self.team_id = team_id
        self.rank = rank
        self.region = region

        self.get_sched()
        self.get_rpi()
        self.get_scores()

        tourney.register_team(self)

    def __repr__(self):
        msg = 'Team: %s -- ' % (self.name)
        msg += 'Rank: %i -- ' % (self.rank)
        msg += 'Region: %s' % (self.region)
        return msg

    def __str__(self):
        msg = 'Rank: %i\n' % (self.rank)
        msg += 'Region: %s' % (self.region)
        return msg

    def get_sched(self):
        sched = _parse_schedule(self.team_id)
        self.sched_frame = sched
        return sched

    def get_rpi(self):
        rpi = _parse_rpi_table(self.team_id)
        self.rpi_frame = rpi
        return rpi

    def get_scores(self):
        try:
            games = self.sched_frame.GameId.values
        except AttributeError:
            self.get_sched()
            games = self.sched_frame.GameId.values

        first = games[0]

        for i in games:
            temp = _parse_box_score(i)
            if i == first:
                if not re.match(self.name, temp[0].index[0]):
                    boxes = temp[0]
                else:
                    boxes = temp[1]
            else:
                if not re.match(self.name, temp[0].index[0]):
                    boxes = pd.concat([boxes, temp[0]])
                else:
                    boxes = pd.concat([boxes, temp[1]])

        boxes['PA'] = self.sched_frame.PointsAgainst.values
        boxes['WL'] = self.sched_frame.WinLoss.values

        boxes.columns.name = 'Stat'

        multi_ind = pd.MultiIndex.from_arrays([[self.name] * boxes.shape[0],
                                                 boxes.index])
        box_scores = pd.DataFrame(boxes.values,
                                  columns=boxes.columns,
                                  index=multi_ind)
        box_scores.index.names = ['Team', 'Opponent']

        self.box_scores = box_scores

        return boxes


class Tournament(object):
    def __init__(self):
        self.teams = {}

    def __repr__(self):
        msg = 'I Currently have data for the following teams: \n'
        msg += pformat(self.teams.keys())
        return msg

    def register_team(self, team):
        self.teams[team.name] = team

        if not 'all_scores' in self.__dict__:
            self.all_scores = team.box_scores
        else:
            self.all_scores = pd.concat([self.all_scores, team.box_scores])


def find_region(x):
    """
    Function to be applied to a pandas Series that finds the region
    a team will be playing through in the 2013 tournament.

    Parameters
    ----------
    x : pd.Series
        The pandas Series that has (at least) the team name under the
        title 'Name' and the espn TeamId under the title 'TeamID'

    Returns
    -------
    x : pd.Series
        The same pandas Series that was passed in, but with the 'Region'
        item filled in appropriately.

    Notes
    -----
    Assumes that module level variables region_starts, region_names,
    and rootHTML are defined.
    """
    name = x['Name']
    check_team = 'teamId/' + str(x['TeamID']) + '">'
    where = rootHTML.find(check_team + name) + len(check_team)
    if where < region_starts[1]:
        region = region_names[0]

    elif where < region_starts[2]:
        region = region_names[1]

    elif where < region_starts[3]:
        region = region_names[2]

    else:
        region = region_names[3]

    x['Region'] = region
    return x


def _unpack(row, kind='td'):
    """
    Unpacks a row of an html table as represented by lxml

    Parameters
    ----------
    row : lxml.html.HtmlElement
        A row of an html table as represented by lxml

    kind : str, optional(default='td')
        A string representing what kind of row the function should look
        for. For example, if you are looking for table data the kind
        would be 'td'. If you are looking for table headers the kind
        would be 'th'.
    """
    els = row.findall('.//%s' % kind)
    return[val.text_content() for val in els]


def _parse_html_table(table, offset=0):
    """
    Applies the _unpack function to an entire table. It will pull
    out the header row and then unpack all others as data

    Parameters
    ----------
    table : lxml.html.HtmlElement
        The html table as represented by lxml

    offset : int
        An integer specifying the offset for the headers in the table.
        This means, starting with 0, which row contains the headers.
        The function will then assume that all rows below are data rows.

    Returns
    -------
    df : pd.DataFrame
        A pandas DataFrame containing the information from the html
        table
    """
    rows = table.findall('.//tr')
    header = _unpack(rows[0 + offset], kind='th')
    data = [_unpack(r) for r in rows[1 + offset:]]
    return TextParser(data, names=header, na_values=['N/A'],
                      thousands=',').get_chunk()


def _parse_box_score(gameId):
    """
    Similar to the _parse_html_table function, but made specifically to
    parse the box score from a college basketball game, as reported
    by espn.com

    Parameters
    ----------
    table : lxml.html.HtmlElement
        The the box score as an html table as represented by lxml

    Returns
    -------
    df : pd.DataFrame
        A pandas DataFrame containing the information from box score
    """
    def fill_df(temp, df):
        # Get field goals made, attempted, and percentage
        df.FGM = temp[2].str.split('-').str.get(0).astype(int).values
        df.FGA = temp[2].str.split('-').str.get(1).astype(int).values
        df.FGP = df.FGM / float(df.FGA)

        # Get 3 pointers made, attempted, and percentage
        df['3PM'] = temp[3].str.split('-').str.get(0).astype(int).values
        df['3PA'] = temp[3].str.split('-').str.get(1).astype(int).values
        df['3PP'] = df['3PM'] / float(df['3PA'])

        # Get free throws made, attempted, and percentage
        df.FTM = temp[4].str.split('-').str.get(0).astype(int).values
        df.FTA = temp[4].str.split('-').str.get(1).astype(int).values
        df.FTP = df.FTM / float(df.FTA)

        temp_vals = temp.ix[:, 5:].values.astype(int).squeeze()

        for i in range(8):
            df.ix[0, i + 9] = temp_vals[i]

        return df

    game_url = box_score_url + str(gameId)
    doc = parse(urlopen(game_url))
    try:
        table = doc.findall('.//table')[1]
        rows = table.findall('.//tr')  # Get all rows

        heads = filter(None, [_unpack(i, 'th') for i in rows])  # Get good headers
        all_heads = [_unpack(i, 'th') for i in rows]  # Get all headers

        # inds will have indexes for the good headers
        inds = []
        count = 0
        for i in range(len(all_heads)):
            if count == len(heads):  # found them all
                break
            else:
                if all_heads[i] == heads[count]:
                    inds.append(i)
                    count += 1  # search for next one

        # TODO: Check this
        away_name = heads[0]
        home_name = heads[4]

        home = pd.DataFrame(columns=['FGM', 'FGA', 'FGP', '3PM', '3PA', '3PP',
                                     'FTM', 'FTA', 'FTP', 'OREB', 'REB', 'AST',
                                     'STL', 'BLK', 'TO', 'PF', 'PTS'],
                            index=[away_name[0]])

        away = pd.DataFrame(columns=['FGM', 'FGA', 'FGP', '3PM', '3PA', '3PP',
                                     'FTM', 'FTA', 'FTP', 'OREB', 'REB', 'AST',
                                     'STL', 'BLK', 'TO', 'PF', 'PTS'],
                            index=[home_name[0]])

        # Get temporary data columns
        temp_home = pd.DataFrame([_unpack(rows[inds[7] + 1])]).drop([0, 1], axis=1)
        temp_away = pd.DataFrame([_unpack(rows[inds[3] + 1])]).drop([0, 1], axis=1)

        home = fill_df(temp_home, home)
        away = fill_df(temp_away, away)
        home.PTS = home.PTS.astype(int)
        away.PTS = away.PTS.astype(int)

    except:
        home = pd.DataFrame(columns=['FGM', 'FGA', 'FGP', '3PM', '3PA', '3PP',
                                         'FTM', 'FTA', 'FTP', 'OREB', 'REB', 'AST',
                                         'STL', 'BLK', 'TO', 'PF', 'PTS'],
                                index=['Broken'])

        away = pd.DataFrame(columns=['FGM', 'FGA', 'FGP', '3PM', '3PA', '3PP',
                                     'FTM', 'FTA', 'FTP', 'OREB', 'REB', 'AST',
                                     'STL', 'BLK', 'TO', 'PF', 'PTS'],
                            index=['Broken'])

    return home, away


def _parse_schedule(teamId):
    """
    Given an espn teamId, it will find and parse their schedule.

    Parameters
    ----------
    teamId : int
        The unique espn id for the team

    Returns
    -------
    df : pd.DataFrame
        A pandas DataFrame containing the following columns:
            - HomeAway: either 'vs' or '@' for home or away, respectively
            - OppRank: either '' or 'num', where num is opponents' rank
            - Opp: The opponents school name
            - WinLoss: Either 'W' for a win or 'L' for a loss
            - Score: The final score of the game
            - PointsFor: Points for the team
            - PointsAgainst: Points against the team
            - GameId: The espn GameId used to get to box score
    """
    url = sched_url + str(teamId)  # Generate url
    doc = parse(urlopen(url))  # Get lxml parsed version of html
    table = doc.findall('.//table')[0]  # Get the table from the html

    table_text = table.text_content()

    df = pd.DataFrame(re_parse_sched.findall(table_text),
                      columns=['HomeAway', 'OppRank',
                               'Opp', 'WinLoss', 'Score'])

    df.OppRank = df.OppRank.str.strip('#')
    df.Opp = df.Opp.str.strip('*')

    # Create columns for points for and against
    df['PointsFor'] = 'None'
    df['PointsAgainst'] = 'None'

    # Fill points column with first score entry if they won
    df.ix[df.WinLoss == 'W', 'PointsFor'] = \
        df.ix[df.WinLoss == 'W'].Score.str.split('-').str.get(0).astype(float)

    # Fill points column with second score entry if they lost
    df.ix[df.WinLoss == 'L', 'PointsFor'] = \
        df.ix[df.WinLoss == 'L'].Score.str.split('-').str.get(1).astype(float)

    # Do the opposite if they lost
    df.ix[df.WinLoss == 'W', 'PointsAgainst'] = \
        df.ix[df.WinLoss == 'W'].Score.str.split('-').str.get(1).astype(float)

    df.ix[df.WinLoss == 'L', 'PointsAgainst'] = \
        df.ix[df.WinLoss == 'L'].Score.str.split('-').str.get(0).astype(float)

    # Do type conversions for points for and against
    df.PointsFor = df.PointsFor.astype(int)
    df.PointsAgainst = df.PointsAgainst.astype(int)

    df['GameId'] = re_opponent_game.findall(urlopen(url).read())

    return df


def _parse_rpi_table(teamId):
    url = rpi_url + str(teamId)
    html = urlopen(url).read()
    data_expr = '</td><td align="left">'
    data = []

    data.append(re.findall('(RPI)' + data_expr + '(\d+)', html)[0])
    data.append(re.findall('>(SOS)' + data_expr + '(\d+)', html)[0])
    data.append(re.findall('(TOP 25)' + data_expr + '(\d+-\d+)', html)[0])
    data.append(re.findall('(TOP 50)' + data_expr + '(\d+-\d+)', html)[0])
    data.append(re.findall('(TOP 150)' + data_expr + '(\d+-\d+)', html)[0])
    data.append(re.findall('(SUB 150)' + data_expr + '(\d+-\d+)', html)[0])
    data.append(re.findall('(NEUTRAL W-L)' + data_expr + '(\d+-\d+)', html)[0])
    data.append(re.findall('(ROAD W-L)' + data_expr + '(\d+-\d+)', html)[0])
    data.append(re.findall('(LAST 12)' + data_expr + '(\d+-\d+)', html)[0])
    data.append(re.findall('(SCORING MARGIN)' + data_expr + '([-\d.]+)', html)[0])

    temp = pd.Series(data)
    names = temp.str.get(0)
    values = temp.str.get(1)

    ret = pd.Series(values.values, index=names)
    ret.name = re.findall(r'Daily RPI - (.+)</h1>', html)[0]

    return ret

### ----------------------- Useful Regular Expressions ------------------- ###
# Find regions on bracketology site
re_region = re.compile(r'<b>(\w+)')

# Find team names and seeds on bracketology site
re_team_name_rank = re.compile(r' class="rank">(\d+)</span><a href="http://' +
                               'insider.espn.go.com/mens-college-basketball/' +
                               'rpi/_/teamId/(\d+)">([\w.\s&]+)')

# Find team opponent and game recap id from schedule page html content
re_opponent_game = re.compile(r'(?:boxscore|recap)\?gameId=(\d+)')

re_parse_sched = re.compile(r'(vs|@)(#\d+)?([-\w\s\'*.()&]+)([WL])' +
                             '(\d+-\d{3}(?=\s)|\d+-\d{2})')

### ----------------------------- Useful urls ---------------------------- ###
# Root bracket url
bracket_url = 'http://espn.go.com/mens-college-basketball/bracketology'

# To have TeamId from dataframe appended to it and used with re_opponent_game
sched_url = 'http://insider.espn.go.com/mens-college-basketball' + \
            '/team/schedule/_/id/'

# To be used with gameId to get box score for a game
box_score_url = 'http://insider.espn.go.com/ncb/boxscore?gameId='

# Url to access a team's roster
roster_url = 'http://insider.espn.go.com/mens-college-basketball' + \
             '/team/roster/_/id/'

rpi_url = 'http://insider.espn.go.com/mens-college-basketball/rpi/_/teamId/'


### ------------------------------ Gather data --------------------------- ###
# Get html for root bracketology page
rootHTML = urlopen(bracket_url).read()

# Find region names/starting place in string
check_region = '<h3><b>'  # Appears before all region names
region_names = re_region.findall(rootHTML)
region_starts = [rootHTML.find(check_region + i) + len(check_region)
                 for i in region_names]

# Fill in dataframe with team seeds/names/TeamIDs
df = pd.DataFrame(re_team_name_rank.findall(rootHTML), columns=['Rank',
                                                                'TeamID',
                                                                'Name'])
# Fill region for each team
df['Region'] = None
df = df.apply(find_region, axis=1)

# Fix some dtypes and string formatting
df.Rank = df.Rank.astype(int)
df.TeamID = df.TeamID.astype(int)
df.Name = df.Name.str.title()
df.Region = df.Region.str.title()

# tourney = Tournament()

# num_teams = df.shape[0]

# for i in range(num_teams):
#     team = df.ix[i]
#     name = team['Name']
#     team_id = team['TeamID']
#     rank = team['Rank']
#     region = team['Region']
#     Team(name, team_id, rank, region)
#     print('Finished %i of %i: %s(%i)' % (i, num_teams, name, team_id))

# NOTE: I ran this Tuesday night with the for loop above. I saved the data
#       in this shelve so I don't need to wait for it to run again.
db = shelve.open('tourney_object.db')
tourney = db['tourney']
db.close()
