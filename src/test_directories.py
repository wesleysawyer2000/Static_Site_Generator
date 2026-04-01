import unittest
from directories import *


class TestTextNode(unittest.TestCase):

    def test_extract_title(self):
        markdown = '''
        #### Heading level 4
        # Heading level 1
        ## Heading level 2
        '''
        answer = "Heading level 1"
        self.assertEqual(extract_title(markdown), answer)





if __name__ == "__main__":
    unittest.main()