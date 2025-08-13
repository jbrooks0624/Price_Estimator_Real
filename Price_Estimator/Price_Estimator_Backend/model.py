from typing import Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum


# --------------- CTL 2.0 models ---------------

class CTL2Mode(str, Enum):
    percent = "percent"
    pieces = "pieces"


class CTL2Action(str, Enum):
    scrap = "scrap"
    restock = "restock"
    level = "level"


class CTL2Segment(BaseModel):
    mode: CTL2Mode
    length: float
    percent: Optional[float] = None
    pieces: Optional[int] = None
    action: CTL2Action

    # Accept user-facing labels like "Level to Balance" and normalise to enum values
    @validator("action", pre=True)
    def _normalise_action(cls, value):  # type: ignore[no-redef]
        if isinstance(value, str):
            lowered = value.strip().lower()
            if "level" in lowered:
                return "level"
            if "restock" in lowered:
                return "restock"
            if "scrap" in lowered:
                return "scrap"
        return value


class CutToLength2Input(BaseModel):
    skipped: bool = True
    segments: List[CTL2Segment] = Field(default_factory=list)


# --------------- Price Estimator Input ---------------


class PriceEstimatorInput(BaseModel):
    """All parameters accepted by the legacy ``main`` function."""

    master_coil_width: float = 48
    master_coil_weight: float = 40000
    master_coil_cost: float = 100
    master_coil_thickness: float = 0.0700
    master_coil_length: Optional[float] = None

    # Examine coil
    examine_coil_scrap_percent: Optional[float] = None
    examine_coil_cost: Optional[float] = None
    skip_examine_coil: bool = False

    # Trimming
    trimming_width_cropped: Optional[float] = None
    trimming_cost: Optional[float] = None
    skip_trimming: bool = False

    # Pickle & oil
    pickle_scrap_percent: Optional[float] = None
    pickle_cost: Optional[float] = None
    skip_pickle: bool = False

    # Coating
    coating_scrap_percent: Optional[float] = None
    coating_cost: Optional[float] = None
    skip_coating: bool = False

    # Slitting
    widths_per_cut: Optional[List[float]] = None
    num_cuts_needed: Optional[List[int]] = None
    slitting_scrap_percent: Optional[float] = None
    slitting_width_cropped: Optional[float] = None
    slitting_cost: Optional[float] = None
    skip_slitting: bool = False

    # Cut to length
    cut_percent: Optional[float] = None
    cut_cost: Optional[float] = None
    cut_weight: Optional[float] = None
    skip_cut: bool = False

    # Storage costs
    storage_start: float = 0.0
    storage_examine: float = 0.0
    storage_trimming: float = 0.0
    storage_pickle: float = 0.0
    storage_coating: float = 0.0
    storage_slitting: float = 0.0
    storage_cut: float = 0.0
    storage_end: float = 0.0

    # Freight costs
    freight_start: float = 0.0
    freight_examine: float = 0.0
    freight_trimming: float = 0.0
    freight_pickle: float = 0.0
    freight_coating: float = 0.0
    freight_slitting: float = 0.0
    freight_cut: float = 0.0
    freight_end: float = 0.0

    margin: float = 15.0

    # Cut To Length 2.0 (structured, optional; not used in calculations yet)
    ctl2: Optional[CutToLength2Input] = None

# --------------- Price Estimator Output ---------------

class PriceEstimatorOutput(BaseModel):
    """Hard-coded schema mirroring every *non-CALC* print statement produced by
    the legacy implementation.  All fields are optional because individual
    prints can be suppressed when a processing step is skipped.
    """

    # Start of flow
    storage_at_start: Optional[float] = None
    freight_at_start: Optional[float] = None
    running_cost_after_start: Optional[float] = None

    # Examine coil
    cost_to_examine_coil: Optional[float] = None
    examine_scrap_weight: Optional[int] = None
    storage_after_examine: Optional[float] = None
    freight_after_examine: Optional[float] = None
    running_cost_after_examine: Optional[float] = None

    # Trimming
    cost_to_trim: Optional[float] = None
    trimming_scrap_weight: Optional[int] = None
    storage_after_trimming: Optional[float] = None
    freight_after_trimming: Optional[float] = None
    running_cost_after_trimming: Optional[float] = None

    # Pickle & oil
    cost_to_pickle_and_oil: Optional[float] = None
    pickle_scrap_weight: Optional[int] = None
    storage_after_pickle: Optional[float] = None
    freight_after_pickle: Optional[float] = None
    running_cost_after_pickle: Optional[float] = None

    # Coating
    cost_to_coat: Optional[float] = None
    coating_scrap_weight: Optional[int] = None
    storage_after_coating: Optional[float] = None
    freight_after_coating: Optional[float] = None
    running_cost_after_coating: Optional[float] = None

    # Slitting
    cost_to_slit: Optional[float] = None
    slitting_scrap_weight: Optional[int] = None
    storage_after_slitting: Optional[float] = None
    freight_after_slitting: Optional[float] = None
    running_cost_after_slitting: Optional[float] = None

    # Cut to length
    cost_to_cut_to_length: Optional[float] = None
    cut_scrap_weight: Optional[int] = None
    storage_after_cut: Optional[float] = None
    freight_after_cut: Optional[float] = None
    running_cost_after_cut: Optional[float] = None

    # End
    storage_at_end: Optional[float] = None
    freight_at_end: Optional[float] = None

    # Summary
    total_cost: Optional[float] = None  # actually cost per unit
    final_weight: Optional[int] = None
    scrap_percent: Optional[float] = None
    scrap_weight: Optional[int] = None
    selling_price: Optional[float] = None


    class Config:
        extra = "ignore"

