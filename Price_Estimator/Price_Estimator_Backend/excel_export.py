import pandas as pd
import io
from datetime import datetime

def build_excel_bytes(final_costs, selling_prices, outputs, avg_cost, avg_price):
    data = {
        'Coil #': [f'Coil #{i+1}' for i in range(len(final_costs))],
        'Total Cost': final_costs,
        'Selling Price': selling_prices,
    }
    df = pd.DataFrame(data)
    avg_row = pd.DataFrame({'Coil #': ['AVERAGE'], 'Total Cost': [avg_cost], 'Selling Price': [avg_price]})
    df = pd.concat([df, avg_row], ignore_index=True)
    # Each coil in its own sheet, only main output (no calculations), with bolded process titles and blank rows between processes
    coil_sheets = {}
    process_titles = [
        '--- EXAMINE COIL ---',
        '--- TRIMMING ---',
        '--- PICKLE & OIL ---',
        '--- COATING ---',
        '--- SLITTING ---',
        '--- CUT TO LENGTH ---',
    ]
    for i, output in enumerate(outputs):
        main_output = output
        # Remove calculation blocks
        calc_markers = [
            'EXAMINE_COIL_CALC:',
            'TRIMMING_CALC:',
            'PICKLE_CALC:',
            'COATING_CALC:',
            'SLITTING_CALC:',
            'CUT_CALC:',
        ]
        for marker in calc_markers:
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
                main_output = before_calc
                if rest_block:
                    main_output += '\n' + '\n'.join(rest_block)
                main_output = main_output.strip()
        # Build rows, bold process titles, add blank row after each process
        lines = [l for l in main_output.splitlines() if l.strip()]
        rows = []
        for idx, line in enumerate(lines):
            is_title = line.strip().upper() in process_titles
            rows.append({'Output': line, 'Bold': is_title})
            # If this is a process title, add the next lines until the next process title or end, then add a blank row
            if is_title:
                # Find where the next process title is
                j = idx + 1
                while j < len(lines) and lines[j].strip().upper() not in process_titles:
                    rows.append({'Output': lines[j], 'Bold': False})
                    j += 1
                rows.append({'Output': '', 'Bold': False})  # blank row
        # Remove duplicate lines (since we add lines in the inner loop)
        seen = set()
        unique_rows = []
        for row in rows:
            key = (row['Output'], row['Bold'])
            if key not in seen:
                unique_rows.append(row)
                seen.add(key)
        # Only keep the Output column for Excel, but keep bold info for formatting
        coil_sheets[f'Coil {i+1}'] = pd.DataFrame(unique_rows)
    output_buffer = io.BytesIO()
    with pd.ExcelWriter(output_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Summary')
        for sheet_name, sheet_df in coil_sheets.items():
            # Write only the Output column
            sheet_df[['Output']].to_excel(writer, index=False, sheet_name=sheet_name)
            # Bold process titles and add blank rows
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            bold_format = workbook.add_format({'bold': True})
            for idx, val in enumerate(sheet_df['Bold']):
                if val:
                    worksheet.set_row(idx + 1, None, bold_format)  # +1 for header
    output_buffer.seek(0)
    return output_buffer 