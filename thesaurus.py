import textwrap
from nltk.corpus import wordnet as wn

POS = {
    'v': 'verb', 'a': 'adjective', 's': 'satellite adjective', 
    'n': 'noun', 'r': 'adverb'}

def info(word, pos=None):
    for i, syn in enumerate(wn.synsets(word, pos)):
        syns = [n.replace('_', ' ') for n in syn.lemma_names]
        ants = [a for m in syn.lemmas for a in m.antonyms()]
        ind = ' '*12
        defn= textwrap.wrap(syn.definition, 64)
        print 'sense %d (%s)' % (i + 1, POS[syn.pos])
        print 'definition: ' + ('\n' + ind).join(defn)
        print '  synonyms:', ', '.join(syns)
        if ants:
            print '  antonyms:', ', '.join(a.name for a in ants)
        if syn.examples:
            print '  examples: ' + ('\n' + ind).join(syn.examples)
        print

info('near')