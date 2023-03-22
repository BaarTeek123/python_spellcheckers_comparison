from re import findall
import language_tool_python
import textblob
from autocorrect import Speller
# grammar
from gingerit.gingerit import GingerIt  # limit to 300 chars for free trial
# spell checkers
from spellchecker import SpellChecker

from gramformer import Gramformer  # needs run "python -m spacy download en"
import torch
from jamspell import TSpellCorrector
import spacy
import pysbd

from decorators import timeit

""" load spell checkers """
language_tool = language_tool_python.LanguageTool('en-US')
gingerit_tool = GingerIt()
spell_checker_tool = SpellChecker(language=u'en', distance=10)
autocorrect_tool = Speller()
jamspell_corrector = TSpellCorrector()
model = spacy.load('en_core_web_md')
# jamspell_corrector.LoadLangModel(model)
jamspell_corrector.LoadLangModel("../modells/en.bin")

segmentor = pysbd.Segmenter(language="en", clean=False)


# set seed for gramformer

def set_seed(seed):
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
#
#
set_seed(1212)
gramformer_tool = Gramformer(models=1)

@timeit
def correct_with_spellchecker(word_or_list_of_words='') -> str:
    """ A function which returns corrected spelling (by SpellChecker)"""
    if isinstance(word_or_list_of_words, str) and " " in word_or_list_of_words:
        word_or_list_of_words = word_or_list_of_words.split()

    if isinstance(word_or_list_of_words, list):
        return " ".join(list(filter(lambda item: item is not None,[spell_checker_tool.correction(word) for word in word_or_list_of_words])))+'.'
    return " ".join(word_or_list_of_words) + '.'


@timeit
def correct_with_autocorrect(sentence: str) -> str:
    """ A function which returns corrected spelling (by Speller from autocorrect)"""
    return autocorrect_tool(sentence)

@timeit
def correct_with_textblob(sentence) -> str:
    """A function which returns corrected spelling (by TextBlob)"""
    return str(textblob.TextBlob(sentence).correct())

@timeit
def correct_with_gingerit(sentence: str) -> str:
    """ A function which returns corrected sentence (by GingerIt from gingerit.gingerit)"""
    if len(sentence) < 300:
        return gingerit_tool.parse(sentence)['result']
    # workaround for GingerIt free trial limits.
    subsegments = []
    tmp = ''
    for word in sentence.split():
        if len(tmp + word) > 300:
            subsegments.append(tmp)
            tmp = ''
        tmp += ' ' + word
    return " ".join([gingerit_tool.parse(sub)['result'] for sub in subsegments])



@timeit
def correct_with_languagetool(sentence: str) -> str:
    """ A function which returns corrected sentence (by language_tool from language_tool_python)"""
    return language_tool.correct(sentence)

@timeit
def correct_with_gramformer(sentence: str) -> str:
    """ A function which returns corrected sentence using GramFormer (from gramformer)"""
    return list(gramformer_tool.correct(sentence))[0]

@timeit
def correct_with_jamspell(sentence: str) -> str:
    """ A function which returns corrected sentence using JamSpell (from JamSpell)"""
    return jamspell_corrector.FixFragment(sentence)

