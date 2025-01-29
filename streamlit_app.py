import streamlit as st

st.set_page_config(
    page_title="Sine Wave Phasing Analysis Home",
    page_icon="🏠",
    layout="wide"
)



# Custom CSS that adapts to theme
st.markdown("""
    <style>
    /* Using CSS variables for theme-aware styling */
    .big-font {
        font-size: 30px !important;
        font-weight: bold;
        color: var(--text-color);
    }
    .medium-font {
        font-size: 20px !important;
        color: var(--text-color);
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        background-color: var(--background-color);
        border: 1px solid var(--border-color);
        margin: 10px 0px;
    }
    
    /* Theme-aware variables */
    [data-testid="stAppViewContainer"] {
        --text-color: inherit;
        --background-color: rgba(128, 128, 128, 0.1);
        --border-color: rgba(128, 128, 128, 0.2);
    }

    /* Ensure text remains visible in both themes */
    .card h3 {
        color: inherit;
    }
    .card p, .card ul, .card ol {
        color: inherit;
    }

    /* Style adjustments for buttons */
    .stButton button {
        width: 100%;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

if 'phasing_results' not in st.session_state:
    st.session_state['phasing_results'] = None
    
if 'phasing_df' not in st.session_state:
    st.session_state['phasing_df'] = None

if 'gene_df' not in st.session_state:
    st.session_state['gene_df'] = None

# Header
st.markdown('<p class="big-font">Welcome to Phasing Analysis App </p>', unsafe_allow_html=True)

# Introduction
st.markdown("""
This app provides tools for analyzing and visualizing phasing data using the decaying sine wave model.
Navigate through different pages to analyze your data and explore curve fitting parameters.
""")

# Main content with cards for each page
st.markdown('<p class="medium-font">Available Tools:</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>Data Analysis</h3>
        <p>Upload and analyze your phasing data:</p>
        <ul>
            <li>Upload CSV data files</li>
            <li>Fit the data with decaying sine wave model</li>
            <li>Visualize results with interactive plots</li>
            <li>Download processed data and figures</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Analysis Page ➡️"):
        st.switch_page("pages/01_phasing_analysis.py")

with col2:
    st.markdown("""
    <div class="card">
        <h3>Curve Playground</h3>
        <p>Explore fitting parameters interactively:</p>
        <ul>
            <li>Adjust curve parameters in real-time</li>
            <li>Visualize parameter effects</li>
            <li>Understand parameter relationships</li>
            <li>Test different configurations</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Playground ➡️"):
        st.switch_page("pages/02_playground.py")

with col3:
    st.markdown("""
    <div class="card">
        <h3>Individual Gene</h3>
        <p>Calculate the adjustedd average value for individual genes</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Individual Gene Analysis ➡️"):
        st.switch_page("pages/03_individual_gene.py")

# Quick Start Guide
st.markdown("""
<div class="card">
    <h3>🚀 Quick Start Guide</h3>
    <ol>
        <li><b>Phasing Analysis:</b> Start by uploading your CSV file in the Analysis page</li>
        <li><b>Review Phasing Results:</b> Examine the fitted curves and parameter values</li>
        <li><b>Export Results:</b> Download your processed data and visualizations</li>        
        <li><b>Explore Parameters:</b> Use the Curve Playground to understand parameter effects</li>
        <li><b>Gene Analysis:</b> Upload the CSV file for individual gene phasing data</li>
        <li><b>Review Phasing Results:</b> Examine the phasing data of one particular gene relative to population average</li>
        <li><b>Export Results:</b> Download your adjusted gene average table</li>             
    </ol>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("For questions or issues, please go to the github repo: https://github.com/zhuweix/SinePhasingAnalyzerOnline")