"""
Веб-интерфейс для Code Quality Analyzer
Запуск: streamlit run src/web_app.py
"""
import streamlit as st
from metrics import CodeMetrics
from report_generator import ReportGenerator
import pandas as pd


def main():
    """Основная функция веб-приложения"""
    st.set_page_config(
        page_title="Code Quality Analyzer",
        page_icon="🔍",
        layout="wide"
    )

    st.title("🔍 Code Quality Analyzer")
    st.markdown("Анализ качества Python-кода с детальными метриками")

    # Боковая панель с режимами
    st.sidebar.header("⚙️ Настройки")
    mode = st.sidebar.radio(
        "Выберите режим:",
        ["📝 Вставить код", "📁 Загрузить файл", "📊 Сравнить файлы"]
    )

    if mode == "📝 Вставить код":
        mode_paste_code()
    elif mode == "📁 Загрузить файл":
        mode_upload_file()
    else:
        mode_compare_files()


def mode_paste_code():
    """Режим вставки кода"""
    st.header("📝 Вставьте код для анализа")

    code = st.text_area(
        "Python код:",
        height=300,
        placeholder="Вставьте ваш Python код здесь..."
    )

    if st.button("🔍 Анализировать", type="primary"):
        if code.strip():
            with st.spinner("Анализ кода..."):
                analyzer = CodeMetrics(code, "pasted_code.py")
                metrics = analyzer.analyze()
                display_results(metrics)
        else:
            st.warning("⚠️ Пожалуйста, вставьте код для анализа")


def mode_upload_file():
    """Режим загрузки файла"""
    st.header("📁 Загрузите Python файл")

    uploaded_file = st.file_uploader(
        "Выберите .py файл",
        type=['py'],
        help="Загрузите Python файл для анализа"
    )

    if uploaded_file is not None:
        code = uploaded_file.read().decode('utf-8')
        st.code(code, language='python', line_numbers=True)

        if st.button("🔍 Анализировать", type="primary"):
            with st.spinner("Анализ кода..."):
                analyzer = CodeMetrics(code, uploaded_file.name)
                metrics = analyzer.analyze()
                display_results(metrics)


def mode_compare_files():
    """Режим сравнения двух файлов"""
    st.header("📊 Сравнение двух файлов")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Файл 1")
        file1 = st.file_uploader("Загрузите первый файл", type=['py'], key="file1")

    with col2:
        st.subheader("Файл 2")
        file2 = st.file_uploader("Загрузите второй файл", type=['py'], key="file2")

    if file1 and file2:
        if st.button("🔍 Сравнить", type="primary"):
            with st.spinner("Анализ файлов..."):
                code1 = file1.read().decode('utf-8')
                code2 = file2.read().decode('utf-8')

                analyzer1 = CodeMetrics(code1, file1.name)
                analyzer2 = CodeMetrics(code2, file2.name)

                metrics1 = analyzer1.analyze()
                metrics2 = analyzer2.analyze()

                display_comparison(metrics1, metrics2)


def display_results(metrics):
    """Отображение результатов анализа"""
    score = metrics['overall_score']

    # Общий балл
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.metric(
            "🎯 Общий балл",
            f"{score['total']}/100",
            delta=None
        )

    with col2:
        grade_color = get_grade_color(score['letter_grade'])
        st.markdown(
            f"<h1 style='text-align: center; color: {grade_color};'>{score['letter_grade']}</h1>",
            unsafe_allow_html=True
        )

    with col3:
        quality = get_quality_label(score['total'])
        st.metric("Качество", quality)

    # Разбивка по метрикам
    st.markdown("### 📈 Детальная разбивка")

    breakdown = score['breakdown']

    col1, col2, col3 = st.columns(3)

    with col1:
        display_metric_bar("📚 Documentation", breakdown['documentation'], 15)
        display_metric_bar("🔄 Complexity", breakdown['complexity'], 20)

    with col2:
        display_metric_bar("✨ Code Style", breakdown['code_style'], 20)
        display_metric_bar("🏗️ Structure", breakdown['structure'], 15)

    with col3:
        display_metric_bar("🔍 Duplication", breakdown['duplication'], 15)
        display_metric_bar("🧪 Test Coverage", breakdown['test_coverage'], 15)

    # Статистика кода
    st.markdown("---")
    st.markdown("### 📊 Статистика кода")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Строк кода", metrics['code_lines'])
    col2.metric("Функций", metrics['functions']['count'])
    col3.metric("Классов", metrics['classes']['count'])
    col4.metric("Импортов", metrics['imports']['count'])

    # Детали
    with st.expander("🔍 Детали анализа"):
        display_details(metrics)

    # Рекомендации
    st.markdown("---")
    st.markdown("### 💡 Рекомендации")

    recommendations = generate_recommendations(metrics)
    for rec in recommendations:
        if "✅" in rec:
            st.success(rec)
        else:
            st.info(f"• {rec}")

    # Кнопки экспорта
    st.markdown("---")
    st.markdown("### 💾 Экспорт отчёта")

    col1, col2, col3 = st.columns(3)

    with col1:
        txt_report = ReportGenerator.generate_text_report(metrics)
        st.download_button(
            "📄 Скачать TXT",
            txt_report,
            file_name=f"{metrics['filename']}_report.txt",
            mime="text/plain"
        )

    with col2:
        json_report = ReportGenerator.generate_json_report(metrics)
        st.download_button(
            "📊 Скачать JSON",
            json_report,
            file_name=f"{metrics['filename']}_report.json",
            mime="application/json"
        )

    with col3:
        md_report = ReportGenerator.generate_markdown_report(metrics)
        st.download_button(
            "📝 Скачать MD",
            md_report,
            file_name=f"{metrics['filename']}_report.md",
            mime="text/markdown"
        )


def display_comparison(metrics1, metrics2):
    """Отображение сравнения двух файлов"""
    st.markdown("---")
    st.markdown("## 🏆 Результаты сравнения")

    score1 = metrics1['overall_score']['total']
    score2 = metrics2['overall_score']['total']

    # Определение победителя
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown(f"### {metrics1['filename']}")
        st.metric("Балл", f"{score1}/100", delta=None)
        if score1 > score2:
            st.success("🏆 Победитель!")

    with col2:
        st.markdown("### VS")

    with col3:
        st.markdown(f"### {metrics2['filename']}")
        st.metric("Балл", f"{score2}/100", delta=None)
        if score2 > score1:
            st.success("🏆 Победитель!")
        elif score1 == score2:
            st.info("🤝 Ничья")

    # Таблица сравнения
    st.markdown("---")
    st.markdown("### 📊 Детальное сравнение")

    comparison_data = {
        "Метрика": [
            "Documentation",
            "Complexity",
            "Code Style",
            "Structure",
            "Duplication",
            "Test Coverage",
            "ИТОГО"
        ],
        metrics1['filename']: [
            f"{metrics1['overall_score']['breakdown']['documentation']}/15",
            f"{metrics1['overall_score']['breakdown']['complexity']}/20",
            f"{metrics1['overall_score']['breakdown']['code_style']}/20",
            f"{metrics1['overall_score']['breakdown']['structure']}/15",
            f"{metrics1['overall_score']['breakdown']['duplication']}/15",
            f"{metrics1['overall_score']['breakdown']['test_coverage']}/15",
            f"{score1}/100"
        ],
        metrics2['filename']: [
            f"{metrics2['overall_score']['breakdown']['documentation']}/15",
            f"{metrics2['overall_score']['breakdown']['complexity']}/20",
            f"{metrics2['overall_score']['breakdown']['code_style']}/20",
            f"{metrics2['overall_score']['breakdown']['structure']}/15",
            f"{metrics2['overall_score']['breakdown']['duplication']}/15",
            f"{metrics2['overall_score']['breakdown']['test_coverage']}/15",
            f"{score2}/100"
        ]
    }

    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True)

    # Индивидуальные результаты
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"### {metrics1['filename']}")
        display_metric_bars_compact(metrics1['overall_score']['breakdown'])

    with col2:
        st.markdown(f"### {metrics2['filename']}")
        display_metric_bars_compact(metrics2['overall_score']['breakdown'])


def display_metric_bar(label, value, max_value):
    """Отображение метрики с progress bar"""
    percentage = (value / max_value) * 100
    st.write(f"**{label}**")
    st.progress(percentage / 100)
    st.write(f"{value}/{max_value}")


def display_metric_bars_compact(breakdown):
    """Компактное отображение всех метрик"""
    display_metric_bar("📚 Documentation", breakdown['documentation'], 15)
    display_metric_bar("🔄 Complexity", breakdown['complexity'], 20)
    display_metric_bar("✨ Code Style", breakdown['code_style'], 20)
    display_metric_bar("🏗️ Structure", breakdown['structure'], 15)
    display_metric_bar("🔍 Duplication", breakdown['duplication'], 15)
    display_metric_bar("🧪 Test Coverage", breakdown['test_coverage'], 15)


def display_details(metrics):
    """Отображение детальной информации"""

    # Сложность
    st.markdown("**🔄 Цикломатическая сложность:**")
    complexity = metrics['complexity']
    st.write(f"Средняя: {complexity['average']}, Максимальная: {complexity['maximum']}")

    if complexity['complex_functions']:
        st.warning("Сложные функции:")
        for func in complexity['complex_functions']:
            st.write(f"- {func['name']} (сложность: {func['complexity']}, строка {func['line']})")

    # Дублирование
    st.markdown("**🔍 Дублирование кода:**")
    duplication = metrics.get('duplication', {})
    st.write(f"Найдено пар: {duplication.get('duplicate_pairs', 0)}")

    if duplication.get('duplicates'):
        st.warning("Дубликаты:")
        for dup in duplication['duplicates']:
            st.write(f"- {dup['function1']} ≈ {dup['function2']} ({dup['similarity']}% похожи)")

    # Покрытие тестами
    st.markdown("**🧪 Покрытие тестами:**")
    coverage = metrics.get('coverage', {})
    st.write(f"Тестов найдено: {coverage.get('test_functions', 0)}")
    st.write(f"Покрытие: {coverage.get('coverage_estimate', 0)}%")


def generate_recommendations(metrics):
    """Генерация рекомендаций"""
    recommendations = []

    # Документация
    if metrics['docstrings']['coverage_percent'] < 80:
        recommendations.append(
            f"Добавьте docstrings (текущее покрытие: {metrics['docstrings']['coverage_percent']}%)"
        )

    # Сложность
    if metrics['complexity']['complex_functions']:
        recommendations.append(
            f"Упростите сложные функции (найдено {len(metrics['complexity']['complex_functions'])})"
        )

    # Дублирование
    duplication = metrics.get('duplication', {})
    if duplication.get('duplicate_pairs', 0) > 0:
        recommendations.append(
            f"Устраните дублирование кода ({duplication['duplicate_pairs']} пар)"
        )

    # Тесты
    coverage = metrics.get('coverage', {})
    if not coverage.get('has_tests'):
        recommendations.append("Добавьте unit-тесты")

    # Стиль
    if metrics['code_style']['issues_count'] > 0:
        recommendations.append(
            f"Исправьте проблемы стиля ({metrics['code_style']['issues_count']} проблем)"
        )

    if not recommendations:
        recommendations.append("✅ Отличное качество кода! Нет замечаний.")

    return recommendations


def get_grade_color(grade):
    """Получение цвета для оценки"""
    colors = {
        'A': '#28a745',  # зелёный
        'B': '#5cb85c',  # светло-зелёный
        'C': '#ffc107',  # жёлтый
        'D': '#fd7e14',  # оранжевый
        'F': '#dc3545'   # красный
    }
    return colors.get(grade, '#6c757d')


def get_quality_label(score):
    """Получение текстовой метки качества"""
    if score >= 90:
        return "Отлично"
    elif score >= 80:
        return "Хорошо"
    elif score >= 70:
        return "Средне"
    elif score >= 60:
        return "Ниже среднего"
    else:
        return "Плохо"


if __name__ == "__main__":
    main()