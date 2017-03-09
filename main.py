import random
from glob import glob
from collections import defaultdict

def load_lexicon(fname):
    with open(fname, 'r') as f:
        return [l.lower().strip() for l in f.readlines()]

def load_lexicons(pattern):
    return sum([load_lexicon(f) for f in glob(pattern)], [])

animals = load_lexicon('data/animals.txt')
adjs = load_lexicons('data/adjectives/*.txt')
advs = load_lexicons('data/adverbs/*.txt')
cnt_nouns = load_lexicons('data/countable_nouns/*.txt')
ucnt_nouns = load_lexicons('data/uncountable_nouns/*.txt')
verbs = load_lexicons('data/verbs/*.txt')
prefixes = load_lexicon('data/prefixes.txt')

def name(type):
    if type == 'unit':
        vocabs = [
            random.choice([adjs, nationalities]),
            animals
        ]
    elif type in ['action', 'event']:
        vocabs = [
            advs,
            verbs
        ]
    elif type in ['property', 'condition']:
        vocabs = [
            adjs,
            ucnt_nouns
        ]

    names = [random.choice(vocab) for vocab in vocabs]

    if random.random() >= 0.98:
        names[0] = random.choice(prefixes) + names[0]

    return ' '.join(names).title()


def weighted_choice(choices):
    """
    Random selects a key from a dictionary,
    where each key's value is its probability weight.
    """
    # Randomly select a value between 0 and
    # the sum of all the weights.
    rand = random.uniform(0, sum(choices.values()))

    # Seek through the dict until a key is found
    # resulting in the random value.
    summ = 0.0
    for key, value in choices.items():
        summ += value
        if rand < summ: return key

    # If this returns False,
    # it's likely because the knowledge is empty.
    return False


class Markov():
    def __init__(self, fname, state_size=3):
        """
        Recommended `state_size` in [2,5]
        """
        terms = load_lexicon(fname)
        mem = defaultdict(lambda: defaultdict(int))

        for t in terms:
            # Beginning & end
            mem['^'][t[:state_size]] += 1
            mem[t[-state_size:]]['$'] += 1

            for i in range(len(t) - state_size):
                prev = t[i:i+state_size]
                next = t[i+1:i+1+state_size]
                mem[prev][next] += 1

        self.mem = mem
        self.state_size = state_size

    def generate(self):
        ch = weighted_choice(self.mem['^'])
        out = [ch]
        while True:
            ch = weighted_choice(self.mem[ch])
            if ch == '$':
                break
            out.append(ch[self.state_size-1])
        return ''.join(out)

countries = load_lexicon('data/countries.txt')
nation_mkv = Markov('data/countries.txt')

def nation():
    n = nation_mkv.generate()
    while n in countries:
        n = nation_mkv.generate()
    return n.title()

def nationality():
    n = nation()
    if n[-1] == 'a':
        return n + 'n'
    if n[-1] == 'i':
        return n + random.choice(['', 'c', 'sh', 'an'])
    if n[-1] == 'e':
        return n + random.choice(['se', 'an'])
    if n[-1] == 'y':
        return n[:-1] + 'ian'
    if n[-1] == 'u':
        return n + 'vian'
    else:
        return n + random.choice(['ian', 'ean', 'ese', 'an', 'ish', 'ic', 'i'])

nationalities = [nationality() for n in range(16)]

if __name__ == '__main__':
    type = random.choice(['unit', 'action', 'event', 'property', 'condition', 'nation'])
    if type == 'nation':
        print('Nation: {}'.format(nation()))
    else:
        print('{}: {}'.format(type.title(), name(type)))
