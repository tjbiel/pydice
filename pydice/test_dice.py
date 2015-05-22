import unittest, random
import dice

# all hail stochastic testing
CASE_ITERATIONS = 10000
MAX_DIE_SIZE = 20
MAX_N_DICE = 20

# helpers for randomization
def random_ndice(upper_limit=MAX_N_DICE):
    return random.randint(1, upper_limit) + 1

def random_size():
    return random.randint(1, MAX_DIE_SIZE+1)

def faces_from_size(x_size=MAX_DIE_SIZE):
    return range(1, x_size+1)

def random_faces(x_size=MAX_DIE_SIZE):
    return faces_from_size(random.randint(2, x_size+1))

def random_mod(limit=MAX_DIE_SIZE):
    return random.randint(1, limit+1)


# cases
class DieResultInFaces(unittest.TestCase):
    """
    A Die object should always return values in
    its die faces, specified at init.
    """
    
    def test(self):
        for x in xrange(CASE_ITERATIONS):
            f = random_faces()
            d = dice.Die(faces=f)
            d.roll()
            self.assertTrue(d.result in f)


class CheckRollNDX(unittest.TestCase):
    """
    Verifies the roll_ndx() function generates a Roll with the appropriate
    dice.
    """    
    def test(self):
        for x in xrange(CASE_ITERATIONS):
            n_dice = random_ndice()
            x_size = random_size()
            faces = faces_from_size(x_size)

            r = dice.roll_ndx(n_dice, x_size)
            
            # number of Dice in Roll should be n_dice
            self.assertTrue(len(r.dice) == n_dice)
            
            for d in r.dice:
                # each Die in Roll should have a result in faces
                self.assertTrue(d.result in faces,
                    'roll_ndx({n}, {x}) contains {d} result {r} not in faces {f}'\
                    .format(n=n_dice, x=x_size, d=d, r=d.result, f=faces))
            
            # overall result should be between n_dice and n_dice * x_size
            lower_limit = n_dice
            self.assertTrue(r.total >= lower_limit,
                'roll_ndx({n}, {x}) yielded result {r} with total {t} less than {l}'\
                .format(n=n_dice, x=x_size, r=r.result, t=r.total, l=lower_limit))
                
            upper_limit = n_dice * x_size
            self.assertTrue(r.total <= upper_limit,
                'roll_ndx({n}, {x}) yielded total {t} greater than {l}'\
                .format(n=n_dice, x=x_size, r=r.result, t=r.total, l=upper_limit))


class NDXRollString(unittest.TestCase):
    """
    Check that the standard ndx roll string pattern (e.g. '6d6') is parsed
    correctly and generates valid results.
    """
    pattern = '{n}d{x}'
    
    # testing ndx
    def test(self):
        for x in xrange(CASE_ITERATIONS):
            n_dice = random_ndice()
            x_size = random_size()
            faces = faces_from_size(x_size)
            
            test_string = self.pattern.format(n=n_dice, x=x_size)
            r = dice.roll(test_string)
            
            # number of Dice in Roll should be n_dice
            self.assertTrue(len(r.dice) == n_dice)
            
            for d in r.dice:
                # each Die in Roll should have a result in faces
                self.assertTrue(d.result in faces,
                    'Parsed {s} contains {d} result {r} not in faces {f}'\
                    .format(s=test_string, d=d, r=d.result, f=faces))
            
            # overall result should be between n_dice and n_dice * x_size
            lower_limit = n_dice
            self.assertTrue(r.total >= lower_limit,
                'Parsed {s} yielded result {r} with total {t} less than {l}'\
                .format(s=test_string, r=r.result, t=r.total, l=lower_limit))
                
            upper_limit = n_dice * x_size
            self.assertTrue(r.total <= upper_limit,
                'Parsed {s} yielded total {t} greater than {l}'\
                .format(s=test_string, r=r.result, t=r.total, l=upper_limit))


class NDXwmodRollString(unittest.TestCase):
    """
    Check that a modified roll patter roll string pattern (e.g., '3d6+3') is
    parsed correctly and generates valid results.    
    """
    pattern = '{n}d{x}{plusminus}{mod}'
    # testing ndx
    def test(self):
        for x in xrange(CASE_ITERATIONS):
            n_dice = random_ndice()
            x_size = random_size()
            mod = random_size()
            faces = faces_from_size(x_size)
            
            if random.randint(1,2) == 1:
                plusminus = '+'
                mod_int = mod
            else:
                plusminus = '-'
                mod_int = -1 * mod
            
            test_string = self.pattern.format(n=n_dice, x=x_size,
                                              plusminus=plusminus,
                                              mod=mod)
            r = dice.roll(test_string)
            
            # number of Dice in Roll should be n_dice
            self.assertTrue(len(r.dice) == n_dice)
            
            for d in r.dice:
                # each Die in Roll should have a result in faces or faces*mod
                faces_w_mod = faces + [f+mod for f in faces]
                self.assertTrue(d.result in faces,
                    'Parsed {s} contains {d} result {r} not in faces(+mod) {f}'\
                    .format(s=test_string, d=d, r=d.result, f=faces_w_mod))
            
            # overall result should be between n_dice+mode and n_dice*x_size+mod
            lower_limit = n_dice + mod_int
            self.assertTrue(r.total >= lower_limit,
                'Parsed {s} yielded result {r} with total {t} less than {l}'\
                .format(s=test_string, r=r.result, t=r.total, l=lower_limit))
                
            upper_limit = n_dice * x_size + mod_int
            self.assertTrue(r.total <= upper_limit,
                'Parsed {s} yielded result {r} with total {t} greater than {l}'\
                .format(s=test_string, r=r.result, t=r.total, l=upper_limit))


def main():
    unittest.main()

if __name__ == '__main__':
    main()
