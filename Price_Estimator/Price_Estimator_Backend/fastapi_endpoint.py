from fastapi import FastAPI
from fastapi.responses import JSONResponse
from io import StringIO
from contextlib import redirect_stdout
import re
import sys
import os
from typing import Any, Dict
from dotenv import load_dotenv

# Make sure the local directory is importable when the application is started
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

# Load environment variables from .env if present
load_dotenv()

try:
    # Prefer relative imports when the package is discovered correctly (e.g. when
    # running ``uvicorn Price_Estimator_Backend.fastapi_endpoint:app``)
    from .model import PriceEstimatorInput, PriceEstimatorOutput  # type: ignore
    from .calculator import calculate_price  # type: ignore
except ImportError:  # pragma: no cover
    # Not executed as a package; import sibling modules directly.
    from model import PriceEstimatorInput, PriceEstimatorOutput  # type: ignore
    from calculator import calculate_price  # type: ignore

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Price Estimator API", version="1.0.0")

# CORS configuration from environment
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
allowed_origins = [o.strip() for o in allowed_origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["POST"],
    allow_headers=["*"],
)


NON_CALCULATION_PATTERN = re.compile(r".*_CALC:.*", re.IGNORECASE)
HEADER_PATTERN = re.compile(r"^[-]{3,}|^---.*---$")


def _normalise_label(label: str) -> str:
    """Convert a human-readable label (coming from a print statement) into a
    valid python identifier suitable for JSON keys.
    """
    cleaned = re.sub(r"[^0-9a-zA-Z]+", "_", label).strip("_")
    return cleaned.lower()


def _parse_stdout(raw_stdout: str) -> Dict[str, Any]:
    """Parse stdout from the legacy implementation and convert human-readable
    lines into a dict whose keys match ``PriceEstimatorOutput`` fields."""

    section_alias = {
        "examine coil": "examine",
        "trimming": "trimming",
        "pickle & oil": "pickle",
        "coating": "coating",
        "slitting": "slitting",
        "cut to length": "cut",
    }

    data: Dict[str, Any] = {}
    current_section: str | None = None

    for line in raw_stdout.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        # Skip separator lines ("-----" etc.)
        if HEADER_PATTERN.match(stripped):
            continue

        # Identify section headers like "--- TRIMMING ---"
        header_match = re.match(r"---\s*(.*?)\s*---", stripped, re.IGNORECASE)
        if header_match:
            header_text = header_match.group(1).lower()
            current_section = section_alias.get(header_text, None)
            continue

        # Skip detailed calculation breakdowns
        if NON_CALCULATION_PATTERN.search(stripped):
            continue

        # Special handling for summary line containing 3 numbers
        if stripped.upper().startswith("FINAL WEIGHT"):
            # Example: "FINAL WEIGHT: 39800 (SCRAP %: 0.50, SCRAP WEIGHT: 200)"
            match = re.match(r"FINAL WEIGHT:\s*([\d.]+).*SCRAP %:\s*([\d.]+).*SCRAP WEIGHT:\s*([\d.]+)", stripped, re.IGNORECASE)
            if match:
                data["final_weight"] = int(float(match.group(1)))
                data["scrap_percent"] = float(match.group(2))
                data["scrap_weight"] = int(float(match.group(3)))
            continue

        # Typical "LABEL: VALUE" prints
        if ":" in stripped:
            label, value = stripped.split(":", 1)
            raw_key = label.strip()
            value = value.strip()

            # Handle ambiguous "SCRAP WEIGHT" label by using current section prefix
            if raw_key.upper() == "SCRAP WEIGHT" and current_section:
                key = f"{current_section}_scrap_weight"
            else:
                key = _normalise_label(raw_key)
                # Normalise some known variations
                key = key.replace("cost_to_pickle_oil", "cost_to_pickle_and_oil")

            # Numeric conversion if possible
            if value.replace(".", "", 1).isdigit():
                parsed_num: Any = float(value) if "." in value else int(value)
                # Scrap-weight fields should be integers
                if key.endswith("_scrap_weight"):
                    parsed_num = int(round(float(parsed_num)))
                parsed = parsed_num
            else:
                parsed = value
            data[key] = parsed
        else:
            # Bare words (e.g., "TRIMMING: SKIPPED")
            key = _normalise_label(stripped)
            data[key] = True

    return data


@app.post("/estimate", response_model=PriceEstimatorOutput, summary="Run price estimation")
def estimate_price(body: PriceEstimatorInput):  # noqa: D401
    """Run the full pricing calculation and return a structured result."""
    try:
        # Build payload excluding None fields and drop structured fields that
        # the pure calculator does not yet accept (e.g. ctl2)
        print(body.ctl2)
        payload = body.dict(exclude_none=True)
        payload.pop("ctl2", None)
        # print(payload)
        return calculate_price(**payload)
    except Exception as exc:  # pragma: no cover
        return JSONResponse(status_code=500, content={"detail": str(exc)})