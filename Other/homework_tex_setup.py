"""
Utility to automatically set up a new Latex homework assignment.

"""

preamble = """\
%% Preamble
  \documentclass\{homework\}

  \hwTitle\{Assignment 1\} % Assignment title
  \hwDueDate\{Thursday,\ September\ 12,\ 2013\} % Due date
  \hwClass\{Math I\} % Course/class
  \hwAuthor\{Spencer Lyon\} % Your name
  \hwInstructor\{Stacchetti\} % Instructor Name
  \\author\{Spencer Lyon\}

  \usepackage[shortlabels]\{enumitem\}
  \usepackage\{setspace\}
  \usepackage\{booktabs\}

  % Set up listings
  \usepackage\{listings\}
  \usepackage\{color\}

  \definecolor\{dkgreen\}\{rgb\}\{0,0.6,0\}
  \definecolor\{gray\}\{rgb\}\{0.5,0.5,0.5\}
  \definecolor\{mauve\}\{rgb\}\{0.58,0,0.82\}

  \lstset\{frame=tb,
    language=Python,
    aboveskip=3mm,
    belowskip=3mm,
    showstringspaces=false,
    columns=flexible,
    basicstyle=\{\small\ttfamily\},
    numbers=left,
    stepnumber=5,
    numberstyle=\\tiny\color\{gray\},
    keywordstyle=\color\{blue\},
    commentstyle=\color\{dkgreen\},
    stringstyle=\color\{mauve\},
    breaklines=true,
    breakatwhitespace=true
    tabsize=4
  \}

%% New Commands I use alot
  \\newcommand\{\TODO\}[1]\{ \{\color\{magenta\} TODO: #1\} \}
  \\newcommand\{\st\}[0]\{ \{\text\{ such that \} \} \}

  \makeatletter
  \def\Let@\{\def\\\{\\notag\math@cr\}\}
  \makeatother

  % partial derivative as a fraction
  \\newcommand\{\\fracpd\}[2]\{
    \ensuremath\{\frac\{\partial #1\}\{\partial #2\}\}
  \}

  % fraction with parenthesis around it
  \\newcommand\{\pfrac\}[2]\{
    \ensuremath\{ \left( \\frac\{#1\}\{#2\} \\right)\}
  \}

  % two row small bracketed matrix
  \\newcommand\{\sbmtwo\}[2]\{
   \ensuremath\{ \left[\begin\{smallmatrix\} #1 \\ #2 \end\{smallmatrix\}\\right]\}
  \}

  % two row bracketed matrix
  \\newcommand\{\\bmtwo\}[2]\{
   \ensuremath\{ \\begin\{bmatrix\} #1 \\ #2 \end\{bmatrix\}\}
  \}

  % Setup for matrix2latex python
  \providecommand\{\e\}[1]\{\ensuremath\{\\times 10^\{#1\}\}\}
  \usepackage\{caption\}
"""
