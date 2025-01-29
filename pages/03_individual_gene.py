import streamlit as st
import io
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from utility import (
    fit_function, upper_function, lower_function,
    process_data, process_gene_data, get_plot_defaults
)

def plot_settings_sidebar():
    """
    Create sidebar for plot settings
    """
    st.sidebar.header("Plot Settings")
    
    # Get default values
    defaults = get_plot_defaults()
    
    # Title and labels
    title = st.sidebar.text_input("Plot Title", value=defaults['title'])
    xlabel = st.sidebar.text_input("X-axis Label", value=defaults['xlabel'])
    ylabel = st.sidebar.text_input("Y-axis Label", value=defaults['ylabel'])
    
    # Axis limits
    st.sidebar.subheader("Axis Limits")
    col1, col2 = st.sidebar.columns(2)
        
    with col1:
        pos_min = st.number_input("Pos Min", value=defaults['location_range'][0])
        xlim_min = st.number_input("X Min", value=defaults['xlim'][0])
        ylim_min = st.number_input("Y Min", value=defaults['ylim'][0])
        xtick_min = st.number_input("X tick Min", value=defaults['xticks_popt'][0])
        xtick_space = st.number_input("X tick Spacing", value=defaults['xticks_popt'][2])
    
    with col2:
        pos_max = st.number_input("Pos Max", value=defaults['location_range'][1])
        xlim_max = st.number_input("X Max", value=defaults['xlim'][1])
        ylim_max = st.number_input("Y Max", value=defaults['ylim'][1])
        xtick_max = st.number_input("X tick Max", value=defaults['xticks_popt'][1])        
    # Combine all parameters
    plot_params = {
        'title': title,
        'xlabel': xlabel,
        'ylabel': ylabel,
        'xlim': [xlim_min, xlim_max],
        'ylim': [ylim_min, ylim_max],
        'location_range': [pos_min, pos_max],
        'xticks': np.arange(xtick_min, xtick_max+1, xtick_space),
        'yticks': np.arange(ylim_min, ylim_max + 1, (ylim_max - ylim_min) / 5)
    }
    
    return plot_params

def create_visualization(df, result_dict, gene, adj_value, plot_params):
    """
    Create visualization for phasing analysis data
    """
    fig, ax = plt.subplots(figsize=(5, 4))
    
    # Get data points
    xpos = df['Pos'].values
    y = df['Value'].values
    
    # Create scatter plot of data points
    g = sns.scatterplot(x=xpos, y=y, s=3, label='Data', ax=ax)
    
    if result_dict is not None:
        # Generate fitting curve points
        x_fit = np.linspace(plot_params['xlim'][0], plot_params['xlim'][1], 1000)
        
        # Get fit parameters
        popt = result_dict['fit_params']
        A_fit, l_fit, w_0_fit, theta0_fit, b_fit, s_fit = popt
        
        # Plot fitted sine wave
        y_fit = fit_function(x_fit, A_fit, l_fit, w_0_fit, theta0_fit, b_fit, s_fit)
        g = sns.lineplot(x=x_fit, y=y_fit, label='Population Fitted Curve', ax=g, color='red', lw=1)

        y_fit_adj = y_fit + adj_value
        g = sns.lineplot(x=x_fit, y=y_fit_adj, label='Adjusted Curve', ax=g, color='.4', lw=1, ls='--')        
    
    # Set plot parameters
    g.set(xlabel=plot_params['xlabel'],
          ylabel=plot_params['ylabel'],
          xlim=plot_params['xlim'],
          ylim=plot_params['ylim'],
          xticks=plot_params['xticks'],
          yticks=plot_params['yticks'],
          title=plot_params['title'] + f' {gene}')
    g.legend(markerscale=2)
    return fig


def save_figure_to_bytes(fig, format='png', dpi=300):
    """Save matplotlib figure to bytes in specified format"""
    buf = io.BytesIO()
    fig.savefig(buf, format=format, dpi=dpi, bbox_inches='tight')
    buf.seek(0)
    return buf


def main():
    st.title("Analyze Adjusted Average Value for Individual Genes")
    st.markdown("""
    Adjust the average value for uneven locations of values within one gene based on phasing analysis.
    This analysis uses the result from phasing analysis (recommended). The users could also manually put the result.
    """)

    # Get plot settings from sidebar
    with st.sidebar:
        plot_params = plot_settings_sidebar()
    
    phasing_results = st.session_state.get('phasing_results', None)
    # Main content
    uploaded_file = st.file_uploader(
        "Choose a CSV file (or csv.gz file)",
        type="csv",
        help="CSV should contain columns: Gene, Pos, Value"
    )

    if uploaded_file is not None and phasing_results is not None:
        df = pd.read_csv(uploaded_file)
        fit_params = phasing_results['results']['fit_params']
        xmin, xmax = plot_params['location_range']
        gene_df = process_gene_data(
            df, fit_params, xmin=xmin, xmax=xmax)
        # Show data preview
        st.subheader("Result Preview")
        st.dataframe(gene_df.head(), use_container_width=True)        
        st.session_state['gene_results'] = {
            'result_df': gene_df,
            'filename': uploaded_file.name
        }
        gene_dict = dict(zip(gene_df['Gene'], gene_df['Adj.Average']))
        st.download_button(
            label="Download Gene Table (CSV)",
            data=gene_df.to_csv(index=False).encode('utf-8'),
                file_name='gene_adjusted_average.csv',
                mime='text/csv'
            )     

        target_gene = st.sidebar.text_input("Gene Name", value="")
        target_gene = target_gene.strip()
        if len(target_gene) > 0:
            adj_value = gene_dict.get(target_gene, None)
            if adj_value is None:
                st.error(f"{target_gene} is not Found in the provided table")
            target_df = gene_df.loc[gene_df['Gene'] == target_gene]
            fig = create_visualization(target_df, phasing_results, target_gene, adj_value, plot_params)
            st.pyplot(fig)
    

if __name__ == "__main__":
    main()