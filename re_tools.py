"""
Created Mar 11, 2013

Author: Spencer Lyon

A collection of tools for using regular expressions in python
"""
import re

prun_match_1 = r'\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)'
prun_match_2 = r'\s+([\d.]+)\s+([\w_.{}]+):(\d+)\(([\w<>]+)\)'
prun_match = prun_match_1 + prun_match_2

prun_re = re.compile(prun_match)
