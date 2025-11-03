import json
from json_utils import load_json_file, json_to_dataframe, get_json_structure


def test_json_utils():
    """Test the JSON utilities with our sample data."""
    try:
        # Load the sample JSON file
        json_data = load_json_file("sample_data.json")
        print("✅ Successfully loaded JSON file")
        print(f"Data type: {type(json_data)}")
        print(f"Keys: {list(json_data.keys()) if isinstance(json_data, dict) else 'N/A'}")
        
        # Get JSON structure
        structure = get_json_structure(json_data)
        print("\n✅ JSON Structure:")
        print(json.dumps(structure, indent=2))
        
        # Convert to DataFrame
        df = json_to_dataframe(json_data)
        print(f"\n✅ Successfully converted to DataFrame")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print("\nFirst 5 rows:")
        print(df.head())
        
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


if __name__ == "__main__":
    test_json_utils()