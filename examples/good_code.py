"""
Модуль математических и текстовых операций
Демонстрация отличного кода для Code Quality Analyzer
"""


class Calculator:
    """Калькулятор для базовых математических операций"""

    def add(self, a, b):
        """
        Сложение двух чисел

        Args:
            a: Первое число
            b: Второе число

        Returns:
            Сумма a и b
        """
        return a + b

    def power(self, base, exponent):
        """
        Возведение в степень

        Args:
            base: Основание
            exponent: Показатель степени

        Returns:
            Результат возведения base в степень exponent
        """
        result = 1
        for _ in range(exponent):
            result *= base
        return result


def calculate_average(numbers):
    """
    Вычисление среднего арифметического

    Args:
        numbers: Список чисел

    Returns:
        Среднее значение или 0 для пустого списка
    """
    if not numbers:
        return 0
    total = sum(numbers)
    count = len(numbers)
    return total / count


def reverse_string(text):
    """
    Переворот строки

    Args:
        text: Исходная строка

    Returns:
        Перевёрнутая строка
    """
    if not text:
        return ""

    reversed_text = ""
    for char in text:
        reversed_text = char + reversed_text

    return reversed_text


# Unit-тесты
def test_calculator_add():
    """Тест сложения"""
    calc = Calculator()
    assert calc.add(2, 3) == 5
    assert calc.add(-1, 1) == 0


def test_calculator_power():
    """Тест возведения в степень"""
    calc = Calculator()
    assert calc.power(2, 3) == 8
    assert calc.power(5, 0) == 1


def test_calculate_average():
    """Тест вычисления среднего"""
    assert calculate_average([1, 2, 3, 4, 5]) == 3.0
    assert calculate_average([10]) == 10.0


def test_reverse_string():
    """Тест переворота строки"""
    assert reverse_string("hello") == "olleh"
    assert reverse_string("") == ""