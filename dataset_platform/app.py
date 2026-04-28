import streamlit as st

st.set_page_config(
    page_title="Dataset Discovery Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a professional look, ensuring it works well in both light and dark modes
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        transition: all 0.3s ease;
        font-weight: bold;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    /* Style cards/expanders for a cleaner look */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1.1rem;
    }
    /* Add a subtle top border to distinct sections */
    hr {
        margin-top: 3rem;
        margin-bottom: 3rem;
        opacity: 0.5;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌍 Dataset Discovery & Analysis Platform")

st.markdown("""
### Welcome to your Data Science Workspace! 🚀

This expert-level platform allows you to seamlessly discover, upload, analyze, and visualize datasets, all within a modern, professional interface. 
Streamlit automatically adapts to your system's **Light** or **Dark** mode. You can toggle this manually via the top-right menu (⋮) -> Settings -> Theme.

---

### 📌 How to use the platform

Navigate using the sidebar on the left:

1. **🔍 Search:** Discover datasets hosted on GitHub across various domains.
2. **📤 Upload:** Bring your own data by uploading a `.csv` file.
3. **📊 Analyze:** Dive into your dataset with automated Exploratory Data Analysis (EDA).
4. **📈 Visualize:** Generate interactive, publication-ready Plotly charts.
5. **🤖 ML Models:** Train and evaluate quick Machine Learning models (like Linear Regression) with smart column auto-selection.

---
*Developed as a comprehensive final-year Data Science portfolio project.*
""")

# Initialize session state for the uploaded dataset
if "df" not in st.session_state:
    st.session_state.df = None
if "dataset_name" not in st.session_state:
    st.session_state.dataset_name = None
