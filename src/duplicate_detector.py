"""
Модуль для обнаружения дублирования кода (copy-paste detection)
"""
import ast
from difflib import SequenceMatcher
from typing import Dict, List, Any


class DuplicateCodeDetector:
    """Детектор дублирования кода"""

    def __init__(self, code: str, min_function_lines: int = 3):
        """
        Инициализация детектора

        Args:
            code: Python код для анализа
            min_function_lines: Минимальное количество строк в функции для проверки
        """
        self.code = code
        self.min_function_lines = min_function_lines
        try:
            self.tree = ast.parse(code)
        except SyntaxError:
            self.tree = None

    def analyze(self) -> Dict[str, Any]:
        """
        Анализ кода на дублирование

        Returns:
            Словарь с результатами анализа дублирования
        """
        if self.tree is None:
            return self._empty_result()

        duplicates = self.detect()

        return {
            'duplicate_pairs': duplicates['duplicate_pairs'],
            'duplicates': duplicates['duplicates'],
            'duplication_percent': duplicates['duplication_percent'],
            'severity': duplicates['severity']
        }

    def detect(self) -> Dict[str, Any]:
        """
        Обнаружение дубликатов кода

        Returns:
            Информация о найденных дубликатах
        """
        if self.tree is None:
            return self._empty_result()

        # Извлечение всех функций
        functions = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                # ИГНОРИРУЕМ ТЕСТЫ
                if node.name.startswith('test_'):
                    continue

                func_code = ast.get_source_segment(self.code, node)
                if func_code:
                    # Подсчёт строк в функции (убираем пустые и def)
                    lines = [line for line in func_code.split('\n')
                            if line.strip() and not line.strip().startswith('def')]

                    # Фильтруем слишком короткие функции
                    if len(lines) >= self.min_function_lines:
                        functions.append({
                            'name': node.name,
                            'code': func_code,
                            'normalized': self._normalize_code(func_code),
                            'line': node.lineno
                        })

        # Поиск похожих функций
        duplicates = []
        duplicate_function_names = set()

        for i in range(len(functions)):
            for j in range(i + 1, len(functions)):
                similarity = self._calculate_similarity(
                    functions[i]['normalized'],
                    functions[j]['normalized']
                )

                if similarity >= 0.75:  # 75% порог похожести
                    duplicates.append({
                        'function1': functions[i]['name'],
                        'function2': functions[j]['name'],
                        'similarity': round(similarity * 100, 1),
                        'line1': functions[i]['line'],
                        'line2': functions[j]['line']
                    })
                    duplicate_function_names.add(functions[i]['name'])
                    duplicate_function_names.add(functions[j]['name'])

        # Расчёт процента дублирования
        total_functions = len(functions) if functions else 1
        duplication_percent = (len(duplicate_function_names) / total_functions) * 100

        # Определение серьёзности
        severity = self._calculate_severity(len(duplicates), duplication_percent)

        return {
            'duplicate_pairs': len(duplicates),
            'duplicates': duplicates,
            'duplication_percent': round(duplication_percent, 1),
            'severity': severity
        }

    def _normalize_code(self, code: str) -> str:
        """
        Нормализация кода для сравнения

        Args:
            code: Исходный код

        Returns:
            Нормализованный код
        """
        # Удаляем пробелы, табуляции, пустые строки
        lines = [line.strip() for line in code.split('\n') if line.strip()]
        # Убираем имена переменных и параметров (упрощённо)
        normalized = '\n'.join(lines)
        return normalized.lower()

    def _calculate_similarity(self, code1: str, code2: str) -> float:
        """
        Вычисление похожести двух фрагментов кода

        Args:
            code1: Первый фрагмент
            code2: Второй фрагмент

        Returns:
            Коэффициент похожести (0.0 - 1.0)
        """
        return SequenceMatcher(None, code1, code2).ratio()

    def _calculate_severity(self, duplicate_pairs: int,
                           duplication_percent: float) -> str:
        """
        Определение уровня серьёзности дублирования

        Args:
            duplicate_pairs: Количество пар дубликатов
            duplication_percent: Процент дублирования

        Returns:
            Уровень: 'none', 'low', 'medium', 'high'
        """
        if duplicate_pairs == 0:
            return 'none'
        elif duplicate_pairs <= 2 and duplication_percent < 30:
            return 'low'
        elif duplicate_pairs <= 5 or duplication_percent < 50:
            return 'medium'
        else:
            return 'high'

    def _empty_result(self) -> Dict[str, Any]:
        """Пустой результат для некорректного кода"""
        return {
            'duplicate_pairs': 0,
            'duplicates': [],
            'duplication_percent': 0.0,
            'severity': 'none'
        }