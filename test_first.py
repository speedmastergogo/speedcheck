import math
import pytest
@pytest.mark.square
def test_sqrt():
    num = 25
    assert math.sqrt(25)==5
@pytest.mark.square
def test_square():
    num = 5
    assert 5*5 ==45 
@pytest.mark.others
def testequality():
    assert 14 == 15