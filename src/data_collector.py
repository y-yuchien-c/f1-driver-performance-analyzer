import fastf1
import pandas as pd 
import os

class DriverDataCollector:
    def __init__(self, cache_dir='./data/cache'):
        os.makedirs(cache_dir, exist_ok = True)
        fastf1.Cache.enable_cache(cache_dir)

    def get_driver_race_data(self, year, race_name, driver_code):
        """Get race data for a specific driver"""
        session = fastf1.get_session(year, race_name, 'R')
        session.load()

        driver_laps = session.laps.pick_driver(driver_code)

        return {
            'laps': driver_laps,
            'results': session.results[session.results['Abbreviation'] == driver_code].iloc[0] if len(session.results[session.results['Abbreviation'] == driver_code]) >0 else None
        }

    def get_qualifying_data(self, year, race_name, driver_code):
        """Get qualifying performance"""
        quali = fastf1.get_session(year, race_name, 'Q')
        quali.load()

        driver_laps = quali.laps.pick_driver(driver_code)
        best_lap = driver_laps.pick_fastest()

        if best_lap is None or best_lap.empty:
            return None
        return {
            'best_time': best_lap['LapTime'].total_seconds(),
            'position': quali.results[quali.results['Abbreviation'] == driver_code]['Position'].values[0] if len(quali.results[quali.results['Abbreviation'] == driver_code]) > 0 else None 
        }

    def get_season_races(self, year):
        """Get list of all races in a season"""
        schedule = fastf1.get_event_schedule(year)
        return schedule['EventName'].tolist()