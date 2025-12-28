"""
Главный модуль CLI для анализа качества кода
"""
import sys
import io

# Исправление кодировки для Windows
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except:
        pass  # Если не получилось - используем стандартную кодировку

import argparse
import json
from pathlib import Path
from metrics import CodeMetrics
from report_generator import ReportGenerator


def safe_print(text):
    """Безопасный вывод с поддержкой эмодзи для Windows"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Если консоль не поддерживает Unicode - убираем эмодзи
        clean_text = text.encode('ascii', 'ignore').decode('ascii')
        print(clean_text)


def analyze_file(filepath: str, output_dir: str = "reports", output_format: str = "text") -> None:
    """
    Анализ файла с кодом

    Args:
        filepath: путь к файлу для анализа
        output_dir: директория для сохранения отчётов
        output_format: формат отчёта (text, json, markdown, all)
    """
    # Чтение файла
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        safe_print(f"❌ Error: File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        safe_print(f"❌ Error reading file: {e}")
        sys.exit(1)

    filename = Path(filepath).name

    safe_print(f"🔍 Analyzing: {filename}")
    safe_print("=" * 70)

    # Анализ кода
    try:
        analyzer = CodeMetrics(code, filename)
        metrics = analyzer.analyze()
    except ValueError as e:
        safe_print(f"❌ Error analyzing code: {e}")
        sys.exit(1)

    # Создаём директорию для отчётов
    output_path_dir = Path(output_dir)
    output_path_dir.mkdir(parents=True, exist_ok=True)

    # Генерация отчётов
    base_name = Path(filename).stem

    # TEXT отчёт
    if output_format in ["text", "all"]:
        report = ReportGenerator.generate_text_report(metrics)
        print(report)

        # Сохранение в файл
        txt_path = output_path_dir / f"{base_name}_report.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(report)
        safe_print(f"\n💾 Text report saved: {txt_path}")

    # JSON отчёт
    if output_format in ["json", "all"]:
        json_path = output_path_dir / f"{base_name}_report.json"

        # ReportGenerator.generate_json_report возвращает данные, не сохраняет
        json_data = ReportGenerator.generate_json_report(metrics)

        # Сохраняем сами
        with open(json_path, 'w', encoding='utf-8') as f:
            if isinstance(json_data, str):
                f.write(json_data)
            else:
                json.dump(json_data, f, indent=2, ensure_ascii=False)

        safe_print(f"💾 JSON report saved: {json_path}")

    # Markdown отчёт
    if output_format in ["markdown", "all"]:
        md_path = output_path_dir / f"{base_name}_report.md"

        # ReportGenerator.generate_markdown_report возвращает текст, не сохраняет
        md_content = ReportGenerator.generate_markdown_report(metrics)

        # Сохраняем сами
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        safe_print(f"💾 Markdown report saved: {md_path}")


def analyze_directory(directory: str, output_dir: str = "reports", output_format: str = "text") -> None:
    """
    Анализ всех Python файлов в директории

    Args:
        directory: путь к директории
        output_dir: директория для сохранения отчётов
        output_format: формат отчёта
    """
    dir_path = Path(directory)

    if not dir_path.exists():
        safe_print(f"❌ Error: Directory not found: {directory}")
        sys.exit(1)

    python_files = list(dir_path.glob("*.py"))

    if not python_files:
        safe_print(f"⚠️  No Python files found in: {directory}")
        sys.exit(0)

    safe_print(f"📁 Found {len(python_files)} Python file(s) in {directory}")
    safe_print("=" * 70)

    for filepath in python_files:
        safe_print(f"\n{'=' * 70}")
        analyze_file(str(filepath), output_dir, output_format)


def main():
    """Главная функция CLI"""
    parser = argparse.ArgumentParser(
        description='Code Quality Analyzer - Analyze Python code quality'
    )

    parser.add_argument(
        '--file',
        type=str,
        help='Path to Python file to analyze'
    )

    parser.add_argument(
        '--directory',
        type=str,
        help='Path to directory with Python files'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        default='reports',
        help='Output directory for reports (default: reports)'
    )

    parser.add_argument(
        '--format',
        type=str,
        choices=['text', 'json', 'markdown', 'all'],
        default='text',
        help='Report format: text, json, markdown, or all (default: text)'
    )

    args = parser.parse_args()

    if not args.file and not args.directory:
        parser.print_help()
        safe_print("\n❌ Error: Please specify --file or --directory")
        sys.exit(1)

    if args.file:
        analyze_file(args.file, args.output_dir, args.format)
    elif args.directory:
        analyze_directory(args.directory, args.output_dir, args.format)


if __name__ == '__main__':
    main()
