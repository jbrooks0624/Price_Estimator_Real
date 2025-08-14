from typing import List

def examine_coil(master_coil_weight: float, scrap_percent: float = .01, cost: float = 15):

    return cost, master_coil_weight * scrap_percent

def trimmming(examine_scrap_weight: float,
              master_coil_weight: float, 
              master_coil_width: float, 
              width_cropped: float = 1, 
              cost: float = 15):

    scrap_percent = 1 - (width_cropped / master_coil_width)

    # scrap_percent = .01
    # 1 percent

    scrap_weight = (master_coil_weight - examine_scrap_weight) * scrap_percent

    return cost, scrap_weight

def pickle_and_oil(master_coil_weight: float,
                   examine_scrap_weight: float, 
                   trimming_scrap_weight: float, 
                   scrap_percent: float = .01, 
                   cost: float = 15):
    
    scrap_weight = (master_coil_weight - examine_scrap_weight - trimming_scrap_weight) * scrap_percent


    return  cost, scrap_weight

def coating(master_coil_weight: float,
            examine_scrap_weight: float, 
            trimming_scrap_weight: float, 
            pickle_scrap_weight: float,
            scrap_percent: float = .01, 
            cost: float = 15):

    scrap_weight = (master_coil_weight - examine_scrap_weight - trimming_scrap_weight - pickle_scrap_weight) * scrap_percent
    
    return  cost, scrap_weight

def slitting(master_coil_width: float,
            master_coil_weight: float,
            examine_scrap_weight: float, 
            trimming_scrap_weight: float, 
            pickle_scrap_weight: float,
            coating_scrap_weight: float,
            width_per_cut: float = 1,
            num_cuts_needed: int = 1,
            scrap_percent: float = .01, 
            width_cropped: float = 1,
            cost: float = 15):
    
    updated_weight = master_coil_weight - examine_scrap_weight - trimming_scrap_weight - pickle_scrap_weight - coating_scrap_weight

    weight_per_cut = ((width_per_cut / num_cuts_needed) / (master_coil_width - width_cropped)) * updated_weight

    # scrap_weight = updated_weight - weight_per_cut

    scrap_weight = updated_weight * scrap_percent

    return cost, scrap_weight

def slitting_v2(
        master_coil_width: float,
        master_coil_weight: float,
        examine_scrap_weight: float, 
        trimming_scrap_weight: float, 
        pickle_scrap_weight: float,
        coating_scrap_weight: float,
        widths_per_cut: List[float] = [5],
        num_cuts_needed: List[float] = [1],
        width_cropped: float = 0,
        cost: float = 15):

    
    updated_weight = master_coil_weight - examine_scrap_weight - trimming_scrap_weight - pickle_scrap_weight - coating_scrap_weight

    # Diagnostics removed for production
    
    used_weight = sum(((w * nc)/(master_coil_width - width_cropped)) * updated_weight for w, nc in zip(widths_per_cut, num_cuts_needed))
    scrap_weight = updated_weight - used_weight

    return cost, scrap_weight
    

def cut_to_length(
    segments,
    total_length: float,
    running_weight: float,
    cost: float = 1.0,
):
    """
    Implement Cut To Length (sequential cuts) logic.
    """
    original_length = float(total_length or 0.0)
    current_length = original_length

    for segment in segments or []:
        mode = _seg_get(segment, "mode")
        action = _seg_get(segment, "action")
        length_per_cut = float(_seg_get(segment, "length") or 0.0)

        mode_str = _to_enum_value_str(mode)
        action_str = _to_enum_value_str(action)

        if length_per_cut <= 0 or current_length <= 0:
            continue

        if mode_str == "percent":
            percent_value = _seg_get(segment, "percent")
            x = float(percent_value or 0.0)
            if x > 1:
                x = x / 100.0
            selected_length = current_length * max(min(x, 1.0), 0.0)
            num_pieces = int(selected_length // length_per_cut)
            used_length = num_pieces * length_per_cut
            leftover_length = max(current_length - used_length, 0.0)
        elif mode_str == "pieces":
            pieces_value = int(_seg_get(segment, "pieces") or 0)
            used_length = float(pieces_value) * length_per_cut
            leftover_length = max(current_length - used_length, 0.0)
        else:
            continue

        if action_str == "level":
            current_length = leftover_length
            continue
        elif action_str == "scrap":
            scrap_length = leftover_length
            scrap_percent = (scrap_length / original_length) if original_length else 0.0
            scrap_weight = scrap_percent * float(running_weight or 0.0)
            return float(cost), float(scrap_weight)
        elif action_str == "restock":
            return float(cost), 0.0
        else:
            continue

    return 0.0, 0.0

# pcikle and oil 150 pounds
# cut to length scrap weight 150


def _seg_get(segment, field_name, default=None):
    """Return a field from a CTL2 segment which may be a dict or an object.

    This helper lets us accept either the Pydantic ``CTL2Segment`` model or a
    plain dict from the caller without importing model types here.
    """
    if isinstance(segment, dict):
        return segment.get(field_name, default)
    return getattr(segment, field_name, default)


def _to_enum_value_str(value_obj) -> str:
    """Convert enum-like objects or strings to a lowercase value string.

    - If ``value_obj`` has a ``.value``, use it
    - Else use its string form, and if it contains a dot, take the last token
      (e.g. "CTL2Action.scrap" -> "scrap")
    """
    if value_obj is None:
        return ""
    enum_value = getattr(value_obj, "value", None)
    base = enum_value if enum_value is not None else str(value_obj)
    text = str(base)
    if "." in text:
        text = text.split(".")[-1]
    return text.lower()


def cut_to_length_2(
    segments,
    total_length: float,
    running_weight: float,
    cost: float = 1.0,
):
    """
    Implement Cut To Length 2 (sequential cuts) logic.

    For each segment:
      - mode == "percent":
          x = percent (accepts 0-1 or 0-100). Select x% of current length for
          cutting into pieces of length ``length``. Leftover length after cut is
          remainder of that selection plus the untouched (1-x)%:
              leftover = current_length - floor((x*current_length)/length) * length

      - mode == "pieces":
          Use ``pieces`` pieces of ``length``. Leftover is any remaining length:
              leftover = max(current_length - pieces*length, 0)

      - action == "level":
          Set current_length = leftover and continue to the next segment.

      - action == "scrap":
          Scrap the leftover. Scrap percent is leftover/current_length and the
          scrap weight is that percent applied to ``running_weight``. Return
          (cost, scrap_weight).

      - action == "restock":
          Treat leftover as restocked: no scrap weight. Return (cost, 0).

    If no terminal action (scrap/restock) is encountered, returns (0, 0).
    """

    original_length = float(total_length or 0.0)
    current_length = original_length

    for segment in segments or []:
        mode = _seg_get(segment, "mode")
        action = _seg_get(segment, "action")
        length_per_cut = float(_seg_get(segment, "length") or 0.0)

        # Normalise enums/strings
        mode_str = _to_enum_value_str(mode)
        action_str = _to_enum_value_str(action)

        # Guard against invalid length values
        if length_per_cut <= 0 or current_length <= 0:
            # Nothing usable to cut; move on
            continue

        if mode_str == "percent":
            percent_value = _seg_get(segment, "percent")
            x = float(percent_value or 0.0)
            if x > 1:
                x = x / 100.0
            selected_length = current_length * max(min(x, 1.0), 0.0)
            num_pieces = int(selected_length // length_per_cut)
            used_length = num_pieces * length_per_cut
            leftover_length = max(current_length - used_length, 0.0)
        elif mode_str == "pieces":
            pieces_value = int(_seg_get(segment, "pieces") or 0)
            used_length = float(pieces_value) * length_per_cut
            leftover_length = max(current_length - used_length, 0.0)
        else:
            # Unknown mode; skip
            continue


        if action_str == "level":
            current_length = leftover_length
            continue
        elif action_str == "scrap":
            scrap_length = leftover_length
            # Scrap percent should be based on the ORIGINAL total length, not the running length
            scrap_percent = (scrap_length / original_length) if original_length else 0.0
            scrap_weight = scrap_percent * float(running_weight or 0.0)
            return float(cost), float(scrap_weight)
        elif action_str == "restock":
            return float(cost), 0.0
        else:
            # Unknown action; skip
            continue

    # If we processed all segments without a terminal action
    return 0.0, 0.0
