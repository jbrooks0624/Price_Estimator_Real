import streamlit as st
from excel_export import build_excel_bytes
from datetime import datetime

def display_outputs(outputs, final_costs, selling_prices):
    if not outputs:
        return
    avg_cost = sum(final_costs) / len(final_costs) if final_costs else 0
    avg_price = sum(selling_prices) / len(selling_prices) if selling_prices else 0
    excel_bytes = build_excel_bytes(final_costs, selling_prices, outputs, avg_cost, avg_price)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # Centered, green, Excel-logo button
    st.markdown("""
        <style>
        .centered-download {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 1.5rem;
        }
        .stDownloadButton>button {
            background-color: #fff !important;
            color: #21a366 !important;
            border-radius: 6px !important;
            border: 2px solid #21a366 !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
            padding: 0.5rem 1.5rem !important;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .centered-title {
            text-align: center;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="centered-download">', unsafe_allow_html=True)
    st.download_button(
        label='Download as Excel',
        data=excel_bytes,
        file_name=f'price_summary_{timestamp}.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        key='download-excel',
        help='Download all coil results as an Excel file.'
    )
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<h3 class="centered-title">FINAL INFORMATION FOR ALL COILS</h3>', unsafe_allow_html=True)
    st.markdown(f"**Average TOTAL COST:** {avg_cost:.4f}")
    st.markdown(f"**Average SELLING PRICE:** {avg_price:.4f}")
    # Show each coil's output side by side
    st.markdown('<h3 class="centered-title">Estimate Output by Coil</h3>', unsafe_allow_html=True)
    st.markdown('<div class="scroll-x-coils"><div class="scroll-x-coils-inner">', unsafe_allow_html=True)
    cols = st.columns(len(outputs))
    for idx, (col, output) in enumerate(zip(cols, outputs)):
        with col:
            with st.container():
                st.markdown(f'### Coil #{idx+1}')
                calc_markers = [
                    ('EXAMINE_COIL_CALC:', 'Show calculation for Examine Coil'),
                    ('TRIMMING_CALC:', 'Show calculation for Trimming'),
                    ('PICKLE_CALC:', 'Show calculation for Pickle & Oil'),
                    ('COATING_CALC:', 'Show calculation for Coating'),
                    ('SLITTING_CALC:', 'Show calculation for Slitting'),
                    ('CUT_CALC:', 'Show calculation for Cut to Length'),
                ]
                calcs = []
                main_output = output
                for marker, label in calc_markers:
                    if marker in main_output:
                        parts = main_output.split(marker, 1)
                        before_calc = parts[0].rstrip()
                        after_calc = parts[1].lstrip()
                        calc_lines = after_calc.splitlines()
                        calc_block = []
                        rest_block = []
                        in_calc = True
                        for line in calc_lines:
                            if in_calc and line.strip() == '':
                                in_calc = False
                                continue
                            if in_calc:
                                calc_block.append(line)
                            else:
                                rest_block.append(line)
                        calc_str = '\n'.join(calc_block)
                        calcs.append((label, calc_str))
                        main_output = before_calc
                        if rest_block:
                            main_output += '\n' + '\n'.join(rest_block)
                        main_output = main_output.strip()
                st.code(main_output, language='text')
                for label, calc_str in calcs:
                    if calc_str:
                        with st.expander(label):
                            st.markdown(f'<span style="font-size: 0.85em;">{calc_str.replace(chr(10), "<br>")}</span>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True) 