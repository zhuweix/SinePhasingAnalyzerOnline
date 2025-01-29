import pandas as pd
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import streamlit as st

def fit_function(x, A, l, w_0, theta_0, b, s):
    """
    Define the sine wave fitting function with exponential decay
    
    Parameters:
    -----------
    x : array-like
        Input positions
    A : float
        Amplitude
    l : float
        Decay constant
    w_0 : float
        Angular frequency
    theta_0 : float
        Phase offset
    b : float
        Baseline
    s : float
        Slope
    """
    return A * np.exp(-l * x) * np.sin(w_0 * x + theta_0) + b + s*x

def upper_function(x, A, l, b, s):
    """
    Define the upper envelope function
    """
    return A * np.exp(-l * x) + b + s*x

def lower_function(x, A, l, b, s):
    """
    Define the lower envelope function
    """
    return -A * np.exp(-l * x) + b + s*x

def calc_sine_fit(y, xpos):
    """
    Calculate sine wave fit parameters and statistics
    
    Parameters:
    -----------
    y : array-like
        Input y values
    xpos : array-like
        Input x positions
    
    Returns:
    --------
    dict
        Dictionary containing fit parameters and statistics
    """
    # Initial parameter guesses
    max_a = np.max(y) * 1.1
    guess_w_0 = 2*np.pi / 160
    guess_theta_0 = -np.pi/2
    guess_b = np.mean(y)
    initial_guess = [max_a, 1/160, guess_w_0, guess_theta_0, guess_b, 0]
    
    # Perform curve fitting
    try:
        popt, pcov = curve_fit(fit_function, xpos, y, p0=initial_guess)
        y_fit = fit_function(xpos, *popt)
        
        # Extract parameters
        _, l_fit, w_0_fit, theta0_fit, _, _ = popt
        
        # Calculate statistics
        spacing = 2*np.pi / w_0_fit
        sst = np.sum((y-np.mean(y))**2)
        ssr = np.sum((y-y_fit)**2)
        r2 = 1 - ssr/sst
        adj_r2 = 1 - (1-r2)*(len(y)-1)/(len(y)-len(initial_guess)-1)
        decay = np.exp(-l_fit * spacing)
        
        # Calculate errors
        perr = np.sqrt(np.diag(pcov))
        s_fit = popt[-1] * 1000
        A_fit = popt[0]
        b_fit = popt[-2]
        adj_mean = np.mean(y_fit)
        err_A = perr[0]
        err_s = perr[-1]*1000
        err_w0 = perr[2]
        err_spacing = 2*np.pi / (w_0_fit**2)*err_w0
        
        # Compile results
        result = {
            'Adj.R2': adj_r2,
            'Spacing': spacing,
            'Error_spacing': err_spacing,
            'Adj.Mean': adj_mean,
            'Amplitude': A_fit,
            'Error_Amp': err_A,
            'Slope': s_fit,
            'Error_Slope': err_s,
            'Decay': decay,
            'b0': b_fit,
            'theta0': theta0_fit,
            'fit_params': popt,
            'fit_errors': perr
        }
        return result
    
    except Exception as e:
        st.error(f"Fitting failed: {str(e)}")
        return None

def process_data(df: pd.DataFrame, xmin: int=-50, xmax: int=1000):
    """
    Process the DataFrame for phasing analysis
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataframe containing methylation data
        Must have columns: 'Pos', 'Value'
    xmin : int
        Minimum x value to include in analysis
    xmax : int
        Maximum x value to include in analysis
        
    Returns:
    --------
    tuple
        (processed_dataframe, result_dictionary)
    """
    # Ensure required columns exist
    required_columns = ['Pos', 'Value']
    if not all(col in df.columns for col in required_columns):
        st.error("CSV must contain columns: 'Pos', 'Value'")
        return None
    
    try:
        # Process data
        df['Pos'] = df['Pos'].values.astype(int)
        df = df.loc[(df['Pos'] >= xmin) & (df['Pos'] <= xmax)]
        df.sort_values(by='Pos', inplace=True)
        
        # Perform fitting
        ydata = df['Value'].values
        xdata = df['Pos'].values
        result_dict = calc_sine_fit(ydata, xdata)
        
        return df, result_dict
    
    except Exception as e:
        st.error(f"Data processing failed: {str(e)}")
        return None, None

def get_plot_defaults():
    """
    Return default plot parameters
    """
    return {
        'title': 'Phasing Analysis',
        'xlabel': 'Relative to +1 Nucleosome (bp)',
        'ylabel': 'Relative Methylation Rate',
        'location_range': [-50, 1000],
        'xlim': [-50, 1000],
        'ylim': [0, 2],  
        'xticks': np.arange(0, 1001, 200),
        'yticks': np.arange(-2, 2.1, 0.5)
    }