import pandas as pd
from json_utils import load_json_file, json_to_dataframe
from visualizer import JSONVisualizer
import plotly.graph_objects as go


def test_visualizer():
    """Test the JSON visualizer with our sample data."""
    try:
        # Load the sample JSON file
        json_data = load_json_file("sample_data.json")
        print("✅ Successfully loaded JSON file")
        
        # Convert to DataFrame
        df = json_to_dataframe(json_data)
        print("✅ Successfully converted to DataFrame")
        
        # Initialize visualizer
        visualizer = JSONVisualizer(df)
        print("✅ Successfully initialized visualizer")
        
        # Test histogram
        try:
            fig = visualizer.create_histogram('founded')
            print("✅ Successfully created histogram")
            # fig.show()  # Uncomment to display
        except Exception as e:
            print(f"❌ Error creating histogram: {str(e)}")
        
        # Test bar chart
        try:
            fig = visualizer.create_bar_chart('company')
            print("✅ Successfully created bar chart")
            # fig.show()  # Uncomment to display
        except Exception as e:
            print(f"❌ Error creating bar chart: {str(e)}")
        
        # Test correlation heatmap
        try:
            fig = visualizer.create_correlation_heatmap()
            print("✅ Successfully created correlation heatmap")
            # fig.show()  # Uncomment to display
        except Exception as e:
            print(f"❌ Error creating correlation heatmap: {str(e)}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_visualizer()