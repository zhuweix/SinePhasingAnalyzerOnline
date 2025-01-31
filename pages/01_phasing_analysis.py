import io
import json
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from utility import (
    fit_function, upper_function, lower_function,
    process_data, get_plot_defaults
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
        pos_max = st.number_input("Pos Min", value=defaults['location_range'][1])
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
        'yticks': np.arange(ylim_min, ylim_max*1.05, (ylim_max - ylim_min) / 5)
    }
    
    return plot_params


def create_visualization(df, result_dict, plot_params):
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
        g = sns.lineplot(x=x_fit, y=y_fit, label='Fitted', ax=g, color='red', lw=1)
        
        # Plot envelopes
        y_high = upper_function(x_fit, A_fit, l_fit, b_fit, s_fit)
        y_low = lower_function(x_fit, A_fit, l_fit, b_fit, s_fit)
        x_low, x_high = plot_params['xlim']
        bleft = x_low * s_fit + b_fit
        bright = x_high * s_fit + b_fit
        g = sns.lineplot(x=(x_low, x_high), y=(bleft, bright), lw=2, ls='--', color='.3', ax=g)
        g = sns.lineplot(x=x_fit, y=y_high, lw=2, ls='--', color='0.5', ax=g,)
        g = sns.lineplot(x=x_fit, y=y_low, lw=2, ls='--', color='0.5', ax=g,)
    
    # Set plot parameters
    g.set(xlabel=plot_params['xlabel'],
          ylabel=plot_params['ylabel'],
          xlim=plot_params['xlim'],
          ylim=plot_params['ylim'],
          xticks=plot_params['xticks'],
          yticks=plot_params['yticks'],
          title=plot_params['title'])
    g.legend(markerscale=2)
    return fig

def save_figure_to_bytes(fig, format='png', dpi=300):
    """Save matplotlib figure to bytes in specified format"""
    buf = io.BytesIO()
    fig.savefig(buf, format=format, dpi=dpi, bbox_inches='tight')
    buf.seek(0)
    return buf

def prepare_results_for_json(result_dict):
    """Convert numpy values to Python native types for JSON serialization"""
    json_safe_dict = {}
    for key, value in result_dict.items():
        if isinstance(value, np.ndarray):
            json_safe_dict[key] = value.tolist()
        elif isinstance(value, np.float64):
            json_safe_dict[key] = float(value)
        else:
            json_safe_dict[key] = value
    return json_safe_dict

def prepare_results_for_csv(result_dict):
    """Convert results dictionary to 2-column format for CSV"""
    metrics = []
    
    # Add main metrics with uncertainties
    metrics.extend([
        ['Spacing (bp)', f"{result_dict['Spacing']:.1f}"],
        ['Spacing Error (bp)', f"{result_dict['Error_spacing']:.1f}"],
        ['Amplitude', f"{result_dict['Amplitude']:.3f}"],
        ['Amplitude Error', f"{result_dict['Error_Amp']:.3f}"],
        ['Slope (per kb)', f"{result_dict['Slope']:.2f}"],
        ['Slope Error (per kb)', f"{result_dict['Error_Slope']:.2f}"],
        ['Adjusted R²', f"{result_dict['Adj.R2']:.3f}"],
        ['Decay per Period', f"{result_dict['Decay']:.3f}"],
        ['Phase (rad)', f"{result_dict['theta0']:.2f}"],
        ['Baseline (b0)', f"{result_dict['b0']:.3f}"]
    ])
    
    # Create DataFrame
    results_df = pd.DataFrame(metrics, columns=['Metric', 'Value'])
    return results_df

def display_fit_results(result_dict):
    """
    Display fitting results in a formatted way
    """
    if result_dict is None:
        st.error("No fitting results available")
        return

    # Create three columns for displaying results
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Adjusted R²", 
            f"{result_dict['Adj.R2']:.3f}")
        st.metric("Nucleosome Spacing (bp)", 
                 f"{result_dict['Spacing']:.1f} ± {result_dict['Error_spacing']:.1f}")

    with col2:
        st.metric("Amplitude", 
                 f"{result_dict['Amplitude']:.3f} ± {result_dict['Error_Amp']:.3f}")
        st.metric("Decay per Period", 
                 f"{result_dict['Decay']:.3f}")
    with col3:
        st.metric("Slope (per kb)", 
                 f"{result_dict['Slope']:.2f} ± {result_dict['Error_Slope']:.2f}")
        st.metric("Phase (rad)", 
                 f"{result_dict['theta0']:.2f}")    

def main():
    st.title("Phasing Analysis")
    st.markdown("Upload CSV file containing phasing data for analysis.")
    
    # Get plot settings from sidebar
    plot_params = plot_settings_sidebar()
    
    # Main content
    uploaded_file = st.file_uploader(
        "Choose a CSV file (required columns: Pos, Value)",
        type="csv",
        help="CSV should contain columns: Pos, Value"
    )
    
    if uploaded_file is not None:
        # Load and process data
        df = pd.read_csv(uploaded_file)
        
        # Process data with specified range
        xmin, xmax = plot_params['location_range']
        processed_result = process_data(df, xmin=xmin, xmax=xmax)
        
        if processed_result is not None:
            processed_df, result_dict = processed_result
            # Save to session state with a specific key
            st.session_state['phasing_results'] = {
                'results': result_dict,
                'filename': uploaded_file.name
            }
            
            # Show data preview
            st.subheader("Data Preview")
            st.dataframe(processed_df.head(), use_container_width=True)
            
            # Display fitting results
            st.subheader("Fitting Results")
            display_fit_results(result_dict)
            
            # Create visualization
            fig = create_visualization(processed_df, result_dict, plot_params)
            
            # Show plot
            st.subheader("Phasing Analysis Plot")
            st.pyplot(fig)
            
            # Download section
            st.subheader("Download Options")
            col1, col2, col3 = st.columns(3)
            
            # Download processed data
            with col1:
                st.download_button(
                    label="Download Processed Data (CSV)",
                    data=processed_df.to_csv(index=False).encode('utf-8'),
                    file_name='processed_data.csv',
                    mime='text/csv'
                )
            
            # Download results
            with col2:
                # Prepare results for JSON
                json_safe_results = prepare_results_for_json(result_dict)
                col21, col22 = st.columns(2)
                with col21:
                    st.download_button(
                        label="Download Results (JSON)",
                        data=json.dumps(json_safe_results, indent=2),
                        file_name='fitting_results.json',
                        mime='application/json'
                    )
                with col22:
                    # Convert results to CSV format
                    results_df = prepare_results_for_csv(result_dict)
                    st.download_button(
                        label="Download Results (CSV)",
                        data=results_df.to_csv(index=False).encode('utf-8'),
                        file_name='fitting_results.csv',
                        mime='text/csv'
                    )
            
            # Download figure
            with col3:
                fig_format = st.selectbox(
                    "Figure Format",
                    options=['png', 'pdf', 'svg'],
                    index=0
                )
                
                fig_bytes = save_figure_to_bytes(fig, format=fig_format)
                st.download_button(
                    label=f"Download Figure ({fig_format.upper()})",
                    data=fig_bytes,
                    file_name=f'phasing_plot.{fig_format}',
                    mime=f'image/{fig_format}'
                )

if __name__ == "__main__":
    main()