import spacy
import random
from pattern3.text.en import lexeme

def make_grammar_mistake(sentence):
    doc = nlp(sentence)
    for token in doc:
        if token.pos_ == 'VERB':
            # Replace the verb with a random conjugation
            verb = token.lemma_
            conjugations = [verb]
            for form in ['inf', '1sg', '2sg', '3sg', 'pl']:
                conjugations.append(token._.conjugacy.get(form, verb))
            new_verb = random.choice(conjugations)
            sentence = sentence[:token.idx] + new_verb + sentence[token.idx+token.__len__():]
            break  # Only replace the first verb found
    return sentence

nlp = spacy.load('en_core_web_sm')
sentence = "He was doing mouse"
doc = nlp(sentence)

import nltk
from nltk.tokenize import word_tokenize


def split_chunks(sentence):
    # tokenize the sentence into words
    words = nltk.word_tokenize(sentence)

    # use part-of-speech tagging to get the part of speech for each word
    pos_tags = nltk.pos_tag(words)

    # create a chunk pattern using regular expressions
    chunk_pattern = r'''
        NP: {<DT>?<JJ.*>*<NN.*>+}  # chunk one or more noun phrases
        VP: {<MD>?<VB.*>+}         # chunk one or more verb phrases'''
        # # PP: {<IN><NP>}             # chunk prepositional phrases
        # # ADJP: {<JJ.*>}             # chunk one or more adjective phrases
        # '''

    # create a chunk parser using the chunk pattern
    chunk_parser = nltk.RegexpParser(chunk_pattern)

    # parse the part-of-speech tagged sentence and get the chunks
    chunks = chunk_parser.parse(pos_tags)

    # convert the chunks to a list of strings
    chunk_strings = []
    for subtree in chunks.subtrees():
        if subtree.label() in ['NP', 'VP']:
            chunk_strings.append(' '.join(word for word, tag in subtree.leaves()))

    return chunk_strings

def detect_tense(sentence):
    # tokenize the sentence into words
    words = word_tokenize(sentence)

    # use part-of-speech tagging to get the tense of the verbs
    pos_tags = nltk.pos_tag(words)

    # extract the tense of the verbs
    present = False
    past = False
    future = False
    present_continuous = False
    past_participle = False

    for word, tag in pos_tags:
        print(word, tag)

        # if tag.startswith('V'):  # check if the word is a verb
        #     if tag.endswith('IN'):  # infinitive
        #         # ignore infinitive for tense detection
        #         continue
        #     elif tag.endswith('VBG'):  # present participle/gerund
        #         present_continuous = True
        #     elif tag.endswith('VBD'):  # past tense
        #         past = True
        #     elif tag.endswith('VBN'):  # past participle
        #         past_participle = True
        #     elif tag.endswith('VBZ'):  # present tense, 3rd person singular
        #         present = True
        #     elif tag.endswith('VBP'):  # present tense, not 3rd person singular
        #         present = True
        #     elif tag.endswith('MD'):  # modal verb, indicating future tense
        #         future = True

    # if no verb was found, assume present tense
    if not (present or past or future or present_continuous or past_participle):
        present = True

    # create a list of detected tenses
    tenses = []
    if present:
        tenses.append('present')
    if past:
        tenses.append('past')
    if future:
        tenses.append('future')
    if present_continuous:
        tenses.append('present continuous')
    if past_participle:
        tenses.append('past participle')

    return tenses


import spacy
from spacy.matcher import Matcher
from spacy.util import filter_spans
from spacy.attrs import LOWER, POS, ENT_TYPE, IS_ALPHA

nlp = spacy.load('en_core_web_sm')

def get_verb_form(sentence):
    VERB_PATTERN = [{'POS': 'VERB', 'OP': '?'},
                    {'POS': 'AUX', 'OP': '*'},
                    {'POS': 'VERB', 'OP': '+'}]

    # instantiate a Matcher instance
    matcher = Matcher(nlp.vocab)
    matcher.add("Verb phrase", [VERB_PATTERN])

    doc = nlp(sentence)
    # call the matcher to find matches
    matches = matcher(doc)
    spans = [doc[start:end] for _, start, end in matches]
    return ([[(token.text, token.tag_, token.pos_, token.lemma_) for token in span] for span in spans])


sentences = ['The cat sat on the mat. He quickly ran to the market. '
            'The dog has gonr into the water. '
            'The author is being writing a book.'
            'The dog jumps']


for sentence in sentences:

    for verbs in get_verb_form(sentence):
        for v in verbs:
            print(lexeme(v[3]))




# print([(token.text, token.tag_, token.pos_) for token in [doc[start:end] for _, start, end in matches]])