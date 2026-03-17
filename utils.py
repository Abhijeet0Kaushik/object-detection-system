"""
Utility functions for log analysis and visualization
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import glob


class DetectionAnalyzer:
    """Analyze detection logs and generate insights"""
    
    def __init__(self, log_file=None):
        """
        Initialize analyzer
        
        Args:
            log_file: Path to CSV log file. If None, uses latest log.
        """
        if log_file is None:
            # Find latest log file
            log_files = glob.glob("logs/detections_*.csv")
            if not log_files:
                raise FileNotFoundError("No detection logs found")
            log_file = max(log_files, key=os.path.getctime)
        
        self.log_file = log_file
        self.df = pd.read_csv(log_file)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
    
    def get_summary(self):
        """Get summary statistics"""
        summary = {
            'total_detections': len(self.df),
            'unique_objects': self.df['object'].nunique(),
            'duration': (self.df['timestamp'].max() - self.df['timestamp'].min()).total_seconds(),
            'start_time': self.df['timestamp'].min(),
            'end_time': self.df['timestamp'].max()
        }
        return summary
    
    def get_object_counts(self):
        """Get total count for each object type"""
        return self.df['object'].value_counts().to_dict()
    
    def get_detection_timeline(self, object_type=None, resample='1min'):
        """
        Get timeline of detections
        
        Args:
            object_type: Filter by specific object type
            resample: Time interval for grouping (e.g., '1min', '5min', '1H')
        
        Returns:
            DataFrame with timestamp index and detection counts
        """
        df = self.df.copy()
        
        if object_type:
            df = df[df['object'] == object_type]
        
        df.set_index('timestamp', inplace=True)
        timeline = df.resample(resample).size()
        
        return timeline
    
    def get_confidence_stats(self, object_type=None):
        """Get confidence statistics"""
        df = self.df.copy()
        
        if object_type:
            df = df[df['object'] == object_type]
        
        stats = {
            'mean': df['confidence'].mean(),
            'median': df['confidence'].median(),
            'min': df['confidence'].min(),
            'max': df['confidence'].max(),
            'std': df['confidence'].std()
        }
        
        return stats
    
    def plot_object_distribution(self, save_path=None):
        """Plot distribution of detected objects"""
        plt.figure(figsize=(12, 6))
        
        counts = self.df['object'].value_counts()
        counts.plot(kind='bar', color='steelblue')
        
        plt.title('Object Detection Distribution', fontsize=16, fontweight='bold')
        plt.xlabel('Object Type', fontsize=12)
        plt.ylabel('Detection Count', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Chart saved to {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_timeline(self, object_type=None, resample='1min', save_path=None):
        """Plot detection timeline"""
        timeline = self.get_detection_timeline(object_type, resample)
        
        plt.figure(figsize=(14, 6))
        timeline.plot(color='darkgreen', linewidth=2)
        
        title = f"Detection Timeline - {object_type}" if object_type else "All Detections Timeline"
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('Detections', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Timeline saved to {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_confidence_distribution(self, save_path=None):
        """Plot confidence score distribution"""
        plt.figure(figsize=(12, 6))
        
        self.df['confidence'].hist(bins=30, color='coral', edgecolor='black', alpha=0.7)
        
        plt.title('Confidence Score Distribution', fontsize=16, fontweight='bold')
        plt.xlabel('Confidence Score', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Confidence chart saved to {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def generate_report(self, output_dir="reports"):
        """Generate complete analysis report with charts"""
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Get summary
        summary = self.get_summary()
        
        # Generate report text
        report_lines = [
            "="*60,
            "OBJECT DETECTION ANALYSIS REPORT",
            "="*60,
            "",
            f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Log File: {self.log_file}",
            "",
            "SUMMARY STATISTICS",
            "-"*60,
            f"Total Detections: {summary['total_detections']}",
            f"Unique Object Types: {summary['unique_objects']}",
            f"Detection Duration: {summary['duration']:.1f} seconds",
            f"Start Time: {summary['start_time']}",
            f"End Time: {summary['end_time']}",
            "",
            "OBJECT COUNTS",
            "-"*60
        ]
        
        # Add object counts
        for obj, count in sorted(self.get_object_counts().items(), key=lambda x: x[1], reverse=True):
            report_lines.append(f"{obj}: {count}")
        
        report_lines.append("")
        report_lines.append("CONFIDENCE STATISTICS")
        report_lines.append("-"*60)
        
        # Add confidence stats for top objects
        top_objects = self.df['object'].value_counts().head(5).index
        for obj in top_objects:
            stats = self.get_confidence_stats(obj)
            report_lines.append(f"\n{obj}:")
            report_lines.append(f"  Mean: {stats['mean']:.3f}")
            report_lines.append(f"  Median: {stats['median']:.3f}")
            report_lines.append(f"  Range: {stats['min']:.3f} - {stats['max']:.3f}")
        
        report_lines.append("")
        report_lines.append("="*60)
        
        # Save text report
        report_path = os.path.join(output_dir, f"report_{timestamp}.txt")
        with open(report_path, 'w') as f:
            f.write('\n'.join(report_lines))
        
        print(f"\n📊 Report generated: {report_path}")
        
        # Generate charts
        self.plot_object_distribution(
            os.path.join(output_dir, f"distribution_{timestamp}.png")
        )
        self.plot_timeline(
            resample='1min',
            save_path=os.path.join(output_dir, f"timeline_{timestamp}.png")
        )
        self.plot_confidence_distribution(
            os.path.join(output_dir, f"confidence_{timestamp}.png")
        )
        
        print(f"✅ All reports saved to {output_dir}/")
        
        return report_path


def print_log_summary(log_file=None):
    """Quick function to print log summary"""
    analyzer = DetectionAnalyzer(log_file)
    summary = analyzer.get_summary()
    counts = analyzer.get_object_counts()
    
    print("\n" + "="*50)
    print("DETECTION LOG SUMMARY")
    print("="*50)
    print(f"Total Detections: {summary['total_detections']}")
    print(f"Duration: {summary['duration']:.1f}s")
    print("\nTop Objects:")
    for obj, count in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {obj}: {count}")
    print("="*50 + "\n")
