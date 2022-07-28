from cgi import test
from rotten import *

def test1():
    assert get_movie_score('toy story 4') == ("94", "97")

def test2():
    get_movie_cast('toy story 4')

test2()