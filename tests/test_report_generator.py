"""
Тесты для модуля report_generator
"""
import pytest
from src.report_generator import ReportGenerator


@pytest.fixture
def sample_metrics():
    """Примерные метрики для тестирования"""
    return {
        'filename': 'test.py',
        'total_lines': 10,
        'code_lines': 8,
        'functions': {'count': 2, 'names': ['func1', 'func2']},
        'classes': {'count': 0, 'names': []},
        'imports': {'count': 1},
        'complexity': {
            'average': 3.0,
            'maximum': 5,
            'complex_functions': []
        },
        'docstrings': {
            'total_functions': 2,
            'functions_documented': 1,
            'total_classes': 0,
            'classes_documented': 0,
            'coverage_percent': 50.0
        },
        'code_style': {
            'issues_count': 0,
            'issues': []
        },
        'duplication': {
            'duplicate_pairs': 0,
            'duplicates': [],
            'duplication_percent': 0.0,
            'severity': 'none'
        },
        'coverage': {
            'has_tests': True,
            'test_functions': 1,
            'coverage_estimate': 50.0,
            'coverage_level': 'medium'
        },
        'overall_score': {
            'total': 75.0,
            'letter_grade': 'C',
            'breakdown': {
                'documentation': 7.5,
                'complexity': 15.0,
                'code_style': 20.0,
                'structure': 15.0,
                'duplication': 15.0,
                'test_coverage': 7.5
            }
        }
    }


def test_text_report_generation(sample_metrics):
    """Тест генерации текстового отчёта"""
    report = ReportGenerator.generate_text_report(sample_metrics)

    assert isinstance(report, str)
    assert 'CODE QUALITY REPORT' in report
    assert 'test.py' in report
    assert '75' in report
    assert 'C' in report


def test_json_report_generation(sample_metrics):
    """Тест генерации JSON отчёта"""
    report = ReportGenerator.generate_json_report(sample_metrics)

    assert isinstance(report, str)
    assert 'filename' in report
    assert 'overall_score' in report

    # Проверка что это валидный JSON
    import json
    parsed = json.loads(report)
    assert parsed['filename'] == 'test.py'


def test_markdown_report_generation(sample_metrics):
    """Тест генерации Markdown отчёта"""
    report = ReportGenerator.generate_markdown_report(sample_metrics)

    assert isinstance(report, str)
    assert '# Code Quality Report' in report
    assert 'test.py' in report
    assert '75' in report


def test_recommendations_generation(sample_metrics):
    """Тест генерации рекомендаций"""
    recommendations = ReportGenerator._generate_recommendations(sample_metrics)

    assert isinstance(recommendations, list)
    assert len(recommendations) > 0

    # Должна быть рекомендация по документации (50% coverage)
    assert any("docstring" in rec.lower() for rec in recommendations)