"""Sample test module"""

# TODO: Remove this file
def inc(value):
    """Sample test function"""
    return value + 1

def test_passes():
    """Sample passing test case"""
    assert inc(3) == 4

def test_fails():
    """Sample failing test case"""
    assert inc(3) == 5
