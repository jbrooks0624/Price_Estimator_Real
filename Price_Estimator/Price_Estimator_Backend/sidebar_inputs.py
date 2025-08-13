import streamlit as st

def sidebar_coil_inputs(coil_idx, coil_state):
    st.sidebar.markdown(f"### Coil #{coil_idx+1}")
    # Master Coil Info
    coil_state['master_coil_width'] = st.sidebar.number_input(f'Master Coil Width #{coil_idx+1}', min_value=0.0, value=coil_state['master_coil_width'], step=1.0, format="%.4f", key=f'master_coil_width_{coil_idx}')
    coil_state['master_coil_weight'] = st.sidebar.number_input(f'Master Coil Weight #{coil_idx+1}', min_value=0.0, value=coil_state['master_coil_weight'], step=1.0, key=f'master_coil_weight_{coil_idx}')
    coil_state['master_coil_cost'] = st.sidebar.number_input(f'Master Coil Cost #{coil_idx+1}', min_value=0.0, value=coil_state['master_coil_cost'], step=1.0, format="%.4f", key=f'master_coil_cost_{coil_idx}')
    coil_state['margin'] = st.sidebar.number_input(f'Margin (%) #{coil_idx+1}', min_value=0.0, value=coil_state['margin'], step=0.1, key=f'margin_{coil_idx}')
    # Value Added Processes
    with st.sidebar.expander(f'Examine Coil #{coil_idx+1} (optional)'):
        coil_state['examine_skip'] = st.checkbox(f'Skip Examine Coil #{coil_idx+1}', key=f'examine_skip_{coil_idx}', value=coil_state['examine_skip'])
        coil_state['examine_scrap_percent_check'] = st.checkbox(f'Set Scrap Percent (default: 0.01) #{coil_idx+1}', disabled=coil_state['examine_skip'], key=f'examine_scrap_percent_check_{coil_idx}', value=coil_state['examine_scrap_percent_check'])
        if coil_state['examine_scrap_percent_check'] and not coil_state['examine_skip']:
            coil_state['examine_scrap_percent'] = st.number_input(f'Examine Coil Scrap Percent #{coil_idx+1}', min_value=0.0, max_value=1.0, value=coil_state['examine_scrap_percent'], step=0.01, format="%.4f", disabled=coil_state['examine_skip'], key=f'examine_scrap_percent_{coil_idx}')
        coil_state['examine_cost_check'] = st.checkbox(f'Set Examine Coil Cost (default: 25) #{coil_idx+1}', disabled=coil_state['examine_skip'], key=f'examine_cost_check_{coil_idx}', value=coil_state['examine_cost_check'])
        if coil_state['examine_cost_check'] and not coil_state['examine_skip']:
            coil_state['examine_cost'] = st.number_input(f'Examine Coil Cost #{coil_idx+1}', min_value=0.0, value=coil_state['examine_cost'], step=1.0, format="%.4f", disabled=coil_state['examine_skip'], key=f'examine_cost_{coil_idx}')
    with st.sidebar.expander(f'Trimming #{coil_idx+1} (optional)'):
        coil_state['trimming_skip'] = st.checkbox(f'Skip Trimming #{coil_idx+1}', key=f'trimming_skip_{coil_idx}', value=coil_state['trimming_skip'])
        coil_state['trimming_width_cropped_check'] = st.checkbox(f'Set Final Width After Trimming (default: {coil_state["master_coil_width"] - 1.0:.4f}) #{coil_idx+1}', disabled=coil_state['trimming_skip'], key=f'trimming_width_cropped_check_{coil_idx}', value=coil_state['trimming_width_cropped_check'])
        if coil_state['trimming_width_cropped_check'] and not coil_state['trimming_skip']:
            final_width_input = st.number_input(f'Final Width After Trimming #{coil_idx+1}', min_value=0.0, value=(coil_state['master_coil_width'] - coil_state['trimming_width_cropped']), step=0.01, format="%.4f", disabled=coil_state['trimming_skip'], key=f'trimming_final_width_{coil_idx}')
            # Validation: final width cannot exceed master width
            if final_width_input > coil_state['master_coil_width']:
                st.error(f"Final width ({final_width_input}) exceeds master coil width ({coil_state['master_coil_width']}).")
            width_cropped_calc = coil_state['master_coil_width'] - final_width_input
            coil_state['trimming_width_cropped'] = round(width_cropped_calc, 4)
        coil_state['trimming_cost_check'] = st.checkbox(f'Set Trimming Cost (default: 25) #{coil_idx+1}', disabled=coil_state['trimming_skip'], key=f'trimming_cost_check_{coil_idx}', value=coil_state['trimming_cost_check'])
        if coil_state['trimming_cost_check'] and not coil_state['trimming_skip']:
            coil_state['trimming_cost'] = st.number_input(f'Trimming Cost #{coil_idx+1}', min_value=0.0, value=coil_state['trimming_cost'], step=1.0, format="%.4f", disabled=coil_state['trimming_skip'], key=f'trimming_cost_{coil_idx}')
    with st.sidebar.expander(f'Pickle & Oil #{coil_idx+1} (optional)'):
        coil_state['pickle_skip'] = st.checkbox(f'Skip Pickle & Oil #{coil_idx+1}', key=f'pickle_skip_{coil_idx}', value=coil_state['pickle_skip'])
        coil_state['pickle_scrap_percent_check'] = st.checkbox(f'Set Scrap Percent (default: 0.01) #{coil_idx+1}', disabled=coil_state['pickle_skip'], key=f'pickle_scrap_percent_check_{coil_idx}', value=coil_state['pickle_scrap_percent_check'])
        if coil_state['pickle_scrap_percent_check'] and not coil_state['pickle_skip']:
            coil_state['pickle_scrap_percent'] = st.number_input(f'Pickle & Oil Scrap Percent #{coil_idx+1}', min_value=0.0, max_value=1.0, value=coil_state['pickle_scrap_percent'], step=0.01, format="%.4f", disabled=coil_state['pickle_skip'], key=f'pickle_scrap_percent_{coil_idx}')
        coil_state['pickle_cost_check'] = st.checkbox(f'Set Pickle & Oil Cost (default: 25) #{coil_idx+1}', disabled=coil_state['pickle_skip'], key=f'pickle_cost_check_{coil_idx}', value=coil_state['pickle_cost_check'])
        if coil_state['pickle_cost_check'] and not coil_state['pickle_skip']:
            coil_state['pickle_cost'] = st.number_input(f'Pickle & Oil Cost #{coil_idx+1}', min_value=0.0, value=coil_state['pickle_cost'], step=1.0, format="%.4f", disabled=coil_state['pickle_skip'], key=f'pickle_cost_{coil_idx}')
    with st.sidebar.expander(f'Coating #{coil_idx+1} (optional)'):
        coil_state['coating_skip'] = st.checkbox(f'Skip Coating #{coil_idx+1}', key=f'coating_skip_{coil_idx}', value=coil_state['coating_skip'])
        coil_state['coating_scrap_percent_check'] = st.checkbox(f'Set Scrap Percent (default: 0.01) #{coil_idx+1}', disabled=coil_state['coating_skip'], key=f'coating_scrap_percent_check_{coil_idx}', value=coil_state['coating_scrap_percent_check'])
        if coil_state['coating_scrap_percent_check'] and not coil_state['coating_skip']:
            coil_state['coating_scrap_percent'] = st.number_input(f'Coating Scrap Percent #{coil_idx+1}', min_value=0.0, max_value=1.0, value=coil_state['coating_scrap_percent'], step=0.01, format="%.4f", disabled=coil_state['coating_skip'], key=f'coating_scrap_percent_{coil_idx}')
        coil_state['coating_cost_check'] = st.checkbox(f'Set Coating Cost (default: 25) #{coil_idx+1}', disabled=coil_state['coating_skip'], key=f'coating_cost_check_{coil_idx}', value=coil_state['coating_cost_check'])
        if coil_state['coating_cost_check'] and not coil_state['coating_skip']:
            coil_state['coating_cost'] = st.number_input(f'Coating Cost #{coil_idx+1}', min_value=0.0, value=coil_state['coating_cost'], step=1.0, format="%.4f", disabled=coil_state['coating_skip'], key=f'coating_cost_{coil_idx}')
    with st.sidebar.expander(f'Slitting #{coil_idx+1} (optional)'):
        coil_state['slitting_skip'] = st.checkbox(f'Skip Slitting #{coil_idx+1}', key=f'slitting_skip_{coil_idx}', value=coil_state['slitting_skip'])
        if f'slitting_widths_per_cut_{coil_idx}' not in st.session_state:
            st.session_state[f'slitting_widths_per_cut_{coil_idx}'] = coil_state['slitting_widths_per_cut']
        if f'slitting_num_cuts_needed_{coil_idx}' not in st.session_state:
            st.session_state[f'slitting_num_cuts_needed_{coil_idx}'] = coil_state['slitting_num_cuts_needed']
        widths_per_cut = st.session_state[f'slitting_widths_per_cut_{coil_idx}']
        num_cuts_needed = st.session_state[f'slitting_num_cuts_needed_{coil_idx}']
        st.markdown('**Cuts**')
        total_width = sum(widths_per_cut)
        over_width = total_width > coil_state['master_coil_width']
        for i in range(len(widths_per_cut)):
            cols = st.columns([3, 3, 1])
            with cols[0]:
                if over_width:
                    widths_per_cut[i] = st.number_input(f'Width per Cut #{i+1} (Coil {coil_idx+1})', min_value=0.0, value=widths_per_cut[i], step=0.01, key=f'slitting_width_per_cut_{coil_idx}_{i}', disabled=coil_state['slitting_skip'], format="%.4f", help='Sum of widths exceeds master coil width', label_visibility='visible')
                    st.markdown(f'<style>div[data-testid="stNumberInput"][aria-label="Width per Cut #{i+1} (Coil {coil_idx+1})"] input {{background-color: #ffcccc !important;}}</style>', unsafe_allow_html=True)
                else:
                    widths_per_cut[i] = st.number_input(f'Width per Cut #{i+1} (Coil {coil_idx+1})', min_value=0.0, value=widths_per_cut[i], step=0.01, key=f'slitting_width_per_cut_{coil_idx}_{i}', disabled=coil_state['slitting_skip'], format="%.4f")
            with cols[1]:
                num_cuts_needed[i] = st.number_input(f'Num Cuts #{i+1} (Coil {coil_idx+1})/n', min_value=1, value=num_cuts_needed[i], step=1, key=f'slitting_num_cuts_needed_{coil_idx}_{i}', disabled=coil_state['slitting_skip'])
            with cols[2]:
                st.markdown("<br>", unsafe_allow_html=True)
                delete_clicked = st.button('➖', key=f'delete_cut_{coil_idx}_{i}', disabled=coil_state['slitting_skip'] or len(widths_per_cut) <= 1, help='Delete this cut')
                add_clicked = False
                if i == len(widths_per_cut) - 1 and len(widths_per_cut) < 10:
                    add_clicked = st.button('➕', key=f'add_cut_{coil_idx}_{i}', disabled=coil_state['slitting_skip'], help='Add another cut')
                if delete_clicked:
                    widths_per_cut.pop(i)
                    num_cuts_needed.pop(i)
                    st.rerun()
                if add_clicked:
                    widths_per_cut.append(10.0)
                    num_cuts_needed.append(1)
                    st.rerun()
        st.session_state[f'slitting_widths_per_cut_{coil_idx}'] = widths_per_cut
        st.session_state[f'slitting_num_cuts_needed_{coil_idx}'] = num_cuts_needed
        coil_state['slitting_widths_per_cut'] = widths_per_cut
        coil_state['slitting_num_cuts_needed'] = num_cuts_needed
        if over_width:
            st.error(f"Sum of widths per cut ({total_width}) exceeds master coil width ({coil_state['master_coil_width']})!")
        st.markdown(f"**Width Cropped (from Trimming):** {coil_state['trimming_width_cropped'] if coil_state['trimming_width_cropped_check'] and not coil_state['trimming_skip'] else 0.0}")
        coil_state['slitting_width_cropped'] = coil_state['trimming_width_cropped'] if coil_state['trimming_width_cropped_check'] and not coil_state['trimming_skip'] else 0.0
        coil_state['slitting_cost_check'] = st.checkbox(f'Set Slitting Cost (default: 25) #{coil_idx+1}', disabled=coil_state['slitting_skip'], key=f'slitting_cost_check_{coil_idx}', value=coil_state['slitting_cost_check'])
        if coil_state['slitting_cost_check'] and not coil_state['slitting_skip']:
            coil_state['slitting_cost'] = st.number_input(f'Slitting Cost #{coil_idx+1}', min_value=0.0, value=coil_state['slitting_cost'], step=1.0, format="%.4f", disabled=coil_state['slitting_skip'], key=f'slitting_cost_{coil_idx}')
    with st.sidebar.expander(f'Cut to Length #{coil_idx+1} (optional)'):
        coil_state['cut_skip'] = st.checkbox(f'Skip Cut to Length #{coil_idx+1}', key=f'cut_skip_{coil_idx}', value=coil_state['cut_skip'])
        coil_state['cut_percent'] = st.number_input(f'Cut to Length Percent (e.g. 10 for 10%) #{coil_idx+1}', min_value=0.01, max_value=100.0, value=coil_state['cut_percent'], step=0.01, disabled=coil_state['cut_skip'], key=f'cut_percent_{coil_idx}')
        coil_state['cut_cost_check'] = st.checkbox(f'Set Cut Cost (default: 25) #{coil_idx+1}', disabled=coil_state['cut_skip'], key=f'cut_cost_check_{coil_idx}', value=coil_state['cut_cost_check'])
        if coil_state['cut_cost_check'] and not coil_state['cut_skip']:
            coil_state['cut_cost'] = st.number_input(f'Cut to Length Cost #{coil_idx+1}', min_value=0.0, value=coil_state['cut_cost'], step=1.0, format="%.4f", disabled=coil_state['cut_skip'], key=f'cut_cost_{coil_idx}')
        coil_state['cut_weight_check'] = st.checkbox(f'Set Cut Scrap Weight (default: 150) #{coil_idx+1}', disabled=coil_state['cut_skip'], key=f'cut_weight_check_{coil_idx}', value=coil_state['cut_weight_check'])
        if coil_state['cut_weight_check'] and not coil_state['cut_skip']:
            coil_state['cut_weight'] = st.number_input(f'Cut to Length Scrap Weight #{coil_idx+1}', min_value=0.0, value=coil_state['cut_weight'], step=1.0, disabled=coil_state['cut_skip'], key=f'cut_weight_{coil_idx}')
    # Storage
    st.sidebar.header(f'Storage Costs (per step) #{coil_idx+1}')
    coil_state['storage_start'] = st.sidebar.number_input(f'Storage at Start #{coil_idx+1}', min_value=0.0, value=coil_state['storage_start'], step=0.01, format="%.4f", key=f'storage_start_{coil_idx}')
    coil_state['storage_examine'] = st.sidebar.number_input(f'Storage after Examine #{coil_idx+1}', min_value=0.0, value=coil_state['storage_examine'], step=0.01, format="%.4f", key=f'storage_examine_{coil_idx}')
    coil_state['storage_trimming'] = st.sidebar.number_input(f'Storage after Trimming #{coil_idx+1}', min_value=0.0, value=coil_state['storage_trimming'], step=0.01, format="%.4f", key=f'storage_trimming_{coil_idx}')
    coil_state['storage_pickle'] = st.sidebar.number_input(f'Storage after Pickle & Oil #{coil_idx+1}', min_value=0.0, value=coil_state['storage_pickle'], step=0.01, format="%.4f", key=f'storage_pickle_{coil_idx}')
    coil_state['storage_coating'] = st.sidebar.number_input(f'Storage after Coating #{coil_idx+1}', min_value=0.0, value=coil_state['storage_coating'], step=0.01, format="%.4f", key=f'storage_coating_{coil_idx}')
    coil_state['storage_slitting'] = st.sidebar.number_input(f'Storage after Slitting #{coil_idx+1}', min_value=0.0, value=coil_state['storage_slitting'], step=0.01, format="%.4f", key=f'storage_slitting_{coil_idx}')
    coil_state['storage_cut'] = st.sidebar.number_input(f'Storage after Cut to Length #{coil_idx+1}', min_value=0.0, value=coil_state['storage_cut'], step=0.01, format="%.4f", key=f'storage_cut_{coil_idx}')
    coil_state['storage_end'] = st.sidebar.number_input(f'Storage at End #{coil_idx+1}', min_value=0.0, value=coil_state['storage_end'], step=0.01, format="%.4f", key=f'storage_end_{coil_idx}')
    # Freight
    st.sidebar.header(f'Freight Costs (per step) #{coil_idx+1}')
    coil_state['freight_start'] = st.sidebar.number_input(f'Freight at Start #{coil_idx+1}', min_value=0.0, value=coil_state['freight_start'], step=1.0, format="%.4f", key=f'freight_start_{coil_idx}')
    coil_state['freight_examine'] = st.sidebar.number_input(f'Freight after Examine #{coil_idx+1}', min_value=0.0, value=coil_state['freight_examine'], step=1.0, format="%.4f", key=f'freight_examine_{coil_idx}')
    coil_state['freight_trimming'] = st.sidebar.number_input(f'Freight after Trimming #{coil_idx+1}', min_value=0.0, value=coil_state['freight_trimming'], step=1.0, format="%.4f", key=f'freight_trimming_{coil_idx}')
    coil_state['freight_pickle'] = st.sidebar.number_input(f'Freight after Pickle & Oil #{coil_idx+1}', min_value=0.0, value=coil_state['freight_pickle'], step=1.0, format="%.4f", key=f'freight_pickle_{coil_idx}')
    coil_state['freight_coating'] = st.sidebar.number_input(f'Freight after Coating #{coil_idx+1}', min_value=0.0, value=coil_state['freight_coating'], step=1.0, format="%.4f", key=f'freight_coating_{coil_idx}')
    coil_state['freight_slitting'] = st.sidebar.number_input(f'Freight after Slitting #{coil_idx+1}', min_value=0.0, value=coil_state['freight_slitting'], step=1.0, format="%.4f", key=f'freight_slitting_{coil_idx}')
    coil_state['freight_cut'] = st.sidebar.number_input(f'Freight after Cut to Length #{coil_idx+1}', min_value=0.0, value=coil_state['freight_cut'], step=1.0, format="%.4f", key=f'freight_cut_{coil_idx}')
    coil_state['freight_end'] = st.sidebar.number_input(f'Freight at End #{coil_idx+1}', min_value=0.0, value=coil_state['freight_end'], step=1.0, format="%.4f", key=f'freight_end_{coil_idx}') 