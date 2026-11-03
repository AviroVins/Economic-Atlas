"""Tworzy celowo błędną kopię wyniku w data/test/ (do wykazania, że kontrole działają).

  python scripts/make_invalid_copy.py data/processed/observations.csv data/test/observations-invalid.csv
  python scripts/checks.py data/test/observations-invalid.csv     # oczekiwane: naruszenia 3 rodzajów (duplikat, ujemna wartość, nieznana jednostka), kod wyjścia 1
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import pandas as pd

src, dst = sys.argv[1], sys.argv[2]
df = pd.read_csv(src, dtype={"unit_id": str})
bad = pd.concat([df, df.iloc[[0]]], ignore_index=True)           # 1) zdublowany klucz
bad.loc[bad.index[1], "value"] = -5                               # 2) ujemna wartość
bad.loc[bad.index[2], "unit_id"] = "000000000000"                 # 3) nieznana jednostka
bad.to_csv(dst, index=False)
print(f"Zapisano błędną kopię: {dst}")
