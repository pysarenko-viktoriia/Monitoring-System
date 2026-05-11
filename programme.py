# ============================================
# Назва завдання: Система моніторингу довкілля
# Студент: Писаренко Вікторія Віталіївна
# Додатковий функціонал: прогноз якості, порівняння локацій, найгірший рівень якості та найкращий
# ============================================

import debugging
from abc import ABC, abstractmethod
from enum import Enum

class AlertLevel(Enum):
    '''Клас, який відповідає за рівень небезпеки'''
    INFO = 1
    WARNING = 2
    DANGER = 3
    CRITICAL = 4

class Location:
    '''
    Клас, який представляє локацію з його харатеристиками.
    Атрибути: назва, список координат, тип локації.

    Перевірка типів, порівняння з іншими на рівність координат, рядок з інформацією про локацію.
    '''
    def __init__(self, name: str, list_of_coord: list[int | float], type_of_location: str):
        '''
        Ініціалізація класу Location.
        
        Атрибути:
        name: назва локації
        latitude, longtitude: широта, довгота (координати локації)
        type_of_location: тип локації (парк, дорога, промзона)
        '''
        self.name = debugging.require_non_empty_str(name, 'Назва локації')
        self.latitude, self.longitude = debugging.require_correct_coordinates(list_of_coord)
        self.type_of_location = debugging.checking_type_of_location(type_of_location, self.name)

    def __eq__(self, other) -> bool:
        '''Перевірка координат на рівність, чи знаходиться одна локація там, де й інша'''
        if not isinstance(other, Location):
            return NotImplemented
        return self.latitude == other.latitude and self.longitude == other.longitude
    
    def __str__(self) -> str:
        '''Повертається рядок з інформацією про локацію'''
        return f'Локація {self.name} з координатами {self.latitude} широти, {self.longitude} довготи має тип {self.type_of_location}'

    def __repr__(self) -> str:
        """Технічне представлення об'єкта"""
        return f"Location({self.name!r}, lat={self.latitude}, lon={self.longitude}, type={self.type_of_location!r})"
    

class Measurement(ABC):
    '''
    Абстрактний клас, який визначає рівень небезпеки даної локації.
    
    Атрибути: отримане значення за певним критерієм, одиниця, дата й час, локація.
    Перевірка типів, порівняння з іншими "менше ніж", визначення індексу (абстрактний метод), чи є локація безпечною.
    '''
    def __init__(self, value: float, unit: str, date: list[int], time: list[int], location: Location):
        '''
        Ініціалізація класу Measurement.
        
        Атрибути:
        value: значення рівня небезпеки
        unit: одиниця виміру, за якою проводилось дослідження
        time: дата й час вимірів
        location: локація, об'єкт класу Location
        '''
        self.location = location
        self.value = debugging.require_positive(value, 'Значення')
        self.unit = debugging.require_non_empty_str(unit, 'Одиниця виміру')
        self.date = debugging.checking_date(date)
        self.time = debugging.checking_time(time)
    
    @abstractmethod
    def quality_index(self) -> int:
        pass

    def is_safe(self) -> bool:
        '''Повертається True, якщо індекс безпеки менше 100'''
        return self.quality_index() < 100

    def __eq__(self, other: 'Measurement') -> bool:
        '''Повертається True, якщо індекс якості рівний'''
        if not isinstance(other, Measurement):
            return NotImplemented
        return self.quality_index() == other.quality_index()

    def __lt__(self, other: 'Measurement') -> bool:
        '''Повертається True, якщо індекс даної локації менший від іншого'''
        if not isinstance(other, Measurement):
            return NotImplemented
        return self.quality_index() < other.quality_index()

class AirQuality(Measurement):
    '''
    Клас-нащадок від абстрактного класу Measurement, який визначає індекс якості повітря.
    Критерії: pm25, pm10, co2, o3, зазначена локація класу Location.
    '''
    def __init__(self, pm25: float, pm10: float, co2: float, o3: float, date: list[int], time: list[int], location: Location):
        '''
        Ініціалізація класу AirQuality.
        
        Атрибути:
        pm25: суміш твердих мікрочастинок, тип float
        pm10: більші тверді частинки за попередні, тип float
        со2: рівень вуглекислого газу, тип float
        о3: рівень озону, тип float
        '''
        super().__init__(pm25, 'µg/m³', date, time, location)
        self.pm25 = float(pm25)
        self.pm10 = debugging.require_positive(pm10, 'Кількість твердих частинок')
        self.co2 = debugging.require_positive(co2, 'Вуглекислий газ')
        self.o3 = debugging.require_positive(o3, 'Озон')
 
    def quality_index(self) -> int:
        '''Визначення індексу якості повітря'''
        if self.pm25 < 12.1:
            return int(self.pm25 / 12.0 * 50)
        elif self.pm25 < 35.5:
            return int(51 + (self.pm25 - 12.1) / (35.4 - 12.1) * 49)
        elif self.pm25 < 55.5:
            return int(101 + (self.pm25 - 35.5) / (55.4 - 35.5) * 49)
        elif self.pm25 < 150.5:
            return int(151 + (self.pm25 - 55.5) / (150.4 - 55.5) * 49)
        elif self.pm25 < 250.5:
            return int(201 + (self.pm25 - 150.5) / (250.4 - 150.5) * 99)
        else:
            return min(500, int(301 + (self.pm25 - 250.5) / (500.4 - 250.5) * 199))
 
    def __str__(self) -> str:
        return (f'AirQuality | Кількість твердих мікрочастинок = {self.pm25} µg/m³, кількість твердих частинок = {self.pm10} µg/m³, '
        f'\nвуглекислий газ = {self.co2} ppm, озон={self.o3} µg/m³ | AQI={self.quality_index()}')
    
class WaterQuality(Measurement):
    '''
    Клас-нащадок від абстрактного класу Measurement, який визначає індекс якості води.
    Критерії: рівень pH, рівень розчиненого кисню, рівень каламутності
    '''
    def __init__(self, ph: float, oxygen: float, turbidity: float, date: list[int], time: list[int], location: Location):
        '''
        Ініціалізація класу WaterQuality.
        
        Атрибути:
        ph: рівень ph, тип float
        oxygen: рівень розчиненого кисню, тип float
        turbidity: рівень каламутності, тип float
        '''
        super().__init__(ph, 'pH', date, time, location)
        self.ph = debugging.require_correct_ph(ph)
        self.oxygen = debugging.require_positive(oxygen, 'Рівень розчиненого кисню')
        self.turbidity = debugging.require_positive(turbidity, 'Рівень каламутності')

    def quality_index(self) -> int:
        '''Визначення індексу якості води'''
        ph_score = abs(self.ph - 7.0) * 30
        oxygen_score = max(0, (6 - self.oxygen) * 20)
        turb_score = min(200, self.turbidity * 2)
        return min(500, int(ph_score + oxygen_score + turb_score))
    
    def __str__(self) -> str:
        return (f'WaterQuality | pH = {self.ph}, рівень розчиненого кисню = {self.oxygen} mg/L, '
        f'\nрівень каламутності = {self.turbidity} NTU | QI = {self.quality_index()}')
    
class NoiseLevel(Measurement):
    '''
    Клас-нащадок від абстрактного класу Measurement, який визначає рівень шуму.
    Критерії: рівень шуму в децибелах, джерело шуму
    '''
    def __init__(self, decibels: float, source: str, date: list[int], time: list[int], location: Location):
        '''
        Ініціалізація класу NoiseLevel.
        
        Атрибути:
        decibels: рівень шуму в дБ, тип float
        source: джерело шуму, тип str
        '''
        super().__init__(decibels, 'dB', date, time, location)
        self.decibels = debugging.require_positive(decibels, 'Рівень (дБ)')
        self.source = debugging.require_non_empty_str(source, 'Джерело шуму')

    def quality_index(self) -> int:
        '''Визначення індексу шуму'''
        if self.decibels < 55:
            return int(self.decibels / 55 * 50)
        elif self.decibels < 70:
            return int(50 + (self.decibels - 55) / 15 * 50)
        elif self.decibels < 85:
            return int(100 + (self.decibels - 70) / 15 * 100)
        else:
            return min(500, int(200 + (self.decibels - 85) * 5))
        
    def __str__(self) -> str:
        return f'NoiseLevel | Рівень (дБ) = {self.decibels} dB, джерело шуму = {self.source} | NQI = {self.quality_index()}'
    
class Alert:
    '''Клас для повідомлень про тривогу'''
    def __init__(self, station: "MonitoringStation", alert_type: str, level: AlertLevel, measurement: Measurement):
        '''
        Ініціалізація класу Alert.

        Атрибути:
        station: станція класу MonitoringStation
        alert_type: тип тривоги
        level: рівень тривогиг з AlertLevel
        date, time: дата й час
        '''
        self.station = station
        self.alert_type = alert_type
        self.level = level
        self.date = measurement.date
        self.time = measurement.time
 
    def __str__(self) -> str:
        '''Повідомлення про рівень тривоги на певній станції з усіма іншими атрибутами цього класу'''
        date_str = f"{self.date[0]:02d}.{self.date[1]:02d}"
        time_str = f"{self.time[0]:02d}:{self.time[1]:02d}"
        return (f'[{self.level.name}] Тривога на станції {self.station.location.name}: '
                f'{self.alert_type} (Дата: {date_str}, Час: {time_str})')
    
class MonitoringStation:
    '''Клас, який відповідає за станції, за якими відбувається спостереження'''
    def __init__(self, location: Location, sensors: list[AirQuality | NoiseLevel | WaterQuality]):
        '''
        Ініціалізація класу MonitoringStation.

        Атрибути:
        location: локація типу Location
        sensors: тип спостереження (якість повітря, води, рівень шуму)
        measurements: список, куди будуть зберігатись зроблені вимірювання
        '''
        self.location = location
        self.sensors = sensors
        self.measurements = []
 
    def take_measurement(self, measurement: Measurement) -> Measurement:
        '''Зберігає нове вимірювання в список measurements та повертає його.'''
        if not isinstance(measurement, Measurement):
            raise TypeError("Очікується об'єкт типу Measurement")
        if not any(isinstance(measurement, sensor) for sensor in self.sensors):
            raise TypeError(f"Станція не підтримує тип '{type(measurement).__name__}'")
        self.measurements.append(measurement)
        return measurement
 
    def average(self, period_diff: list[int], current_point: list[int]) -> dict:
        '''
        Розрахунок середнього за період на основі списків часу.
        period_diff: тривалість періоду назад [години, хвилини]
        current_point: точка відліку (умовний "зараз") [години, хвилини]
        '''
        period_diff = debugging.checking_time(period_diff)
        current_point = debugging.checking_time(current_point)
        period_minutes = period_diff[0] * 60 + period_diff[1]
        now_minutes = current_point[0] * 60 + current_point[1]
        recent = []
        for m in self.measurements:
            m_minutes = m.time[0] * 60 + m.time[1]
            if 0 <= (now_minutes - m_minutes) <= period_minutes:
                recent.append(m)
        if not recent:
            return {}
 
        groups = {}
        for m in recent:
            name = type(m).__name__
            if name not in groups:
                 groups[name] = []
            groups[name].append(m.quality_index())
        return {name: round(sum(val) / len(val), 2) for name, val in groups.items()}
    
    def forecast_quality(self, sensor_type) -> tuple[str, str]:
        '''
        Прогнозує тенденцію якості для заданого типу сенсора на основі наявних вимірювань.
        sensor_type: клас вимірювання (AirQuality, WaterQuality, NoiseLevel)
        Повертає словник з поточним середнім індексом, прогнозованим індексом та прогнозом.
        '''
        relevant = [m for m in self.measurements if isinstance(m, sensor_type)]
        if not relevant:
            return (f'Помилка: немає даних для {sensor_type.__name__}', 'error')
        
        indices = [m.quality_index() for m in relevant]
        avg = sum(indices) / len(indices)
    
        if len(indices) >= 2:
            delta = indices[-1] - indices[0]
            if delta > 10:
                trend = 'погіршення'
                forecast = min(500, int(avg + abs(delta) * 0.5))
            elif delta < -10:
                trend = 'покращення'
                forecast = max(0, int(avg - abs(delta) * 0.5))
            else:
                trend = 'стабільно'
                forecast = int(avg)
        else:
            trend = 'недостатньо даних для прогнозу'
            forecast = int(avg)
        return {
            'sensor': sensor_type.__name__,
            'current_avg_qi': round(avg, 2),
            'forecast_qi': forecast,
            'trend': trend,
        }
 
    def __repr__(self) -> str:
        """Технічне представлення об'єкта"""
        return f'MonitoringStation({self.location.name!r}, sensors={[s.__name__ for s in self.sensors]})'

class MonitoringSystem:
    '''Клас для представлення системи моніторингу довкілля'''
    def __init__(self):
        '''
        Ініціалізація класу MonitoringSystem.
        Створені чотири списки
        total_qis: для загальних середніх індексів якості
        stations: для станцій
        alerts: тривог
        qis: індексів якості
        '''
        self.total_qis = []
        self.stations = []
        self.alerts = []
        self.qis = []
 
    def add_station(self, station: MonitoringStation):
        '''Додає станцію до системи'''
        self.stations.append(station)
 
    def get_level_alert(self, qi: int) -> AlertLevel:
        '''Визначає рівень небезпеки по індексу якості'''
        if qi >= 300:
            return AlertLevel.CRITICAL
        elif qi >= 200:
            return AlertLevel.DANGER
        elif qi >= 100:
            return AlertLevel.WARNING
        else:
            return AlertLevel.INFO

    def check_all(self) -> list[Alert]:
        '''Перевіряє всі станції та генерує тривоги.'''
        new_alerts = []
        self.alerts = []
        for station in self.stations:
            for measurement in station.measurements:
                qi = measurement.quality_index()
                level = self.get_level_alert(qi)
                if level == AlertLevel.INFO:
                    continue
                alert = Alert(
                    station=station,
                    alert_type=f"{type(measurement).__name__} QI={qi}",
                    level=level,
                    measurement=measurement,
                )
                new_alerts.append(alert)
        self.alerts.extend(new_alerts)
        return new_alerts
 
    def __len__(self) -> int:
        '''Визначає кількість стацій (довжину списку stations)'''
        return len(self.stations)
 
    def report(self) -> list[str]:
        '''
        Звіт системи моніторингу довкілля
        
        1. Кількість станцій
        2. Кожна станція з вимірюваннями й індексами якості по кожному, прогноз вимірювань, середній індекс локації
        3. Середній показник всіх станцій
        4. Аналіз порівняння: найгірший індекс якості, найкращий індекс якості
        5. Тривоги: рівень тривоги, локація та тип вимірювання
        '''
        lines = ['='*30, 'ЗВІТ СИСТЕМИ МОНІТОРИНГУ ДОВКІЛЛЯ', '='*30]
        lines.append(f'Станцій: {len(self.stations)}')
        all_m = []
        self.total_qis = []
        for station in self.stations:
            lines.append(f'\n{station.location.name} ({station.location.type_of_location})')
            lines.append(f'Координати: {station.location.latitude}, {station.location.longitude}')
            lines.append(f'Вимірювань: {len(station.measurements)}')
            qis = []

            for m in station.measurements:
                all_m.append(m) 
                qis.append(m.quality_index()) 
            for m in station.measurements:
                lines.append(f' - {m}')
            lines.append('\n')
            for sensor_cls in station.sensors:
                forecast = station.forecast_quality(sensor_cls)
                if "error" not in forecast:
                    lines.append(
                        f"Прогноз {forecast['sensor']}: поточний QI={forecast['current_avg_qi']}, "
                        f"прогноз QI={forecast['forecast_qi']}, прогноз: {forecast['trend']}"
                    )
            if qis:
                avg = sum(qis) / len(qis)
                lines.append(f'Середній індекс локації: {avg:.2f}')
                self.total_qis.append(avg)
        if self.total_qis:
            final_avg = sum(self.total_qis) / len(self.total_qis)
            lines.append(f'\nСередній показник всіх станцій: {final_avg:.2f}')
        else:
            lines.append('\nДані відсутні.')

        if all_m:
            best_con = min(all_m)
            worst_con = max(all_m)
            best_level_alert = self.get_level_alert(best_con.quality_index())
            worst_level_alert = self.get_level_alert(worst_con.quality_index())
            lines.append('\n')
            lines.append("-" * 49)
            lines.append("АНАЛІЗ ПОРІВНЯННЯ")
            lines.append(f"Найкраща екологічна ситуація: {best_con.quality_index()} QI, рівень тривоги: {best_level_alert.name}")
            lines.append(f"Локація: {best_con.location.name}") 
            lines.append(f"\nНайгірша екологічна ситуація: {worst_con.quality_index()} QI, рівень тривоги: {worst_level_alert.name}")
            lines.append(f"Локація: {worst_con.location.name}")
            lines.append("-" * 49)

        if self.alerts:
            lines.append("\nАКТИВНІ ТРИВОГИ:")
            for alert in self.alerts:
                lines.append(f"{alert}")
        
        lines.append("=" * 60)
        return "\n".join(lines)
