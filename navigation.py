import streamlit as st

def navigation_bar():
    """Create a theme-aware navigation bar"""
    st.markdown("""
        <style>
        /* Theme-aware navigation styling */
        .nav-button {
            display: inline-block;
            padding: 8px 20px;
            background-color: var(--background-color);
            border: 1px solid var(--border-color);
            border-radius: 5px;
            margin: 5px;
            text-decoration: none;
            color: inherit;
            font-weight: bold;
            transition: background-color 0.3s;
        }
        .nav-button:hover {
            background-color: var(--hover-color);
        }
        .nav-container {
            text-align: center;
            padding: 10px;
            margin-bottom: 20px;
        }
        
        /* Theme-aware variables */
        [data-testid="stAppViewContainer"] {
            --background-color: rgba(128, 128, 128, 0.1);
            --border-color: rgba(128, 128, 128, 0.2);
            --hover-color: rgba(128, 128, 128, 0.2);
        }
        
        /* Ensure text remains visible in both themes */
        .nav-button {
            text-decoration: none !important;
        }
        .nav-button:hover {
            text-decoration: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="nav-container">
            <a href="/" target="_self" class="nav-button">🏠 Home</a>
            <a href="/01_phasing_analysis" target="_self" class="nav-button">📊 Analysis</a>
            <a href="/02_playground" target="_self" class="nav-button">🎮 Playground</a>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")