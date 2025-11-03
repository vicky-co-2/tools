import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any, List, Optional
import numpy as np


class JSONVisualizer:
    """Visualizer for JSON data that creates interactive plots."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the visualizer with a DataFrame.
        
        Args:
            df (pd.DataFrame): DataFrame to visualize
        """
        self.df = df
    
    def create_histogram(self, column: str, title: Optional[str] = None) -> go.Figure:
        """
        Create a histogram for a numeric column.
        
        Args:
            column (str): Column name to plot
            title (str, optional): Plot title
            
        Returns:
            go.Figure: Plotly figure object
        """
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame")
        
        if title is None:
            title = f'Distribution of {column}'
            
        fig = px.histogram(self.df, x=column, title=title)
        return fig
    
    def create_bar_chart(self, column: str, title: Optional[str] = None) -> go.Figure:
        """
        Create a bar chart for a categorical column.
        
        Args:
            column (str): Column name to plot
            title (str, optional): Plot title
            
        Returns:
            go.Figure: Plotly figure object
        """
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame")
        
        if title is None:
            title = f'Count of {column}'
        
        value_counts = self.df[column].value_counts().head(20)  # Limit to top 20
        fig = px.bar(x=value_counts.index, y=value_counts.values, title=title)
        fig.update_xaxes(title_text=column)
        fig.update_yaxes(title_text='Count')
        return fig
    
    def create_scatter_plot(self, x_column: str, y_column: str, 
                           color_column: Optional[str] = None,
                           title: Optional[str] = None) -> go.Figure:
        """
        Create a scatter plot for two numeric columns.
        
        Args:
            x_column (str): Column name for x-axis
            y_column (str): Column name for y-axis
            color_column (str, optional): Column name for color coding
            title (str, optional): Plot title
            
        Returns:
            go.Figure: Plotly figure object
        """
        if x_column not in self.df.columns:
            raise ValueError(f"Column '{x_column}' not found in DataFrame")
        if y_column not in self.df.columns:
            raise ValueError(f"Column '{y_column}' not found in DataFrame")
        
        if title is None:
            title = f'{y_column} vs {x_column}'
            
        if color_column and color_column in self.df.columns:
            fig = px.scatter(self.df, x=x_column, y=y_column, color=color_column, title=title)
        else:
            fig = px.scatter(self.df, x=x_column, y=y_column, title=title)
            
        return fig
    
    def create_box_plot(self, column: str, group_column: Optional[str] = None,
                       title: Optional[str] = None) -> go.Figure:
        """
        Create a box plot for a numeric column.
        
        Args:
            column (str): Column name to plot
            group_column (str, optional): Column name to group by
            title (str, optional): Plot title
            
        Returns:
            go.Figure: Plotly figure object
        """
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame")
        
        if title is None:
            title = f'Box plot of {column}'
            
        if group_column and group_column in self.df.columns:
            fig = px.box(self.df, y=column, x=group_column, title=title)
        else:
            fig = px.box(self.df, y=column, title=title)
            
        return fig
    
    def create_correlation_heatmap(self, columns: Optional[List[str]] = None,
                                  title: Optional[str] = None) -> go.Figure:
        """
        Create a correlation heatmap for numeric columns.
        
        Args:
            columns (list, optional): Specific columns to include
            title (str, optional): Plot title
            
        Returns:
            go.Figure: Plotly figure object
        """
        if columns:
            numeric_df = self.df[columns].select_dtypes(include=[np.number])
        else:
            numeric_df = self.df.select_dtypes(include=[np.number])
        
        if numeric_df.empty or len(numeric_df.columns) < 2:
            raise ValueError("Not enough numeric columns for correlation heatmap")
        
        if title is None:
            title = 'Correlation Heatmap'
        
        corr_matrix = numeric_df.corr()
        fig = px.imshow(corr_matrix, text_auto=True, title=title)
        return fig
    
    def create_line_chart(self, x_column: str, y_column: str,
                         title: Optional[str] = None) -> go.Figure:
        """
        Create a line chart for two columns.
        
        Args:
            x_column (str): Column name for x-axis
            y_column (str): Column name for y-axis
            title (str, optional): Plot title
            
        Returns:
            go.Figure: Plotly figure object
        """
        if x_column not in self.df.columns:
            raise ValueError(f"Column '{x_column}' not found in DataFrame")
        if y_column not in self.df.columns:
            raise ValueError(f"Column '{y_column}' not found in DataFrame")
        
        if title is None:
            title = f'{y_column} over {x_column}'
            
        fig = px.line(self.df, x=x_column, y=y_column, title=title)
        return fig
    
    def create_pie_chart(self, column: str, title: Optional[str] = None) -> go.Figure:
        """
        Create a pie chart for a categorical column.
        
        Args:
            column (str): Column name to plot
            title (str, optional): Plot title
            
        Returns:
            go.Figure: Plotly figure object
        """
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame")
        
        if title is None:
            title = f'Distribution of {column}'
        
        value_counts = self.df[column].value_counts().head(15)  # Limit to top 15
        fig = px.pie(values=value_counts.values, names=value_counts.index, title=title)
        return fig