import streamlit as st
import pandas as pd

st.set_page_config(page_title="Upload Dataset", page_icon="📤")

st.title("📤 Upload Dataset")
st.markdown("Upload your own CSV dataset to begin analysis, visualization, and modeling.")

# Check if a dataset is already loaded
if st.session_state.get("df") is not None:
    st.info(f"📁 Currently loaded dataset: **{st.session_state.dataset_name}**")
    if st.button("Clear Dataset", type="secondary"):
        st.session_state.df = None
        st.session_state.dataset_name = None
        st.rerun()
    st.markdown("---")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    with st.spinner("Loading dataset..."):
        try:
            # Read the CSV file
            df = pd.read_csv(uploaded_file)
            
            # Save to session state
            st.session_state.df = df
            st.session_state.dataset_name = uploaded_file.name
            
            st.success(f"Successfully loaded '{uploaded_file.name}'!")
            
            st.write("### Data Preview")
            st.dataframe(df.head(), use_container_width=True)
            
            # Display basic metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Rows", df.shape[0])
            with col2:
                st.metric("Total Columns", df.shape[1])
                
            st.info("👉 You can now proceed to the **Analyze** or **Visualize** pages from the sidebar.")
            
        except Exception as e:
            st.error(f"Error loading the CSV file. Please ensure it's a valid CSV format.\n\nDetails: {e}")
