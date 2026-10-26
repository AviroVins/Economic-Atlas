"""Automatyczne kontrole jakości danych po transformacji (Lab 3).

Każda kontrola zwraca listę naruszeń; pusta lista = reguła spełniona.
CLI:  python scripts/checks.py data/processed/observations.csv   (kod wyjścia 1 przy naruszeniach)
"""
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["city", "unit_id", "indicator_code", "year", "value", "is_missing"]


def check_required_columns(df):
    return [f"brak kolumny: {c}" for c in REQUIRED if c not in df.columns]


def check_unique_key(df):
    """Warunek: jedna wartość na (unit_id, indicator_code, year)."""
    dup = df.duplicated(subset=["unit_id", "indicator_code", "year"], keep=False)
    return [f"powtórzony klucz: {r.unit_id}/{r.indicator_code}/{r.year}" for r in df[dup].itertuples()]


def check_known_units(df, expected_units):
    """Warunek: tylko jednostki z config/cities.json."""
    bad = set(df["unit_id"].astype(str)) - set(map(str, expected_units))
    return [f"nieznana jednostka: {u}" for u in sorted(bad)]


def check_non_negative(df):
    """Warunek: wskaźniki w projekcie (stopy, liczby, kwoty) nie mogą być ujemne."""
    neg = df[df["value"].notna() & (df["value"] < 0)]
    return [f"ujemna wartość: {r.unit_id}/{r.indicator_code}/{r.year}={r.value}" for r in neg.itertuples()]


def check_missing_flag_consistent(df):
    """Warunek: is_missing == (value jest puste). Brak danych nie oznacza zera."""
    wrong = df[df["is_missing"] != df["value"].isna()]
    return [f"niespójna flaga braku: {r.unit_id}/{r.indicator_code}/{r.year}" for r in wrong.itertuples()]


def run_checks(df, expected_units):
    problems = check_required_columns(df)
    if problems:  # dalsze kontrole wymagają kolumn
        return problems
    return (check_unique_key(df) + check_known_units(df, expected_units)
            + check_non_negative(df) + check_missing_flag_consistent(df))


def load_expected_units():
    cities = json.loads((ROOT / "config/cities.json").read_text(encoding="utf-8"))
    return [c["unit_id"] for c in cities if c["unit_id"]]


if __name__ == "__main__":
    df = pd.read_csv(sys.argv[1], dtype={"unit_id": str})
    problems = run_checks(df, load_expected_units())
    print(f"Naruszeń: {len(problems)}")
    for p in problems:
        print(" -", p)
    sys.exit(1 if problems else 0)
