"""Przetwarzanie: surowe odpowiedzi BDL (JSON) -> tabela 'długa' observations.csv.

  python scripts/prepare_data.py data/raw data/processed/observations.csv

Operacje (opisane w docs/processing.md):
 1. spłaszczenie JSON do wierszy (jednostka, wskaźnik, rok, wartość),
 2. ujednolicenie typów (rok -> liczba całkowita, wartość -> liczba; brak -> puste, NIE zero),
 3. ograniczenie do 18 miast z config/cities.json,
 4. usunięcie identycznych duplikatów,
 5. oznaczenie braków flagą is_missing.
Kontrole jakości uruchamiane są przed zapisem; przy naruszeniach plik wynikowy nie powstaje.
"""
import argparse
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from checks import run_checks  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
COLUMNS = ["unit_id", "unit_name", "indicator_code", "var_id", "year", "value", "attr_id"]


def flatten(raw: dict) -> pd.DataFrame:
    ind = raw["indicator"]
    rows = []
    for page in raw["pages"]:
        for unit in page["response"].get("results", []):
            for v in unit.get("values", []):
                rows.append({
                    "unit_id": str(unit.get("id")), "unit_name": unit.get("name"),
                    "indicator_code": ind["code"], "var_id": ind["var_id"],
                    "year": v.get("year"), "value": v.get("val"), "attr_id": v.get("attrId"),
                })
    return pd.DataFrame(rows, columns=COLUMNS)


def transform(raw_files: list[Path], cities: list[dict]):
    stats = {}
    frames = [flatten(json.loads(p.read_text(encoding="utf-8"))) for p in raw_files]
    df = pd.concat(frames, ignore_index=True)
    stats["records_raw"] = len(df)

    df["year"] = pd.to_numeric(df["year"], errors="raise").astype("int64")
    value_num = pd.to_numeric(df["value"], errors="coerce")
    stats["non_numeric_values"] = int((value_num.isna() & df["value"].notna()).sum())
    df["value"] = value_num

    city_map = {str(c["unit_id"]): c["city"] for c in cities if c["unit_id"]}
    df = df[df["unit_id"].isin(city_map)].copy()
    stats["records_after_city_filter"] = len(df)
    df["city"] = df["unit_id"].map(city_map)

    before = len(df)
    df = df.drop_duplicates().copy()
    stats["duplicates_dropped"] = before - len(df)

    df["is_missing"] = df["value"].isna()
    df = df.sort_values(["indicator_code", "city", "year"]).reset_index(drop=True)
    stats["records_final"] = len(df)
    stats["missing_values"] = int(df["is_missing"].sum())
    out = df[["city", "unit_id", "indicator_code", "year", "value", "is_missing"]]
    return out, stats


def main():
    p = argparse.ArgumentParser()
    p.add_argument("input", type=Path, help="katalog z surowymi plikami JSON lub pojedynczy plik")
    p.add_argument("output", type=Path)
    args = p.parse_args()

    if args.output.resolve() == args.input.resolve():
        p.error("Plik wynikowy musi być inny niż wejściowy")
    raw_files = sorted(args.input.glob("bdl_*.json")) if args.input.is_dir() else [args.input]
    if not raw_files:
        sys.exit("Brak plików wejściowych bdl_*.json")

    cities = json.loads((ROOT / "config/cities.json").read_text(encoding="utf-8"))
    if not any(c["unit_id"] for c in cities):
        sys.exit("Uzupełnij unit_id w config/cities.json (python scripts/discover.py units).")

    df, stats = transform(raw_files, cities)
    problems = run_checks(df, [c["unit_id"] for c in cities if c["unit_id"]])
    if problems:
        print("KONTROLE JAKOŚCI NIE PRZESZŁY:")
        for pr in problems:
            print(" -", pr)
        sys.exit(1)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)
    for k, v in stats.items():
        print(f"{k}: {v}")
    print(f"Zapisano: {args.output}")


if __name__ == "__main__":
    main()
