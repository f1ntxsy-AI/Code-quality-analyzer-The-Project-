"""
Homework Task 1: Basic Functions
Student: Petr Petrov
"""

def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

def find_maximum(numbers):
    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num
