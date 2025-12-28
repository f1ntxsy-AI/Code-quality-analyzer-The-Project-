"""
Тесты для модуля coverage_analyzer
"""
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from coverage_analyzer import CoverageAnalyzer


def test_no_tests():
    """Тест: код без тестов"""
    code = """
def calculate(x):
    return x * 2

def process(data):
    return [i for i in data if i > 0]
"""
    analyzer = CoverageAnalyzer(code, "code.py")
    result = analyzer.analyze()

    assert result['has_tests'] == False
    assert result['coverage_estimate'] == 0.0
    assert result['coverage_level'] == 'none'
    assert len(result['recommendations']) > 0


def test_with_tests():
    """Тест: код с тестами"""
    code = 'def calculate(x):\n    return x * 2\n\ndef test_calculate():\n    assert calculate(2) == 4'
    analyzer = CoverageAnalyzer(code, "code.py")
    result = analyzer.analyze()

    assert result['has_tests'] == True
    assert result['test_count'] == 1
    assert result['function_count'] == 1
    assert result['coverage_estimate'] > 0


def test_coverage_levels():
    """Тест: уровни покрытия"""
    code_excellent = 'def func1():\n    pass\n\ndef test_func1():\n    pass'
    analyzer = CoverageAnalyzer(code_excellent, "code.py")
    result = analyzer.analyze()

    assert result['coverage_estimate'] == 100.0
    assert result['coverage_level'] == 'excellent'


def test_empty_code():
    """Тест: пустой код"""
    code = ""
    analyzer = CoverageAnalyzer(code, "code.py")
    result = analyzer.analyze()

    assert result['has_tests'] == False
    assert result['test_count'] == 0
    assert result['function_count'] == 0
