import unittest
from src.porter_stemmer import PorterStemmer

class TestPorterStem(unittest.TestCase):

    def setUp(self):
        self.stemmer = PorterStemmer()

    def test_step1a(self):
        # Test cases for Step 1a
        self.assertEqual(self.stemmer.step1("caresses"), "caress")
        self.assertEqual(self.stemmer.step1("ponies"), "poni")
        self.assertEqual(self.stemmer.step1("ties"), "ti")
        self.assertEqual(self.stemmer.step1("caress"), "caress")
        self.assertEqual(self.stemmer.step1("cats"), "cat")

    def test_step1b(self):
        # Test cases for Step 1b
        self.assertEqual(self.stemmer.step1("feed"), "feed")
        self.assertEqual(self.stemmer.step1("agreed"), "agree")
        self.assertEqual(self.stemmer.step1("plastered"), "plaster")
        self.assertEqual(self.stemmer.step1("bled"), "bled")
        self.assertEqual(self.stemmer.step1("motoring"), "motor")

    def test_step1c(self):
        # Test cases for Step 1c
        self.assertEqual(self.stemmer.step1("happy"), "happi")
        self.assertEqual(self.stemmer.step1("sky"), "sky")

    def test_step2(self):
        # Test cases for Step 2
        self.assertEqual(self.stemmer.step2("relational"), "relate")
        self.assertEqual(self.stemmer.step2("vileli"), "vile")
        self.assertEqual(self.stemmer.step2("analogousli"), "analogous")
        self.assertEqual(self.stemmer.step2("vietnamization"), "vietnamize")
        self.assertEqual(self.stemmer.step2("formaliti"), "formal")
        self.assertEqual(self.stemmer.step2("sensitiviti"), "sensitive")

    def test_step3(self):
        # Test cases for Step 3
        self.assertEqual(self.stemmer.step3("triplicate"), "triplic")
        self.assertEqual(self.stemmer.step3("formative"), "form")
        self.assertEqual(self.stemmer.step3("formalize"), "formal")
        self.assertEqual(self.stemmer.step3("electriciti"), "electric")
        self.assertEqual(self.stemmer.step3("electrical"), "electric")
        self.assertEqual(self.stemmer.step3("hopeful"), "hope")
        self.assertEqual(self.stemmer.step3("goodness"), "good")
    
    def test_step4(self):
        # Test cases for Step 4
        self.assertEqual(self.stemmer.step4("revival"), "reviv")
        self.assertEqual(self.stemmer.step4("irritant"), "irrit")
        self.assertEqual(self.stemmer.step4("replacement"), "replac")
        self.assertEqual(self.stemmer.step4("adjustment"), "adjust")
        self.assertEqual(self.stemmer.step4("dependent"), "depend")
        self.assertEqual(self.stemmer.step4("adoption"), "adopt")
        self.assertEqual(self.stemmer.step4("homologou"), "homolog")
    
    def test_step5(self):
        # Test cases for Step 5
        self.assertEqual(self.stemmer.step5("probate"), "probat")
        self.assertEqual(self.stemmer.step5("cease"), "ceas")
        self.assertEqual(self.stemmer.step5("controll"), "control")
        self.assertEqual(self.stemmer.step5("roll"), "roll")
    
if __name__ == '__main__':
    unittest.main()
