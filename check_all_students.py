import os
import subprocess

students_dir = "student_submissions"

print("=" * 80)
print("📚 ПРОВЕРКА ВСЕХ СТУДЕНТОВ")
print("=" * 80)
print()

# Проверяем наличие папки
if not os.path.exists(students_dir):
    print(f"❌ Папка '{students_dir}' не найдена!")
    print()
    print("Создайте папку и добавьте туда файлы студентов:")
    print(f"  mkdir {students_dir}")
    print(f"  copy student*.py {students_dir}\\")
    exit(1)

# Получаем список Python файлов
py_files = [f for f in os.listdir(students_dir) if f.endswith('.py')]

if not py_files:
    print(f"❌ В папке '{students_dir}' нет Python файлов!")
    print()
    print("Добавьте туда файлы студентов:")
    print(f"  copy student1_ivanov.py {students_dir}\\")
    print(f"  copy student2_petrov.py {students_dir}\\")
    print(f"  copy student3_sidorov.py {students_dir}\\")
    exit(1)

print(f"📂 Найдено файлов: {len(py_files)}")
print()

# Анализируем каждый файл
for i, filename in enumerate(py_files, 1):
    filepath = os.path.join(students_dir, filename)

    print(f"{'=' * 80}")
    print(f"📝 [{i}/{len(py_files)}] Проверяю: {filename}")
    print(f"{'=' * 80}")

    try:
        result = subprocess.run(
            ["python", "src/main.py", "--file", filepath, "--format", "all"],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )

        if result.returncode == 0:
            print(result.stdout)
            print(f"✅ {filename} - проверен успешно")
        else:
            print(f"⚠️  {filename} - ошибка при проверке")
            if result.stderr:
                print("Ошибка:", result.stderr)
    except Exception as e:
        print(f"❌ {filename} - критическая ошибка: {e}")

    print()

print("=" * 80)
print("✅ ВСЕ СТУДЕНТЫ ПРОВЕРЕНЫ!")
print("=" * 80)
print()
print(f"📊 Проверено файлов: {len(py_files)}")
print(f"📁 Отчёты находятся в папке: reports/")
print()
print("Для каждого студента созданы:")
print("  • filename_report.txt      (текстовый отчёт)")
print("  • filename_report.json     (JSON отчёт)")
print("  • filename_report.md       (Markdown отчёт)")