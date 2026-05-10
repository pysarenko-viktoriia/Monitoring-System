def require_positive(value: float, label: str) -> float:
    """Перевіряє, що значення є додатним числом."""
    if not isinstance(value, (int, float)):
        raise TypeError(f"{label} має бути числом")
    if value < 0:
        raise ValueError(f"{label} має бути додатним")
    return float(value)

def require_non_empty_str(value: str, label: str) -> str:
    """Перевіряє, що значення є непорожнім рядком."""
    if not isinstance(value, str):
        raise TypeError(f"{label} має бути рядком")
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{label} не може бути порожнім")
    return cleaned

def require_float_or_int(value: float, label: str) -> float:
    """Перевіряє, що значення є числом."""
    if not isinstance(value, (int, float)):
        raise TypeError(f"{label} має бути числом")
    return float(value)

def require_correct_coordinates(list_of_coord: list[int | float]) -> tuple[float, float]:
    '''Перевіряє, чи правильні координати.'''
    if not isinstance(list_of_coord, list):
        raise TypeError(f'Має бути введений список')
    if len(list_of_coord) != 2:
        raise IndexError('Мають бути вказані координати з двох чисел')
    coord_1, coord_2 = [require_float_or_int(coord, 'Координата') for coord in list_of_coord]
    if coord_1 < -90 or coord_1 > 90:
        raise ValueError(f'Перша координата має бути в діапазоні між -90 та 90, не {coord_1}')
    if coord_2 < -180 or coord_2 > 180:
        raise ValueError(f'Друга координата має бути в діапазоні між -180 та 180, не {coord_2}')
    return coord_1, coord_2

def require_correct_ph(ph: int | float) -> int | float:
    '''Перевіряє, чи правильно вказаний ph.'''
    if not isinstance(ph, (int, float)):
        raise TypeError('pH має бути числом')
    if ph < 0 or ph > 14:
        raise ValueError('pH має бути в діапазоні від 0 до 14')
    return ph

def checking_type_of_location(type_of_location: str, name: str) -> str:
    '''Перевіряє вказаний тип локації, чи віноситься він до list_of_locations'''
    list_of_locations = ['парк', 'дорога', 'промзона']
    type_of_location = require_non_empty_str(type_of_location, 'Тип локації')
    if type_of_location not in list_of_locations:
        raise ValueError(f'{name} немає у списку доступних для перевірки локацій')
    return type_of_location

def check_list_of_two_int(value, label: str) -> list[int]:
    '''Перевірка, чи є зазначений список з двух чисел'''
    if not isinstance(value, list) or not all(isinstance(x, int) for x in value):
        raise TypeError(f'{label} має бути списком з цілих чисел')
    if len(value) != 2:
        raise IndexError(f'{label} має містити рівно два числа')
    return value

def checking_date(date: list[int]) -> list[int]:
    '''Перевірка правильно вказаної дати: чи є числами, чи в діапазоні'''
    date = check_list_of_two_int(date, 'Дата')
    day = date[0]
    month = date[1]
    if day <= 0 or day >= 32:
        raise ValueError('День має бути в діапазоні між 0 та 31 включно')
    if month < 1 or month > 12:
        raise ValueError('Місяць має бути в діапазоні між 1 та 12')
    return [day, month]

def checking_time(time: list[int]) -> list[int]:
    '''Перевірка правильно вказаного часу: чи є числами, чи є в діапазоні'''
    time = check_list_of_two_int(time, 'Час')
    hour = time[0]
    minute = time[1]
    if hour < 0 or hour > 23:
        raise ValueError('Година має бути зазначеною в діапазоні між 0 та 23')
    if minute < 0 or minute > 59:
        raise ValueError('Хвилини мають бути зазначені в діапазоні між 0 та 59')
    return [hour, minute]