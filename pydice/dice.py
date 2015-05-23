import json, operator, re
from random import choice

ROLL_STRING_PATTERN = '(?P<n_dice>\d+)d(?P<x_size>\d+)(?P<keep>[\^v]{1}\d+)?(?P<mod>[+-]{1}\d+)?'


class Die(object):
    def __init__(self, faces=range(1,7), mod=0,
                 above_okay=False, below_okay=False,
                 name=None, raw=None, roll_now=False,
                 *args, **kwargs):
        """
        Represents a die and the results of rolling it.
        
        Arguments
        faces: list of possible results (faces on a die), each with an equal
            chance of being rolled
        
        mod: a function applied to the raw result of the roll
        
        above_okay: can mod make a result which is above the max in faces?
        
        below_okay: can mod make a result which is below the max in faces?
        
        name: optional
        
        roll_now: or wait for self.roll() to be called manually
        """
        self.faces = faces
        self.mod = mod
        self.above_okay = above_okay
        self.below_okay = False
        self._name = name
        self._raw = raw
        
        if roll_now:
            self.roll()
    
    def roll(self):
        self._raw = choice(self.faces)        
        return self.result
    
    @property
    def result(self):
        r = self._raw + self.mod
        if (r > self.high_face and
            not self.above_okay):
            return self.high_face
        elif (r < self.low_face and
                not self.below_okay):
            return self.low_face
        else:
            return r
    
    @property
    def name(self):
        if self._name:
            return self._name
        else:
            return str(self.__class__.__name__)
    
    @property
    def high_face(self):
        return sorted(self.faces)[-1]
    
    @property
    def low_face(self):
        return sorted(self.faces)[0]
    
    def __repr__(self):
        return '<{n}: faces={f}, result={r}>'.format(
            n=self.name,
            f=self.faces,
            r=self.result
            )


class DN(Die):
    def __init__(self, size, *args, **kwargs):
        super(DN, self).__init__(faces=range(1, size+1),
                                 *args, **kwargs)
        self._name = 'Die (d{size})'.format(size=size)


class Throw(object):
    def __init__(self, dice, roll_now=True, *args, **kwargs):
        """
        Simulates throwing one or more Die objects and exposes a list of the
        results.
        """
        self.dice = dice
        
        if roll_now:
            self.throw()
    
    @property
    def result(self):
        return [d.result for d in self.dice]
    
    def throw(self):
        [d.roll() for d in self.dice]


class Roll(object):
    def __init__(self, dice, plus_pip=False, total_mod=0,
                 roll_now=True, n_dice=None, x_size=None,
                 *args, **kwargs):
        self.plus_pip = plus_pip
        self.throw = Throw(dice, roll_now)
        self.total_mod = total_mod
        self.n_dice = n_dice
        self.x_size = x_size
        
        self._dropped_dice = []
    
    def evaluate(self, val, comp=operator.eq):
        return sum(1 if comp(r, val) else 0 for r in self.throw.result)
    
    @property
    def result(self):
        return {
            'sum': self.sum,
            'total': self.total,
            'faces': self.throw.result,
            'throw_mod': self.total_mod,
            }
    
    @property
    def dice(self):
        return self.throw.dice
    
    @property
    def raw_dice(self):
        return self.dice + self._dropped_dice
    
    @property
    def faces(self):
        return self.throw.result
    
    @property
    def total(self):
        return self.sum + self.total_mod
    
    @property
    def sum(self):
        return sum(r for r in self.throw.result)
    
    @property
    def json(self):
        return json.dumps(self.result)
    
    def __repr__(self):
        return '<Roll: result={r}>'.format(r=self.result)


def ndx(n_dice, x_size):
    return [DN(x_size) for n in xrange(n_dice)]


def roll_ndx(n_dice, x_size=6, total_mod=0, plus_half=False):
    dice = ndx(n_dice, x_size)
    if plus_half:
        dice.append(Die(mod=lambda x: int(floor(x/2))))
    
    return Roll(dice, total_mod=total_mod)


def roll(string='1d6'):
    """
    Takes a string description of a roll and returns a fully-loaded Roll
    object.
    
    Examples
        '1d6': roll a single six-sided die
        '3d6': roll three six-sided dice
        '3d6+1': roll three six-sided dice and add 1 to the total result
        '6d6^3': roll six six-sided dice and keep the 3 highest values
        
    """
    m = re.match(ROLL_STRING_PATTERN, string)
    if not m:
        raise Exception("Error parsing roll from string '{0}'".format(string))
    
    d = m.groupdict()
    n_dice = int(d['n_dice'])
    x_size = int(d['x_size'])
    if d['mod'] is not None:
        mod = int(d['mod'])
    else:
        mod = 0
    
    # get the roll instance
    r = roll_ndx(n_dice, x_size, mod)
    r.n_dice = n_dice
    r.x_size = x_size
    
    # check to see if this is a "best of" roll
    # e.g., 6d6 but keep the top 3: 6d6^3
    if d['keep']:
        keep_n = int(d['keep'][1:])
        
        if d['keep'][0] == '^':
            # keep the top rolls
            f = lambda x, y: cmp(y.result, x.result)
        else:
            f = lambda x, y: cmp(x.result, y.result)
        
        s = sorted(r.dice, cmp=f)
        r._dropped_dice.extend(i for i in s[keep_n:])
        r.throw.dice = s[:keep_n]
    
    return r
