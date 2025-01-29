import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utility import fit_function, upper_function, lower_function, get_plot_defaults


def main():
    st.title("Analyze Adjusted Average Value for Individual Genes")
    st.markdown("""
    Adjust the average value for uneven locations of values within one gene based on phasing analysis.
    This analysis uses the result from phasing analysis (recommended). The users could also manually put the result.
    """)
    

if __name__ == "__main__":
    main()