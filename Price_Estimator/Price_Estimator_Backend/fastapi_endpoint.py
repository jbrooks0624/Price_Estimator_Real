from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sys
import os
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

@app.post("/estimate", response_model=PriceEstimatorOutput, summary="Run price estimation")
def estimate_price(body: PriceEstimatorInput):  # noqa: D401
    """Run the full pricing calculation and return a structured result."""
    try:
        # Build payload excluding None fields; pass structured fields through
        payload = body.dict(exclude_none=True)
        return calculate_price(**payload)
    except Exception as exc:  # pragma: no cover
        return JSONResponse(status_code=500, content={"detail": str(exc)})