import unittest
from programme import (
    Location, AirQuality, WaterQuality, NoiseLevel, 
    MonitoringStation, MonitoringSystem, AlertLevel
)

class TestLocation(unittest.TestCase):
    '''Тестування класу Location'''
    def test_valid_location(self):
        '''Перевірка на валідність локації'''
        loc = Location("Центральний парк", [50.01, 36.23], "парк")
        self.assertEqual(loc.name, "Центральний парк")
        self.assertEqual(loc.latitude, 50.01)

    def test_invalid_coordinates(self):
        '''Знаходить неправильні координати: перша координата в діапазоні від -90 до 90'''
        with self.assertRaises(ValueError):
            Location("Парк", [95.0, 36.0], "парк")

    def test_invalid_name_type(self):
        '''Неправильна назва локації: не може бути числом'''
        with self.assertRaises(TypeError):
            Location(234, [20, 20], 'промзона')

    def test_invalid_location_type(self):
        '''Типу локації "річка" немає в списку можливих локацій для вимірювань'''
        with self.assertRaises(ValueError):
            Location('Дніпро', [40, 20], 'річка')

class TestAirQuality(unittest.TestCase):
    '''Тестування класу AirQuality'''
    def setUp(self):
        self.loc = Location("Тест", [50.0, 50.0], "парк")
        self.date = [1, 5] 
        self.time = [12, 0]

    def test_qi_calculation(self):
        '''Для локації, визначеної вище, перевірка правильно розрахованого індекса якості'''
        air = AirQuality(40.0, 60.0, 600.0, 80.0, self.date, self.time, self.loc)
        self.assertEqual(air.quality_index(), 112)

    def test_is_safe(self):
        '''Перевірка, чи є перше вимірювання безпечним, друге ні'''
        safe_air = AirQuality(10.0, 10.0, 400.0, 20.0, [1, 1], [12, 0], self.loc)
        danger_air = AirQuality(100.0, 100.0, 1000.0, 100.0, [1, 1], [12, 0], self.loc)
        self.assertTrue(safe_air.is_safe())
        self.assertFalse(danger_air.is_safe())

class TestWaterQuality(unittest.TestCase):
    '''Тестування класу WaterQuality'''
    def setUp(self):
        self.loc = Location("Річка", [50.0, 36.0], "промзона")

    def test_water_alert_level(self):
        '''Перевірка, чи є за показниками індекс якості води критичного рівня'''
        system = MonitoringSystem()
        water_critical = WaterQuality(2.0, 0.5, 50.0, [6, 5], [8, 0], self.loc)
        qi = water_critical.quality_index()
        self.assertEqual(system.get_level_alert(qi), AlertLevel.CRITICAL)

class TestMonitoringStation(unittest.TestCase):
    '''Тестування класу MonitoringStation'''
    def setUp(self):
        '''Створення локації та станції за певними вимірюваннями в приклад'''
        self.loc = Location("Станція 1", [50, 30], "дорога")
        self.station = MonitoringStation(self.loc, [AirQuality, NoiseLevel])

    def test_take_measurement(self):
        '''Перевірка на кількість вимірювань за NoiseLevel'''
        noise = NoiseLevel(70.0, "Дорога", [1, 1], [12, 0], self.loc)
        self.station.take_measurement(noise)
        self.assertEqual(len(self.station.measurements), 1)

    def test_take_measurement_wrong_sensor_type(self):
        '''Перевірка, що WaterQuality не відноситься до списку зазначених для вимірювань у станції'''
        water = WaterQuality(7.0, 5.0, 1.0, [1, 1], [12, 0], self.loc)
        with self.assertRaises(TypeError):
            self.station.take_measurement(water)

    def test_average_calculation(self):
        """Перевірка розрахунку середнього значення для різних типів вимірювань"""
        m1 = AirQuality(12.0, 20.0, 400.0, 20.0, [1, 1], [10, 0], self.loc)
        m2 = AirQuality(35.4, 50.0, 800.0, 50.0, [1, 1], [11, 0], self.loc)
        m3 = NoiseLevel(80.0, "Дорога", [1, 1], [11, 30], self.loc)
        self.station.take_measurement(m1)
        self.station.take_measurement(m2)
        self.station.take_measurement(m3)
        avg_recent = self.station.average([2, 0], [12, 0])
        self.assertAlmostEqual(avg_recent['AirQuality'], 75.0, places=0)
        self.assertAlmostEqual(avg_recent['NoiseLevel'], 166.0, places=0)
        avg_all = self.station.average([3, 0], [12, 0])
        self.assertAlmostEqual(avg_all['AirQuality'], 75.0, places=0)

    def test_forecast_trend_improvement(self):
        '''Перевірка прогнозу за двома вимірюваннями'''
        m1 = NoiseLevel(90.0, "Шум", [1, 1], [10, 0], self.loc)
        m2 = NoiseLevel(60.0, "Шум", [1, 1], [11, 0], self.loc)
        self.station.take_measurement(m1)
        self.station.take_measurement(m2)
        forecast = self.station.forecast_quality(NoiseLevel)
        self.assertEqual(forecast['trend'], "покращення")

class TestMonitoringSystem(unittest.TestCase):
    '''Тестування класу MonitoringSystem'''
    def setUp(self):
        '''Створення системи моніторингу, локації, станції за вимірюваннями повітря, додавання станції до системи'''
        self.system = MonitoringSystem()
        self.loc = Location("Центральна", [50, 36], "дорога")
        self.station = MonitoringStation(self.loc, [AirQuality])
        self.system.add_station(self.station)

    def test_alert_generation(self):
        '''Перевірка генерації рівня тривоги, кількості вимірювань тривоги'''
        critical_air = AirQuality(300.0, 400.0, 5000.0, 500.0, [1, 1], [12, 0], self.loc)
        self.station.take_measurement(critical_air)
        alerts = self.system.check_all()
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].level, AlertLevel.CRITICAL)

    def test_report_content(self):
        '''Перевірка цілісності фінального звіту моніторингу довкілля'''
        air = AirQuality(10.0, 10.0, 400.0, 20.0, [1, 1], [12, 0], self.loc)
        self.station.take_measurement(air)
        report = self.system.report()
        self.assertIn("ЗВІТ СИСТЕМИ", report)
        self.assertIn("Центральна", report)

    def test_check_all_no_duplicates(self):
        '''Перевірка, чи не дублюються список тривог, якщо викликати перевірку декілька разів'''
        air = AirQuality(300.0, 400.0, 5000.0, 500.0, [1, 1], [12, 0], self.loc)
        self.station.take_measurement(air)
        self.system.check_all()
        self.system.check_all()
        self.assertEqual(len(self.system.alerts), 1)

if __name__ == '__main__':
    unittest.main()
