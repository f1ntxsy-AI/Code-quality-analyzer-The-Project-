"""
Домашнее задание: Анализ текста
Студент: Иван Иванов
"""

def count_words(text):
    """
    Подсчёт количества слов в тексте

    Args:
        text: Текст для анализа

    Returns:
        Количество слов
    """
    if not text:
        return 0
    words = text.split()
    return len(words)


def find_longest_word(text):
    """Поиск самого длинного слова"""
    if not text:
        return ""

    words = text.split()
    longest = words[0]

    for word in words:
        if len(word) > len(longest):
            longest = word

    return longest


class TextAnalyzer:
    """Анализатор текста"""

    def __init__(self):
        self.text = ""

    def set_text(self, text):
        """Установка текста для анализа"""
        self.text = text

    def get_statistics(self):
        words = self.text.split()
        return {
            'word_count': len(words),
            'char_count': len(self.text),
            'longest_word': max(words, key=len) if words else ""
        }


def test_count_words():
    assert count_words("Hello world") == 2
    assert count_words("") == 0


def test_find_longest_word():
    assert find_longest_word("short longer longest") == "longest"