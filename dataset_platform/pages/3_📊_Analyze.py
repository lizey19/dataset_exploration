import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Ensure utils can be imported by adding parent dir to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.data_analysis import get_dataframe_summary

st.set_page_config(page_title="Analyze Dataset", page_icon="📊")

st.title("📊 Analyze Dataset")
st.markdown("Automated Exploratory Data Analysis (EDA) for your loaded dataset.")

if st.session_state.get("df") is not None:
    df = st.session_state.df
    st.info(f"📁 Analyzing dataset: **{st.session_state.dataset_name}**")
    
    summary = get_dataframe_summary(df)
    
    st.header("1. Dataset Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", summary["shape"][0])
    col2.metric("Total Columns", summary["shape"][1])
    col3.metric("Memory Usage", f"{summary['memory_usage_mb']} MB")
    
    st.markdown("---")
    
    st.header("2. Column Information")
    # Combine data types and missing values into a neat table
    dtypes_df = pd.DataFrame(list(summary["data_types"].items()), columns=["Column", "Data Type"])
    missing_df = pd.DataFrame(list(summary["missing_values"].items()), columns=["Column", "Missing Values"])
    info_df = pd.merge(dtypes_df, missing_df, on="Column")
    
    # Highlight missing values
    st.dataframe(
        info_df.style.highlight_max(subset=['Missing Values'], color='#ff4b4b', axis=0),
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    
    st.header("3. Summary Statistics")
    
    with st.expander("🔢 Numeric Columns Summary", expanded=True):
        num_summary = df.describe()
        if not num_summary.empty:
            st.dataframe(num_summary, use_container_width=True)
        else:
            st.write("No numeric columns available to summarize.")
            
    with st.expander("🔠 Categorical Columns Summary", expanded=False):
        cat_df = df.select_dtypes(exclude=['number'])
        if not cat_df.empty:
            st.dataframe(cat_df.describe(), use_container_width=True)
        else:
            st.write("No categorical columns available.")
            
else:
    st.warning("⚠️ No dataset loaded. Please upload a dataset first.")
    st.page_link("pages/2_📤_Upload.py", label="Go to Upload Page", icon="📤")
