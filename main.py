from programme import Location, AirQuality, NoiseLevel, WaterQuality, MonitoringStation, MonitoringSystem
 
if __name__ == '__main__':
    try:
        '''Створення різних локацій та вимірювань для них, відрізняються рівнем небезпеки'''
        loc_critical = Location("Заводський район", [50.0, 36.0], "промзона")
        air_critical = AirQuality(260.0, 300.0, 2000.0, 200.0, [6, 5], [9, 0], loc_critical)
        noise_critical = NoiseLevel(105.0, "Вибухові роботи", [6, 5], [10, 0], loc_critical)
        water_critical = WaterQuality(2.0, 0.5, 50.0, [6, 5], [8, 0], loc_critical)
 
        loc_danger = Location('Технічний канал Індустріальний', [80.0, 100.0], 'промзона')
        air_danger = AirQuality(160.0, 200.0, 1500.0, 150.0, [6, 5], [11, 0], loc_danger)
        air_danger2 = AirQuality(100.0, 250.0, 1503.0, 90.0, [6, 6], [12, 0], loc_danger)
        noise_danger = NoiseLevel(93.0, "Важка техніка", [6, 5], [12, 0], loc_danger)
        water_danger = WaterQuality(3.0, 1.0, 30.0, [6, 5], [7, 0], loc_danger)
 
        loc_warning = Location('Вулиця Івана Франка', [-20.9, 30.0], 'дорога')
        air_warning = AirQuality(40.0, 60.0, 600.0, 80.0, [6, 5], [8, 0], loc_warning)
        air_warning2 = AirQuality(60.0, 80.0, 650.0, 80.0, [10, 5], [8, 0], loc_warning)
        noise_warning = NoiseLevel(76.0, "Будівельні роботи", [6, 5], [14, 0], loc_warning)
        noise_warning2 = NoiseLevel(76.0, "Будівельні роботи", [10, 7], [14, 0], loc_warning)

        loc_info = Location("Центральний парк", [50.01, 36.23], "парк")
        air_info = AirQuality(8.0, 15.0, 400.0, 20.0, [6, 5], [10, 0], loc_info)
        water_info = WaterQuality(7.2, 8.0, 2.0, [6, 5], [10, 15], loc_info)

        '''Створення системи моніторингу, створюються станції -- додаються локації та вимірювання до них'''
        system = MonitoringSystem()
        station1 = MonitoringStation(loc_critical, [AirQuality, NoiseLevel, WaterQuality])
        station2 = MonitoringStation(loc_danger, [AirQuality, NoiseLevel, WaterQuality])
        station3 = MonitoringStation(loc_warning, [AirQuality, NoiseLevel])
        station4 = MonitoringStation(loc_info, [AirQuality, WaterQuality])

        '''Кожна станція, яка була створена вище, додається до системи моніторингу.
        В кожній станції виконується вимірювання індекса якості
        '''
        for station in [station1, station2, station3, station4]:
            system.add_station(station)
        for meas in [air_critical, noise_critical, water_critical]:
            station1.take_measurement(meas)
        for meas in [air_danger, air_danger2, noise_danger, water_danger]:
            station2.take_measurement(meas)
        for meas in [air_warning, air_warning2, noise_warning, noise_warning2]:
            station3.take_measurement(meas)
        for meas in [air_info, water_info]:
            station4.take_measurement(meas)
        '''Перевірка всіх станцій, визначення рівня небезпеки, створення звіту.
        Визначення середнього для кожного типу вимірювань в станції 1'''
        alerts = system.check_all()
        report = system.report()
        average1 = station1.average([10, 20], [12, 0])
        
    except (ValueError, TypeError, IndexError) as e:
        print(f'Помилка: {e}')
    else:
        '''Друк звіту, виведення інформації про середній індекс'''
        print(report)
        for key, val in average1.items():
            print(f'Середнє за період для {key} локації {station1.location.name} -- {val}')