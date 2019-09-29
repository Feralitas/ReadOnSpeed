#!/usr/bin/env python

# -*- coding: iso-8859-1 -*-

#PATH=$PATH:/c/Users/Tomixed/AppData/Local/conda/conda/envs/hackzurich

from __future__ import print_function, unicode_literals

import sys
import time
import math
import fileinput
from kivy.utils import escape_markup

def to_unicode(text, encoding='utf-8'):
    """Convert ``text`` to unicode using ``encoding``.

    :param text: string object to convert to ``unicode``
    :type text: ``str`` or ``unicode``
    :returns: string object as unicode object
    :rytpe: ``unicode``
    """
    if isinstance(text, str):
        if not isinstance(text, str):
            text = str(text, encoding)
    return text

class fastReader(object):
    

    def get_orp(self, integer):
        """Get Optimal Reading Position (ORP) given ``integer``.
        ORP is slightly left of center.

        :param integer: length of string object to calculate ORP
        :type integer: ``integer``
        :returns: value of ORP
        :rytpe: ``integer``
        """
        percentage = 0.35
        orp = int(math.ceil(integer * percentage))
        if orp > 5:
            return 5
        else:
            return orp

    def calculate_spaces(self, word, max_length):
        """Determine buffer spaces for ``word`` given the ``max_length``.

        :param word: string object for calculation
        :type word: ``unicode``
        :param max_length: value of longest word in full text
        :type max_length: ``integer``
        :returns: word's ORP, number of prefix spaces, and number of post spaces
        :rytpe: ``tuple`` of ``integers``
        """
        max_orp = self.get_orp(max_length)
        if len(word) < 3:
            orp = len(word)
        else:
            orp = self.get_orp(len(word))
        prefix_space = (max_orp - orp)
        postfix_space = (max_length - len(word) - prefix_space)
        
        if orp != 0:
            orp -= 1
        return (orp, prefix_space, postfix_space)

    def find_max(self, reading):
        """Find longest word in ``reading``.

        :param reading: the full string object to be spritzed
        :type reading: ``unicode``
        :returns: number of characters in the longest word
        :rytpe: ``integer``
        """
        reading = sorted(reading, key=len, reverse=True)
        return len(reading[0])

    ##################################################
    #   Output Functions                             #
    ##################################################

    def color_orp_char(self, word, orp):
        """Change color of the ORP letter in ``word`` to red.

        :param word: the word to be color-coded
        :type word: ``unicode``
        :param orp: the index of the ORP letter
        :type orp: ``integer``
        :returns: word with ORP letter in red
        :rytpe: ``unicode``
        """
        color_red = '[color=ff3333]'
        color_restore = '[/color]'
        return escape_markup(word[0:orp]) \
               + color_red + escape_markup(word[orp:orp+1]) \
               + color_restore + escape_markup(word[orp+1:])

    def print_word(self, word, orp_config):
        """Pretty print ``word`` with spritz color formatting

        :param word: the word to be color-coded
        :type word: ``unicode``
        :param orp_config: formatting data for ``word``
        :type orp_config: ``tuple`` of ``integers``
        :returns: Nothing. Prints to console
        :rytpe: ``None``
        """
        (orp, prefix, postfix) = orp_config
        orp = orp - 1           # change for Python list indexing
        print_string = (" " * prefix) + self.color_orp_char(word, orp) + (" " * postfix)

        print("\r{}".format(print_string))
        sys.stdout.flush()

    ##################################################
    #   Clean-Up Functions                           #
    ##################################################

    def parse_article(self, article):
        """Clean up input ``article`` and insert appropriate pauses.
        
        :param article: the full string object to be spritzed
        :type article: ``unicode``
        :returns: words in ``article``
        :rytpe: ``list``
        """
        remove = (',', '.', '!', '?', '-', ';', '-', '(', ')')

        for char in remove:
            article = article.replace(char, " <pause> ") #//MW_TODO doppelte pausen raus

        article = article.strip()
        #article = article.replace("\n", " <pause> ")

        return article.split()

    def word2factor(self, word):
        length=len(word)
        factor = 1
        factor += round(length / 13)
        return factor

    def getNextWord(self):
        
        msPerChar = self.maxMsPerChar - (self.wheelSpeed / 10)
        
        word = self.textToRead[self.wordPos]
        if self.direction > 0:
            if word == "<pause>":
                #(highlightPos, prefix_space, postfix_space) = self.calculate_spaces(self.textToRead[self.wordPos-1], self.max_length)
                durationInSec = (msPerChar*self.charPerWhitespace)/1000
                word=""
                #word = (" " * prefix_space) + self.color_orp_char(self.textToRead[self.wordPos-1], highlightPos) + (" " * postfix_space)
            else:
                (highlightPos, prefix_space, postfix_space) = self.calculate_spaces(word, self.max_length)
                
                durationInSec = (msPerChar*self.word2factor(word))/1000
                word = (" " * prefix_space) + self.color_orp_char(word, highlightPos) + (" " * postfix_space)                    
            self.wordPos = self.wordPos + 1
            if self.wordPos > len(self.textToRead)-1:
                self.wordPos = len(self.textToRead)-1
        elif self.direction < 0:
            if word == "<pause>":
                #(highlightPos, prefix_space, postfix_space) = self.calculate_spaces(self.textToRead[self.wordPos+1], self.max_length)
                
                durationInSec = (msPerChar*self.charPerWhitespace)/1000
                word =""
                #word = (" " * prefix_space) + self.color_orp_char(self.textToRead[self.wordPos+1], highlightPos) + (" " * postfix_space)
            else:
                (highlightPos, prefix_space, postfix_space) = self.calculate_spaces(word, self.max_length)
                
                durationInSec = (msPerChar*self.word2factor(word))/1000
                word = (" " * prefix_space) + self.color_orp_char(word, highlightPos) + (" " * postfix_space)                    
            self.wordPos = self.wordPos - 1
            if self.wordPos < 0:
                self.wordPos = 0
        else:                
            if word == "<pause>":                
                word = ""
            else:
                (highlightPos, prefix_space, postfix_space) = self.calculate_spaces(word, self.max_length)
                word = (" " * prefix_space) + self.color_orp_char(word, highlightPos) + (" " * postfix_space)
                
            durationInSec = 0.05 #(msPerChar*len(word))/1000
        return (word, durationInSec)

    def setWheelSpeed(self, speed):
        self.direction = 1
        if speed == 0:
            self.wheelSpeed = 0
            self.direction = 0
        elif speed < 0:
            #revert!
            self.direction = -1
            if speed < -999:
                self.wheelSpeed = 999
            else:
                self.wheelSpeed = abs(speed)
        elif speed > 999:
            self.wheelSpeed = 999
        else:
            self.wheelSpeed = speed

    def prepareNewText(self, newText):
        self.wordPos = 0
        self.wheelSpeed = 0
        self.max_length = 0
        self.direction = 1
        self. maxMsPerChar = 100
        self.charPerWhitespace = 3
        self.textToRead = self.parse_article(newText)
        self.max_length = self.find_max(self.textToRead)

#variables

##################################################
#   Spritz Function                              #
##################################################

def spritz(wpm, reading):
    """"Spritz" the ``reading``.

    :param wpm: words per minute
    :type wpm: ``integer``
    :param reading: the full string object to be spritzed
    :type reading: ``unicode``
    :returns: Nothing. Prints to console
    :rytpe: ``None``
    """

    wheelSpeed = wpm
    wordPos = 0
    direction = 1

    if wheelSpeed == 0:
        #stop
        direction = 0
    elif wheelSpeed < 0:
        #revert!
        direction = -1
        if wheelSpeed < -999:
            wheelSpeed = 999
        else:
            wheelSpeed = abs(wheelSpeed)
    elif wheelSpeed > 999:
        wheelSpeed = 999
    
    maxMsPerChar = 100
    charPerWhitespace = 3
    msPerChar = maxMsPerChar - (wheelSpeed / 10)
    
    reading = parse_article(reading)
    max_length = find_max(reading)

    if direction > 0:
        for word in reading:
            wordPos = wordPos + 1
            if word == "<pause>":
                time.sleep((msPerChar*charPerWhitespace)/1000)
                continue
            #print ("wait " + str((msPerChar*len(word))/1000)+" ms/char "+ str(msPerChar))
            time.sleep((msPerChar*len(word))/1000)
            orp_config = calculate_spaces(word, max_length)
            print_word(word, orp_config)
    elif direction < 0:
        for word in reversed(reading[:len(reading)-4]):
            wordPos = wordPos - 1
            if word == "<pause>":
                time.sleep((msPerChar*charPerWhitespace)/1000)
                continue
            #print ("wait " + str((msPerChar*len(word))/1000)+" ms/char "+ str(msPerChar))
            time.sleep((msPerChar*len(word))/1000)
            orp_config = calculate_spaces(word, max_length)
            print_word(word, orp_config)
    else:
            time.sleep(msPerChar/1000)
##################################################
#   Main Function                                #
##################################################

def main():
    """Parse command line args and spritz text.
    """
    if len(sys.argv) >= 2 and sys.argv[1]:
        try:
            wpm = int(sys.argv[1])
        except ValueError:
            print ("<wpm> need to be an integer")
            exit(1)
    else:
        wpm = 250

    
    
    #spritz(wpm, article)

    

    article = ""
    
    for line in fileinput.input(sys.argv[2:], openhook=fileinput.hook_encoded("utf-8")):
        article += to_unicode(line)


    reader = fastReader()
    reader.prepareNewText(article)
    reader.setWheelSpeed(wpm)

    for line in reader.textToRead:
        print(line)


    for i in range(100):
        (word, durationInSec) = reader.getNextWord()
        print(word + " at speed " + str(reader.wheelSpeed) + " for " + str(durationInSec))

    

if __name__ == '__main__':
    main()
