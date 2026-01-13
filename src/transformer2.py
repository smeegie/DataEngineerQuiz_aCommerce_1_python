import os, json, csv, re
from src.config import config

RATING_MAP = {"One":1,"Two":2,"Three":3,"Four":4,"Five":5}

def parse_price(s: str) -> float:
    # handles "£" and "Â£"
    s = s or ""
    s = s.replace("Â£", "£").replace("£", "")
    s = re.sub(r"[^0-9.]", "", s)
    return float(s) if s else 0.0

class BookTransformer:
    def run(self) -> None:
        os.makedirs(config["TRANSFORMED_DIRECTORY"], exist_ok=True)
        in_path = os.path.join(config["RAW_DIRECTORY"], "data.jsonl")
        out_path = os.path.join(config["TRANSFORMED_DIRECTORY"], "result.csv")

        with open(in_path, "r", encoding="utf-8") as fin, open(out_path, "w", newline="", encoding="utf-8") as fout:
            writer = None

            for line in fin:
                line = line.strip()
                if not line:
                    continue

                book = json.loads(line)

                rating = RATING_MAP.get(book.get("Rating"), 0)
                price_incl = parse_price(book.get("Price (incl. tax)"))

                if rating >= 4 and price_incl < 20:
                    if writer is None:
                        writer = csv.DictWriter(fout, fieldnames=list(book.keys()))
                        writer.writeheader()
                    writer.writerow(book)
