from process_steps import process_examine_coil, process_trimming, process_pickle, process_coating, process_slitting, process_cut


def print_summary(final_cost, total_weight, master_coil_weight, margin):
    print('-------------SUMMARY------------')
    print(f'TOTAL COST: {final_cost:.4f}')
    print(f'FINAL WEIGHT: {int(round(total_weight))} \n(SCRAP %: {((master_coil_weight - total_weight)/master_coil_weight) * 100:.4f}, SCRAP WEIGHT: {int(round(master_coil_weight - total_weight))})')
    print(f'SELLING PRICE: {final_cost * (1 + margin/100):.4f}')


def main(
    master_coil_width: float = 48,
    master_coil_weight: float = 40000,
    master_coil_cost: float = 100,
    examine_coil_scrap_percent: float = None,
    examine_coil_cost: float = None,
    skip_examine_coil: bool = False,
    trimming_width_cropped: float = None,
    trimming_cost: float = None,
    skip_trimming: bool = False,
    pickle_scrap_percent: float = None,
    pickle_cost: float = None,
    skip_pickle: bool = False,
    coating_scrap_percent: float = None,
    coating_cost: float = None,
    skip_coating: bool = False,
    widths_per_cut: list = None,
    num_cuts_needed: list = None,
    slitting_scrap_percent: float = None,
    slitting_width_cropped: float = None,
    slitting_cost: float = None,
    skip_slitting: bool = False,
    cut_percent: float = None,
    cut_cost: float = None,
    cut_weight: float = None,
    skip_cut: bool = False,
    storage_start: float = 0.0,
    storage_examine: float = 0.0,
    storage_trimming: float = 0.0,
    storage_pickle: float = 0.0,
    storage_coating: float = 0.0,
    storage_slitting: float = 0.0,
    storage_cut: float = 0.0,
    storage_end: float = 0.0,
    freight_start: float = 0.0,
    freight_examine: float = 0.0,
    freight_trimming: float = 0.0,
    freight_pickle: float = 0.0,
    freight_coating: float = 0.0,
    freight_slitting: float = 0.0,
    freight_cut: float = 0.0,
    freight_end: float = 0.0,
    margin: float = 15.0
):
    skip_slitting = bool(skip_slitting)
    total_cost = master_coil_cost * master_coil_weight
    print(f'STORAGE AT START: {storage_start}')
    total_cost += storage_start * master_coil_weight
    print(f'FREIGHT AT START: {freight_start}')
    total_cost += freight_start
    running_weight = master_coil_weight
    print(f'RUNNING COST AFTER START: {total_cost / running_weight:.4f}\n\n\n')

    print('--- EXAMINE COIL ---')
    examine_coil_cost_val, examine_coil_scrap, examine_calc_str = process_examine_coil(master_coil_weight, examine_coil_scrap_percent, examine_coil_cost, skip_examine_coil)
    if not skip_examine_coil:
        print(f'STORAGE AFTER EXAMINE: {storage_examine}')
        total_cost += storage_examine * (master_coil_weight - examine_coil_scrap)
        print(f'FREIGHT AFTER EXAMINE: {freight_examine}')
        total_cost += freight_examine
    total_cost += (master_coil_weight * examine_coil_cost_val)
    running_weight = master_coil_weight - examine_coil_scrap
    print(f'RUNNING COST AFTER EXAMINE: {total_cost / running_weight:.4f}')
    print("\n\n\n")

    print('--- TRIMMING ---')
    trimming_cost_val, trimming_scrap, trimming_calc_str = process_trimming(examine_coil_scrap, master_coil_weight, master_coil_width, trimming_width_cropped, trimming_cost, skip_trimming)
    if not skip_trimming:
        print(f'STORAGE AFTER TRIMMING: {storage_trimming}')
        total_cost += storage_trimming * (master_coil_weight - examine_coil_scrap - trimming_scrap)
        print(f'FREIGHT AFTER TRIMMING: {freight_trimming}')
        total_cost += freight_trimming
    total_cost += ((master_coil_weight - examine_coil_scrap) * trimming_cost_val)
    running_weight = master_coil_weight - examine_coil_scrap - trimming_scrap
    print(f'RUNNING COST AFTER TRIMMING: {total_cost / running_weight:.4f}')
    print("\n\n\n")

    print('--- PICKLE & OIL ---')
    pickle_cost_val, pickle_scrap, pickle_calc_str = process_pickle(master_coil_weight, examine_coil_scrap, trimming_scrap, pickle_scrap_percent, pickle_cost, skip_pickle)
    if not skip_pickle:
        print(f'STORAGE AFTER PICKLE: {storage_pickle}')
        total_cost += storage_pickle * (master_coil_weight - examine_coil_scrap - trimming_scrap - pickle_scrap)
        print(f'FREIGHT AFTER PICKLE: {freight_pickle}')
        total_cost += freight_pickle
    total_cost += ((master_coil_weight - examine_coil_scrap - trimming_scrap) * pickle_cost_val)
    running_weight = master_coil_weight - examine_coil_scrap - trimming_scrap - pickle_scrap
    print(f'RUNNING COST AFTER PICKLE: {total_cost / running_weight:.4f}')
    print("\n\n\n")

    print('--- COATING ---')
    coating_cost_val, coating_weight, coating_calc_str = process_coating(master_coil_weight, examine_coil_scrap, trimming_scrap, pickle_scrap, coating_scrap_percent, coating_cost, skip_coating)
    if not skip_coating:
        print(f'STORAGE AFTER COATING: {storage_coating}')
        total_cost += storage_coating * (master_coil_weight - examine_coil_scrap - trimming_scrap - pickle_scrap - coating_weight)
        print(f'FREIGHT AFTER COATING: {freight_coating}')
        total_cost += freight_coating
    total_cost += ((master_coil_weight - examine_coil_scrap - trimming_scrap - pickle_scrap) * coating_cost_val)
    running_weight = master_coil_weight - examine_coil_scrap - trimming_scrap - pickle_scrap - coating_weight
    print(f'RUNNING COST AFTER COATING: {total_cost / running_weight:.4f}')
    print("\n\n\n")

    print('--- SLITTING ---')
    slitting_cost_val, slitting_weight, slitting_calc_str = process_slitting(master_coil_width, master_coil_weight, examine_coil_scrap, trimming_scrap, pickle_scrap, coating_weight, widths_per_cut, False, num_cuts_needed, False, slitting_scrap_percent, slitting_width_cropped, slitting_cost, skip_slitting)
    if not skip_slitting:
        print(f'STORAGE AFTER SLITTING: {storage_slitting}')
        total_cost += storage_slitting * (master_coil_weight - examine_coil_scrap - trimming_scrap - pickle_scrap - coating_weight - slitting_weight)
        print(f'FREIGHT AFTER SLITTING: {freight_slitting}')
        total_cost += freight_slitting

    total_cost += ((master_coil_weight - examine_coil_scrap - trimming_scrap - pickle_scrap - coating_weight) * slitting_cost_val)
    running_weight = master_coil_weight - examine_coil_scrap - trimming_scrap - pickle_scrap - coating_weight - slitting_weight
    print(f'RUNNING COST AFTER SLITTING: {total_cost / running_weight:.4f}')
    print("\n\n\n")

    print('--- CUT TO LENGTH ---')
    total_weight_before_cut = master_coil_weight - examine_coil_scrap - trimming_scrap - pickle_scrap - coating_weight - slitting_weight
    cut_cost_val, cut_weight_val, cut_calc_str = process_cut(
        cut_percent,
        widths_per_cut,
        num_cuts_needed,
        total_weight_before_cut,
        master_coil_width,
        skip_cut,
        cut_cost
    )
    if not skip_cut:
        print(f'STORAGE AFTER CUT: {storage_cut}')
        total_cost += storage_cut * (total_weight_before_cut - cut_weight_val)
        print(f'FREIGHT AFTER CUT: {freight_cut}')
        total_cost += freight_cut
    total_cost += (total_weight_before_cut * cut_cost_val)
    running_weight = total_weight_before_cut - cut_weight_val
    print(f'RUNNING COST AFTER CUT: {total_cost / running_weight:.4f}')
    print("\n\n\n")
    

    print(f'STORAGE AT END: {storage_end}')
    total_cost += storage_end * (total_weight_before_cut - cut_weight_val)
    print(f'FREIGHT AT END: {freight_end}\n\n')
    total_cost += freight_end

    total_weight = total_weight_before_cut - cut_weight_val
    final_cost = total_cost / total_weight

    print_summary(final_cost, total_weight, master_coil_weight, margin)