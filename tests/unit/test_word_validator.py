import unittest
import json

class TestWordValidator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('data/dictionary/tdk_snapshot_v2.json', 'r', encoding='utf-8') as f:
            cls.tdk_words = set(json.load(f)['words'])
        with open('data/dictionary/content_policy_blocked.json', 'r', encoding='utf-8') as f:
            cls.blocked_words = set(json.load(f)['blocked'])

    def normalize(self, word):
        return word.strip().replace('i', 'İ').replace('ı', 'I').upper()

    def test_valid_words_accepted(self):
        sample_words = ['KİTAP', 'DENİZ', 'BAHAR', 'GÜNEŞ', 'ZAMAN', 'DÜNYA', 'YAŞAM', 'ALTI', 'ALTIN']
        for w in sample_words:
            norm = self.normalize(w)
            self.assertIn(norm, self.tdk_words, f"Expected '{norm}' to be in TDK snapshot")
            self.assertNotIn(norm, self.blocked_words, f"Expected '{norm}' not to be blocked")

    def test_inappropriate_words_blocked(self):
        sample_bad = ['AMK', 'SIK', 'OROSPU', 'PİÇ', 'YARRAK', 'GÖT', 'PORNO', 'SEKS']
        for w in sample_bad:
            norm = self.normalize(w)
            self.assertIn(norm, self.blocked_words, f"Expected '{norm}' to be caught by content policy blocklist")

if __name__ == '__main__':
    unittest.main()
