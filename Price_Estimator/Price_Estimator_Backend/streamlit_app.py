import streamlit as st
import io
import sys
import pandas as pd
from main import main
from session_state_utils import reset_all, reset_master_coil
from datetime import datetime
from sidebar_inputs import sidebar_coil_inputs
from state_management import ensure_coils_state, get_default_coil_state
from output_display import display_outputs
# from streamlit_autorefresh import st_autorefresh

# st_autorefresh(interval=3700000, key="keep_alive")

st.set_page_config(page_title='Mainline Metals Price Estimator')
st.title('Mainline Metals Price Estimator')

# Set custom sidebar width
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            min-width: 400px;
            width: 800px;
            max-width: 800px;
        }
        /* Expand main content area and columns */
        .main .block-container {
            max-width: 150vw !important;
            padding-left: 2rem;
            padding-right: 2rem;
        }
        /* Expand columns for Estimate Output by Coil */
        div[data-testid="column"] {
            min-width: 800px !important;
            max-width: 1000px !important;
            flex: 1 1 500px !important;
        }
        /* Horizontally scrollable container for coil outputs */
        .scroll-x-coils {
            overflow-x: auto;
            min-width: 700px;
            width: 100%;
            padding-bottom: 1rem;
        }
        .scroll-x-coils-inner {
            display: flex;
            flex-direction: row;
            min-width: 2200px;
            gap: 2rem;
        }
        .scroll-x-coils .stColumn {
            min-width: 500px !important;
            max-width: 900px !important;
            flex: 1 1 500px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- MAIN APP LOGIC ---
def run_app():
    ensure_coils_state()
    coils = st.session_state['coils']
    st.sidebar.header('Master Coil Info')
    col_add, col_del = st.sidebar.columns([2,1])
    if col_add.button('Add Coil', key='add_coil'):
        coils.append(get_default_coil_state())
        st.rerun()
    if col_del.button('Delete Coil', key='delete_coil', disabled=len(coils) <= 1):
        if len(coils) > 1:
            coils.pop()
            st.rerun()
    for idx, coil in enumerate(coils):
        sidebar_coil_inputs(idx, coil)
        st.sidebar.markdown('---')
    col1, col2 = st.columns([1,1])
    estimate_clicked = col1.button('Estimate Price')
    clear_clicked = col2.button('Clear Estimate')
    if clear_clicked:
        st.session_state['estimate_output'] = ''
    if estimate_clicked:
        all_outputs = []
        all_final_costs = []
        all_selling_prices = []
        for idx, coil in enumerate(coils):
            buffer = io.StringIO()
            sys_stdout = sys.stdout
            sys.stdout = buffer
            try:
                main(
                    coil['master_coil_width'],
                    coil['master_coil_weight'],
                    coil['master_coil_cost'],
                    coil['examine_scrap_percent'] if coil['examine_scrap_percent_check'] and not coil['examine_skip'] else None,
                    coil['examine_cost'] if coil['examine_cost_check'] and not coil['examine_skip'] else None,
                    coil['examine_skip'],
                    coil['trimming_width_cropped'] if coil['trimming_width_cropped_check'] and not coil['trimming_skip'] else None,
                    coil['trimming_cost'] if coil['trimming_cost_check'] and not coil['trimming_skip'] else None,
                    coil['trimming_skip'],
                    coil['pickle_scrap_percent'] if coil['pickle_scrap_percent_check'] and not coil['pickle_skip'] else None,
                    coil['pickle_cost'] if coil['pickle_cost_check'] and not coil['pickle_skip'] else None,
                    coil['pickle_skip'],
                    coil['coating_scrap_percent'] if coil['coating_scrap_percent_check'] and not coil['coating_skip'] else None,
                    coil['coating_cost'] if coil['coating_cost_check'] and not coil['coating_skip'] else None,
                    coil['coating_skip'],
                    coil['slitting_widths_per_cut'] if not coil['slitting_skip'] else None,
                    coil['slitting_num_cuts_needed'] if not coil['slitting_skip'] else None,
                    None,
                    coil['slitting_width_cropped'] if not coil['slitting_skip'] else None,
                    coil['slitting_cost'] if coil['slitting_cost_check'] and not coil['slitting_skip'] else None,
                    coil['slitting_skip'],
                    (coil['cut_percent'] / 100.0) if coil['cut_percent'] and not coil['cut_skip'] else None,
                    coil['cut_cost'] if coil['cut_cost_check'] and not coil['cut_skip'] else None,
                    coil['cut_weight'] if coil['cut_weight_check'] and not coil['cut_skip'] else None,
                    coil['cut_skip'],
                    coil['storage_start'],
                    coil['storage_examine'],
                    coil['storage_trimming'],
                    coil['storage_pickle'],
                    coil['storage_coating'],
                    coil['storage_slitting'],
                    coil['storage_cut'],
                    coil['storage_end'],
                    coil['freight_start'],
                    coil['freight_examine'],
                    coil['freight_trimming'],
                    coil['freight_pickle'],
                    coil['freight_coating'],
                    coil['freight_slitting'],
                    coil['freight_cut'],
                    coil['freight_end'],
                    coil['margin']
                )
            finally:
                sys.stdout = sys_stdout
            output = buffer.getvalue()
            buffer.close()
            all_outputs.append(output)
            # Parse final cost and selling price for averaging
            final_cost = None
            selling_price = None
            for line in output.splitlines():
                if line.startswith('TOTAL COST:'):
                    try:
                        final_cost = float(line.split(':')[1].strip())
                    except:
                        pass
                if line.startswith('SELLING PRICE:'):
                    try:
                        selling_price = float(line.split(':')[1].strip())
                    except:
                        pass
            if final_cost is not None:
                all_final_costs.append(final_cost)
            if selling_price is not None:
                all_selling_prices.append(selling_price)
        st.session_state['estimate_output'] = all_outputs
        st.session_state['final_costs'] = all_final_costs
        st.session_state['selling_prices'] = all_selling_prices
    # Display the estimate output if available
    if st.session_state.get('estimate_output', ''):
        outputs = st.session_state['estimate_output']
        final_costs = st.session_state.get('final_costs', [])
        selling_prices = st.session_state.get('selling_prices', [])
        display_outputs(outputs, final_costs, selling_prices)

run_app()


