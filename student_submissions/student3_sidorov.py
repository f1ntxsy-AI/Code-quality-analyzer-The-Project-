"""
Homework Task 1: Basic Functions
Student: Sergey Sidorov
"""

def calculate_sum(a):
    """Sum calculator"""
    return sum(a)

def find_maximum(x):
    """Max finder"""
    return max(x)

def calculate_average(data):
    """Average calculator"""
    if len(data) == 0:
        return 0
    return sum(data) / len(data)

def test_sum():
    """Test"""
    assert calculate_sum([1,2,3]) == 6

def test_max():
    """Test"""
    assert find_maximum([1,5,3]) == 5

def test_avg():
    """Test"""
    assert calculate_average([2,4,6]) == 4.0
