from __future__ import unicode_literals, division, absolute_import
import re
import pycountry

class ParseWarning(Warning):

    def __init__(self, value, **kwargs):
        self.value = value
        self.kwargs = kwargs


class TitleParser(object):

    propers = ['proper', 'repack', 'rerip', 'real', 'final']

    specials = ['special']

    editions = ['dc', 'extended', 'uncut', 'remastered', 'unrated', 'theatrical', 'chrono', 'se']

    # TODO: All of the quality related keywords can probably be removed from here, as the quality module handles them
    codecs = ['x264', 'x.264', 'h264', 'h.264', 'XViD']

    # lowercase required
    cutoffs = ['limited', 'xvid', 'h264', 'x264', 'h.264', 'x.264', 'screener', 'unrated', '3d', 'extended',
               'directors', 'director\'s', 'multisubs', 'dubbed', 'subbed', 'multi'] + propers + specials + editions

    remove = ['imax']

    sounds = ['AC3', 'DD5.1', 'DTS']
        
    __languages_name = {'VF', pycountry.languages.get(alpha2='fr')}    
    __languages_code = {}
    __countries_code = {}
    __countries_name = {}
    
    for lang in pycountry.languages:
        __languages_code[lang.bibliographic.lower()] = lang
        __languages_name[lang.name.lower()] = lang
        __languages_name["true" + lang.name.lower()] = lang
        
    for country in pycountry.countries:
        __countries_code[country.alpha3.lower()] = country
        __countries_code[country.alpha2.lower()] = country
        __countries_name[country.name.lower()] = country
        __countries_name["true" + country.name.lower()] = country

    @staticmethod
    def re_not_in_word(regexp):
        return r'(?<![^\W_])' + regexp + r'(?![^\W_])'

    @staticmethod
    def strip_spaces(text):
        """Removes all unnecessary duplicate spaces from a text"""
        return ' '.join(text.split())

    @staticmethod
    def remove_words(text, words, not_in_word=False):
        """Clean all given :words: from :text: case insensitively"""
        for word in words:
            text = TitleParser.ireplace(text, word, '', not_in_word=not_in_word)
        # remove duplicate spaces
        text = ' '.join(text.split())
        return text

    @staticmethod
    def ireplace(data, old, new, count=0, not_in_word=False):
        """Case insensitive string replace"""
        old = re.escape(old)
        if not_in_word:
            old = TitleParser.re_not_in_word(old)
        pattern = re.compile(old, re.I)
        return re.sub(pattern, new, data, count)
    
    @staticmethod
    def language_from_name(word):
        """Retrieves language from name word
        
        :param word: the word to test ('English', 'French', 'German', 'TrueFrench', ...)
        :return: the pycountry.db.Language object, or None if word is not a language name
        """
        lword = word.lower()
        lang = TitleParser.__languages_name.get(lword)
        if not lang:
            lang = TitleParser.__countries_name.get(lword)
        return lang
    
    @staticmethod
    def language_from_code(word):
        """Retrieves language from code word
        
        :param word: the word to test ('en', 'fr', 'ge', ...)
        :return: the pycountry.db.Language object, or None if word is not a language name
        """
        lword = word.lower()
        lang = TitleParser.__languages_code.get(lword)
        if not lang:
            lang = TitleParser.__countries_code.get(lword)
        return lang
    