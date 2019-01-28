from django.test import TestCase

from utils.function import recursive_merge_dicts


class MergeDictTest(TestCase):

    def test_merge(self):
        a = {
            'a': 1,
            'b': {
                'e': 5,
                'g': 7
            },
            'c': 3,
            'd': {
                '1': 'a',
                '2': 'b',
                '3': 'f'
            }
        }
        b = {
            'a': 2,
            'b': {
                'e': 2,
                'f': 6,
            },
            'd': {
                '1': 'a',
                '2': {
                    'a',
                    'b'
                }
            }
        }
        assert recursive_merge_dicts(a, b) == {
            'a': 2,
            'b': {
                'e': 2,
                'g': 7,
                'f': 6
            },
            'c': 3,
            'd': {
                '1': 'a',
                '2': {
                    'b',
                    'a'
                },
                '3': 'f'
            }
        }
