import argparse
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split

from ml.model.soil_transformer import SoilTransformer
from ml.model.dataset import SoilSpectralDataset


def train(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Training on {device}")

    dataset = SoilSpectralDataset(args.data, augment=True)
    val_len = int(len(dataset) * 0.15)
    train_ds, val_ds = random_split(dataset, [len(dataset) - val_len, val_len])

    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True,  num_workers=4, pin_memory=True)
    val_loader   = DataLoader(val_ds,   batch_size=args.batch_size, shuffle=False, num_workers=4, pin_memory=True)

    model = SoilTransformer().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.OneCycleLR(
        optimizer, max_lr=args.lr, steps_per_epoch=len(train_loader), epochs=args.epochs
    )

    bce = nn.BCELoss()
    mse = nn.MSELoss()

    best_val_loss = float("inf")

    for epoch in range(1, args.epochs + 1):
        model.train()
        total_loss = 0.0

        for batch in train_loader:
            spectral = batch["spectral"].to(device)
            scalars  = batch["scalars"].to(device)
            health   = batch["health"].to(device)
            npk      = batch["npk"].to(device)
            om       = batch["om"].to(device)

            out = model(spectral, scalars)
            loss = (
                bce(out["microbiome_health"], health) * 2.0
                + mse(out["nutrients_npk"], npk) * 0.01
                + bce(out["organic_matter"], om)
            )

            optimizer.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()
            total_loss += loss.item()

        avg_train = total_loss / len(train_loader)

        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for batch in val_loader:
                out = model(batch["spectral"].to(device), batch["scalars"].to(device))
                val_loss += bce(out["microbiome_health"], batch["health"].to(device)).item()
        avg_val = val_loss / len(val_loader)

        print(f"Epoch {epoch:03d} | train={avg_train:.4f} | val={avg_val:.4f}")

        if avg_val < best_val_loss:
            best_val_loss = avg_val
            torch.save(model.state_dict(), args.output)
            print(f"  ✓ saved best model → {args.output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data",       required=True)
    parser.add_argument("--output",     default="ml/model/weights/soil_transformer.pt")
    parser.add_argument("--epochs",     type=int,   default=50)
    parser.add_argument("--batch-size", type=int,   default=64)
    parser.add_argument("--lr",         type=float, default=3e-4)
    train(parser.parse_args())
