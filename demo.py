"""
Demo script showing how to use the JSON Analyzer & Visualizer programmatically
"""

import json
from json_utils import load_json_file, json_to_dataframe, get_json_structure
from data_analyzer import JSONDataAnalyzer
from visualizer import JSONVisualizer


def demo_json_analysis(json_file_path):
    """Demonstrate JSON analysis functionality."""
    print(f"Analyzing JSON file: {json_file_path}")
    print("=" * 50)
    
    # Load JSON data
    json_data = load_json_file(json_file_path)
    print("✅ Loaded JSON data successfully")
    
    # Show JSON structure
    structure = get_json_structure(json_data)
    print("\n📋 JSON Structure:")
    print(json.dumps(structure, indent=2))
    
    # Convert to DataFrame
    df = json_to_dataframe(json_data)
    print(f"\n📊 DataFrame shape: {df.shape}")
    print("Columns:", list(df.columns))
    
    # Analyze data
    analyzer = JSONDataAnalyzer(json_data)
    info = analyzer.get_basic_info()
    print(f"\n📈 Dataset Info:")
    print(f"  Rows: {info['shape'][0]}")
    print(f"  Columns: {info['shape'][1]}")
    print(f"  Numeric columns: {len(info['numeric_columns'])}")
    print(f"  Categorical columns: {len(info['categorical_columns'])}")
    
    # Show summary statistics
    summary_stats = analyzer.get_summary_statistics()
    if not summary_stats.empty:
        print("\n📊 Summary Statistics:")
        print(summary_stats)
    
    # Show categorical summary
    categorical_summary = analyzer.get_categorical_summary()
    if categorical_summary:
        print("\n🔤 Categorical Summary:")
        for col, info in categorical_summary.items():
            print(f"  {col}: {info['unique_values']} unique values")
    
    # Show missing data
    missing_data = analyzer.get_missing_data_info()
    if not missing_data.empty:
        print("\n❓ Missing Data:")
        print(missing_data)
    else:
        print("\n✅ No missing data found!")
    
    # Create visualizations
    visualizer = JSONVisualizer(df)
    
    # Try to create a histogram if we have numeric columns
    numeric_cols = info['numeric_columns']
    if numeric_cols:
        try:
            fig = visualizer.create_histogram(numeric_cols[0])
            print(f"\n🎨 Created histogram for {numeric_cols[0]}")
            # fig.show()  # Uncomment to display
        except Exception as e:
            print(f"\n❌ Error creating histogram: {e}")
    
    # Try to create a correlation heatmap if we have multiple numeric columns
    if len(numeric_cols) > 1:
        try:
            fig = visualizer.create_correlation_heatmap()
            print(f"\n🎨 Created correlation heatmap")
            # fig.show()  # Uncomment to display
        except Exception as e:
            print(f"\n❌ Error creating correlation heatmap: {e}")
    
    print("\n" + "=" * 50)
    print("Analysis complete!")


if __name__ == "__main__":
    # Run demo with sample data
    demo_json_analysis("sample_data.json")