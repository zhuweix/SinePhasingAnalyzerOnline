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

def create_parameter_controls(result_dict=None):
    """Create sliders for parameter adjustment"""
    if result_dict is None:
        spacing = st.number_input('Spacing', value=160)
        w = 2 * np.pi / spacing
        amp =  st.number_input('Amplitude', value=0.5)
        decay = st.number_input('Decay (per period)', value=0.8)
        slope = st.number_input('Slope', value=0.2)        
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
    else:
        spacing = st.number_input('Spacing', value=result_dict['Spacing'])
        w = 2 * np.pi / spacing
        amp =  st.number_input('Amplitude', value=result_dict['Amplitude'])
        decay = st.number_input('Decay (per period)', value=result_dict['Decay'])
        slope = st.number_input('Slope', value=result_dict['Slope'])        
        b = st.number_input('b0', value=result_dict['b0'])
        theta0 = st.number_input('theta0', value=result_dict['theta_0'])

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
        'yticks': np.arange(ylim_min, ylim_max + 1, (ylim_max - ylim_min) / 5)
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
    g = sns.lineplot(x=(x_low, x_high), y=(bleft, bright), lw=2, ls='--', color='.3', ax=g)
    g = sns.lineplot(x=x, y=y_high, lw=2, ls='--', color='0.5', ax=g,)
    g = sns.lineplot(x=x, y=y_low, lw=2, ls='--', color='0.5', ax=g,)
    
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


def display_derived_parameters(params):
    """Display derived parameters"""
    # Calculate useful derived parameters
    spacing = 2*np.pi / params['w_0']
    decay_per_period = np.exp(-params['l'] * spacing)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Nucleosome Spacing (bp)", f"{spacing:.1f}")
    with col2:
        st.metric("Decay per Period", f"{decay_per_period:.3f}")
    with col3:
        st.metric("Oscillation Frequency (bp⁻¹)", f"{params['w_0']/(2*np.pi):.4f}")

def main():
    st.title("Curve Playground")
    st.markdown("""
    Adjust the parameters to see how they affect the fitted curve and envelopes.
    Use this playground to understand the relationship between parameters and the resulting curve shape.
    """)
    
    # Get plot defaults
    plot_params = get_plot_defaults()
    
    # Create sidebar for plot range controls
    with st.sidebar:
        st.header("Plot Range")
        col1, col2 = st.columns(2)
        with col1:
            x_min = st.number_input("X Min", value=plot_params['xlim'][0])
            y_min = st.number_input("Y Min", value=plot_params['ylim'][0])
        with col2:
            x_max = st.number_input("X Max", value=plot_params['xlim'][1])
            y_max = st.number_input("Y Max", value=plot_params['ylim'][1])
        
        plot_params['xlim'] = [x_min, x_max]
        plot_params['ylim'] = [y_min, y_max]
    
    # Create two columns for parameters and plot
    col1, col2 = st.columns([1, 2])
    
    # Parameter controls in left column
    with col1:
        st.subheader("Parameters")
        # Check if there's a result_dict in session state
        params = create_parameter_controls(
            st.session_state.get('result_dict', None)
        )
    
    # Plot in right column
    with col2:
        fig = plot_curves(params, plot_params)
        st.pyplot(fig)
    
    # Display derived parameters
    st.subheader("Derived Parameters")
    display_derived_parameters(params)

if __name__ == "__main__":
    main()