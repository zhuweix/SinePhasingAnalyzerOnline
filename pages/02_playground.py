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
        # Default values if no result_dict provided
        return {
            'A': st.slider('Amplitude', 0.0, 2.0, 1.0, 0.1),
            'decay': st.slider('Decay (per kb)', 0.001, 0.02, 0.01, 0.001),
            'space': st.slider('Spacing (bp)', 100, 200, 140, ),
            'theta_0': st.slider('Phase (θ₀)', -np.pi, np.pi, -np.pi/2, 0.1),
            'b': st.slider('b0 ', -1.0, 1.0, 0.0, 0.1),
            's': st.slider('Slope (per kb)', -0.05, 0.05, 0.0, 0.01)
        }
    else:
        # Use values from result_dict as defaults
        popt = result_dict['fit_params']
        return {
            'A': st.slider('Amplitude (A)', 0.0, 2.0, float(popt[0]), 0.1),
            'l': st.slider('Decay Length (l)', 0.001, 0.02, float(popt[1]), 0.001),
            'w_0': st.slider('Angular Frequency (w_0)', 0.01, 0.1, float(popt[2]), 0.001),
            'theta_0': st.slider('Phase (θ₀)', -np.pi, np.pi, float(popt[3]), 0.1),
            'b': st.slider('Baseline (b)', -1.0, 1.0, float(popt[4]), 0.1),
            's': st.slider('Slope (s)', -0.001, 0.001, float(popt[5]), 0.0001)
        }

def plot_curves(params, plot_params):
    """Create plot with current parameters"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Generate x values
    x = np.linspace(plot_params['xlim'][0], plot_params['xlim'][1], 1000)
    
    # Calculate curves
    y_fit = fit_function(x, params['A'], params['l'], params['w_0'], 
                        params['theta_0'], params['b'], params['s'])
    y_high = upper_function(x, params['A'], params['l'], params['b'], params['s'])
    y_low = lower_function(x, params['A'], params['l'], params['b'], params['s'])
    
    # Plot curves
    plt.plot(x, y_fit, 'r-', label='Fitted Curve', lw=2)
    plt.plot(x, y_high, '--', color='0.7', label='Envelope')
    plt.plot(x, y_low, '--', color='0.7')
    
    # Set plot parameters
    plt.xlabel(plot_params['xlabel'])
    plt.ylabel(plot_params['ylabel'])
    plt.title('Interactive Curve Visualization')
    plt.xlim(plot_params['xlim'])
    plt.ylim(plot_params['ylim'])
    plt.grid(True, alpha=0.3)
    plt.legend()
    
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