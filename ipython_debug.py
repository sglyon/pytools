"""
Created October 12, 2012

Author: Spencer Lyon

iPython debugger tools.
"""


def set_trace():
    """
    This function allows the user to set a quick pseudo-breakpoint
    anywhere in a file. Just call set_trace() and the debugger will
    break at that line.

    Notes
    -----
    Taken from Wes McKinney's book Python for Data Analysis
    """
    import sys
    from IPython.core.debugger import Pdb
    Pdb(color_scheme='Linux').set_trace(sys._getframe().f_back)


def debug(f, *args, **kwargs):
    """
    Allows the user to launch pdb in any function.

    Parameters
    ----------
    f: function
        The function you wish to debug

    args:
        The arguments that need to be passed to f

    kwargs:
        Named arguments that must be passed to f

    Returns
    -------
    None

    Notes
    -----
    Taken from Wes McKinney's book Python for Data Analysis
    """
    from IPython.core.debugger import Pdb
    pdb = Pdb(color_scheme='Linux')
    return pdb.runcall(f, *args, **kwargs)
