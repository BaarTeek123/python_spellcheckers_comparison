import json
import re
import urllib3

import nltk.parse.generate as generator
from nltk import CFG, grammar, corpus

# allows using $ in grammar rules
grammar._STANDARD_NONTERM_RE = re.compile('( [\w/][\w$/^<>-]* ) \s*', re.VERBOSE)

# from pattern3.text.en import conjugate, lemma, lexeme, PRESENT, SG, pluralize, referenced

class Sentence:
    def __init__(self, subject, verb_phrase, *args):
        if len(subject) > 1:
            self.subject = subject[0].upper() + subject.lower()[1:]
        else:
            self.subject = subject[0].upper()
        self.verb_phrase = verb_phrase.lower()
        self.rest_of_sent = " ".join(args)
        self.core_sentence = self.subject + ' ' + self.verb_phrase + self.rest_of_sent + '.'

    def __str__(self):
        return f'{self.core_sentence}'

    def set_verb_phrase(self, new_verb_phrase: str):
        self.verb_phrase = new_verb_phrase
        self.core_sentence = self.subject + ' ' + self.verb_phrase + ' ' + self.rest_of_sent + '.'


class PhraseGenerator:
    grammar_rules = """NP -> N_SG | N_PL | PERSON_SG 
NP_3 -> 'He' | 'She' | 'It' | NP_SG
NP_Not_3 -> 'I' | NP_PL
Adj -> JJR 'than' NP | 'the' JJS | VBD | VBG
NP_SG -> Det_SG NNP 
NP_PL -> Det_PL NNPS | PERSON_PL
N_SG -> 'a' NNP_A_CNTBL | 'an' NNP_AN_CNTBL | NNP_UNCTNBL | Det_SG NNP | Det_PL NNPS | Det NNP | Det_NP
PP -> PR NP | PRP$ NP |
Det_SG -> Det | 'this' 
Det_PL -> 'these' | 'some' | 'both' 
Det -> 'the' | 'my' | 'your' | 'our' | 'their' | 'no' | 'that' | 'every' | 'any'
PR -> 'in' | 'on' | 'with' | 'by'
PERSON_PL -> 'we' | 'you' | 'they'
PERSON_SG -> 'I' | 'he' | 'she' | 'it'
MD -> 'ought to' | 'should' | 'could' | 'will' | 'must' | 'would' | 'might' | 'may' | 'can'
I -> 'I' | 'I'
"""

    def __init__(self, grammar_correct_rule: str):
        self.__convert_from_dict_to_gramma_form(get_dict_of_pos_tagged_word(corpus.conll2000))
        self.grammar_rules = f'S -> {grammar_correct_rule}\n{self.grammar_rules}'

    def __convert_from_dict_to_gramma_form(self, dict_tagged_words: dict):
        """A method that converts dictionary to gramma form (defined for nltk.CFG.fromstring()
        , e.g. 'MD -> 'ought to' | 'should' | 'could' | 'will' | 'must' | 'would' | 'might' | 'may' | 'can''
        """
        text = ''
        for key in dict_tagged_words.keys():
            text = text + key + " -> '" + "' | '".join(dict_tagged_words[key]) + "'\n"
        self.grammar_rules += text

    def generate_phrase(self, amount_of_sentences: int = 1) -> list:
        tmp = []
        sent_generator = generator.generate(CFG.fromstring(self.grammar_rules), n=amount_of_sentences)
        for sent in sent_generator:
            tmp.append(" ".join(sent))
        return tmp

def get_dict_of_pos_tagged_word(source_tagged_word_list) -> dict:
    """Function that return dictionary with POS-tags as keys and set of words as values.
    e.g. {'NN': {'radiation', 'consumer', 'border', 'health'}, 'IN': {'of', 'notwithstanding', 'with',
    'from', 'inside', 'between', 'besides'}...}
    An argument should be a list with tuples (word, POS-tag), e.g.: ('Confidence', 'NN'), ('in', 'IN'), ('the', 'DT')"""
    tagged_words = {}
    for tup_word_pos_tag in source_tagged_word_list.tagged_words():
        if tup_word_pos_tag[0].isalnum() and tup_word_pos_tag[1] not in tagged_words.keys():
            tagged_words[tup_word_pos_tag[1]] = {tup_word_pos_tag[0].lower()}
        elif tup_word_pos_tag[0].isalnum():
            tagged_words[tup_word_pos_tag[1]].add(tup_word_pos_tag[0].lower())
    return tagged_words

def is_countable_noun(noun: str) -> bool:
    """Function that checks if the noun is countable or uncountable."""
    noun = re.sub(' ', '\+', noun)
    url = 'https://books.google.com/ngrams/graph?content=many+' + noun + '%2C+much+' + noun + '&year_start=1750&year_end=2020'
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    html = response.data.decode()
    noun = re.sub('\+', ' ', noun)
    try:
        many_data = json.loads(re.search('\{"ngram": "many ' + noun + '".*?\}', html, re.IGNORECASE).group(0))[
            'timeseries']
        many = sum(many_data) / float(len(many_data))
    except:
        many = 0.0

    try:
        much_data = json.loads(re.search('\{"ngram": "much ' + noun + '".*?\}', html, re.IGNORECASE).group(0))[
            'timeseries']
        much = sum(much_data) / float(len(much_data))
    except:
        much = 0.0
    return many >= much


