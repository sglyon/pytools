"""
Created Mar 27, 2013

Author: Chase Coleman & Spencer Lyon

df2latex converts a pandas DataFrame to latex

Notes
-----
Most of this code was taken from matrix2latex and adapted to work
specifically with pandas DataFrame objects.
"""
import sys
import os
import re
import pandas as pd


def to_latex(df, h_row=True, h_col=False, *args, **kwargs):
    if h_row:
        head_r = list(df.columns.astype(str))
        kwargs['headerRow'] = head_r
    if h_col:
        head_c = list(df.index.astype(str))
        kwargs['headerColumn'] = head_c

    return matrix2latex(df.values, *args, **kwargs)


def fix(s, table=False):
    """
    input: (string) s
    output: (string) s
    takes any number in s and replaces the format
    '8e-08' with '8\e{-08}'
    """
    i = re.search('e[-+]\d\d', s)
    while i != None:
        before = s[:i.start()]
        number = s[i.start() + 1:i.start() + 4]
        after = s[i.end():]
        if table:
            num = "%(#)+03d" % {'#': int(number)}
        else:
            num = "%(#)3d" % {'#': int(number)}

        s = '%s\\e{%s}%s' % (before, num, after)
        i = re.search('e[-+]\d\d', s)
    return s


class IOString:
    """
    class that acts like a string, but has the write method
    """
    # For a file like object, writes to the file while keeping
    # a local buffer.
    def __init__(self, fileObject=None):
        self.f = fileObject
        self.s = ""

    def write(self, s):
        try:
            self.f.write(s)
        except AttributeError:
            pass
        self.s += s

    def __str__(self):
        return self.s

    def close(self):
        try:
            self.f.close()
        except AttributeError:
            pass


def assertStr(value, key):
    assert isinstance(value, str), \
           "expected %s to be a str, got %s" % (key, type(value))


def assertKeyFormat(value):
    assertStr(value, "format")
    assert r"%" in value, \
           "expected a format str, got %s" % value
    assert value.count("%") == 1,\
           "expected a single format, got %s" % value


def assertKeyAlignment(value, n):
    assertStr(value, "alignment")
    assert ("c" in value or "l" in value or "r" in value), \
           "expected legal alignment c, l or r, got %s" % value
    counter = dict()
    counter['c'] = 0
    counter['l'] = 0
    counter['r'] = 0
    for v in value:
        if v in counter:
            counter[v] += 1
        else:
            counter[v] = 1
    length = counter['c'] + counter['l'] + counter['r']
    return length


def assertListString(value, key):
    assert isinstance(value, list),\
           "Expected %s to be a list, got %s" % (key, type(value))
    for e in value:
        assertStr(e, "%s element" % key)


def matrix2latex(matr, filename=None, *environments, **keywords):
    m, n = matr.shape

    formatNumber = "$%g$"
    formatColumn = None
    alignment = 'c' * n  # cccc

    headerRow = None
    headerColumn = None
    caption = None
    label = None

    #
    # Conflicts
    #
    if "format" in keywords and "formatColumn" in keywords:
        print('Using both format and formatColumn is not supported,\
               using formatColumn')
        del keywords["format"]

    #
    # User-defined values
    #
    for key in keywords:
        value = keywords[key]
        if key == "format":
            assertKeyFormat(value)
            formatNumber = value
            formatColumn = None
        elif key == "formatColumn":
            # never let both formatColumn and formatNumber to be defined
            formatColumn = value
            formatNumber = None
        elif key == "alignment":
            if len(value) == 1:
                alignment = value * n  # rrrr
            else:
                alignment = value
            assertKeyAlignment(alignment, n)
        elif key == "headerRow":
            assertListString(value, "headerRow")
            headerRow = list(value)
        elif key == "headerColumn":
            assertListString(value, "headerColumn")
            headerColumn = list(value)
        elif key == "caption":
            assertStr(value, "caption")
            caption = value
        elif key == "label":
            assertStr(value, "label")
            if value.startswith('tab:'):
                # this will be added later, avoids 'tab:tab:' as label
                label = value[len('tab:'):]
            else:
                label = value
        else:
            sys.stderr.write("Error: key not recognized '%s'\n" % key)
            sys.exit(2)

    if "headerColumn" in keywords:
        alignment = "r" + alignment

    # Environments
    if len(environments) == 0:          # no environment give, assume table
        environments = ("table", "center", "tabular")

    if not formatColumn:
        formatColumn = [formatNumber] * n

    if headerColumn and headerRow and len(headerRow) == n:
        headerRow.insert(0, "")

    f = None
    if isinstance(filename, str) and filename != '':
        if not filename.endswith('.tex'):  # assure propper file extension
            filename += '.tex'
        f = open(filename, 'w')
        if label == None:
            label = os.path.basename(filename)  # get basename
            # remove extension. TODO: bug with filename=foo.texFoo.tex
            label = label.replace(".tex", "")

    f = IOString(f)
    #
    # Begin block
    #
    for ixEnv in range(0, len(environments)):
        f.write("\t" * ixEnv)
        f.write(r"\begin{%s}" % environments[ixEnv])
        # special environments:
        if environments[ixEnv] == "table":
            f.write("[ht]")
        elif environments[ixEnv] == "center":
            # if caption != None:
            #     f.write("\n" + "\t" * ixEnv)
            #     f.write(r"\caption{%s}" % fix(caption))
            if label != None:
                f.write("\n" + "\t" * ixEnv)
                f.write(r"\label{tab:%s}" % label)
        elif environments[ixEnv] == "tabular":
            f.write("{" + alignment + "}\n")
            f.write("\t" * ixEnv)
            f.write(r"\toprule")
        # newline
        f.write("\n")
    tabs = len(environments)            # number of \t to use

    #
    # Table block
    #

    # Row labels
    if headerRow:
        f.write("\t" * tabs)
        for j in range(0, len(headerRow)):
            f.write(r"%s" % headerRow[j])
            if j != len(headerRow) - 1:
                f.write(" & ")
            else:
                f.write(r"\\" + "\n")
                f.write("\t" * tabs)
                f.write(r"\midrule" + "\n")

    # Values
    for i in range(0, m):
        f.write("\t" * tabs)
        for j in range(0, n):

            if j == 0:                  # first row
                if headerColumn != None:
                    f.write("%s & " % headerColumn[i])

            if '%s' not in formatColumn[j]:
                try:
                    e = float(matr[i][j])            # current element
                except ValueError:  # can't convert to float, use string
                    e = matr[i][j]
                    formatColumn[j] = '%s'
                except TypeError:       # raised for None
                    e = None
            else:
                e = matr[i][j]

            if e == None or e == float('NaN'):
                f.write("-")
            elif e == float('inf'):
                f.write(r"$\infty$")
            elif e == float('-inf'):
                f.write(r"$-\infty$")
            else:
                fcj = formatColumn[j]
                formated = fcj % e
                formated = fix(formated, table=True)  # fix 1e+2
                f.write(formated)
            if j != n - 1:                # not last row
                f.write(" & ")
            else:                       # last row
                f.write(r"\\")
                f.write("\n")

    #
    # End block
    #
    for ixEnv in range(0, len(environments)):
        ixEnv = len(environments) - 1 - ixEnv  # reverse order
        # special environments:
        if environments[ixEnv] == "center":
            pass
        elif environments[ixEnv] == "tabular":
            f.write("\t" * ixEnv)
            f.write(r"\bottomrule" + "\n")
        f.write("\t" * ixEnv)
        f.write(r"\end{%s}" % environments[ixEnv])
        if environments[ixEnv] == "tabular" and caption:
                f.write("\n" + "\t" * ixEnv)
                f.write(r"\caption{%s}" % fix(caption))
        if ixEnv != 0:
            f.write("\n")

    f.close()
    return f.__str__()


class myDF(pd.DataFrame):
    def __latex__(self, h_row=True, h_col=False, *args, **kwargs):
        return to_latex(self, h_row=True, h_col=False, *args, **kwargs)


if __name__ == '__main__':
    import pandas as pd
    import numpy as np
    y = pd.DataFrame([[1, 2, 3], [4, 'hello', np.inf]],
                    columns=['ab', 'b', 'c'],
                    index=['A', 'B'])
    print(to_latex(y))
