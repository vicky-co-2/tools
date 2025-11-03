import json
from json_utils import load_json_file, json_to_dataframe
from data_analyzer import JSONDataAnalyzer


def test_data_analyzer():
    """Test the JSON data analyzer with our sample data."""
    try:
        # Load the sample JSON file
        json_data = load_json_file("sample_data.json")
        print("✅ Successfully loaded JSON file")
        
        # Initialize analyzer
        analyzer = JSONDataAnalyzer(json_data)
        print("✅ Successfully initialized analyzer")
        
        # Get basic info
        info = analyzer.get_basic_info()
        print(f"\n✅ Basic Info:")
        print(f"Shape: {info['shape']}")
        print(f"Columns: {info['columns']}")
        print(f"Numeric columns: {info['numeric_columns']}")
        print(f"Categorical columns: {info['categorical_columns']}")
        print(f"Memory usage: {info['memory_usage']} bytes")
        
        # Get summary statistics
        summary_stats = analyzer.get_summary_statistics()
        print(f"\n✅ Summary Statistics:")
        print(summary_stats)
        
        # Get categorical summary
        categorical_summary = analyzer.get_categorical_summary()
        print(f"\n✅ Categorical Summary:")
        print(json.dumps(categorical_summary, indent=2))
        
        # Get missing data info
        missing_data = analyzer.get_missing_data_info()
        print(f"\n✅ Missing Data Info:")
        print(missing_data)
        
        # Get correlation matrix
        correlation_matrix = analyzer.get_correlation_matrix()
        print(f"\n✅ Correlation Matrix:")
        print(correlation_matrix)
        
        # Get column types
        column_types = analyzer.get_column_types()
        print(f"\n✅ Column Types:")
        for col, dtype in column_types.items():
            print(f"  {col}: {dtype}")
        
        # Get data sample
        sample = analyzer.get_data_sample()
        print(f"\n✅ Data Sample:")
        print(sample)
        
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_data_analyzer()