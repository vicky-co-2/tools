import streamlit as st
import pandas as pd
import json
import os
from json_utils import load_json_file, json_to_dataframe, get_json_structure, validate_json_format
from data_analyzer import JSONDataAnalyzer
from visualizer import JSONVisualizer
import plotly.graph_objects as go
import tempfile


# Set page configuration
st.set_page_config(
    page_title="JSON Data Analyzer & Visualizer",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 JSON Data Analyzer & Visualizer")
st.markdown("""
This tool allows you to analyze and visualize JSON data files up to 5MB in size.
Upload your JSON file below to get started!
""")

# File uploader
uploaded_file = st.file_uploader("Choose a JSON file (max 5MB)", type="json")

if uploaded_file is not None:
    # Create a temporary file to store the uploaded content
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        temp_file_path = tmp_file.name
    
    try:
        # Validate JSON format
        if not validate_json_format(temp_file_path):
            st.error("Invalid JSON format. Please upload a valid JSON file.")
        else:
            # Load JSON data
            json_data = load_json_file(temp_file_path)
            
            # Display basic information
            st.subheader("📋 JSON File Information")
            file_size = os.path.getsize(temp_file_path)
            st.info(f"File name: {uploaded_file.name} | Size: {file_size / (1024*1024):.2f} MB")
            
            # Display JSON structure
            st.subheader("🔍 JSON Structure")
            with st.expander("Click to view JSON structure"):
                structure = get_json_structure(json_data)
                st.json(structure)
            
            # Convert to DataFrame
            try:
                df = json_to_dataframe(json_data)
                st.subheader("📄 Data Preview")
                st.dataframe(df.head(10))
                
                # Initialize analyzer and visualizer
                analyzer = JSONDataAnalyzer(json_data)
                visualizer = JSONVisualizer(df)
                
                # Display basic info
                info = analyzer.get_basic_info()
                st.subheader("📈 Dataset Overview")
                col1, col2, col3 = st.columns(3)
                col1.metric("Rows", info['shape'][0])
                col2.metric("Columns", info['shape'][1])
                col3.metric("Memory Usage", f"{info['memory_usage'] / 1024:.1f} KB")
                
                # Summary statistics
                st.subheader("📊 Summary Statistics")
                summary_stats = analyzer.get_summary_statistics()
                if not summary_stats.empty:
                    st.dataframe(summary_stats)
                else:
                    st.info("No numeric columns found for summary statistics.")
                
                # Missing data
                st.subheader("❓ Missing Data")
                missing_data = analyzer.get_missing_data_info()
                if not missing_data.empty:
                    st.dataframe(missing_data)
                else:
                    st.success("No missing data found!")
                
                # Visualization section
                st.subheader("🎨 Data Visualization")
                
                # Get column lists
                numeric_columns = analyzer.numeric_columns
                categorical_columns = analyzer.categorical_columns
                
                # Tabs for different visualizations
                tab1, tab2, tab3, tab4 = st.tabs(["Histograms", "Bar Charts", "Scatter Plots", "Correlation"])
                
                with tab1:
                    if numeric_columns:
                        selected_col = st.selectbox("Select a numeric column for histogram", numeric_columns, key="hist")
                        if st.button("Generate Histogram", key="hist_btn"):
                            try:
                                fig = visualizer.create_histogram(selected_col)
                                st.plotly_chart(fig, use_container_width=True)
                            except Exception as e:
                                st.error(f"Error generating histogram: {str(e)}")
                    else:
                        st.info("No numeric columns available for histograms.")
                
                with tab2:
                    if categorical_columns:
                        selected_col = st.selectbox("Select a categorical column for bar chart", categorical_columns, key="bar")
                        if st.button("Generate Bar Chart", key="bar_btn"):
                            try:
                                fig = visualizer.create_bar_chart(selected_col)
                                st.plotly_chart(fig, use_container_width=True)
                            except Exception as e:
                                st.error(f"Error generating bar chart: {str(e)}")
                    else:
                        st.info("No categorical columns available for bar charts.")
                
                with tab3:
                    if len(numeric_columns) >= 2:
                        col1, col2 = st.columns(2)
                        x_col = col1.selectbox("X-axis", numeric_columns, key="scatter_x")
                        y_col = col2.selectbox("Y-axis", [col for col in numeric_columns if col != x_col], key="scatter_y")
                        
                        color_col = st.selectbox("Color (optional)", [None] + categorical_columns + numeric_columns, key="scatter_color")
                        if color_col == "None":
                            color_col = None
                        
                        if st.button("Generate Scatter Plot", key="scatter_btn"):
                            try:
                                if color_col:
                                    fig = visualizer.create_scatter_plot(x_col, y_col, color_col)
                                else:
                                    fig = visualizer.create_scatter_plot(x_col, y_col)
                                st.plotly_chart(fig, use_container_width=True)
                            except Exception as e:
                                st.error(f"Error generating scatter plot: {str(e)}")
                    else:
                        st.info("Need at least 2 numeric columns for scatter plots.")
                
                with tab4:
                    if len(numeric_columns) >= 2:
                        if st.button("Generate Correlation Heatmap", key="corr_btn"):
                            try:
                                fig = visualizer.create_correlation_heatmap()
                                st.plotly_chart(fig, use_container_width=True)
                            except Exception as e:
                                st.error(f"Error generating correlation heatmap: {str(e)}")
                    else:
                        st.info("Need at least 2 numeric columns for correlation analysis.")
                
                # Show full dataset
                st.subheader("📂 Full Dataset")
                st.dataframe(df)
                
            except Exception as e:
                st.error(f"Error processing JSON data: {str(e)}")
                st.info("This might be due to a complex nested JSON structure that is difficult to convert to a table format.")
                
                # Still show the raw JSON structure
                st.subheader("📄 Raw JSON Data")
                st.json(json_data)
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
else:
    st.info("Please upload a JSON file to begin analysis.")
    st.subheader("📁 Sample Data")
    st.markdown("To get started, you can use the sample data provided in `sample_data.json` in this directory.")

# Sidebar with instructions
st.sidebar.header("ℹ️ How to Use")
st.sidebar.markdown("""
1. Upload a JSON file (max 5MB)
2. Explore the data structure
3. View summary statistics
4. Create visualizations
5. Analyze missing data
""")

st.sidebar.header("📁 Supported JSON Formats")
st.sidebar.markdown("""
- Flat JSON objects
- Nested JSON structures
- JSON arrays
- Mixed data types
""")