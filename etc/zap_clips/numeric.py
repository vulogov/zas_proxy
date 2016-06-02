__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

import numpy, clips

uniform_clips="(deffunction uniform  (?low ?high) (python-call uniform ?low ?high))"
uniform_int_clips="(deffunction uniform_int  (?low ?high) (python-call uniform_int ?low ?high))"
dice_clips="(deffunction dice  (?barrier) (python-call dice ?barrier))"
variation_clips="(deffunction variation  (?prev_val ?pmin ?pmax ?var_min ?var_max) (python-call variation ?prev_val ?pmin ?pmax ?var_min ?var_max))"

def uniform(_low, _high):
    import numpy as np
    return clips.Float(np.random.uniform(_low, _high))
def uniform_int(_low, _high):
    import numpy as np
    return clips.Integer(int(np.random.uniform(_low, _high)))
def dice(_barrier):
    cast = int(uniform_int(0,100))
    if cast < _barrier:
        return clips.Symbol('TRUE')
    return clips.Symbol('FALSE')
def variation_min(_prev_val, _min, _variation):
    _cm = _prev_val-((_prev_val/100.0)*_variation)
    if _cm < _min:
        _cm = uniform(_min, _prev_val)
    return clips.Float(_cm)
def variation_max(_prev_val, _max, _variation):
    _cm = _prev_val+((_prev_val/100.0)*_variation)
    if _cm > _max:
        _cm = uniform(_prev_val, _max)
    return clips.Float(_cm)
def variation(_prev_val, _min, _max, _var_min, _var_max):
    _cmin = float(variation_min(_prev_val, _min, _var_min))
    _cmax = float(variation_max(_prev_val, _max, _var_max))
    return uniform(_cmin, _cmax)
