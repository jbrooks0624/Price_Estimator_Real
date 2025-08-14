from typing import List, Optional


def _safe_ratio(cost: float, weight: float) -> float:
    """Return cost per unit weight, safeguarding against division by zero."""
    # print(f'cost: {cost}')
    # print(f'weight: {weight}')
    return cost / weight if weight else 0.0

try:
    from .model import PriceEstimatorOutput
    from .process_steps import (
        process_examine_coil,
        process_trimming,
        process_pickle,
        process_coating,
        process_slitting,
        process_cut,
        process_cut_to_length,
    )
except ImportError:  # Support running without package context
    from model import PriceEstimatorOutput
    from process_steps import (
        process_examine_coil,
        process_trimming,
        process_pickle,
        process_coating,
        process_slitting,
        process_cut,
        process_cut_to_length,
    )


def calculate_price(
    # Mirrors ``main`` parameters one-to-one
    master_coil_width: float = 48,
    master_coil_weight: float = 40000,
    master_coil_cost: float = 100,
    master_coil_thickness: float = 0.0700,
    master_coil_length: Optional[float] = None,
    examine_coil_scrap_percent: Optional[float] = None,
    examine_coil_cost: Optional[float] = None,
    skip_examine_coil: bool = False,
    trimming_width_cropped: Optional[float] = None,
    trimming_cost: Optional[float] = None,
    skip_trimming: bool = False,
    pickle_scrap_percent: Optional[float] = None,
    pickle_cost: Optional[float] = None,
    skip_pickle: bool = False,
    coating_scrap_percent: Optional[float] = None,
    coating_cost: Optional[float] = None,
    skip_coating: bool = False,
    widths_per_cut: Optional[List[float]] = None,
    num_cuts_needed: Optional[List[int]] = None,
    slitting_scrap_percent: Optional[float] = None,
    slitting_width_cropped: Optional[float] = None,
    slitting_cost: Optional[float] = None,
    skip_slitting: bool = False,
    cut_to_length: Optional[dict] = None,
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
    margin: float = 15.0,
    # removed: ctl2 (renamed to cut_to_length)
) -> PriceEstimatorOutput:
    """Pure function that performs the full pricing calculation and returns a
    populated ``PriceEstimatorOutput`` with **no console output**.
    """

    out = PriceEstimatorOutput()

    total_cost = master_coil_cost * master_coil_weight
    total_cost += storage_start * master_coil_weight
    total_cost += freight_start
    running_weight = master_coil_weight

    out.storage_at_start = storage_start
    out.freight_at_start = freight_start
    out.running_cost_after_start = _safe_ratio(total_cost, running_weight)

    # -------------------- EXAMINE COIL --------------------
    examine_cost_val, examine_scrap, _ = process_examine_coil(
        master_coil_weight,
        examine_coil_scrap_percent,
        examine_coil_cost,
        skip_examine_coil,
    )
    if not skip_examine_coil:
        total_cost += storage_examine * (master_coil_weight - examine_scrap)
        total_cost += freight_examine
    total_cost += master_coil_weight * examine_cost_val
    running_weight = master_coil_weight - examine_scrap

    out.cost_to_examine_coil = examine_cost_val
    out.examine_scrap_weight = int(round(examine_scrap))
    out.storage_after_examine = storage_examine
    out.freight_after_examine = freight_examine
    out.running_cost_after_examine = _safe_ratio(total_cost, running_weight)

    # -------------------- TRIMMING --------------------
    trimming_cost_val, trimming_scrap, _ = process_trimming(
        examine_scrap,
        master_coil_weight,
        master_coil_width,
        trimming_width_cropped,
        trimming_cost,
        skip_trimming,
    )
    if not skip_trimming:
        total_cost += storage_trimming * (master_coil_weight - examine_scrap - trimming_scrap)
        total_cost += freight_trimming
    total_cost += (master_coil_weight - examine_scrap) * trimming_cost_val
    running_weight = master_coil_weight - examine_scrap - trimming_scrap

    out.cost_to_trim = trimming_cost_val
    out.trimming_scrap_weight = int(round(trimming_scrap))
    out.storage_after_trimming = storage_trimming
    out.freight_after_trimming = freight_trimming
    out.running_cost_after_trimming = _safe_ratio(total_cost, running_weight)

    # -------------------- PICKLE & OIL --------------------
    pickle_cost_val, pickle_scrap, _ = process_pickle(
        master_coil_weight,
        examine_scrap,
        trimming_scrap,
        pickle_scrap_percent,
        pickle_cost,
        skip_pickle,
    )
    if not skip_pickle:
        total_cost += storage_pickle * (master_coil_weight - examine_scrap - trimming_scrap - pickle_scrap)
        total_cost += freight_pickle
    total_cost += (master_coil_weight - examine_scrap - trimming_scrap) * pickle_cost_val
    running_weight = master_coil_weight - examine_scrap - trimming_scrap - pickle_scrap

    out.cost_to_pickle_and_oil = pickle_cost_val
    out.pickle_scrap_weight = int(round(pickle_scrap))
    out.storage_after_pickle = storage_pickle
    out.freight_after_pickle = freight_pickle
    out.running_cost_after_pickle = _safe_ratio(total_cost, running_weight)

    # -------------------- COATING --------------------
    coating_cost_val, coating_scrap, _ = process_coating(
        master_coil_weight,
        examine_scrap,
        trimming_scrap,
        pickle_scrap,
        coating_scrap_percent,
        coating_cost,
        skip_coating,
    )
    if not skip_coating:
        total_cost += storage_coating * (
            master_coil_weight - examine_scrap - trimming_scrap - pickle_scrap - coating_scrap
        )
        total_cost += freight_coating
    total_cost += (
        master_coil_weight - examine_scrap - trimming_scrap - pickle_scrap
    ) * coating_cost_val
    running_weight = (
        master_coil_weight - examine_scrap - trimming_scrap - pickle_scrap - coating_scrap
    )

    out.cost_to_coat = coating_cost_val
    out.coating_scrap_weight = int(round(coating_scrap))
    out.storage_after_coating = storage_coating
    out.freight_after_coating = freight_coating
    out.running_cost_after_coating = _safe_ratio(total_cost, running_weight)

    # -------------------- SLITTING --------------------
    slitting_cost_val, slitting_scrap, _ = process_slitting(
        master_coil_width,
        master_coil_weight,
        examine_scrap,
        trimming_scrap,
        pickle_scrap,
        coating_scrap,
        widths_per_cut,
        False,
        num_cuts_needed,
        False,
        slitting_scrap_percent,
        slitting_width_cropped,
        slitting_cost,
        skip_slitting,
        trimming_width_cropped,
        skip_trimming,
    )
    if not skip_slitting:
        total_cost += storage_slitting * (
            master_coil_weight
            - examine_scrap
            - trimming_scrap
            - pickle_scrap
            - coating_scrap
            - slitting_scrap
        )
        total_cost += freight_slitting
    total_cost += (
        master_coil_weight - examine_scrap - trimming_scrap - pickle_scrap - coating_scrap
    ) * slitting_cost_val
    running_weight = (
        master_coil_weight
        - examine_scrap
        - trimming_scrap
        - pickle_scrap
        - coating_scrap
        - slitting_scrap
    )

    out.cost_to_slit = slitting_cost_val
    out.slitting_scrap_weight = int(round(slitting_scrap))
    out.storage_after_slitting = storage_slitting
    out.freight_after_slitting = freight_slitting
    out.running_cost_after_slitting = _safe_ratio(total_cost, running_weight)

    # -------------------- CUT TO LENGTH --------------------
    if cut_to_length and not cut_to_length.get("skipped", True):
        total_weight_before_cut = running_weight
        total_length_for_cut = float(master_coil_length or 0.0)
        user_cut_cost = float(cut_to_length.get("cost", 1.5))

        _ignored_cost, cut_scrap_weight, _msg = process_cut_to_length(
            cut_to_length.get("segments", []),
            total_length_for_cut,
            total_weight_before_cut,
            skipped=False,
            cost=user_cut_cost,
        )

        # Apply storage/freight at this stage after scrap
        total_cost += storage_cut * (total_weight_before_cut - cut_scrap_weight)
        total_cost += freight_cut
        total_cost += total_weight_before_cut * user_cut_cost
        running_weight = total_weight_before_cut - cut_scrap_weight

        out.cost_to_cut_to_length = user_cut_cost
        out.cut_scrap_weight = int(round(cut_scrap_weight))
        out.storage_after_cut = storage_cut
        out.freight_after_cut = freight_cut
        out.running_cost_after_cut = _safe_ratio(total_cost, running_weight)

    # -------------------- END / SUMMARY --------------------
    total_cost += storage_end * running_weight
    total_cost += freight_end

    out.storage_at_end = storage_end
    out.freight_at_end = freight_end

    final_weight = running_weight
    final_cost_per_unit = _safe_ratio(total_cost, final_weight)

    out.total_cost = final_cost_per_unit
    out.final_weight = int(round(final_weight))
    out.scrap_percent = ((master_coil_weight - final_weight) / master_coil_weight) * 100
    out.scrap_weight = int(round(master_coil_weight - final_weight))
    out.selling_price = final_cost_per_unit * (1 + margin / 100)


    return out
