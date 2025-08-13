import streamlit as st

def get_default_coil_state():
    return {
        'master_coil_width': 48.0,
        'master_coil_weight': 40000.0,
        'master_coil_cost': 100.0,
        'margin': 15.0,
        # Examine Coil
        'examine_skip': True,
        'examine_scrap_percent_check': False,
        'examine_scrap_percent': 0.01,
        'examine_cost_check': False,
        'examine_cost': 15.0,
        # Trimming
        'trimming_skip': True,
        'trimming_width_cropped_check': False,
        'trimming_width_cropped': 1.0,
        'trimming_cost_check': False,
        'trimming_cost': 15.0,
        # Pickle & Oil
        'pickle_skip': True,
        'pickle_scrap_percent_check': False,
        'pickle_scrap_percent': 0.01,
        'pickle_cost_check': False,
        'pickle_cost': 15.0,
        # Coating
        'coating_skip': True,
        'coating_scrap_percent_check': False,
        'coating_scrap_percent': 0.01,
        'coating_cost_check': False,
        'coating_cost': 15.0,
        # Slitting
        'slitting_skip': True,
        'slitting_widths_per_cut': [48.0],
        'slitting_num_cuts_needed': [1],
        'slitting_scrap_percent_check': False,
        'slitting_scrap_percent': 0.01,
        'slitting_width_cropped_check': False,
        'slitting_width_cropped': 1.0,
        'slitting_cost_check': False,
        'slitting_cost': 15.0,
        # Cut to Length
        'cut_skip': True,
        'cut_cost_check': False,
        'cut_cost': 15.0,
        'cut_weight_check': False,
        'cut_weight': 150.0,
        'cut_percent': 20.0,
        # Storage
        'storage_start': 0.0,
        'storage_examine': 0.0,
        'storage_trimming': 0.0,
        'storage_pickle': 0.0,
        'storage_coating': 0.0,
        'storage_slitting': 0.0,
        'storage_cut': 0.0,
        'storage_end': 0.0,
        # Freight
        'freight_start': 0.0,
        'freight_examine': 0.0,
        'freight_trimming': 0.0,
        'freight_pickle': 0.0,
        'freight_coating': 0.0,
        'freight_slitting': 0.0,
        'freight_cut': 0.0,
        'freight_end': 0.0,
    }

def ensure_coils_state():
    if 'coils' not in st.session_state or not st.session_state['coils']:
        st.session_state['coils'] = [get_default_coil_state()] 