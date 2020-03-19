from django.test import TestCase

class SmokeTest(TestCase):
    '''Smoke test'''

    def test_bad_maths(self):
        '''wrong math test'''
        self.assertEqual(1 + 1, 3)