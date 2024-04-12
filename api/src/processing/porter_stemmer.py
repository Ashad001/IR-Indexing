import json
import re

# https://vijinimallawaarachchi.com/2017/05/09/porter-stemming-algorithm/
# https://github.com/jedijulia/porter-stemmer/blob/master/stemmer.py


class PorterStemmer:
    def __init__(self) -> None:
        self.vowels = "aeiou"
        # self.double_consonants = ["bb", "dd", "ff", "gg", "mm", "nn", "pp", "rr", "tt"]
        self.step1_suffixes = ["sses", "ies", "ss", "s"]
        self.step2_sufixes = {
            "ational": "ate",
            "tional": "tion",
            "enci": "ence",
            "anci": "ance",
            "izer": "ize",
            "abli": "able",
            "alli": "al",
            "entli": "ent",
            "eli": "e",
            "ousli": "ous",
            "ization": "ize",
            "ation": "ate",
            "ator": "ate",
            "alism": "al",
            "iveness": "ive",
            "fulness": "ful",
            "ousness": "ous",
            "aliti": "al",
            "iviti": "ive",
            "biliti": "ble",
        }
        self.step3_sufixes = {
            "icate": "ic",
            "ative": "",
            "alize": "al",
            "iciti": "ic",
            "ical": "ic",
            "ful": "",
            "ness": ""
        }
        self.step4_sufixes  = {
            "al": "",
            "ance": "",
            "ence": "",
            "er": "",
            "ic": "",
            "able": "",
            "ible": "",
            "ant": "",
            "ement": "",
            "ment": "",
            "ent": "",
            "ou": "",
            "ism": "",
            "ate": "",
            "iti": "",
            "ous": "",
            "ive": "",
            "ize": ""
        }

    def double_consonant(self, word: str) -> bool:
        """
        Returns True if the word contains double consonants
        
        Args:
            word (str): English word

        Returns:
            bool: True if the word contains double consonants
        """
        if len(word) < 2:
            return False
        if self.is_consonant(word, -1) and self.is_consonant(word, -2):
            return True
        return False


    def stem(self, word: str) -> str:
        """
        Main method to stem the word

        Args:
            word (str): English word

        Returns:
            str: Stemmed word
        """
        # Modification to porter stemmer to handle abbreviations and important words highlighted as capital
        if word == word.upper():
            return word
        word = word.lower()
        word = self.step1(word)
        word = self.step2(word)
        word = self.step3(word)
        word = self.step4(word)
        word = self.step5(word)
        
        return word

    def step1(self, word: str) -> str:
        """
        Args:
            word (str): _description_

        Returns:
            str: _description_
        """

        def step1a(word: str) -> set:
            if word.endswith("sses"):
                word = self.replace(word, "sses", "ss")
            elif word.endswith("ies"):
                word = self.replace(word, "ies", "i")
            elif word.endswith("ss"):
                word = self.replace(word, "ss", "ss")
            elif word.endswith("s"):
                word = self.replace(word, "s", "")
            else:
                pass
            return word

        def step1b(word: str) -> str:
            if word.endswith("eed"):
                stem_idx = word.rfind("eed")
                stem = word[:stem_idx]
                if self.measure(stem) > 0:
                    word = word[:-1]
                return word

            flag = False
            if word.endswith("ed"):
                stem_idx = word.rfind("ed")
                stem = word[:stem_idx]
                if self.contains_vowel(stem):
                    word = stem
                    flag = True

            if word.endswith("ing"):
                stem_idx = word.rfind("ing")
                stem = word[:stem_idx]
                if self.contains_vowel(stem):
                    word = stem
                    flag = True
            if flag:
                if word.endswith("at") or word.endswith("bl") or word.endswith("iz"):
                    word = word + "e"

                if len(word) > 2:
                    if self.double_consonant(word) and (
                        not word.endswith("l")
                        or word.endswith("s")
                        or word.endswith("z")
                    ):
                        word = word[:-1]

                if self.measure(word) == 1 and self.cvc(word):
                    word = word + "e"

            return word

        def step1c(word: str) -> str:
            if word.endswith("y") and self.contains_vowel(word[:-1]):
                word = word[:-1] + "i"
            return word

        word = step1a(word)
        word = step1b(word)
        word = step1c(word)

        return word

    def step2(self, word: str) -> str:
        """
        Replace the word with the given suffixes

        Args:
            word (str): English | Stemmed word

        Returns:
            str: Stemmed word 
        """
        for key, value in self.step2_sufixes.items():
            if word.endswith(key):
                word = self.replaceM(word, key, value, m=0)
                return word
        return word

    def step3(self, word: str) -> str:
        """
        Replace the word with the given suffixes

        Args:
            word (str): English | Stemmed word

        Returns:
            str: Stemmed word
        """
        for key, value in self.step3_sufixes.items():
            if word.endswith(key):
                word = self.replaceM(word, key, value, m=0)
                return word
        return word

    def step4(self, word: str) -> str:
        """
        Args:
            word (str): Englsih | Stemmed word

        Returns:
            str: Stemmed Word
        """
        for key, value in self.step4_sufixes.items():
            if word.endswith(key):
                word = self.replaceM(word, key, value, m=1)
                return word
        if word.endswith('ion'):
            result = word.rfind('ion')
            base = word[:result]
            if self.measure(base) > 1 and (base.endswith('s') or base.endswith('t')):
                word = base
            word = self.replaceM(word, '', '', m = 0)
            
        return word
    
    def step5(self, word: str) -> str:
        
        def step5a(word: str) -> str:
            """
            (m>1) E     → 
            (m=1 and not *o) E   →

            Args:
                word (str): English word

            Returns:
                str: Stemmed Word
            """
            if word.endswith('e'):
                stem = word[:-1]
                if self.measure(stem) > 1 or (self.measure(stem) == 1 and not self.cvc(stem)):
                    word = stem
            return word
        
        def step5b(word: str) -> str:
            """
            (m > 1 and *d and *L) →  single letter

            Args:
                word (str): English | stemmed word

            Returns:
                str: Stemmed Word
            """
            if self.measure(word) > 1 and word.endswith('l') and self.double_consonant(word):
                word = word[:-1]
            return word
        
        word = step5a(word)
        word = step5b(word)
        return word

    def cvc(self, word: str) -> bool:
        """
        *o – the stem ends cvc, where the second c is not W, X or Y (e.g. -WIL, -HOP)
        Args:
            word (str): 

        Returns:
            bool: Returns True if the word ends with cvc
        """
        if len(word) < 3:
            return False

        c1 = -3
        v = -2
        c2 = -1
        third = word[c2]
        if (
            self.is_consonant(word, c1)
            and not self.is_consonant(word, v)
            and self.is_consonant(word, c2)
        ):
            if third != "w" and third != "x" and third != "y":
                return True
        return False

    def replace(self, word: str, remove: str, replace: str):
        result = word.rfind(remove)
        base = word[:result]
        word = base + replace
        return word
    

    def contains_vowel(self, word: str) -> bool:
        """Return True if the word contains vowel"""
        return not self.contains_consonant(word)

    def contains_consonant(self, word: str) -> bool:
        """Return True if the word contains consonant"""
        for w in word:
            if w in self.vowels:
                return False
        return True

    def _is_consonant(self, letter: str) -> bool:
        """
        Returns True if the given letter is a consonant

        Args:
            letter (str): English Letter

        Returns:
            bool: True if the letter is consonant
        """
        return not letter in self.vowels

    def is_consonant(self, word: str, index: int) -> bool:
        """
        Returns True if the index of the word is a consonant

        Args:
            word (str): Word to check
            index (int): Index of the word to check

        Returns:
            bool: True if the word's index is a consonant else False
        """

        if self._is_consonant(word[index]):
            return True
        if word[index].lower() == "y" and self._is_consonant(word[index - 1]):
            return False
        return False

    def get_form(self, word: str) -> str:
        """
        A list of one or more consecutive consonants (ccc…) will be denoted by C,
        and a list of one or more consecutive vowels (vvv…) will be denoted by V.
        Any word, or part of a word, therefore has one of the four forms given below.

        CVCV … C → collection, management
        CVCV … V → conclude, revise
        VCVC … C → entertainment, illumination
        VCVC … V → illustrate, abundance

        Args:
            word (str): English word

        Returns:
            str:  Form of [C]VCVC … [V]
        """
        form = []
        for i in range(len(word)):
            if self.is_consonant(word, i):
                if i != 0:
                    prev: str = form[-1]
                    if prev != "C":
                        form.append("C")
                else:
                    form.append("C")
            else:
                if i != 0:
                    prev: str = form[-1]
                    if prev != "V":
                        form.append("V")
                else:
                    form.append("V")

        return "".join(form)

    def _measure(self, form: str) -> int:
        """
        The value m found is called the measure of any word or word part when represented
        in the form [C](VC)m[V].

        Args:
            form (str): [C](VC)m[V]

        Returns:
            int: measure of any word or token
        """
        m = form.count("VC")
        return m

    def measure(self, word: str) -> int:
        """
        Gets the measure of word or token from self._measure method.

        Args:
            word (str): English word

        Returns:
            int: maesure of word or token
        """
        form = self.get_form(word)
        m = self._measure(form)
        return m

    def replaceM(self, word: str, remove: str, replace: str, m: int = 0) -> str:
        """
        Replace the word with the given suffixes if the measure of the word is greater than m

        Args:
            word (str): word or stem
            remove (str): string to remove
            replace (str): string to replace
            m (int, optional): Defaults to 0.

        Returns:
            str: replaced word
        """
        stem_idx = word.rfind(remove)
        stem = word[:stem_idx]
        if self.measure(stem) > m:
            replaced = stem + replace
            return replaced
        return word

if __name__=='__main__':
    ps = PorterStemmer()
    print(ps.stem("applied"))