"""Pobiera surowe dane BDL dla wskaźników z config/indicators.json (poziom: powiaty/miasta na prawach powiatu).

  python scripts/fetch_bdl.py --years 2019-2023            # wszystkie wskaźniki -> data/raw/
  python scripts/fetch_bdl.py --years 2023 --sample        # Lab 2: jedna próbka -> data/sample.json

Odpowiedzi API zapisywane są bez zmian (w opakowaniu z adresem, datą i nagłówkami limitów).
Istniejące pliki nie są nadpisywane bez --force (oszczędza limity zapytań).
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from bdl_client import BdlClient  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
POWIAT_LEVEL = 5


def parse_years(text: str) -> list[int]:
    if "-" in text:
        a, b = text.split("-")
        return list(range(int(a), int(b) + 1))
    return [int(x) for x in text.split(",")]


def fetch_indicator(client, ind, years):
    params = {"unit-level": POWIAT_LEVEL, "year": years}
    pages = client.get_all_pages(f"data/by-variable/{ind['var_id']}", params)
    return {"indicator": ind, "years_requested": years, "pages": pages}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--years", required=True)
    p.add_argument("--sample", action="store_true", help="tylko pierwszy wskaźnik, ostatni rok -> data/sample.json")
    p.add_argument("--force", action="store_true")
    args = p.parse_args()

    years = parse_years(args.years)
    indicators = [i for i in json.loads((ROOT / "config/indicators.json").read_text(encoding="utf-8"))
                  if i.get("var_id")]
    if not indicators:
        sys.exit("Brak wskaźników z var_id w config/indicators.json - najpierw audyt (discover.py variables).")

    client = BdlClient()
    if args.sample:
        out = ROOT / "data" / "sample.json"
        raw = fetch_indicator(client, indicators[0], [years[-1]])
        out.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Zapisano próbkę: {out}")
        return

    for ind in indicators:
        out = ROOT / "data" / "raw" / f"bdl_{ind['code']}_{ind['var_id']}.json"
        if out.exists() and not args.force:
            print(f"Pomijam (już jest): {out.name}")
            continue
        raw = fetch_indicator(client, ind, years)
        out.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Zapisano: {out.name} (stron: {len(raw['pages'])})")


if __name__ == "__main__":
    main()
