"""
Homework Task 1: Basic Functions
Student: Ivan Ivanov
"""

def calculate_sum(numbers):
    """Calculates sum of numbers"""
    total = 0
    for num in numbers:
        total += num
    return total


def find_maximum(numbers):
    """Finds maximum number in list"""
    if not numbers:
        return None

    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num


def test_calculate_sum():
    """Test sum calculation"""
    assert calculate_sum([1, 2, 3, 4, 5]) == 15
    assert calculate_sum([]) == 0


def test_find_maximum():
    """Test maximum finding"""
    assert find_maximum([1, 5, 3, 2]) == 5
    assert find_maximum([10]) == 10
