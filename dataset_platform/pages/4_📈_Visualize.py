import streamlit as st
import sys
from pathlib import Path

# Ensure utils can be imported
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.visualization import create_histogram, create_scatter, create_heatmap
from utils.data_analysis import get_numeric_columns

st.set_page_config(page_title="Visualize Data", page_icon="📈", layout="wide")

st.title("📈 Visualize Data")
st.markdown("Create interactive, publication-ready charts using your uploaded dataset.")

if st.session_state.get("df") is not None:
    df = st.session_state.df
    st.info(f"📁 Visualizing dataset: **{st.session_state.dataset_name}**")
    
    numeric_cols = get_numeric_columns(df)
    all_cols = df.columns.tolist()
    
    if not numeric_cols:
        st.warning("⚠️ No numeric columns found in the dataset. Most visualizations require numeric data.")
        st.stop()
        
    # Create Tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["📊 Histogram", "📉 Scatter Plot", "🌡️ Correlation Heatmap"])
    
    # We use Streamlit's native theme parsing by not explicitly forcing a white/dark theme in Plotly,
    # but the utility functions we wrote accept a theme argument. 
    # Streamlit now handles Plotly themes beautifully by default.
    theme = None # Allows streamlit to override with user's light/dark mode
    
    with tab1:
        st.header("Distribution Analysis (Histogram)")
        col1, col2 = st.columns([1, 3])
        with col1:
            hist_col = st.selectbox("Select Numeric Column", numeric_cols, key="hist_col")
        with col2:
            if hist_col:
                fig = create_histogram(df, hist_col, theme=theme)
                st.plotly_chart(fig, use_container_width=True, theme="streamlit")
            
    with tab2:
        st.header("Relationship Analysis (Scatter Plot)")
        col_x, col_y, col_c = st.columns(3)
        with col_x:
            x_col = st.selectbox("X-Axis", numeric_cols, key="scatter_x")
        with col_y:
            y_col = st.selectbox("Y-Axis", numeric_cols, key="scatter_y", index=min(1, len(numeric_cols)-1))
        with col_c:
            color_col = st.selectbox("Color By (Optional)", ["None"] + all_cols, key="scatter_color")
            color_param = None if color_col == "None" else color_col
            
        if x_col and y_col:
            fig = create_scatter(df, x_col, y_col, color_param, theme=theme)
            st.plotly_chart(fig, use_container_width=True, theme="streamlit")
            
    with tab3:
        st.header("Correlation Analysis (Heatmap)")
        st.markdown("Displays the correlation matrix for all numeric columns. Values closer to 1 or -1 indicate strong relationships.")
        fig = create_heatmap(df, theme=theme)
        if fig:
            st.plotly_chart(fig, use_container_width=True, theme="streamlit")
        else:
            st.warning("Could not generate heatmap.")
else:
    st.warning("⚠️ No dataset loaded. Please upload a dataset first.")
    st.page_link("pages/2_📤_Upload.py", label="Go to Upload Page", icon="📤")
