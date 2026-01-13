import json
import pandas as pd

class BookTransformer(Transformer):

    def load_data(self) -> pd.DataFrame:
        with open(f"{config['RAW_DIRECTORY']}/data.json", "r", encoding="utf-8") as f:
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

        df["rating_num"] = df["Rating"].map(rating_map)
        df["price"] = (
            df["Price (incl. tax)"]
            .str.replace("£", "", regex=False)
            .astype(float)
        )

        return df[
            (df["rating_num"] >= 4) &
            (df["price"] < 20)
        ].drop(columns=["rating_num", "price"])
