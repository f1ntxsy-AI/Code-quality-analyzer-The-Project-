"""
Модуль генерации отчётов о качестве кода
"""
from typing import Dict, Any, List
from datetime import datetime


class ReportGenerator:
    """Класс для генерации отчётов в разных форматах"""

    @staticmethod
    def generate_text_report(metrics: Dict[str, Any]) -> str:
        """
        Генерация текстового отчёта

        Args:
            metrics: Словарь с метриками кода

        Returns:
            Отчёт в текстовом формате
        """
        lines = []
        lines.append("=" * 70)
        lines.append("=" * 70)
        lines.append("📊 CODE QUALITY REPORT")
        lines.append("=" * 70)
        lines.append(f"File: {metrics['filename']}")
        lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 70)
        lines.append("")

        # Общий балл
        score = metrics['overall_score']
        lines.append(f"🎯 OVERALL SCORE: {score['total']}/100 ({score['letter_grade']})")
        lines.append("")

        # Разбивка баллов
        lines.append("📈 Score Breakdown:")
        breakdown = score['breakdown']
        lines.append(f"  Documentation        {ReportGenerator._progress_bar(breakdown['documentation'], 15)} {breakdown['documentation']}/15")
        lines.append(f"  Complexity           {ReportGenerator._progress_bar(breakdown['complexity'], 20)} {breakdown['complexity']}/20")
        lines.append(f"  Code Style           {ReportGenerator._progress_bar(breakdown['code_style'], 20)} {breakdown['code_style']}/20")
        lines.append(f"  Structure            {ReportGenerator._progress_bar(breakdown['structure'], 15)} {breakdown['structure']}/15")
        lines.append(f"  Duplication          {ReportGenerator._progress_bar(breakdown['duplication'], 15)} {breakdown['duplication']}/15")
        lines.append(f"  Test Coverage        {ReportGenerator._progress_bar(breakdown['test_coverage'], 15)} {breakdown['test_coverage']}/15")
        lines.append("")

        # Статистика кода
        lines.append("📝 Code Statistics:")
        lines.append(f"  Total Lines:        {metrics['total_lines']}")
        lines.append(f"  Code Lines:         {metrics['code_lines']}")
        lines.append(f"  Functions:          {metrics['functions']['count']}")
        lines.append(f"  Classes:            {metrics['classes']['count']}")
        lines.append(f"  Imports:            {metrics['imports']['count']}")
        lines.append("")

        # Сложность
        complexity = metrics['complexity']
        lines.append("🔄 Complexity Analysis:")
        lines.append(f"  Average Complexity: {complexity['average']}")
        lines.append(f"  Maximum Complexity: {complexity['maximum']}")

        if complexity['complex_functions']:
            lines.append("  ⚠️  Complex Functions:")
            for func in complexity['complex_functions']:
                lines.append(f"     - {func['name']} (complexity: {func['complexity']}, line {func['line']})")
        else:
            lines.append("  ✅ No overly complex functions")
        lines.append("")

        # Документация
        docs = metrics['docstrings']
        lines.append("📚 Documentation:")
        lines.append(f"  Functions Documented: {docs['functions_documented']}/{docs['total_functions']}")
        lines.append(f"  Classes Documented:   {docs['classes_documented']}/{docs['total_classes']}")
        lines.append(f"  Coverage:             {docs['coverage_percent']}%")
        lines.append("")

        # Дублирование
        duplication = metrics.get('duplication', {})
        lines.append("🔍 Code Duplication:")
        lines.append(f"  Duplicate Pairs:      {duplication.get('duplicate_pairs', 0)}")
        lines.append(f"  Duplication Rate:     {duplication.get('duplication_percent', 0)}%")
        lines.append(f"  Severity:             {duplication.get('severity', 'none').upper()}")

        if duplication.get('duplicates'):
            lines.append("  ⚠️  Duplicated Functions:")
            for dup in duplication['duplicates']:
                lines.append(f"     - {dup['function1']} ≈ {dup['function2']} ({dup['similarity']}% similar)")
        else:
            lines.append("  ✅ No code duplication detected")
        lines.append("")

        # Покрытие тестами
        coverage = metrics.get('coverage', {})
        lines.append("🧪 Test Coverage:")
        lines.append(f"  Has Tests:            {'Yes' if coverage.get('has_tests') else 'No'}")
        lines.append(f"  Coverage Estimate:    {coverage.get('coverage_estimate', 0)}%")
        lines.append(f"  Test Functions:       {coverage.get('test_functions', 0)}")
        lines.append(f"  Coverage Level:       {coverage.get('coverage_level', 'none').upper()}")

        if coverage.get('has_tests'):
            lines.append("  ✅ Good test coverage")
        else:
            lines.append("  ⚠️  No tests found - add unit tests!")
        lines.append("")

        # Стиль кода
        style = metrics['code_style']
        lines.append("✨ Code Style:")

        if style['issues_count'] == 0:
            lines.append("  ✅ No style issues found!")
        else:
            lines.append(f"  ⚠️  {style['issues_count']} issues found:")
            for issue in style['issues']:
                lines.append(f"     Line {issue['line']}: {issue['message']}")
        lines.append("")

        # Рекомендации
        recommendations = ReportGenerator._generate_recommendations(metrics)
        lines.append("💡 Recommendations:")
        for rec in recommendations:
            lines.append(f"  • {rec}")
        lines.append("")

        lines.append("=" * 70)

        return "\n".join(lines)

    @staticmethod
    def generate_json_report(metrics: Dict[str, Any]) -> str:
        """
        Генерация JSON отчёта

        Args:
            metrics: Словарь с метриками кода

        Returns:
            Отчёт в JSON формате
        """
        import json
        return json.dumps(metrics, indent=2, ensure_ascii=False)

    @staticmethod
    def generate_markdown_report(metrics: Dict[str, Any]) -> str:
        """
        Генерация Markdown отчёта

        Args:
            metrics: Словарь с метриками кода

        Returns:
            Отчёт в Markdown формате
        """
        lines = []
        lines.append(f"# Code Quality Report: {metrics['filename']}")
        lines.append("")
        lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # Общий балл
        score = metrics['overall_score']
        lines.append(f"## 🎯 Overall Score: {score['total']}/100 ({score['letter_grade']})")
        lines.append("")

        # Разбивка баллов
        lines.append("### Score Breakdown")
        lines.append("")
        lines.append("| Category | Score | Max |")
        lines.append("|----------|-------|-----|")
        breakdown = score['breakdown']
        lines.append(f"| Documentation | {breakdown['documentation']} | 15 |")
        lines.append(f"| Complexity | {breakdown['complexity']} | 20 |")
        lines.append(f"| Code Style | {breakdown['code_style']} | 20 |")
        lines.append(f"| Structure | {breakdown['structure']} | 15 |")
        lines.append(f"| Duplication | {breakdown['duplication']} | 15 |")
        lines.append(f"| Test Coverage | {breakdown['test_coverage']} | 15 |")
        lines.append("")

        # Рекомендации
        recommendations = ReportGenerator._generate_recommendations(metrics)
        lines.append("## 💡 Recommendations")
        lines.append("")
        for rec in recommendations:
            lines.append(f"- {rec}")
        lines.append("")

        return "\n".join(lines)

    @staticmethod
    def _progress_bar(value: float, max_value: float, width: int = 20) -> str:
        """Генерация визуального progress bar"""
        filled = int((value / max_value) * width)
        empty = width - filled
        return f"[{'█' * filled}{'░' * empty}]"

    @staticmethod
    def _generate_recommendations(metrics: Dict[str, Any]) -> List[str]:
        """
        Генерация рекомендаций по улучшению кода

        Args:
            metrics: Словарь с метриками

        Returns:
            Список рекомендаций
        """
        recommendations = []

        # Проверка документации
        doc_coverage = metrics['docstrings']['coverage_percent']
        if doc_coverage < 80:
            recommendations.append(
                f"Add docstrings to functions and classes (current coverage: {doc_coverage}%)"
            )

        # Проверка сложности
        complex_funcs = metrics['complexity']['complex_functions']
        if complex_funcs:
            func_names = ', '.join([f['name'] for f in complex_funcs[:3]])
            recommendations.append(
                f"Reduce complexity of functions: {func_names}"
            )

        # Проверка дублирования
        duplication = metrics.get('duplication', {})
        if duplication.get('duplicate_pairs', 0) > 0:
            recommendations.append(
                f"Remove code duplication ({duplication['duplicate_pairs']} duplicate pairs found)"
            )

        # Проверка тестов
        coverage = metrics.get('coverage', {})
        if not coverage.get('has_tests', False):
            recommendations.append(
                "Add unit tests to verify code functionality"
            )
        elif coverage.get('coverage_estimate', 0) < 80:
            recommendations.append(
                f"Increase test coverage (current: {coverage['coverage_estimate']}%)"
            )

        # Проверка стиля
        style_issues = metrics['code_style']['issues_count']
        if style_issues > 0:
            recommendations.append(
                f"Fix code style issues ({style_issues} issues found)"
            )

        # Если нет рекомендаций - отличный код!
        if not recommendations:
            recommendations.append(
                "✅ Excellent code quality! No major improvements needed."
            )

        return recommendations