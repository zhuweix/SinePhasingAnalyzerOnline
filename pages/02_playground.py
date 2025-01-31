import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utility import fit_function, upper_function, lower_function, get_plot_defaults

st.set_page_config(
    page_title="Curve Fit Playground",
    page_icon="🎮",
    layout="wide"
)

def create_parameter_controls(phasing_results=None):
    """Create sliders for parameter adjustment"""
    if phasing_results is None:
        spacing = st.number_input('Spacing', value=160)
        w = 2 * np.pi / spacing
        amp =  st.number_input('Amplitude', value=0.5)
        decay = st.number_input('Decay (per period)', value=0.8)
        slope = st.number_input('Slope (per kb)', value=0.2)/ 1000  
        b = st.number_input('b0', value=1)
        theta0 = st.number_input('theta0', value=-1.57)
        params = {
            'A': amp,
            'l': -np.log(decay) / spacing,
            'w_0': w,
            'theta_0': theta0,
            'b': b,
            's': slope
        }
        return params

    result_dict = phasing_results['results']
    spacing = st.number_input('Spacing', value=result_dict['Spacing'])
    w = 2 * np.pi / spacing
    amp =  st.number_input('Amplitude', value=result_dict['Amplitude'])
    decay = st.number_input('Decay (per period)', value=result_dict['Decay'])
    slope = st.number_input('Slope (per kb)', value=result_dict['Slope'])/ 1000     
    b = st.number_input('b0', value=result_dict['b0'])
    theta0 = st.number_input('theta0', value=result_dict['theta0'])

    params = {
        'A': amp,
        'l': -np.log(decay) / spacing,
        'w_0': w,
        'theta_0': theta0,
        'b': b,
        's': slope
    }
    return params

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
        xlim_min = st.number_input("X Min", value=defaults['xlim'][0])
        ylim_min = st.number_input("Y Min", value=defaults['ylim'][0])
        xtick_min = st.number_input("X tick Min", value=defaults['xticks_popt'][0])
        xtick_space = st.number_input("X tick Spacing", value=defaults['xticks_popt'][2])
    
    with col2:
        xlim_max = st.number_input("X Max", value=defaults['xlim'][1])
        ylim_max = st.number_input("Y Max", value=defaults['ylim'][1])
        xtick_max = st.number_input("X tick Max", value=defaults['xticks_popt'][1])        
    # Combine all parameters
    plot_params_new = {
        'title': title,
        'xlabel': xlabel,
        'ylabel': ylabel,
        'xlim': [xlim_min, xlim_max],
        'ylim': [ylim_min, ylim_max],
        'xticks': np.arange(xtick_min, xtick_max+1, xtick_space),
        'yticks': np.arange(ylim_min, ylim_max*1.01, (ylim_max - ylim_min) / 5)
    }
    
    return plot_params_new


def plot_curves(params, plot_params):
    """Create plot with current parameters"""
    fig, ax = plt.subplots(figsize=(5, 4))
    
    # Generate x values
    x = np.linspace(plot_params['xlim'][0], plot_params['xlim'][1], 1000)
    
    # Calculate curves
    y_fit = fit_function(x, params['A'], params['l'], params['w_0'], 
                        params['theta_0'], params['b'], params['s'])
    y_high = upper_function(x, params['A'], params['l'], params['b'], params['s'])
    y_low = lower_function(x, params['A'], params['l'], params['b'], params['s'])
    x_low, x_high = plot_params['xlim']
    bleft = x_low * params['s'] + params['b']
    bright = x_high * params['s'] + params['b']  

    # Plot curves
    g = sns.lineplot(x=x, y=y_fit, label='Fitted', color='red', lw=1, ax=ax)    
    g = sns.lineplot(x=(x_low, x_high), y=(bleft, bright), lw=2, ls='--', color='.3', ax=g, label='BaseLine')
    g = sns.lineplot(x=x, y=y_high, lw=2, ls='--', color='0.5', ax=g, label='Envelope')
    g = sns.lineplot(x=x, y=y_low, lw=2, ls='--', color='0.5', ax=g,)
    g.legend(markerscale=2)
    # Set plot parameters
    g.set(xlabel=plot_params['xlabel'],
          ylabel=plot_params['ylabel'],
          xlim=plot_params['xlim'],
          ylim=plot_params['ylim'],
          xticks=plot_params['xticks'],
          yticks=plot_params['yticks'],
          title=plot_params['title'])

    return fig

def main():
    st.title("Curve Playground")
    st.markdown("""
    Adjust the parameters to see how they affect the fitted curve and envelopes.
    Use this playground to understand the relationship between parameters and the resulting curve shape.
    """)
    # Create sidebar for plot range controls
    with st.sidebar:
        plot_params = plot_settings_sidebar()
    # Create two columns for parameters and plot
    col1, col2 = st.columns([1, 2])
    
    # Parameter controls in left column
    with col1:
        st.subheader("Parameters")
        # Check if there's a result_dict in session state
        params = create_parameter_controls(
            st.session_state.get('phasing_results', None)
        )
    
    # Plot in right column
    with col2:
        fig = plot_curves(params, plot_params)
        st.pyplot(fig)
    

if __name__ == "__main__":
    main()