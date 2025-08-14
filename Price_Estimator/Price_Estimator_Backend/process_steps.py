from value_added_processes import *


def process_examine_coil(master_coil_weight, examine_coil_scrap_percent, examine_coil_cost, skip_examine_coil):
    if skip_examine_coil:
        return 0, 0, ''
    kwargs = {}
    if examine_coil_scrap_percent is not None:
        kwargs['scrap_percent'] = examine_coil_scrap_percent
    if examine_coil_cost is not None:
        kwargs['cost'] = examine_coil_cost
    examine_coil_cost_val, examine_coil_scrap = examine_coil(master_coil_weight, **kwargs)
    return examine_coil_cost_val, examine_coil_scrap, ''


def process_trimming(examine_coil_scrap, master_coil_weight, master_coil_width, trimming_width_cropped, trimming_cost, skip_trimming):
    if skip_trimming:
        return 0, 0, ''
    kwargs = {}
    if trimming_width_cropped is not None:
        kwargs['width_cropped'] = trimming_width_cropped
    if trimming_cost is not None:
        kwargs['cost'] = trimming_cost
    trimming_cost_val, trimming_scrap = trimmming(
        examine_coil_scrap,
        master_coil_weight,
        master_coil_width,
        **kwargs,
    )
    return trimming_cost_val, trimming_scrap, ''


def process_pickle(master_coil_weight, examine_coil_scrap, trimming_scrap, pickle_scrap_percent, pickle_cost, skip_pickle):
    if skip_pickle:
        return 0, 0, ''
    kwargs = {}
    if pickle_scrap_percent is not None:
        kwargs['scrap_percent'] = pickle_scrap_percent
    if pickle_cost is not None:
        kwargs['cost'] = pickle_cost
    pickle_cost_val, pickle_scrap = pickle_and_oil(
        master_coil_weight,
        examine_coil_scrap,
        trimming_scrap,
        **kwargs,
    )
    return pickle_cost_val, pickle_scrap, ''


def process_coating(master_coil_weight, examine_coil_scrap, trimming_scrap, pickle_scrap, coating_scrap_percent, coating_cost, skip_coating):
    if skip_coating:
        return 0, 0, ''
    kwargs = {}
    if coating_scrap_percent is not None:
        kwargs['scrap_percent'] = coating_scrap_percent
    if coating_cost is not None:
        kwargs['cost'] = coating_cost
    coating_cost_val, coating_weight = coating(
        master_coil_weight,
        examine_coil_scrap,
        trimming_scrap,
        pickle_scrap,
        **kwargs,
    )
    return coating_cost_val, coating_weight, ''


def process_slitting(master_coil_width, master_coil_weight, examine_coil_scrap, trimming_scrap, pickle_scrap, coating_weight, widths_per_cut, skip_widths_per_cut, num_cuts_needed, skip_num_cuts_needed, slitting_scrap_percent, slitting_width_cropped, slitting_cost, skip_slitting, trimming_width_cropped, trimming_skip):   
    if skip_slitting:
        return 0, 0, ''
    kwargs = {}
    if trimming_skip:
        trimming_width_cropped = 0
    else:
        trimming_width_cropped = master_coil_width - trimming_width_cropped 
    num_cuts_needed = num_cuts_needed if num_cuts_needed is not None else [1]
    slitting_cost = 15.0 if slitting_cost is False else slitting_cost
    kwargs['width_cropped'] = trimming_width_cropped
    if slitting_cost is not None:
        kwargs['cost'] = slitting_cost
    slitting_cost_val, slitting_weight = slitting_v2(
        master_coil_width,
        master_coil_weight,
        examine_coil_scrap,
        trimming_scrap,
        pickle_scrap,
        coating_weight,
        widths_per_cut,
        num_cuts_needed,
        **kwargs,
    )
    return slitting_cost_val, slitting_weight, ''


def process_cut(cut_percent, widths_per_cut, num_cuts_needed, total_weight, master_coil_width, skip_cut, cut_cost = 15.0):
    # Legacy path removed in favour of structured Cut To Length. Kept for import compatibility.
    return 0, 0, ''


def process_cut_to_length(ctl_segments, total_length, running_weight, skipped=True, cost=1.0):
    """
    Thin wrapper for the Cut To Length 2 operation. Not wired into calculations yet.
    Returns (cost, scrap_weight, message).
    """
    if skipped:
        return 0.0, 0.0, ''
    from value_added_processes import cut_to_length
    cost_val, scrap_weight = cut_to_length(
        ctl_segments,
        total_length,
        running_weight,
        cost,
    )
    return cost_val, scrap_weight, ''