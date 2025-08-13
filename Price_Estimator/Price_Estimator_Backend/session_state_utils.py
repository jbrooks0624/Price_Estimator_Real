import streamlit as st

def reset_all():
    # Examine Coil
    st.session_state['examine_skip'] = True
    st.session_state['examine_scrap_percent_check'] = False
    st.session_state['examine_scrap_percent'] = 0.01
    st.session_state['examine_cost_check'] = False
    st.session_state['examine_cost'] = 15.0
    # Trimming
    st.session_state['trimming_skip'] = True
    st.session_state['trimming_width_cropped_check'] = False
    st.session_state['trimming_width_cropped'] = 1.0
    st.session_state['trimming_cost_check'] = False
    st.session_state['trimming_cost'] = 15.0
    # Pickle & Oil
    st.session_state['pickle_skip'] = True
    st.session_state['pickle_scrap_percent_check'] = False
    st.session_state['pickle_scrap_percent'] = 0.01
    st.session_state['pickle_cost_check'] = False
    st.session_state['pickle_cost'] = 15.0
    # Coating
    st.session_state['coating_skip'] = True
    st.session_state['coating_scrap_percent_check'] = False
    st.session_state['coating_scrap_percent'] = 0.01
    st.session_state['coating_cost_check'] = False
    st.session_state['coating_cost'] = 15.0
    # Slitting
    st.session_state['slitting_skip'] = True
    st.session_state['slitting_widths_per_cut'] = [st.session_state['master_coil_width']]
    st.session_state['slitting_num_cuts_needed'] = [1]
    st.session_state['slitting_scrap_percent_check'] = False
    st.session_state['slitting_scrap_percent'] = 0.01
    st.session_state['slitting_width_cropped_check'] = False
    st.session_state['slitting_width_cropped'] = 1.0
    st.session_state['slitting_cost_check'] = False
    st.session_state['slitting_cost'] = 15.0
    # Cut to Length
    st.session_state['cut_skip'] = True
    st.session_state['cut_cost_check'] = False
    st.session_state['cut_cost'] = 15.0
    st.session_state['cut_weight_check'] = False
    st.session_state['cut_weight'] = 150.0
    # Output
    st.session_state['estimate_output'] = ''
    # Storage (between steps)
    st.session_state['storage_start'] = 0.0
    st.session_state['storage_examine'] = 0.0
    st.session_state['storage_trimming'] = 0.0
    st.session_state['storage_pickle'] = 0.0
    st.session_state['storage_coating'] = 0.0
    st.session_state['storage_slitting'] = 0.0
    st.session_state['storage_cut'] = 0.0
    st.session_state['storage_end'] = 0.0
    # Freight (between steps)
    st.session_state['freight_start'] = 0.0
    st.session_state['freight_examine'] = 0.0
    st.session_state['freight_trimming'] = 0.0
    st.session_state['freight_pickle'] = 0.0
    st.session_state['freight_coating'] = 0.0
    st.session_state['freight_slitting'] = 0.0
    st.session_state['freight_cut'] = 0.0
    st.session_state['freight_end'] = 0.0

def reset_master_coil():
    st.session_state['master_coil_width'] = 48.0
    st.session_state['master_coil_weight'] = 40000.0
    st.session_state['master_coil_cost'] = 100.0 