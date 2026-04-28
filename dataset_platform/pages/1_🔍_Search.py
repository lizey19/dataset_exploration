import streamlit as st
import sys
from pathlib import Path

# Ensure utils can be imported by adding parent dir to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.github_api import search_github_datasets

st.set_page_config(page_title="Search Datasets", page_icon="🔍")

st.title("🔍 Search Datasets")
st.markdown("Search for publicly available dataset repositories on GitHub. Click on the results to view more details.")

query = st.text_input("Enter keywords (e.g., 'covid', 'finance', 'climate')", placeholder="Type a topic...")

col1, col2 = st.columns([1, 5])
with col1:
    search_btn = st.button("Search", type="primary")

if search_btn or query:
    if query:
        with st.spinner("Searching GitHub..."):
            results = search_github_datasets(query)
            
        if results:
            st.success(f"Found {len(results)} results for '{query}'!")
            
            for i, repo in enumerate(results):
                # We use expanders for a clean UI
                with st.expander(f"📁 {repo['name']}  |  ⭐ {repo['stars']} stars", expanded=(i==0)):
                    st.write(f"**Description:** {repo['description']}")
                    st.write(f"**Author:** `{repo['author']}`")
                    st.markdown(f"[🔗 View Repository on GitHub]({repo['html_url']})")
        else:
            st.warning("No results found. Try different keywords.")
    else:
        st.info("Please enter a search query to begin.")
