"""
Example: Analyzing Detection Logs
Demonstrates how to use the analytics utilities
"""

from utils import DetectionAnalyzer, print_log_summary
import sys


def example_basic_summary():
    """Example 1: Print quick summary of latest log"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Quick Summary")
    print("="*60)
    
    try:
        print_log_summary()
    except FileNotFoundError:
        print("No detection logs found. Run the detector first!")
        print("Usage: python app.py")


def example_detailed_analysis():
    """Example 2: Detailed analysis of detection data"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Detailed Analysis")
    print("="*60)
    
    try:
        analyzer = DetectionAnalyzer()
        
        # Get summary
        summary = analyzer.get_summary()
        print(f"\nTotal Detections: {summary['total_detections']}")
        print(f"Duration: {summary['duration']:.1f} seconds")
        print(f"Unique Objects: {summary['unique_objects']}")
        
        # Get object counts
        print("\nObject Counts:")
        counts = analyzer.get_object_counts()
        for obj, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {obj}: {count}")
        
        # Get confidence statistics for top object
        if counts:
            top_object = max(counts, key=counts.get)
            stats = analyzer.get_confidence_stats(top_object)
            print(f"\nConfidence Stats for '{top_object}':")
            print(f"  Mean: {stats['mean']:.3f}")
            print(f"  Median: {stats['median']:.3f}")
            print(f"  Range: {stats['min']:.3f} - {stats['max']:.3f}")
            print(f"  Std Dev: {stats['std']:.3f}")
        
    except FileNotFoundError:
        print("\nNo detection logs found. Run the detector first!")


def example_timeline_analysis():
    """Example 3: Analyze detection timeline"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Timeline Analysis")
    print("="*60)
    
    try:
        analyzer = DetectionAnalyzer()
        
        # Get timeline at 30-second intervals
        timeline = analyzer.get_detection_timeline(resample='30s')
        
        print("\nDetection Timeline (30-second intervals):")
        print(timeline.head(10))
        
        # Find peak detection time
        peak_time = timeline.idxmax()
        peak_count = timeline.max()
        
        print(f"\nPeak Detection Time: {peak_time}")
        print(f"Detections at Peak: {peak_count}")
        
    except FileNotFoundError:
        print("\nNo detection logs found. Run the detector first!")


def example_generate_full_report():
    """Example 4: Generate complete report with visualizations"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Generate Full Report")
    print("="*60)
    
    try:
        analyzer = DetectionAnalyzer()
        
        print("\nGenerating comprehensive report...")
        print("This will create:")
        print("  - Text summary report")
        print("  - Object distribution chart")
        print("  - Detection timeline graph")
        print("  - Confidence distribution histogram")
        
        report_path = analyzer.generate_report()
        
        print(f"\n✅ Report generated successfully!")
        print(f"View the report at: {report_path}")
        print(f"Charts saved in: reports/")
        
    except FileNotFoundError:
        print("\nNo detection logs found. Run the detector first!")
        print("Usage: python app.py")


def example_object_specific_analysis():
    """Example 5: Analyze specific object type"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Object-Specific Analysis")
    print("="*60)
    
    try:
        analyzer = DetectionAnalyzer()
        
        # Get available objects
        counts = analyzer.get_object_counts()
        
        if not counts:
            print("\nNo objects detected in logs")
            return
        
        # Analyze most common object
        top_object = max(counts, key=counts.get)
        
        print(f"\nAnalyzing: {top_object}")
        print(f"Total detections: {counts[top_object]}")
        
        # Get confidence stats
        stats = analyzer.get_confidence_stats(top_object)
        print("\nConfidence Statistics:")
        print(f"  Average: {stats['mean']:.3f}")
        print(f"  Median: {stats['median']:.3f}")
        print(f"  Minimum: {stats['min']:.3f}")
        print(f"  Maximum: {stats['max']:.3f}")
        
        # Get timeline
        timeline = analyzer.get_detection_timeline(top_object, resample='1min')
        print(f"\nDetection frequency over time:")
        print(f"  Total minutes with detections: {(timeline > 0).sum()}")
        print(f"  Average detections per minute: {timeline.mean():.1f}")
        print(f"  Peak detections in 1 minute: {timeline.max()}")
        
    except FileNotFoundError:
        print("\nNo detection logs found. Run the detector first!")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("  DETECTION LOG ANALYSIS EXAMPLES")
    print("="*70)
    print("\nThis script demonstrates various ways to analyze detection logs")
    print("Make sure you have run the detector first to generate logs!\n")
    
    # Run all examples
    example_basic_summary()
    example_detailed_analysis()
    example_timeline_analysis()
    example_object_specific_analysis()
    example_generate_full_report()
    
    print("\n" + "="*70)
    print("  ANALYSIS COMPLETE")
    print("="*70)
    print("\nYou can now:")
    print("  1. Check the reports/ directory for generated charts")
    print("  2. Import these functions in your own scripts")
    print("  3. Customize the analysis for your specific needs\n")


if __name__ == "__main__":
    # Check if user wants help
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("\nUsage: python example_analytics.py")
        print("\nThis script analyzes detection logs and generates reports")
        print("First run the detector to generate logs:")
        print("  python app.py")
        print("\nThen run this script to analyze the results:")
        print("  python example_analytics.py")
        sys.exit(0)
    
    main()
