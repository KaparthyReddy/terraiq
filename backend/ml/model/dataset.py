import torch
from torch.utils.data import Dataset
import pandas as pd
import numpy as np


class SoilSpectralDataset(Dataset):
    """
    Expects a parquet file with columns:
      spectral_0 ... spectral_255  — NIR reflectance per band
      ph, moisture_pct, temperature_c, electrical_conductivity
      microbiome_health_score, nitrogen_ppm, phosphorus_ppm,
      potassium_ppm, organic_matter_pct
    """

    N_BANDS = 256

    def __init__(self, parquet_path: str, augment: bool = False):
        self.df = pd.read_parquet(parquet_path)
        self.augment = augment

        self.spectral_cols = [f"spectral_{i}" for i in range(self.N_BANDS)]
        self.scalar_cols = ["ph", "moisture_pct", "temperature_c", "electrical_conductivity"]

        # Normalise scalars
        self.scalar_mean = self.df[self.scalar_cols].mean().values.astype(np.float32)
        self.scalar_std  = self.df[self.scalar_cols].std().values.astype(np.float32) + 1e-6

    def __len__(self) -> int:
        return len(self.df)

    def __getitem__(self, idx: int) -> dict:
        row = self.df.iloc[idx]

        spectral = row[self.spectral_cols].values.astype(np.float32)
        if self.augment:
            spectral += np.random.normal(0, 0.002, spectral.shape).astype(np.float32)
            spectral = np.clip(spectral, 0, 1)

        scalars = row[self.scalar_cols].values.astype(np.float32)
        scalars = (scalars - self.scalar_mean) / self.scalar_std

        return {
            "spectral": torch.from_numpy(spectral),
            "scalars":  torch.from_numpy(scalars),
            "health":   torch.tensor(row["microbiome_health_score"], dtype=torch.float32),
            "npk":      torch.tensor(
                [row["nitrogen_ppm"], row["phosphorus_ppm"], row["potassium_ppm"]],
                dtype=torch.float32,
            ),
            "om":       torch.tensor(row["organic_matter_pct"] / 10.0, dtype=torch.float32),
        }
