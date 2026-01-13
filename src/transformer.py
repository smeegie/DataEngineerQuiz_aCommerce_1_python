import json
import os
import pandas as pd

from src.config import config


class Transformer:
    def run(self) -> None:
        df = self.load_data()
        df_transformed = self.transform(df)
        self.save(df_transformed)

    def load_data(self) -> pd.DataFrame:
        raise NotImplementedError

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    def save(self, df: pd.DataFrame) -> None:
        os.makedirs(config["TRANSFORMED_DIRECTORY"], exist_ok=True)
        out_path = os.path.join(config["TRANSFORMED_DIRECTORY"], "result.csv")
        df.to_csv(out_path, index=False)


class BookTransformer(Transformer):
    def load_data(self) -> pd.DataFrame:
        input_path = os.path.join(config["RAW_DIRECTORY"], "data.json")
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return pd.DataFrame(data)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        rating_map = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5,
        }


        df["Price (excl. tax)"] = (
            df["Price (excl. tax)"]
            .str.replace("Â£", "£", regex=False)
            .str.replace("£", "", regex=False)
            .astype(float)
        )


        df["Price (incl. tax)"] = (
            df["Price (incl. tax)"]
            .str.replace("Â£", "£", regex=False)
            .str.replace("£", "", regex=False)
            .astype(float)
        )

        df["Tax"] = (
            df["Tax"]
            .str.replace("Â£", "£", regex=False)
            .str.replace("£", "", regex=False)
            .astype(float)
        )


        df["Currency"] = "Pound"
        # Convert rating text → number
        df["rating_num"] = df["Rating"].map(rating_map)

        # Apply filters
        df_filtered = df[
            (df["rating_num"] >= 4) &
            (df["Price (excl. tax)"] < 20)
        ]

        # Drop helper columns
        return df_filtered.drop(columns=["rating_num"])
