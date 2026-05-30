import torch
import torch.nn as nn
import math


class SpectralPositionalEncoding(nn.Module):
    """Sinusoidal positional encoding for spectral band sequences."""

    def __init__(self, d_model: int, max_len: int = 512):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer("pe", pe.unsqueeze(0))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x + self.pe[:, : x.size(1)]


class SoilTransformer(nn.Module):
    """
    Transformer encoder that takes a soil NIR spectral signature
    (sequence of reflectance values per band) and outputs:
      - microbiome_health: float [0, 1]
      - nutrient_vector: [N, P, K] predicted ppm
      - organic_matter: float pct
    """

    def __init__(
        self,
        n_bands: int = 256,
        d_model: int = 128,
        nhead: int = 8,
        num_layers: int = 4,
        dim_feedforward: int = 512,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.input_proj = nn.Linear(1, d_model)
        self.pos_enc = SpectralPositionalEncoding(d_model, max_len=n_bands)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            batch_first=True,
            norm_first=True,  # Pre-LN for training stability
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.pool = nn.AdaptiveAvgPool1d(1)

        # Auxiliary scalar features: ph, moisture, temperature, ec
        self.scalar_proj = nn.Linear(4, d_model)

        self.head_health = nn.Sequential(
            nn.Linear(d_model * 2, 64), nn.GELU(), nn.Linear(64, 1), nn.Sigmoid()
        )
        self.head_nutrients = nn.Sequential(
            nn.Linear(d_model * 2, 64), nn.GELU(), nn.Linear(64, 3), nn.ReLU()
        )
        self.head_om = nn.Sequential(
            nn.Linear(d_model * 2, 32), nn.GELU(), nn.Linear(32, 1), nn.Sigmoid()
        )

    def forward(
        self,
        spectral: torch.Tensor,          # (B, n_bands)
        scalars: torch.Tensor,            # (B, 4)  [ph, moisture, temp, ec]
        src_key_padding_mask: torch.Tensor | None = None,
    ) -> dict[str, torch.Tensor]:
        x = spectral.unsqueeze(-1)        # (B, n_bands, 1)
        x = self.input_proj(x)            # (B, n_bands, d_model)
        x = self.pos_enc(x)
        x = self.encoder(x, src_key_padding_mask=src_key_padding_mask)

        # Global average pool over band dimension
        pooled = self.pool(x.transpose(1, 2)).squeeze(-1)  # (B, d_model)

        scalar_emb = self.scalar_proj(scalars)              # (B, d_model)
        fused = torch.cat([pooled, scalar_emb], dim=-1)    # (B, d_model * 2)

        return {
            "microbiome_health": self.head_health(fused).squeeze(-1),
            "nutrients_npk": self.head_nutrients(fused),
            "organic_matter": self.head_om(fused).squeeze(-1),
        }
