import fastf1
from src.data_collector import DriverDataCollector
from src.performance_metrics import PerformanceMetrics
import argparse

def analyze_driver(year, race, driver_code):
    """Analyze single driver performace"""
    print(f"\n{'='*60}")
    print(f"Analyzing {driver_code} - {year} {race} Grand Prix")
    print(f"{'='*60}\n")

    collector = DriverDataCollector()

    print("Loading race data...")
    race_data = collector.get_driver_race_data(year, race, driver_code)

    if race_data['laps'].empty:
        print(f"No data found for {driver_code}")
        return
    
    metrics = PerformanceMetrics(race_data['laps'])

    print("\n📊 CONSISTENCY ANALYSIS")
    print("-" * 60)
    consistency = metrics.consistency_score()
    if consistency:
        print(f"  Average Lap Time:    {consistency['mean_laptime']:.3f}s")
        print(f"  Standard Deviation:  {consistency['std_laptime']:.3f}s")
        print(f"  Consistency Score:   {consistency['coefficient_variation']:.4f} (lower = better)")
        print(f"  Clean Laps Analyzed: {consistency['num_laps']}")
    
    print("\n🏁 SECTOR ANALYSIS")
    print("-" * 60)
    sectors = metrics.sector_analysis()
    for sector, data in sectors.items():
        print(f"\n  {sector.upper()}:")
        print(f"    Best:    {data['best']:.3f}s")
        print(f"    Average: {data['avg']:.3f}s")
        print(f"    Std Dev: {data['std']:.3f}s")
    
    print("\n🛞 TIRE MANAGEMENT")
    print("-" * 60)
    tire_data = metrics.tire_management()
    if not tire_data.empty:
        print(tire_data.to_string(index=False))
    else:
        print("  Insufficient data for tire analysis")

    if race_data['results'] is not None:
        print(f"\n🏆 RACE RESULT")
        print("-" * 60)
        print(f"  Position: {race_data['results']['Position']}")
        print(f"  Points:   {race_data['results']['Points']}")
    
    print("\n" + "="*60 + "\n")

def compare_drivers(year, race, driver1_code, driver2_code):
    """Compare two drivers head-to-head"""
    print(f"\n{'='*60}")
    print(f"Comparing {driver1_code} vs {driver2_code}")
    print(f"{year} {race} Grand Prix")
    print(f"{'='*60}\n")

    collector = DriverDataCollector()

    print(f"Loading data for {driver1_code}...")
    d1_data = collector.get_driver_race_data(year, race, driver1_code)
    
    print(f"Loading data for {driver2_code}...")
    d2_data = collector.get_driver_race_data(year, race, driver2_code)

    if d1_data['laps'].empty or d2_data['laps'].empty:
        print("Error: Missing data for one or both drivers")
        return 

    from src.comparisons import DriverComparison

    comparison = DriverComparison(d1_data, d2_data, driver1_code, driver2_code)

    print("\n📊 HEAD-TO-HEAD COMPARISON")
    print("-" * 60)
    summary = comparison.head_to_head_summary()
    if summary is not None:
        print(summary.to_string())
    
    print("\n📈 Generating visualizations...")
    comparison.plot_pace_distribution(f'{driver1_code}_vs_{driver2_code}_pace_dist.png')
    comparison.plot_lap_time_progression(f'{driver1_code}_vs_{driver2_code}_progression.png')
    
    print("\n" + "="*60 + "\n")

def main():
    parser = argparse.ArgumentParser(description='F1 Driver Performance Analyzer')
    parser.add_argument('--year', type=int, default=2024, help='Season year (default: 2024)')
    parser.add_argument('--race', type=str, default='Bahrain', help='Race name (default: Bahrain)')
    parser.add_argument('--driver', type=str, help='Driver code (e.g., VER, HAM, LEC)')
    parser.add_argument('--compare', nargs=2, metavar=('DRIVER1', 'DRIVER2'), 
                        help='Compare two drivers (e.g., --compare VER PER)')
                    
    args = parser.parse_args()
    
    if args.compare:
        compare_drivers(args.year, args.race, args.compare[0], args.compare[1])
    elif args.driver:
        analyze_driver(args.year, args.race, args.driver)
    else:
        parser.error("Please provide either --driver for single analysis or --compare for comparison")

if __name__ == "__main__":
    main()