
import Tree

verbose = False
def printV(*args):
    if verbose:
        print(*args)

# A Python implementation of the AIMA CYK-Parse algorithm in Fig. 23.5 (p. 837).
def CYKParse(words, grammar):
    T = {}
    P = {}
    # Instead of explicitly initializing all P[X, i, k] to 0, store
    # only non-0 keys, and use this helper function to return 0 as needed.
    def getP(X, i, k):
        key = str(X) + '/' + str(i) + '/' + str(k)
        if key in P:
            return P[key]
        else:
            return 0

    #Modify Grammar function, isolates unit rules from binary grammar rules
    def modifyGrammar(grammar):
        units = set()
        for rule in grammar['syntax']:
            if (len(rule) == 3):
                units.add(tuple(rule))
        grammar['syntax'] = [x for x in grammar['syntax'] if len(x) == 4]
        return units

    #Unit rule parse function, adds unit rules to head if possible
    #if X -> Y exists, and Y -> Z C exists, X -> Y -> Z C is added
    #if X -> Y exists, and Y -> Z exists, X -> Y -> Z is added
    def unitRuleParse(X, i, j, units, T, P):
        for unit in units:
            if unit[1] == X and (getP(X,i,j) * unit[2]) > getP(unit[0],i,j):
                P[unit[0] + '/' + str(i) + '/' + str(j)] = getP(X,i,j) * unit[2]
                T[unit[0] + '/' + str(i) + '/' + str(j)] = Tree.Tree(unit[0], T[X+'/'+str(i)+'/'+str(j)], '')
                new_units = units.copy()
                new_units.remove(unit)
                unitRuleParse(unit[0], i, j, new_units, T, P)

    #merge all names with multiple words into one word with periods in between
    words = ' '.join(words)
    for i in range(len(grammar['lexicon'])):
        if grammar['lexicon'][i][0] == 'Name' and len(grammar['lexicon'][i][1].split()) > 1 and grammar['lexicon'][i][1] in words:
            length = len(' '.join(grammar['lexicon'][i][1].split()))
            pos = words.find(grammar['lexicon'][i][1])
            grammar['lexicon'][i][1] = '.'.join(grammar['lexicon'][i][1].split())
            words = words[:pos] + grammar['lexicon'][i][1] + words[pos+length:]
    words = words.split()

            

    #Replace Grammar properly
    units = modifyGrammar(grammar)
    # Insert lexical categories for each word
    for i in range(len(words)):
        for X, p in getGrammarLexicalRules(grammar, words[i]):
            P[X + '/' + str(i) + '/' + str(i)] = p
            T[X + '/' + str(i) + '/' + str(i)] = Tree.Tree(X, None, None, lexiconItem=words[i])
            unitRuleParse(X, i, i, units, T, P)

    # Construct X_i:j from Y_i:j + Z_j+i:k, shortest spans first
    for i, j, k in subspans(len(words)):
        for X, Y, Z, p in getGrammarSyntaxRules(grammar):
            PYZ = getP(Y, i, j) * getP(Z, j+1, k) * p
            if PYZ > getP(X, i, k):
                P[X + '/' + str(i) + '/' + str(k)] = PYZ
                T[X + '/' + str(i) + '/' + str(k)] = Tree.Tree(X, T[Y+'/'+str(i)+'/'+str(j)], T[Z+'/'+str(j+1)+'/'+str(k)])
                unitRuleParse(X, i, k, units, T, P)
    printV('T:', [str(t)+':'+str(T[t]) for t in T])
    return T, P

# Python uses 0-based indexing, requiring some changes from the book's
# 1-based indexing: i starts at 0 instead of 1
def subspans(N):
    for length in range(2, N+1):
        for i in range(N+1 - length):
            k = i + length - 1
            for j in range(i, k):
                yield i, j, k

# These two getXXX functions use yield instead of return so that a single pair can be sent back,
# and since that pair is a tuple, Python permits a friendly 'X, p' syntax
# in the calling routine.
def getGrammarLexicalRules(grammar, word):
    for rule in grammar['lexicon']:
        if rule[1] == word:
            yield rule[0], rule[2]

def getGrammarSyntaxRules(grammar):
    rulelist = []
    for rule in grammar['syntax']:
        yield rule[0], rule[1], rule[2], rule[3]

# 'Grammar' here is used to include both the syntax part and the lexicon part.

# E0 from AIMA, ps. 834.  Note that some syntax rules were added or modified 
# to shoehorn the rules into Chomsky Normal Form. 
def getGrammarE0Original():
    return {
        'syntax' : [
            ['S', 'NP', 'VP', 0.9 * 0.45 * 0.6],
            ['S', 'Pronoun', 'VP', 0.9 * 0.25 * 0.6],
            ['S', 'Name', 'VP', 0.9 * 0.10 * 0.6],
            ['S', 'Noun', 'VP', 0.9 * 0.10 * 0.6],
            ['S', 'NP', 'Verb', 0.9 * 0.45 * 0.4],
            ['S', 'Pronoun', 'Verb', 0.9 * 0.25 * 0.4],
            ['S', 'Name', 'Verb', 0.9 * 0.10 * 0.4],
            ['S', 'Noun', 'Verb', 0.9 * 0.10 * 0.4],
            ['S', 'S', 'Conj+S', 0.1],
            ['Conj+S', 'Conj', 'S', 1.0],
            ['NP', 'Article', 'Noun', 0.25],
            ['NP', 'Article+Adjs', 'Noun', 0.15],
            ['NP', 'Article+Adjective', 'Noun', 0.05],
            ['NP', 'Digit', 'Digit', 0.15],
            ['NP', 'NP', 'PP', 0.2],
            ['NP', 'NP', 'RelClause', 0.15],
            ['NP', 'NP', 'Conj+NP', 0.05],
            ['Article+Adjs', 'Article', 'Adjs', 1.0],
            ['Article+Adjective', 'Article', 'Adjective', 1.0],
            ['Conj+NP', 'Conj', 'NP', 1.0],
            ['VP', 'VP', 'NP', 0.6 * 0.55],
            ['VP', 'VP', 'Adjective', 0.6 * 0.1],
            ['VP', 'VP', 'PP', 0.6 * 0.2],
            ['VP', 'VP', 'Adverb', 0.6 * 0.15],
            ['VP', 'Verb', 'NP', 0.4 * 0.55],
            ['VP', 'Verb', 'Adjective', 0.4 * 0.1],
            ['VP', 'Verb', 'PP', 0.4 * 0.2],
            ['VP', 'Verb', 'Adverb', 0.4 * 0.15],
            ['Adjs', 'Adjective', 'Adjs', 0.8],
            ['PP', 'Prep', 'NP', 0.65],
            ['PP', 'Prep', 'Pronoun', 0.2],
            ['PP', 'Prep', 'Name', 0.1],
            ['PP', 'Prep', 'Noun', 0.05],
            ['RelClause', 'RelPro', 'VP', 0.6],
            ['RelClause', 'RelPro', 'Verb', 0.4]
        ],
        'lexicon' : [
            ['Noun', 'stench', 0.05],
            ['Noun', 'breeze', 0.05],
            ['Noun', 'wumpus', 0.05],
            ['Noun', 'pits', 0.05],
            ['Noun', 'dungeon', 0.05],
            ['Noun', 'frog', 0.05],
            ['Noun', 'balrog', 0.7],
            ['Verb', 'is', 0.1],
            ['Verb', 'feel', 0.1],
            ['Verb', 'smells', 0.1],
            ['Verb', 'stinks', 0.05],
            ['Verb', 'wanders', 0.65],
            ['Adjective', 'right', 0.1],
            ['Adjective', 'dead', 0.05],
            ['Adjective', 'smelly', 0.02],
            ['Adjective', 'breezy', 0.02],
            ['Adjective', 'green', 0.81],
            ['Adverb', 'here', 0.05],
            ['Adverb', 'ahead', 0.05],
            ['Adverb', 'nearby', 0.02],
            ['Adverb', 'below', 0.88],
            ['Pronoun', 'me', 0.1],
            ['Pronoun', 'you', 0.03],
            ['Pronoun', 'I', 0.1],
            ['Pronoun', 'it', 0.1],
            ['Pronoun', 'she', 0.67],
            ['RelPro', 'that', 0.4],
            ['RelPro', 'which', 0.15],
            ['RelPro', 'who', 0.2],
            ['RelPro', 'whom', 0.02],
            ['RelPro', 'whoever', 0.23],
            ['Name', 'Ali', 0.01],
            ['Name', 'Bo', 0.01],
            ['Name', 'Boston', 0.01],
            ['Name', 'Marios', 0.97],
            ['Article', 'the', 0.4],
            ['Article', 'a', 0.3],
            ['Article', 'an', 0.05],
            ['Article', 'every', 0.05],
            ['Prep', 'to', 0.2],
            ['Prep', 'in', 0.1],
            ['Prep', 'on', 0.05],
            ['Prep', 'near', 0.10],
            ['Prep', 'alongside', 0.55],
            ['Conj', 'and', 0.5],
            ['Conj', 'or', 0.1],
            ['Conj', 'but', 0.2],
            ['Conj', 'yet', 0.2],
            ['Digit', '0', 0.1],
            ['Digit', '1', 0.1],
            ['Digit', '2', 0.1],
            ['Digit', '3', 0.1],
            ['Digit', '4', 0.1],
            ['Digit', '5', 0.1],
            ['Digit', '6', 0.1],
            ['Digit', '7', 0.1],
            ['Digit', '8', 0.1],
            ['Digit', '9', 0.1]
        ]
    }
#E0 directly from AIMA, p.834 directly
def getGrammarE0():
    return {
        'syntax' : [
            ['S', 'NP', 'VP', 0.9],
            ['S', 'S', 'Conj+S', 0.1],
            ['Conj+S', 'Conj', 'S', 1.0],
            ['NP', 'Pronoun', 0.25],
            ['NP', 'Name', 0.1],
            ['NP', 'Noun', 0.1],
            ['NP', 'Article', 'Noun', 0.25],
            ['NP', 'Article+Adjs', 'Noun', 0.05],
            ['NP', 'Digit', 'Digit', 0.05],
            ['NP', 'NP', 'PP', 0.1],
            ['NP', 'NP', 'RelClause', 0.05],
            ['NP', 'NP', 'Conj+NP', 0.05],
            ['Article+Adjs', 'Article', 'Adjs', 1.0],
            ['Conj+NP', 'Conj', 'NP', 1.0],
            ['VP', 'Verb', 0.4],
            ['VP', 'VP', 'NP', 0.35],
            ['VP', 'VP', 'Adjective', 0.05],
            ['VP', 'VP', 'PP', 0.1],
            ['VP', 'VP', 'Adverb', 0.1],
            ['Adjs', 'Adjective', 0.8],
            ['Adjs', 'Adjective', 'Adjs', 0.2],
            ['PP', 'Prep', 'NP', 1],
            ['RelClause', 'RelPro', 'VP', 1]
        ],
        'lexicon' : [
            ['Noun', 'stench', 0.05],
            ['Noun', 'breeze', 0.05],
            ['Noun', 'wumpus', 0.5], #originally 0.05
            ['Noun', 'pits', 0.05],
            ['Noun', 'dungeon', 0.05],
            ['Noun', 'frog', 0.05],
            ['Noun', 'balrog', 0.7],
            ['Verb', 'is', 0.8], #originally 0.1
            ['Verb', 'feel', 0.1],
            ['Verb', 'smells', 0.1],
            ['Verb', 'stinks', 0.05],
            ['Verb', 'wanders', 0.65],
            ['Adjective', 'right', 0.1],
            ['Adjective', 'dead', 0.9], #originally 0.05
            ['Adjective', 'smelly', 0.02],
            ['Adjective', 'breezy', 0.02],
            ['Adjective', 'green', 0.81],
            ['Adverb', 'here', 0.05],
            ['Adverb', 'ahead', 0.05],
            ['Adverb', 'nearby', 0.02],
            ['Adverb', 'below', 0.88],
            ['Pronoun', 'me', 0.1],
            ['Pronoun', 'you', 0.03],
            ['Pronoun', 'I', 0.1],
            ['Pronoun', 'it', 0.1],
            ['Pronoun', 'she', 0.67],
            ['RelPro', 'that', 0.4],
            ['RelPro', 'which', 0.15],
            ['RelPro', 'who', 0.2],
            ['RelPro', 'whom', 0.02],
            ['RelPro', 'whoever', 0.23],
            ['Name', 'Ali', 0.01],
            ['Name', 'Bo', 0.01],
            ['Name', 'Boston', 0.01],
            ['Name', 'Marios', 0.97],
            ['Article', 'the', 0.0004], #originally 0.4
            ['Article', 'a', 0.3],
            ['Article', 'an', 0.05],
            ['Article', 'every', 0.05],
            ['Prep', 'to', 0.2],
            ['Prep', 'in', 0.1],
            ['Prep', 'on', 0.05],
            ['Prep', 'near', 0.10],
            ['Prep', 'alongside', 0.55],
            ['Conj', 'and', 0.5],
            ['Conj', 'or', 0.1],
            ['Conj', 'but', 0.2],
            ['Conj', 'yet', 0.2],
            ['Digit', '0', 0.1],
            ['Digit', '1', 0.1],
            ['Digit', '2', 0.1],
            ['Digit', '3', 0.1],
            ['Digit', '4', 0.1],
            ['Digit', '5', 0.1],
            ['Digit', '6', 0.1],
            ['Digit', '7', 0.1],
            ['Digit', '8', 0.1],
            ['Digit', '9', 0.1]
        ]
    }

# To experiment with the 'garden path' sentence 'the old man the boat' 
def getGrammarGardenPath():
    return {
        'syntax' : [
            ['S', 'NP', 'VP', 0.25],
            ['S', 'Noun', 'VP', 0.25],
            ['S', 'NP', 'Verb', 0.25],
            ['S', 'Noun', 'Verb', 0.25],
            ['NP', 'Article', 'Noun', 0.4],
            ['NP', 'Article+Adjs', 'Noun', 0.2],
            ['NP', 'Article+Adjective', 'Noun', 0.4],
            ['Article+Adjs', 'Article', 'Adjs', 1.0],
            ['Article+Adjective', 'Article', 'Adjective', 1.0],
            ['Adjs', 'Adjective', 'Adjs', 0.8],
            ['VP', 'Verb', 'NP', 1.0],
        ],
        'lexicon' : [
            ['Noun', 'man', 0.5],
            ['Noun', 'old', 0.1],
            ['Noun', 'boat', 0.4],
            ['Verb', 'man', 0.1],
            ['Verb', 'sail', 0.1],
            ['Verb', 'think', 0.8],
            ['Adjective', 'old', 0.1],
            ['Adjective', 'young', 0.1],
            ['Adjective', 'red', 0.8],
            ['Article', 'the', 0.4],
            ['Article', 'a', 0.3],
            ['Article', 'an', 0.05],
            ['Article', 'every', 0.05]
        ]
    }

# To experiment with 'I saw a man with my telescope' 
def getGrammarTelescope():
    return {
        'syntax' : [
            ['S', 'Pronoun', 'VP', 1],
            ['VP', 'Verb', 'NP', 0.6],
            ['VP', 'Verb', 'NP+AdverbPhrase', 0.4],
            ['NP', 'Article', 'Noun', 0.3],
            ['NP', 'Adjective', 'Noun', 0.3],
            ['NP', 'NP', 'AdjectivePhrase', 0.4],
            ['NP+AdverbPhrase', 'NP', 'AdverbPhrase', 1.0],
            ['AdverbPhrase', 'Preposition', 'NP', 1.0],
        ],
        'lexicon' : [
            ['Pronoun', 'I', 1.0],
            ['Noun', 'man', 0.8],
            ['Noun', 'telescope', 0.2],
            ['Verb', 'saw', 1.0],
            ['Article', 'the', 0.7],
            ['Article', 'a', 0.3],
            ['Adjective', 'my', 1.0],
            ['Preposition', 'with', 1.0],
         ]
    }

#to experiment for lexical probabilities
def getGrammarForTest():
    return {
        'syntax' : [
            ['S', 'Adverb', 'VP', 0.1],
            ['S', 'Noun', 'VP', 0.9],
            ['VP', 'Verb', 'Noun', 0.8],
            ['VP', 'Noun', 'Verb', 0.2],
        ],
        'lexicon' : [
            ['Adverb', 'quickly', 0.4],
            ['Adverb', 'sarcastically', 0.4],  
            ['Adverb', 'tomorrow', 0.2],
            ['Noun', 'Tuesday', 0.5],
            ['Noun', 'tomorrow', 0.5],
            ['Verb', 'is', 1.0],
         ]
    }

#Converted Grammar Weather function
def getGrammarWeather():
    return {
        'syntax' : [
            ['S', 'Greeting', 'S', 0.25],
            ['S', 'NP', 'VP', 0.25], #0.5 -> 0.25
            ['S', 'WQuestion', 'VP', 0.25],
            ['S', 'WQuestion', 'NP+VP', 0.25], #added
            ['NP+VP', 'NP', 'VP', 1.0], #added
            ['VP', 'Verb', 'NP', 0.5], #0.7 -> 0.5
            ['VP', 'Verb', 'NP+AdverbPhrase', 0.3],
            ['VP', 'Verb', 'AdjPhrase', 0.2], #added
            ['NP', 'Article', 'Noun', 0.2],
            ['NP', 'Adjective', 'Noun', 0.2],
            ['NP', 'Noun', 0.2],
            ['NP', 'Pronoun', 0.2],
            ['NP', 'Name', 0.2],
            ['NP+AdverbPhrase', 'NP', 'AdverbPhrase', 0.75],
            ['NP+AdverbPhrase', 'AdverbPhrase', 'NP', 0.2],
            ['NP+AdverbPhrase', 'Adverb', 'NP+AdverbPhrase', 0.05],
            ['AdjPhrase', 'Adjective', 'PP', 1.0], #added
            ['PP', 'AdverbPhrase', 'AdverbPhrase', 1.0], #added
            ['AdverbPhrase', 'Preposition', 'NP', 0.2], 
            ['AdverbPhrase', 'Adverb', 'AdverbPhrase', 0.2],
            ['AdverbPhrase', 'AdverbPhrase', 'Adverb', 0.4],
            ['AdverbPhrase', 'Adverb', 0.2],
        ],
        'lexicon' : [
            ['Greeting', 'hi', 0.5],
            ['Greeting', 'hello', 0.5],
            ['WQuestion', 'what', 0.25], #0.5 -> 0.25
            ['WQuestion', 'will', 0.25], #added 
            ['WQuestion', 'when', 0.25],
            ['WQuestion', 'which', 0.25],
            ['Verb', 'am', 0.5],
            ['Verb', 'is', 0.25], #0.5 -> 0.25
            ['Verb', 'be', 0.25], #added
            ['Name', 'Peter', 0.1],
            ['Name', 'Sue', 0.1],
            ['Name', 'Irvine', 0.4], #0.8 -> 0.4
            ['Name', 'Tustin', 0.2], #added
            ['Name', 'Pasadena', 0.2], #added
            ['Pronoun', 'I', 1.0],
            ['Noun', 'man', 0.2],
            ['Noun', 'name', 0.2],
            ['Noun', 'temperature', 0.2], #0.6-> 0.2
            ['Noun', 'yesterday', 0.1], #added
            ['Noun', 'today', 0.1], #added
            ['Noun', 'tomorrow', 0.1], #added
            ['Noun', 'now', 0.1], #added
            ['Article', 'the', 0.7],
            ['Article', 'a', 0.3],
            ['Adjective', 'my', 0.5], #1 -> 0.5
            ['Adjective', 'hotter', 0.5], #added
            ['Adverb', 'now', 0.4],
            ['Adverb', 'today', 0.2], #0.3 -> 0.2
            ['Adverb', 'yesterday', 0.1], #added
            ['Adverb', 'tomorrow', 0.3],
            ['Preposition', 'with', 0.5],
            ['Preposition', 'in', 0.25], #0.5 -> 0.25
            ['Preposition', 'than', 0.25], #added
         ]
    }

#Converted Grammar Weather function
def getGrammarWeatherTwoFiveOne():
    return {
        'syntax' : [
            ['S', 'Greeting', 'S', 0.25],
            ['S', 'NP', 'VP', 0.5],
            ['S', 'WQuestion', 'VP', 0.25],
            ['VP', 'Verb', 'NP', 0.7],
            ['VP', 'Verb', 'NP+AdverbPhrase', 0.3],
            ['NP', 'Article', 'Noun', 0.2],
            ['NP', 'Adjective', 'Noun', 0.2],
            ['NP', 'Noun', 0.2],
            ['NP', 'Pronoun', 0.2],
            ['NP', 'Name', 0.2],
            ['NP+AdverbPhrase', 'NP', 'AdverbPhrase', 0.75],
            ['NP+AdverbPhrase', 'AdverbPhrase', 'NP', 0.2],
            ['NP+AdverbPhrase', 'Adverb', 'NP+AdverbPhrase', 0.05],
            ['AdverbPhrase', 'Preposition', 'NP', 0.2], 
            ['AdverbPhrase', 'Adverb', 'AdverbPhrase', 0.2],
            ['AdverbPhrase', 'AdverbPhrase', 'Adverb', 0.4],
            ['AdverbPhrase', 'Adverb', 0.2],
        ],
        'lexicon' : [
            ['Greeting', 'hi', 0.5],
            ['Greeting', 'hello', 0.5],
            ['WQuestion', 'what', 0.5],
            ['WQuestion', 'when', 0.25],
            ['WQuestion', 'which', 0.25],
            ['Verb', 'am', 0.5],
            ['Verb', 'is', 0.5],
            ['Name', 'Peter', 0.1],
            ['Name', 'Sue', 0.1],
            ['Name', 'Irvine', 0.4],
            ['Name', 'Tustin', 0.2],
            ['Name', 'Pasadena', 0.2],
            ['Pronoun', 'I', 1.0],
            ['Noun', 'man', 0.2],
            ['Noun', 'name', 0.2],
            ['Noun', 'temperature', 0.6],
            ['Article', 'the', 0.7],
            ['Article', 'a', 0.3],
            ['Adjective', 'my', 1.0],
            ['Adverb', 'now', 0.4],
            ['Adverb', 'today', 0.2],
            ['Adverb', 'yesterday', 0.1],
            ['Adverb', 'tomorrow', 0.3],
            ['Preposition', 'with', 0.5],
            ['Preposition', 'in', 0.5],
         ]
    }


# Sample sentences:
# Hi, I am Peter. I am Peter. Hi, my name is Peter. My name is Peter.
# What is the temperature in Irvine? What is the temperature in Irvine now? 
# What is the temperature in Irvine tomorrow? 
# 
def getGrammarWeatherOriginal():
    return {
        'syntax' : [
            ['S', 'Greeting', 'S', 0.25],
            ['S', 'NP', 'VP', 0.25],
            ['S', 'Pronoun', 'VP', 0.25],
            ['S', 'WQuestion', 'VP', 0.25],
            ['VP', 'Verb', 'NP', 0.4],
            ['VP', 'Verb', 'Name', 0.2],
            ['VP', 'Verb', 'NP', 0.1],
            ['VP', 'Verb', 'NP+AdverbPhrase', 0.3],
            ['NP', 'Article', 'Noun', 0.5],
            ['NP', 'Adjective', 'Noun', 0.5],
            ['NP+AdverbPhrase', 'NP', 'AdverbPhrase', 0.2],
            ['NP+AdverbPhrase', 'Noun', 'AdverbPhrase', 0.2],
            ['NP+AdverbPhrase', 'Noun', 'Adverb', 0.2],
            ['NP+AdverbPhrase', 'NP', 'Adverb', 0.15],
            ['NP+AdverbPhrase', 'AdverbPhrase', 'NP', 0.05],
            ['NP+AdverbPhrase', 'AdverbPhrase', 'Noun', 0.05],
            ['NP+AdverbPhrase', 'Adverb', 'Noun', 0.05],
            ['NP+AdverbPhrase', 'Adverb', 'NP+AdverbPhrase', 0.05],
            ['NP+AdverbPhrase', 'Adverb', 'NP', 0.05],
            ['AdverbPhrase', 'Preposition', 'NP', 0.2],
            ['AdverbPhrase', 'Preposition', 'Name', 0.2],
            ['AdverbPhrase', 'Adverb', 'AdverbPhrase', 0.2],
            ['AdverbPhrase', 'AdverbPhrase', 'Adverb', 0.4],
        ],
        'lexicon' : [
            ['Greeting', 'hi', 0.5],
            ['Greeting', 'hello', 0.5],
            ['WQuestion', 'what', 0.5],
            ['WQuestion', 'when', 0.25],
            ['WQuestion', 'which', 0.25],
            ['Verb', 'am', 0.5],
            ['Verb', 'is', 0.5],
            ['Name', 'Peter', 0.1],
            ['Name', 'Sue', 0.1],
            ['Name', 'Irvine', 0.8],
            ['Pronoun', 'I', 1.0],
            ['Noun', 'man', 0.2],
            ['Noun', 'name', 0.2],
            ['Noun', 'temperature', 0.6],
            ['Article', 'the', 0.7],
            ['Article', 'a', 0.3],
            ['Adjective', 'my', 1.0],
            ['Adverb', 'now', 0.4],
            ['Adverb', 'today', 0.3],
            ['Adverb', 'tomorrow', 0.3],
            ['Preposition', 'with', 0.5],
            ['Preposition', 'in', 0.5],
         ]
    }

def getGrammarWeatherExtended():
    return {
        'syntax' : [
            ['S', 'Greeting', 'S', 0.25],
            ['S', 'NP', 'VP', 0.25],
            ['S', 'WQuestion', 'VP', 0.25],
            ['S', 'WQuestion', 'NP+VP', 0.2],
            ['S', 'VP', 0.1],
            ['NP+VP', 'NP', 'VP', 1.0], 
            ['VP', 'Verb', 'NP', 0.5],
            ['VP', 'Verb', 'NP+AdverbPhrase', 0.3],
            ['VP', 'Verb', 'AdjPhrase', 0.2], 
            ['NP', 'Article', 'Noun', 0.1],
            ['NP', 'Adjective', 'NP', 0.1],
            ['NP', 'Noun', 0.2],
            ['NP', 'Pronoun', 0.2],
            ['NP', 'Name', 0.2],
            ['NP+AdverbPhrase', 'NP', 'AdverbPhrase', 0.75],
            ['NP+AdverbPhrase', 'AdverbPhrase', 'NP', 0.2],
            ['NP+AdverbPhrase', 'Adverb', 'NP+AdverbPhrase', 0.05],
            ['AdjPhrase', 'Adjective', 'PP', 1.0],
            ['PP', 'AdverbPhrase', 0.5],
            ['PP', 'AdverbPhrase', 'AdverbPhrase', 1.0], 
            ['AdverbPhrase', 'Preposition', 'NP', 0.2], 
            ['AdverbPhrase', 'Adverb', 'AdverbPhrase', 0.2],
            ['AdverbPhrase', 'AdverbPhrase', 'Adverb', 0.4],
            ['AdverbPhrase', 'Adverb', 0.2],
        ],
        'lexicon' : [
            ['Greeting', 'hi', 0.5],
            ['Greeting', 'hello', 0.5],
            ['WQuestion', 'what', 0.25], 
            ['WQuestion', 'will', 0.25], 
            ['WQuestion', 'when', 0.25],
            ['WQuestion', 'which', 0.25],
            ['Verb', 'am', 0.25],
            ['Verb', 'set', 0.25],
            ['Verb', 'is', 0.25], 
            ['Verb', 'be', 0.25], 
            ['Name', 'Irvine', 0.2], 
            ['Name', 'Tustin', 0.2], 
            ['Name', 'Pasadena', 0.1],
            ['Name', 'Portland', 0.1],
            ['Name', 'San Jose', 0.1],
            ['Name', 'home', 0.1],
            ['Pronoun', 'I', 1.0],
            ['Noun', 'man', 0.2],
            ['Noun', 'name', 0.2],
            ['Noun', 'temperature', 0.2], 
            ['Noun', 'yesterday', 0.1], 
            ['Noun', 'today', 0.1], 
            ['Noun', 'tomorrow', 0.1], 
            ['Noun', 'now', 0.05],
            ['Noun', 'Celsius', 0.05],
            ['Article', 'the', 0.7],
            ['Article', 'a', 0.3],
            ['Adjective', 'my', 0.5], 
            ['Adjective', 'hotter', 0.5], 
            ['Adverb', 'now', 0.4],
            ['Adverb', 'today', 0.2], 
            ['Adverb', 'yesterday', 0.1], 
            ['Adverb', 'tomorrow', 0.3],
            ['Preposition', 'with', 0.25],
            ['Preposition', 'to', 0.25],
            ['Preposition', 'in', 0.25], 
            ['Preposition', 'than', 0.25], 
         ]
    }

def getGrammarWeatherCustomLocations(locationsDict):
    grammar = {
        'syntax' : [
            ['S', 'Greeting', 'S', 0.1],
            ['S', 'NP', 0.05],
            ['S', 'NP', 'S', 0.1],
            ['S', 'NP', 'VP', 0.1],
            ['S', 'WQuestion', 'NP+AdverbPhrase', 0.1],
            ['S', 'VP', 'NP+AdverbPhrase', 0.05],
            ['S', 'WQuestion', 'VP', 0.15],
            ['S', 'NP+AdverbPhrase', 0.05],
            ['S', 'PP', 0.05],
            ['S', 'WQuestion', 'NP+VP', 0.15],
            ['S', 'VP', 0.1],
            ['NP+VP', 'NP', 'VP', 1.0], 
            ['VP', 'Verb', 'NP', 0.5],
            ['VP', 'Verb', 'NP+AdverbPhrase', 0.2],
            ['VP', 'Verb', 'AdjPhrase', 0.2],
            ['VP', 'AdjPhrase', 0.1],
            ['NP', 'Article', 'NP', 0.1],
            ['NP', 'Adjective', 'NP', 0.1],
            ['NP', 'Noun', 'Adjective', 0.1],
            ['NP', 'Noun', 0.2],
            ['NP', 'Pronoun', 0.1],
            ['NP', 'Name', 0.2],
            ['Verb', 'Verb', 'VerbAdd', 1.0],
            ['NP+AdverbPhrase', 'NP', 'AdverbPhrase', 0.75],
            ['NP+AdverbPhrase', 'AdverbPhrase', 'NP', 0.2],
            ['NP+AdverbPhrase', 'Adverb', 'NP+AdverbPhrase', 0.05],
            ['AdjPhrase', 'Adjective', 'PP', 1.0],
            ['PP', 'AdverbPhrase', 0.5],
            ['PP', 'AdverbPhrase', 'AdverbPhrase', 1.0], 
            ['AdverbPhrase', 'Preposition', 'NP', 0.2], 
            ['AdverbPhrase', 'Adverb', 'AdverbPhrase', 0.2],
            ['AdverbPhrase', 'AdverbPhrase', 'Adverb', 0.2],
            ['AdverbPhrase', 'AdverbPhrase', 'Adjective', 0.2],
            ['AdverbPhrase', 'Adverb', 0.2],
        ],
        'lexicon' : [
            ['Greeting', 'hi', 0.5],
            ['Greeting', 'hello', 0.5],
            ['WQuestion', 'what', 0.15],
            ['WQuestion', 'say', 0.1],
            ['WQuestion', 'will', 0.1],
            ['WQuestion', 'was', 0.05],
            ['WQuestion', 'is', 0.1],
            ['WQuestion', 'when', 0.25],
            ['WQuestion', 'which', 0.20],
            ['WQuestion', 'are', 0.05],
            ['Verb', 'am', 0.25],
            ['Verb', 'set', 0.25],
            ['Verb', 'is', 0.05],
            ['Verb', 'has', 0.05],
            ['Verb', 'was', 0.1],
            ['Verb', 'will', 0.05],
            ['Verb', 'add', 0.10],
            ['Verb', 'be', 0.05],
            ['Verb', 'tell', 0.1],
            ['VerbAdd','be', 1.0],
            ['Pronoun', 'I', 0.5],
            ['Pronoun', 'me', 0.5],
            ['Noun', 'man', 0.1],
            ['Noun', 'database', 0.1],
            ['Noun', 'name', 0.05],
            ['Noun', 'age', 0.05],
            ['Noun', 'city', 0.1],
            ['Noun', 'temperature', 0.05],
            ['Noun', 'rain', 0.025],
            ['Noun', 'snow', 0.025],
            ['Noun', 'alert', 0.025],
            ['Noun', 'alerts', 0.025],
            ['Noun', 'yesterday', 0.1], 
            ['Noun', 'today', 0.05], 
            ['Noun', 'tomorrow', 0.05], 
            ['Noun', 'now', 0.05],
            ['Noun', 'Celsius', 0.025],
            ['Noun', 'metric', 0.025],
            ['Noun', 'standard', 0.025],
            ['Noun', 'imperial', 0.025],
            ['Noun', 'sunrise', 0.05],
            ['Noun', 'sunset', 0.05],
            ['Article', 'the', 0.4],
            ['Article', 'any', 0.3],
            ['Article', 'a', 0.3],
            ['Adjective', 'my', 0.1],
            ['Adjective', 'weather', 0.1],
            ['Adjective', 'your', 0.1],
            ['Adjective', 'hotter', 0.2],
            ['Adjective', 'warmer', 0.1],
            ['Adjective', 'colder', 0.1],
            ['Adjective', 'amount', 0.05],
            ['Adjective', 'random', 0.05],
            ['Adjective', 'morning', 0.05],
            ['Adjective', 'evening', 0.05],
            ['Adjective', 'nighttime', 0.05],
            ['Adjective', 'afternoon', 0.05],
            ['Adverb', 'now', 0.4],
            ['Adverb', 'today', 0.2], 
            ['Adverb', 'yesterday', 0.1], 
            ['Adverb', 'tomorrow', 0.1],
            ['Adverb', 'there', 0.1],
            ['Adverb', 'favorite', 0.1],
            ['Preposition', 'with', 0.25],
            ['Preposition', 'to', 0.25],
            ['Preposition', 'in', 0.15],
            ['Preposition', 'of', 0.1],
            ['Preposition', 'than', 0.25], 
         ]
    }
    for key in locationsDict.keys():
        probability = 1/(len(locationsDict))
        grammar['lexicon'].append(['Name', key, probability])

    return grammar
# Unit testing code
if __name__ == '__main__':
    verbose = True
    #CYKParse(['the', 'wumpus', 'is', 'dead'], getGrammarE0())
    #CYKParse(['the', 'wumpus', 'is', 'dead'], getGrammarE0Original())
    #CYKParse(['the', 'wumpus', 'is'], getGrammarE0())
    #CYKParse(['the', 'wumpus', 'is'], getGrammarE0Original())
    #CYKParse(['the', 'old', 'man', 'the', 'boat'], getGrammarGardenPath())
    #CYKParse(['I', 'saw', 'a', 'man', 'with', 'my', 'telescope'], getGrammarTelescope())
    #CYKParse(['my', 'name', 'is', 'Peter'], getGrammarWeather())
    #CYKParse(['my', 'name', 'is', 'Peter'], getGrammarWeatherOriginal())
    #CYKParse(['hi', 'I', 'am', 'Peter'], getGrammarWeather())
    #CYKParse(['hi', 'I', 'am', 'Peter'], getGrammarWeatherOriginal())
    #CYKParse(['what', 'is', 'the', 'temperature', 'in', 'Irvine'], getGrammarWeather())
    #CYKParse(['what', 'is', 'the', 'temperature', 'in', 'Irvine'], getGrammarWeatherOriginal())
    #CYKParse(['what', 'is', 'the', 'temperature', 'in', 'Irvine', 'now'], getGrammarWeather())
    #CYKParse(['what', 'is', 'the', 'temperature', 'in', 'Irvine', 'now'], getGrammarWeatherOriginal())
    #CYKParse(['what', 'is', 'the', 'temperature', 'now', 'in', 'Irvine'], getGrammarWeather())
    #CYKParse(['what', 'is', 'the', 'temperature', 'now', 'in', 'Irvine'], getGrammarWeatherOriginal())
    #CYKParse(['what', 'is', 'now', 'the', 'temperature', 'in', 'Irvine'], getGrammarWeather())
    #CYKParse(['what', 'is', 'now', 'the', 'temperature', 'in', 'Irvine'], getGrammarWeatherOriginal())
    #CYKParse(['will', 'yesterday', 'be', 'hotter', 'than', 'today', 'in', 'Pasadena'], getGrammarWeather())
    #CYKParse(['what', 'is', 'now', 'the', 'temperature'], getGrammarWeatherExtended())
    #CYKParse(['will', 'yesterday', 'be', 'hotter', 'than', 'today'], getGrammarWeatherExtended())
    #CYKParse(['will', 'yesterday', 'be', 'hotter', 'than', 'today', 'in', 'Pasadena'], getGrammarWeatherExtended())
    #CYKParse(['set', 'the', 'temperature', 'to', 'Celsius'], getGrammarWeatherExtended())

    #testing for  experiment
    #CYKParse(['tomorrow', 'is', 'Tuesday'], getGrammarForTest())


# Hi, I am Peter. I am Peter. Hi, my name is Peter. My name is Peter.
# What is the temperature in Irvine? What is the temperature in Irvine now? 
# What is the temperature in Irvine tomorrow? 