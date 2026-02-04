import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
from src.performance_metrics import PerformanceMetrics

class DriverComparison:
    def __init__(self, driver1_data, driver2_data, driver1_name, driver2_name):
        """Compare two drivers' performance"""
        self.d1_laps = driver1_data['laps']
        self.d2_laps = driver2_data['laps']
        self.d1_name = driver1_name
        self.d2_name = driver2_name
        self.d1_result = driver1_data['results']
        self.d2_result = driver2_data['results']
    
    def head_to_head_summary(self):
        """Compare overall metrics between two drivers"""
        metrics1 = PerformanceMetrics(self.d1_laps)
        metrics2 = PerformanceMetrics(self.d2_laps)

        consistency1 = metrics1.consistency_score()
        consistency2 = metrics2.consistency_score()

        if not consistency1 or not consistency2:
            return None
        
        comparison = pd.DataFrame({
            self.d1_name: [
                consistency1['mean_laptime'],
                consistency1['std_laptime'],
                consistency1['coefficient_variation'],
                self.d1_result['Position'] if self.d1_result is not None else None,
                self.d1_result['Points'] if self.d1_result is not None else None
            ],
            self.d2_name: [
                consistency2['mean_laptime'],
                consistency2['std_laptime'],
                consistency2['coefficient_variation'],
                self.d2_result['Position'] if self.d2_result is not None else None,
                self.d2_result['Points'] if self.d2_result is not None else None
            ]
        }, index=['Avg Lap Time (s)', 'Std Dev (s)', 'Consistency (CV)', 'Final Position', 'Points'])

        return comparison

    def plot_pace_distribution(self, save_path = None):
        """Plot lap time distributions for both drivers"""
        fig, ax = plt.subplots(figsize = (12, 6))

        d1_clean = self.d1_laps[self.d1_laps['PitOutTime'].isna()]['LapTime'].dt.total_seconds()
        d2_clean = self.d2_laps[self.d2_laps['PitOutTime'].isna()]['LapTime'].dt.total_seconds()

        sns.kdeplot(d1_clean, label = self.d1_name, ax = ax, fill = True, alpha = 0.5, color = '#FF1E00')
        sns.kdeplot(d2_clean, label = self.d2_name, ax = ax, fill = True, alpha = 0.5, color = '#0090FF')

        ax.axvline(d1_clean.mean(), color = '#FF1E00', linestyle='--', linewidth = 2, alpha = 0.8)
        ax.axvline(d2_clean.mean(), color = '#0090FF', linestyle='--', linewidth = 2, alpha = 0.8)

        ax.set_xlabel('Lap Time (seconds)', fontsize = 12)
        ax.set_ylabel('Density', fontsize = 12)
        ax.set_title(f'Lap Time Distribution: {self.d1_name} vs {self.d2_name}', fontsize = 14, fontweight = 'bold')
        ax.legend(fontsize = 11)
        ax.grid(True, alpha = 0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi = 300, bbox_inches = 'tight')
            print(f"\n Saved plot to: {save_path}")
        else:
            plt.show()
        
        return fig
    
    def plot_lap_time_progression(self, save_path = None):
        """Plot lap times over the race"""
        fig, ax = plt.subplots(figsize = (14, 7))

        d1_laps = self.d1_laps[self.d1_laps['PitOutTime'].isna()].copy()
        d2_laps = self.d2_laps[self.d2_laps['PitOutTime'].isna()].copy()

        d1_laps['LapTimeSec'] = d1_laps['LapTime'].dt.total_seconds()
        d2_laps['LapTimeSec'] = d2_laps['LapTime'].dt.total_seconds()

        ax.plot(d1_laps['LapNumber'], d1_laps['LapTimeSec'], 
                marker = 'o', label = self.d1_name, color = '#FF1E00', linewidth=2, markersize = 4)
        ax.plot(d2_laps['LapNumber'], d2_laps['LapTimeSec'], 
                marker = 'o', label = self.d2_name, color = '#0090FF', linewidth=2, markersize = 4)
        
        ax.set_xlabel('Lap Number', fontsize = 12)
        ax.set_ylabel('Lap Time (seconds)', fontsize = 12)
        ax.set_title(f'Lap Time Progression: {self.d1_name} vs {self.d2_name}', fontsize = 14, fontweight = 'bold')
        ax.legend(fontsize = 11)
        ax.grid(True, alpha = 0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi = 300, bbox_inches = 'tight')
            print(f"Saved plot to: {save_path}")
        else:
            plt.show()
        
        return fig
