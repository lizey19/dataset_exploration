import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_histogram(df: pd.DataFrame, column: str, theme: str = "plotly_white"):
    """Creates a histogram for a given numeric column."""
    fig = px.histogram(
        df, 
        x=column, 
        title=f"Distribution of {column}",
        template=theme,
        marginal="box", # Adds a box plot on top
        color_discrete_sequence=["#636EFA"]
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        title_font_size=20,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig

def create_scatter(df: pd.DataFrame, x_col: str, y_col: str, color_col: str = None, theme: str = "plotly_white"):
    """Creates a scatter plot for two numeric columns."""
    fig = px.scatter(
        df, 
        x=x_col, 
        y=y_col, 
        color=color_col,
        title=f"{x_col} vs {y_col}",
        template=theme, 
        opacity=0.7
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        title_font_size=20,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig

def create_heatmap(df: pd.DataFrame, theme: str = "plotly_white"):
    """Creates a correlation heatmap for numeric columns."""
    numeric_df = df.select_dtypes(include=['number'])
    if numeric_df.empty:
        return None
        
    corr = numeric_df.corr()
    fig = px.imshow(
        corr, 
        text_auto=".2f", 
        aspect="auto",
        title="Correlation Heatmap",
        color_continuous_scale="RdBu_r",
        template=theme
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        title_font_size=20,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig
