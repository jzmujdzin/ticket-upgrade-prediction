from torch.utils.data import Dataset
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.base import TransformerMixin
from sklearn.preprocessing import StandardScaler


class UpgradeDataset(Dataset):
    def __init__(
        self,
        X: pd.DataFrame,
        y: np.ndarray,
        scaler_class: TransformerMixin = StandardScaler,
    ) -> None:
        self.X = X.values
        self.y = y.reshape(-1, 1)
        self.scaler_class = scaler_class

        self.X_scaler = None
        self.y_scaler = None

        # scale only when scaler is provided
        if self.scaler_class:
            self._scale_datasets()

    def _scale_datasets(self) -> None:
        self.X_scaler = self.scaler_class()
        self.X = self.X_scaler.fit_transform(self.X)

        self.y_scaler = self.scaler_class()
        self.y_scaler.fit_transform(self.y)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, index):
        X = self.X[index]
        y = self.y[index]

        return X, y

    @classmethod
    def from_dir(
        cls,
        data_path: Path = Path(__file__).parents[3]
        / "data"
        / "preprocessed_upgrade.csv",
        y_col: str = "UPGRADED_FLAG",
    ):
        """Loads class using data from chosen directory"""
        data = pd.read_csv(data_path)
        X = data.drop(columns=y_col)
        y = data[y_col].values

        return cls(X=X, y=y)


if __name__ == "__main__":
    dataset = UpgradeDataset.from_dir()
    print(dataset[0])
