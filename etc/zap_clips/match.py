__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

import clips

filename_match_clips="(deffunction filename_match (?str ?patt) (python-call filename_match ?str ?patt))"
re_match_clips="(deffunction re_match (?str ?patt) (python-call re_match ?str ?patt))"

def filename_match(_str, _patt):
    from fnmatch import fnmatch
    if fnmatch(_str, _patt):
        return clips.Symbol('TRUE')
    return clips.Symbol('FALSE')

def re_match(_str, _patt):
    import re
    if re.match(str(_patt), str(_str)) != None:
        return clips.Symbol('TRUE')
    return clips.Symbol('FALSE')

