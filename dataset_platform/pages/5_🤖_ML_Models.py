import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import plotly.express as px
import sys
from pathlib import Path

# Ensure utils can be imported
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.data_analysis import get_numeric_columns

st.set_page_config(page_title="ML Models", page_icon="🤖", layout="wide")

st.title("🤖 Basic Machine Learning")
st.markdown("Run simple Linear Regression models on your dataset to predict values based on relationships.")

if st.session_state.get("df") is not None:
    # Drop missing values for simple modeling to avoid errors
    df_raw = st.session_state.df
    df = df_raw.dropna() 
    
    numeric_cols = get_numeric_columns(df)
    
    if len(numeric_cols) < 2:
        st.warning("⚠️ Not enough numeric columns for regression. You need at least two numeric columns (X and y).")
        st.stop()
        
    st.info(f"📁 Modeling on dataset: **{st.session_state.dataset_name}**")
    if len(df) < len(df_raw):
        st.caption(f"Note: {len(df_raw) - len(df)} rows containing missing values were dropped automatically for modeling.")
    
    # Auto-select best columns based on highest correlation
    corr = df[numeric_cols].corr()
    corr_unstacked = corr.abs().unstack()
    # Remove self-correlations (which are 1.0)
    corr_unstacked = corr_unstacked[corr_unstacked < 0.999]
    
    if not corr_unstacked.empty:
        best_pair = corr_unstacked.idxmax()
        default_x_col = best_pair[0]
        default_y_col = best_pair[1]
    else:
        default_x_col = numeric_cols[0]
        default_y_col = numeric_cols[1]

    st.header("Configure Linear Regression")
    
    col1, col2 = st.columns(2)
    with col1:
        x_col = st.selectbox("Select Feature (Independent Variable X)", numeric_cols, index=numeric_cols.index(default_x_col))
    with col2:
        y_col = st.selectbox("Select Target (Dependent Variable y)", numeric_cols, index=numeric_cols.index(default_y_col))
        
    if x_col == y_col:
        st.error("Feature and Target cannot be the same column.")
        st.stop()
        
    if st.button("Run Regression", type="primary", use_container_width=True):
        with st.spinner("Training model..."):
            X = df[[x_col]]
            y = df[y_col]
            
            # Train test split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Model training
            model = LinearRegression()
            model.fit(X_train, y_train)
            
            # Prediction
            y_pred = model.predict(X_test)
            
            # Evaluation
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            st.success("✨ Model trained successfully!")
            
            # Display metrics in cards
            st.markdown("### Model Performance Metrics")
            m_col1, m_col2 = st.columns(2)
            m_col1.metric("R² Score (Accuracy)", round(r2, 4), help="1.0 is perfect prediction. 0.0 is predicting the mean.")
            m_col2.metric("Mean Squared Error (MSE)", round(mse, 4), help="Lower is better.")
            
            st.markdown("---")
            
            # Visualization
            st.markdown("### Prediction vs Actual Plot")
            
            plot_df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
            fig = px.scatter(
                plot_df, x='Actual', y='Predicted', 
                title=f"Actual vs Predicted {y_col}",
                template=None,
                opacity=0.7,
                color_discrete_sequence=["#00CC96"]
            )
            
            # Add line of perfect prediction (y=x)
            min_val = min(y_test.min(), y_pred.min())
            max_val = max(y_test.max(), y_pred.max())
            fig.add_shape(
                type="line", line=dict(dash='dash', color='red', width=2),
                x0=min_val, y0=min_val, x1=max_val, y1=max_val
            )
            
            st.plotly_chart(fig, use_container_width=True, theme="streamlit")
            
else:
    st.warning("⚠️ No dataset loaded. Please upload a dataset first.")
    st.page_link("pages/2_📤_Upload.py", label="Go to Upload Page", icon="📤")
