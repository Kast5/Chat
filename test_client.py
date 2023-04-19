import os
import sys
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from client import create_presence_message, parse_response

class TestClass(unittest.TestCase):

    def test_def_presence_message(self):
        test = create_presence_message()
        test[TIME] = 1.1
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_def_200_parse(self):
        self.assertEqual(parse_response({RESPONSE: 200}), '200 : OK')

    def test_400_parse(self):
        self.assertEqual(parse_response({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    def test_no_response(self):
        self.assertRaises(ValueError, parse_response, {ERROR: 'Bad Request'})



if __name__ == '__main__':
    unittest.main()