import numpy as np 
import pandas as pd

class PerformanceMetrics:
    def __init__(self, driver_laps):
        """Initialize with driver lap data"""
        self.laps = driver_laps.copy()

        self.laps['LapTimeSec'] = self.laps['LapTime'].dt.total_seconds()

    def consistency_score(self):
        """Calculate lap time consistency (lower is more consistent)"""
        clean_laps = self.laps[
            (self.laps['PitOutTime'].isna()) &
            (self.laps['LapTimeSec'].notna()) &
            (self.laps['LapTimeSec'] < self.laps['LapTimeSec'].quantile(0.95))
        ]

        if len(clean_laps) ==0:
            return None

        mean_time = clean_laps['LapTimeSec'].mean()
        std_time = clean_laps['LapTimeSec'].std()

        return {
            'mean_laptime': mean_time,
            'std_laptime': std_time,
            'coefficient_variation': std_time/mean_time if mean_time>0 else None,
            'num_laps' : len(clean_laps)
        }

    def sector_analysis(self):
        """Analyze performance by sector"""
        sector = {}

        for sector_num in [1, 2, 3]:
            sector_col = f'Sector{sector_num}Time'

            if sector_col not in self.laps.columns:
                continue
            valid_times = self.laps[self.laps[sector_col].notna()][sector_col]

            if len(valid_times) == 0:
                continue
            
            times_sec = valid_times.dt.total_seconds()

            sector[f'sector_{sector_num}'] = {
                'best': times_sec.min(),
                'avg': times_sec.mean(),
                'std': times_sec.std(),
                'num_laps': len(times_sec)
            }
        return sector

    def tire_management(self):
        """Analyze tire management across stints"""
        stint_analysis = []

        for stint in self.laps['Stint'].unique():
            stint_laps = self.laps[
                (self.laps['Stint'] == stint) &
                (self.laps['LapTimeSec'].notna()) &
                (self.laps['PitOutTime'].isna())
            ]

            if len(stint_laps) <5:
                continue
            
            early_laps = stint_laps.head(5)['LapTimeSec'].mean()
            late_laps = stint_laps.tail(5)['LapTimeSec'].mean()

            stint_analysis.append({
                'stint': int(stint),
                'compound': stint_laps['Compound'].iloc[0] if 'Compound' in stint_laps.columns else 'Unknown',
                'total_laps': len(stint_laps),
                'early_pace': early_laps,
                'late_pace': late_laps,
                'pace_dropoff': late_laps - early_laps,
                'dropoff_per_lap': (late_laps - early_laps) / len(stint_laps) if len(stint_laps) >0 else None
            })
        return pd.DataFrame(stint_analysis) if stint_analysis else pd.DataFrame()

    