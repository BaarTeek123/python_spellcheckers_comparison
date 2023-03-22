import os
from nltk.tokenize import RegexpTokenizer
import re
import spacy
import string
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag


walk_dir = './texts'
pattern = r' *[\.\?!][\'"\)\]]* *|\n+'
# pattern = r"(?<=\b[^.\d])\s*[.!?](?=\s|$)|[.!?](?=\s|$)"



def split_sentences(text, pattern):
    return list(filter(str.strip, re.split(pattern, text)))


def filter_sentences_with_verbs(sentences, limit: int = 10000):
    verb_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']  # Define the verb tags
    filtered_sentences = []
    for sentence in sentences:
        tokens = word_tokenize(sentence)
        tagged_tokens = pos_tag(tokens)
        if any(tag in verb_tags for word, tag in tagged_tokens):
            filtered_sentences.append(sentence)
        if len(filtered_sentences) > limit:
            return filtered_sentences
    return filtered_sentences

# size = 0
# __sentence_tokenizer = RegexpTokenizer('[.;!?\n]', gaps=True)
# for root, subdirs, files in os.walk(walk_dir):
#     for file in files:
#         output = ''
#         with open(root + '/' + file, "r") as f:
#             text = split_sentences(f.read(), pattern)
#             for sentence in text:
#                 if len(sentence.split()) > 3:
#                     output += ''.join([x if x in (string.printable) else '' for x in sentence]) + '.\n'
#
#         with open("texts/input_sentences.txt", mode='a') as f:
#             f.write(output)
#         # f = open(root + '/' + file, "r")
#         # text = split_sentences(f.read(), pattern)
#         # print(len(text), type(text))
#         # filter_sentences_with_verbs(text)
#         # print(len(text), type(text))
#
#
#
#
#
#         # for sentence in __sentence_tokenizer.tokenize(f.read()):
#         #     print(sentence)


if __name__ == '__main__':
    with open('./texts/input_sentences.txt') as f:
        sentences = f.read().replace('\t', '')

    with open('texts/input_sentences.txt', mode='w+') as f:
        f.write(sentences)

