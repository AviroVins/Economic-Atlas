import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from checks import run_checks  # noqa: E402
from prepare_data import transform  # noqa: E402

FIXTURE = Path(__file__).parent / "fixtures" / "bdl_TEST_1.json"
CITIES = [{"city": "Miasto A", "unit_id": "A1"}, {"city": "Miasto B", "unit_id": "B2"}]
UNITS = ["A1", "B2"]


def test_transform_filters_dedups_and_flags_missing():
    df, stats = transform([FIXTURE], CITIES)
    assert stats["records_raw"] == 6
    assert stats["records_after_city_filter"] == 5   # powiat ZZ odrzucony
    assert stats["duplicates_dropped"] == 1
    assert len(df) == 4 and stats["missing_values"] == 1
    assert df.loc[df["is_missing"], "value"].isna().all()   # brak != 0


def test_checks_pass_on_clean_output():
    df, _ = transform([FIXTURE], CITIES)
    assert run_checks(df, UNITS) == []


def test_checks_detect_broken_copy():
    df, _ = transform([FIXTURE], CITIES)
    bad = pd.concat([df, df.iloc[[0]]], ignore_index=True)   # duplikat klucza
    bad.loc[1, "value"] = -5                                  # ujemna wartość
    bad.loc[2, "unit_id"] = "XX"                              # nieznana jednostka
    problems = run_checks(bad, UNITS)
    assert any("powtórzony klucz" in p for p in problems)
    assert any("ujemna" in p for p in problems)
    assert any("nieznana jednostka" in p for p in problems)


def test_repeatability():
    a, _ = transform([FIXTURE], CITIES)
    b, _ = transform([FIXTURE], CITIES)
    pd.testing.assert_frame_equal(a, b)
