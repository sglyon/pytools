"""
Created Mar 16, 2013

Author: Spencer Lyon

File to gather/examine college basketball data for march madness
"""
import re
from urllib2 import urlopen
import pandas as pd


def find_region(x):
    name = x['Name']
    check_team1 = 'teamId/' + str(x['TeamID']) + '">'
    where = rootHTML.find(check_team1 + name) + len(check_team1)
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

re_team_name = re.compile(r'RPI - (\w+\s\w+)')
re_region = re.compile(r'<b>(\w+)')
re_team_name_rank = re.compile(r' class="rank">(\d+)</span><a href="http://' +
                               'insider.espn.go.com/mens-college-basketball/' +
                               'rpi/_/teamId/(\d+)">([\w.\s]+)')

rootHTML = urlopen('http://espn.go.com/mens-college-basketball/bracketology').read()
ok = rootHTML.find('Okla')
zag = rootHTML.find('GONZ')
indy = rootHTML.find('INDI')

check_region = '<h3><b>'  # Appears before all region names

region_names = re_region.findall(rootHTML)
region_starts = [rootHTML.find(check_region + i) + len(check_region)
                 for i in region_names]

df = pd.DataFrame(re_team_name_rank.findall(rootHTML), columns=['Rank',
                                                                'TeamID',
                                                                'Name'])

df['Region'] = None
df = df.apply(find_region, axis=1)

df.Rank = df.Rank.astype(int)
df.TeamID = df.TeamID.astype(int)

for i in region_names:
    print(i, df[df.Region==i].shape)
