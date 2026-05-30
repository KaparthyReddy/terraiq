import torch
import numpy as np
from typing import Optional

from ml.model.soil_transformer import SoilTransformer
from app.core.config import settings

_model: Optional[SoilTransformer] = None


def load_model() -> SoilTransformer:
    global _model
    if _model is None:
        _model = SoilTransformer()
        state = torch.load(settings.MODEL_PATH, map_location="cpu", weights_only=True)
        _model.load_state_dict(state)
        _model.eval()
    return _model


def predict(
    spectral_signature: str,
    ph: float,
    moisture_pct: float,
    temperature_c: float,
    electrical_conductivity: float,
) -> dict:
    """
    Run inference given a comma-separated spectral string and scalar readings.
    Returns microbiome_health, nutrients_npk, organic_matter.
    """
    model = load_model()

    spectral = np.array([float(v) for v in spectral_signature.split(",")], dtype=np.float32)
    spectral_t = torch.from_numpy(spectral).unsqueeze(0)  # (1, n_bands)

    scalars = np.array([ph, moisture_pct, temperature_c, electrical_conductivity], dtype=np.float32)
    scalars_t = torch.from_numpy(scalars).unsqueeze(0)    # (1, 4)

    with torch.no_grad():
        out = model(spectral_t, scalars_t)

    return {
        "microbiome_health": round(out["microbiome_health"].item(), 4),
        "nitrogen_ppm":      round(out["nutrients_npk"][0, 0].item(), 2),
        "phosphorus_ppm":    round(out["nutrients_npk"][0, 1].item(), 2),
        "potassium_ppm":     round(out["nutrients_npk"][0, 2].item(), 2),
        "organic_matter_pct": round(out["organic_matter"].item() * 10.0, 3),
    }
