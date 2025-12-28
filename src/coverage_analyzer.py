"""
Модуль для анализа покрытия кода тестами
"""
import ast
import os
from typing import Dict, Any, List
from pathlib import Path


class CoverageAnalyzer:
    """Анализатор покрытия кода тестами"""

    def __init__(self, code: str, filepath: str = "code.py"):
        """
        Инициализация анализатора

        Args:
            code: исходный код Python
            filepath: путь к файлу (для поиска тестов)
        """
        self.code = code
        self.filepath = filepath
        self.tree = ast.parse(code)
        self.functions = []
        self.classes = []
        self._extract_definitions()

    def _extract_definitions(self):
        """Извлечение функций и классов"""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                self.functions.append({
                    'name': node.name,
                    'line': node.lineno,
                    'is_test': node.name.startswith('test_')
                })
            elif isinstance(node, ast.ClassDef):
                self.classes.append({
                    'name': node.name,
                    'line': node.lineno
                })

    def check_test_presence(self) -> bool:
        """Проверка наличия тестов в коде или рядом"""
        # Проверка тестов в самом файле
        has_tests_in_file = any(f['is_test'] for f in self.functions)

        # Проверка наличия test_*.py файлов рядом
        has_test_file = self._check_test_file_exists()

        return has_tests_in_file or has_test_file

    def _check_test_file_exists(self) -> bool:
        """Проверка существования файла с тестами"""
        if not self.filepath or self.filepath == "code.py":
            return False

        # Проверяем папку tests/
        base_name = Path(self.filepath).stem
        test_file_patterns = [
            f"tests/test_{base_name}.py",
            f"test_{base_name}.py",
            f"{base_name}_test.py"
        ]

        for pattern in test_file_patterns:
            if os.path.exists(pattern):
                return True

        return False

    def estimate_coverage(self) -> float:
        """
        Оценка покрытия тестами (базовая эвристика)

        Returns:
            Процент предполагаемого покрытия (0-100)
        """
        # Простая эвристика: если есть тесты - 70%, иначе 0%
        if self.check_test_presence():
            # Считаем соотношение тестов к функциям
            test_functions = sum(1 for f in self.functions if f['is_test'])
            non_test_functions = len(self.functions) - test_functions

            if non_test_functions == 0:
                return 100.0 if test_functions > 0 else 0.0

            # Базовая оценка: если на каждую функцию есть тест
            coverage_ratio = min(test_functions / non_test_functions, 1.0)
            return round(coverage_ratio * 100, 1)
        else:
            return 0.0

    def analyze(self) -> Dict[str, Any]:
        """
        Полный анализ покрытия

        Returns:
            Результаты анализа
        """
        has_tests = self.check_test_presence()
        coverage_estimate = self.estimate_coverage()

        test_functions = [f for f in self.functions if f['is_test']]
        non_test_functions = [f for f in self.functions if not f['is_test']]

        return {
            'has_tests': has_tests,
            'coverage_estimate': coverage_estimate,
            'test_count': len(test_functions),
            'function_count': len(non_test_functions),
            'test_ratio': round(len(test_functions) / len(non_test_functions), 2) if non_test_functions else 0,
            'coverage_level': self._get_coverage_level(coverage_estimate),
            'recommendations': self._generate_recommendations(has_tests, coverage_estimate)
        }

    def _get_coverage_level(self, coverage: float) -> str:
        """Определение уровня покрытия"""
        if coverage >= 80:
            return 'excellent'
        elif coverage >= 60:
            return 'good'
        elif coverage >= 40:
            return 'moderate'
        elif coverage > 0:
            return 'low'
        else:
            return 'none'

    def _generate_recommendations(self, has_tests: bool, coverage: float) -> List[str]:
        """Генерация рекомендаций по тестированию"""
        recommendations = []

        if not has_tests:
            recommendations.append("Add unit tests to verify code functionality")
            recommendations.append("Create tests/ directory with test files")
        elif coverage < 60:
            recommendations.append(f"Improve test coverage (current: {coverage}%, target: 80%+)")
            recommendations.append("Add tests for untested functions")

        return recommendations
