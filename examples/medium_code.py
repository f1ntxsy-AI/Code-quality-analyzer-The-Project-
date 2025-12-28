"""
Модуль обработки данных
"""

def process_list(items):
    """Обработка списка элементов"""
    result = []
    for item in items:
        if item > 10:
            result.append(item * 2)
    return result


def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total


class DataProcessor:
    """Процессор данных"""

    def transform(self, data):
        transformed = []
        for d in data:
            if isinstance(d, int):
                transformed.append(d ** 2)
            else:
                transformed.append(str(d))
        return transformed

    def filter_data(self, data, threshold):
        return [d for d in data if d > threshold]


def test_process_list():
    """Тест process_list"""
    assert process_list([5, 15, 20]) == [30, 40]