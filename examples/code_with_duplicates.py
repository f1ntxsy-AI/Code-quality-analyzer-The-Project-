"""
Пример кода с дублированием
Для демонстрации copy-paste detection
"""

def process_user_data(user):
    """Обработка данных пользователя"""
    result = []
    for item in user.get('items', []):
        if item['active']:
            result.append(item['value'])
    return result


def process_admin_data(admin):
    """Обработка данных администратора"""
    result = []
    for item in admin.get('items', []):
        if item['active']:
            result.append(item['value'])
    return result


def calculate_total_v1(data):
    """Вычисление суммы (версия 1)"""
    total = 0
    for value in data:
        if value > 0:
            total += value
    return total


def calculate_total_v2(data):
    """Вычисление суммы (версия 2)"""
    total = 0
    for value in data:
        if value > 0:
            total += value
    return total


def unique_function(x, y):
    """Уникальная функция без дубликатов"""
    return x ** 2 + y ** 2
