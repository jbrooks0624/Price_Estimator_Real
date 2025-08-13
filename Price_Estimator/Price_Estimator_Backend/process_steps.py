from value_added_processes import *


def process_examine_coil(master_coil_weight, examine_coil_scrap_percent, examine_coil_cost, skip_examine_coil):
    if skip_examine_coil:
        print('EXAMINE COIL: SKIPPED\n\n\n')
        return 0, 0, ''
    kwargs = {}
    scrap_percent = examine_coil_scrap_percent if examine_coil_scrap_percent is not None else 0.01
    cost = examine_coil_cost if examine_coil_cost is not None else 15.0
    if examine_coil_scrap_percent is not None:
        kwargs['scrap_percent'] = examine_coil_scrap_percent
    if examine_coil_cost is not None:
        kwargs['cost'] = examine_coil_cost
    examine_coil_cost_val, examine_coil_scrap = examine_coil(master_coil_weight, **kwargs)
    print(f'COST TO EXAMINE COIL: {examine_coil_cost_val:.4f}\nSCRAP WEIGHT: {int(round(examine_coil_scrap))}\n\n\n')
    calc_str = f"scrap_weight = master_coil_weight * scrap_percent\n    = {master_coil_weight} * {scrap_percent}\n    = {master_coil_weight * scrap_percent}"
    print(f"EXAMINE_COIL_CALC:\n{calc_str}\n")
    return examine_coil_cost_val, examine_coil_scrap, calc_str


def process_trimming(examine_coil_scrap, master_coil_weight, master_coil_width, trimming_width_cropped, trimming_cost, skip_trimming):
    if skip_trimming:
        print('TRIMMING: SKIPPED\n\n\n')
        return 0, 0, ''
    kwargs = {}
    width_cropped = trimming_width_cropped if trimming_width_cropped is not None else 1.0
    cost = trimming_cost if trimming_cost is not None else 15.0
    if trimming_width_cropped is not None:
        kwargs['width_cropped'] = trimming_width_cropped
    if trimming_cost is not None:
        kwargs['cost'] = trimming_cost
    trimming_cost_val, trimming_scrap = trimmming(examine_coil_scrap, master_coil_weight, master_coil_width, **kwargs)
    print(f'COST TO TRIM: {trimming_cost_val:.4f}\nSCRAP WEIGHT: {int(round(trimming_scrap))}\n\n\n')
    calc_str = f"scrap_percent = width_cropped / master_coil_width\n    = {width_cropped} / {master_coil_width}\n    = {width_cropped/master_coil_width}\nscrap_weight = (master_coil_weight - examine_coil_scrap) * scrap_percent\n    = ({master_coil_weight} - {examine_coil_scrap}) * {width_cropped/master_coil_width}\n    = {(master_coil_weight - examine_coil_scrap) * (width_cropped/master_coil_width)}"
    print(f"TRIMMING_CALC:\n{calc_str}\n")
    return trimming_cost_val, trimming_scrap, calc_str


def process_pickle(master_coil_weight, examine_coil_scrap, trimming_scrap, pickle_scrap_percent, pickle_cost, skip_pickle):
    if skip_pickle:
        print('PICKLE & OIL: SKIPPED\n\n\n')
        return 0, 0, ''
    kwargs = {}
    scrap_percent = pickle_scrap_percent if pickle_scrap_percent is not None else 0.01
    cost = pickle_cost if pickle_cost is not None else 15.0
    if pickle_scrap_percent is not None:
        kwargs['scrap_percent'] = pickle_scrap_percent
    if pickle_cost is not None:
        kwargs['cost'] = pickle_cost
    pickle_cost_val, pickle_scrap = pickle_and_oil(master_coil_weight, examine_coil_scrap, trimming_scrap, **kwargs)
    print(f'COST TO PICKLE & OIL: {pickle_cost_val:.4f}\nSCRAP WEIGHT: {int(round(pickle_scrap))}\n\n\n')
    calc_str = f"scrap_weight = (master_coil_weight - examine_coil_scrap - trimming_scrap) * scrap_percent\n    = ({master_coil_weight} - {examine_coil_scrap} - {trimming_scrap}) * {scrap_percent}\n    = {(master_coil_weight - examine_coil_scrap - trimming_scrap) * scrap_percent}"
    print(f"PICKLE_CALC:\n{calc_str}\n")
    return pickle_cost_val, pickle_scrap, calc_str


def process_coating(master_coil_weight, examine_coil_scrap, trimming_scrap, pickle_scrap, coating_scrap_percent, coating_cost, skip_coating):
    if skip_coating:
        print('COATING: SKIPPED\n\n\n')
        return 0, 0, ''
    kwargs = {}
    scrap_percent = coating_scrap_percent if coating_scrap_percent is not None else 0.01
    cost = coating_cost if coating_cost is not None else 15.0
    if coating_scrap_percent is not None:
        kwargs['scrap_percent'] = coating_scrap_percent
    if coating_cost is not None:
        kwargs['cost'] = coating_cost
    coating_cost_val, coating_weight = coating(master_coil_weight, examine_coil_scrap, trimming_scrap, pickle_scrap, **kwargs)
    print(f'COST TO COAT: {coating_cost_val:.4f}\nSCRAP WEIGHT: {int(round(coating_weight))}\n\n\n')
    calc_str = f"scrap_weight = (master_coil_weight - examine_coil_scrap - trimming_scrap - pickle_scrap) * scrap_percent\n    = ({master_coil_weight} - {examine_coil_scrap} - {trimming_scrap} - {pickle_scrap}) * {scrap_percent}\n    = {(master_coil_weight - examine_coil_scrap - trimming_scrap - pickle_scrap) * scrap_percent}"
    print(f"COATING_CALC:\n{calc_str}\n")
    return coating_cost_val, coating_weight, calc_str


def process_slitting(master_coil_width, master_coil_weight, examine_coil_scrap, trimming_scrap, pickle_scrap, coating_weight, widths_per_cut, skip_widths_per_cut, num_cuts_needed, skip_num_cuts_needed, slitting_scrap_percent, slitting_width_cropped, slitting_cost, skip_slitting, trimming_width_cropped, trimming_skip):   
    if skip_slitting:
        print('SLITTING: SKIPPED\n\n\n')
        return 0, 0, ''
    kwargs = {}
    if trimming_skip:
        trimming_width_cropped = 0
    else:
        trimming_width_cropped = master_coil_width - trimming_width_cropped 
    num_cuts_needed = num_cuts_needed if num_cuts_needed is not None else [1]
    width_cropped = slitting_width_cropped if slitting_width_cropped is not None else 1.0
    slitting_cost = 15.0 if slitting_cost is False else slitting_cost
    kwargs['width_cropped'] = trimming_width_cropped
    if slitting_cost is not None:
        kwargs['cost'] = slitting_cost
    slitting_cost_val, slitting_weight = slitting_v2(master_coil_width, master_coil_weight, examine_coil_scrap, trimming_scrap, pickle_scrap, coating_weight, widths_per_cut, num_cuts_needed, **kwargs)
    print(f'COST TO SLIT: {slitting_cost_val:.4f}\nSCRAP WEIGHT: {int(round(slitting_weight))}\n\n\n')
    updated_weight = master_coil_weight - examine_coil_scrap - trimming_scrap - pickle_scrap - coating_weight
    used_weight = sum(((w * nc)/(master_coil_width - width_cropped)) * updated_weight for w, nc in zip(widths_per_cut, num_cuts_needed))
    calc_str = f"updated_weight = master_coil_weight - examine_coil_scrap - trimming_scrap - pickle_scrap - coating_weight\n    = {master_coil_weight} - {examine_coil_scrap} - {trimming_scrap} - {pickle_scrap} - {coating_weight}\n    = {updated_weight}\nused_weight = sum(((w * nc)/({master_coil_width} - {width_cropped})) * updated_weight for w, nc in zip({widths_per_cut}, {num_cuts_needed}))\n    = {used_weight}\nscrap_weight = updated_weight - used_weight\n    = {updated_weight} - {used_weight}"
    print(f"SLITTING_CALC:\n{calc_str}\n")
    return slitting_cost_val, slitting_weight, calc_str


def process_cut(cut_percent, widths_per_cut, num_cuts_needed, total_weight, master_coil_width, skip_cut, cut_cost = 15.0):
    
    if skip_cut:
        print('CUT TO LENGTH: SKIPPED\n\n\n')
        return 0, 0, ''
    # cut_cost = 15.0
    print(f'cut_percent: {cut_percent}')
    print(f'cut_cost: {cut_cost}')
    if cut_cost is not None and cut_percent is not None:
        print('cut_to_length')
        cut_cost_val, cut_weight_val = cut_to_length(
            cut_percent,
            total_weight,
            master_coil_width,
            cut_cost
        )
    else:
        # fallback: use default values
        cut_cost_val, cut_weight_val = 15.0, 150.0
    print(f'COST TO CUT TO LENGTH: {cut_cost_val:.4f}\nSCRAP WEIGHT: {int(round(cut_weight_val))}\n\n\n')
    calc_str = f"cut_cost = {cut_cost_val}\ncut_weight = {cut_weight_val}"
    print(f"CUT_CALC:\n{calc_str}\n")
    return cut_cost_val, cut_weight_val, calc_str 