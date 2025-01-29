import streamlit as st

def navigation_bar():
    """Create a navigation bar with styled buttons"""
    st.markdown("""
        <style>
        .nav-button {
            display: inline-block;
            padding: 8px 20px;
            background-color: #f0f2f6;
            border-radius: 5px;
            margin: 5px;
            text-decoration: none;
            color: #262730;
            font-weight: bold;
        }
        .nav-button:hover {
            background-color: #dfe1e6;
        }
        .nav-container {
            text-align: center;
            padding: 10px;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="nav-container">
            <a href="/" target="_self" class="nav-button">Home</a>
            <a href="/phasing_analysis" target="_self" class="nav-button">Phasing Analysis</a>
            <a href="/02_playground" target="_self" class="nav-button">Curve Playground</a>
            <a href="/03_individual_gene" target="_self" class="nav-button">Adjusted Level for Individual Genes</a>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")