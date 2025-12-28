"""
Модуль анализа метрик качества кода
"""
import ast
from typing import Dict, Any, List
from duplicate_detector import DuplicateCodeDetector
from coverage_analyzer import CoverageAnalyzer


class CodeMetrics:
    """Класс для анализа метрик качества Python кода"""

    def __init__(self, code: str, filename: str = "code.py"):
        """
        Инициализация анализатора

        Args:
            code: Python код для анализа
            filename: Имя файла (опционально)
        """
        self.code = code
        self.filename = filename
        try:
            self.tree = ast.parse(code)
        except SyntaxError:
            self.tree = None

    def analyze(self) -> Dict[str, Any]:
        """
        Полный анализ кода

        Returns:
            Словарь с метриками качества кода
        """
        if self.tree is None:
            return self._empty_metrics()

        metrics = {
            'filename': self.filename,
            'total_lines': len(self.code.split('\n')),
            'code_lines': self._count_code_lines(),
            'functions': self._function_info(),
            'classes': self._class_info(),
            'imports': self._import_info(),
            'complexity': self._function_complexity(),
            'docstrings': self._check_docstrings(),
            'code_style': self._check_code_style(),
            'duplication': self._check_duplication(),
            'coverage': self._check_coverage()
        }

        metrics['overall_score'] = self._calculate_score(metrics)

        return metrics

    def _count_code_lines(self) -> int:
        """Подсчёт строк кода (без пустых и комментариев)"""
        lines = self.code.split('\n')
        code_lines = 0

        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                code_lines += 1

        return code_lines

    def _function_info(self) -> Dict[str, Any]:
        """Информация о функциях"""
        functions = [node for node in ast.walk(self.tree)
                    if isinstance(node, ast.FunctionDef)]

        return {
            'count': len(functions),
            'names': [f.name for f in functions]
        }

    def _class_info(self) -> Dict[str, Any]:
        """Информация о классах"""
        classes = [node for node in ast.walk(self.tree)
                  if isinstance(node, ast.ClassDef)]

        return {
            'count': len(classes),
            'names': [c.name for c in classes]
        }

    def _import_info(self) -> Dict[str, Any]:
        """Информация об импортах"""
        imports = [node for node in ast.walk(self.tree)
                  if isinstance(node, (ast.Import, ast.ImportFrom))]

        return {
            'count': len(imports)
        }

    def _function_complexity(self) -> Dict[str, Any]:
        """
        Анализ цикломатической сложности функций

        Returns:
            Словарь с информацией о сложности
        """
        functions = [node for node in ast.walk(self.tree)
                    if isinstance(node, ast.FunctionDef)
                    and not node.name.startswith('test_')]  # ИГНОРИРУЕМ ТЕСТЫ

        if not functions:
            return {
                'average': 1.0,
                'maximum': 1,
                'complex_functions': []
            }

        complexities = []
        complex_funcs = []

        for func in functions:
            complexity = self._calculate_complexity(func)
            complexities.append(complexity)

            if complexity > 10:  # Порог сложности
                complex_funcs.append({
                    'name': func.name,
                    'complexity': complexity,
                    'line': func.lineno
                })

        avg_complexity = sum(complexities) / len(complexities)

        return {
            'average': round(avg_complexity, 1),
            'maximum': max(complexities) if complexities else 1,
            'complex_functions': complex_funcs
        }

    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """
        Вычисление цикломатической сложности функции

        Args:
            node: AST узел функции

        Returns:
            Значение сложности
        """
        complexity = 1  # Базовая сложность

        for child in ast.walk(node):
            # +1 за каждое ветвление
            if isinstance(child, (ast.If, ast.While, ast.For,
                                 ast.ExceptHandler, ast.With)):
                complexity += 1
            # +1 за логические операторы
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        return complexity

    def _check_docstrings(self) -> Dict[str, Any]:
        """
        Проверка наличия docstrings

        Returns:
            Информация о документации
        """
        functions = [node for node in ast.walk(self.tree)
                    if isinstance(node, ast.FunctionDef)]
        classes = [node for node in ast.walk(self.tree)
                  if isinstance(node, ast.ClassDef)]

        functions_with_docs = sum(1 for f in functions
                                 if ast.get_docstring(f))
        classes_with_docs = sum(1 for c in classes
                               if ast.get_docstring(c))

        total_items = len(functions) + len(classes)
        documented_items = functions_with_docs + classes_with_docs

        coverage = (documented_items / total_items * 100) if total_items > 0 else 0

        return {
            'total_functions': len(functions),
            'functions_documented': functions_with_docs,
            'total_classes': len(classes),
            'classes_documented': classes_with_docs,
            'coverage_percent': round(coverage, 1)
        }

    def _check_code_style(self) -> Dict[str, Any]:
        """
        Проверка стиля кода (упрощённая)

        Returns:
            Информация о проблемах стиля
        """
        issues = []

        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                # Проверка длины функции
                if hasattr(node, 'end_lineno') and hasattr(node, 'lineno'):
                    func_length = node.end_lineno - node.lineno
                    if func_length > 50:
                        issues.append({
                            'line': node.lineno,
                            'message': f'Function {node.name} is too long ({func_length} lines)'
                        })

                # Проверка количества параметров
                if len(node.args.args) > 5:
                    issues.append({
                        'line': node.lineno,
                        'message': f'Function {node.name} has too many parameters ({len(node.args.args)})'
                    })

        return {
            'issues_count': len(issues),
            'issues': issues
        }

    def _check_duplication(self) -> Dict[str, Any]:
        """
        Проверка дублирования кода

        Returns:
            Информация о дубликатах
        """
        detector = DuplicateCodeDetector(self.code)
        return detector.analyze()

    def _check_coverage(self) -> Dict[str, Any]:
        """
        Проверка покрытия тестами

        Returns:
            Информация о тестах
        """
        analyzer = CoverageAnalyzer(self.code)
        return analyzer.analyze()

    def _calculate_score(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Вычисление общего балла качества кода

        Args:
            metrics: Словарь с метриками

        Returns:
            Словарь с общим баллом и разбивкой
        """
        # Documentation (15 баллов)
        doc_coverage = metrics['docstrings']['coverage_percent']
        doc_score = (doc_coverage / 100) * 15

        # Complexity (20 баллов)
        avg_complexity = metrics['complexity']['average']

        # Правильный расчёт: чем меньше сложность, тем лучше
        if avg_complexity <= 5:
            complexity_score = 20  # Отлично
        elif avg_complexity <= 10:
            complexity_score = 15  # Хорошо
        elif avg_complexity <= 15:
            complexity_score = 10  # Средне
        else:
            complexity_score = 5   # Плохо

        # Code Style (20 баллов)
        style_issues = metrics['code_style']['issues_count']
        if style_issues == 0:
            style_score = 20
        elif style_issues <= 3:
            style_score = 15
        elif style_issues <= 10:
            style_score = 10
        else:
            style_score = 5

        # Structure (15 баллов)
        structure_score = 15

        # Штрафы за структуру
        if metrics['functions']['count'] == 0:
            structure_score -= 5
        if metrics['code_lines'] > 500:
            structure_score -= 5

        structure_score = max(0, structure_score)

        # Duplication (15 баллов)
        duplication = metrics.get('duplication', {})
        duplication_percent = duplication.get('duplication_percent', 0)

        if duplication_percent == 0:
            duplication_score = 15
        elif duplication_percent < 10:
            duplication_score = 12
        elif duplication_percent < 25:
            duplication_score = 8
        else:
            duplication_score = 3

        # Test Coverage (15 баллов)
        coverage = metrics.get('coverage', {})
        coverage_estimate = coverage.get('coverage_estimate', 0)

        if coverage_estimate >= 80:
            coverage_score = 15
        elif coverage_estimate >= 60:
            coverage_score = 12
        elif coverage_estimate >= 40:
            coverage_score = 8
        elif coverage_estimate >= 20:
            coverage_score = 5
        else:
            coverage_score = 0

        # Общий балл
        total = (doc_score + complexity_score + style_score +
                structure_score + duplication_score + coverage_score)
        total = round(total, 1)

        # Буквенная оценка
        if total >= 90:
            letter_grade = 'A'
        elif total >= 80:
            letter_grade = 'B'
        elif total >= 70:
            letter_grade = 'C'
        elif total >= 60:
            letter_grade = 'D'
        else:
            letter_grade = 'F'

        return {
            'total': total,
            'letter_grade': letter_grade,
            'breakdown': {
                'documentation': round(doc_score, 1),
                'complexity': round(complexity_score, 1),
                'code_style': round(style_score, 1),
                'structure': round(structure_score, 1),
                'duplication': round(duplication_score, 1),
                'test_coverage': round(coverage_score, 1)
            }
        }

    def _empty_metrics(self) -> Dict[str, Any]:
        """Пустые метрики для некорректного кода"""
        return {
            'filename': self.filename,
            'total_lines': 0,
            'code_lines': 0,
            'functions': {'count': 0, 'names': []},
            'classes': {'count': 0, 'names': []},
            'imports': {'count': 0},
            'complexity': {'average': 0.0, 'maximum': 0, 'complex_functions': []},
            'docstrings': {
                'total_functions': 0,
                'functions_documented': 0,
                'total_classes': 0,
                'classes_documented': 0,
                'coverage_percent': 0.0
            },
            'code_style': {'issues_count': 0, 'issues': []},
            'duplication': {
                'duplicate_pairs': 0,
                'duplicates': [],
                'duplication_percent': 0.0,
                'severity': 'none'
            },
            'coverage': {
                'has_tests': False,
                'test_functions': 0,
                'coverage_estimate': 0.0,
                'coverage_level': 'none'
            },
            'overall_score': {
                'total': 0.0,
                'letter_grade': 'F',
                'breakdown': {
                    'documentation': 0.0,
                    'complexity': 0.0,
                    'code_style': 0.0,
                    'structure': 0.0,
                    'duplication': 0.0,
                    'test_coverage': 0.0
                }
            }
        }