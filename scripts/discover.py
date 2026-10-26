"""Eksploracja katalogu BDL (audyt danych, Lab 2).

Przykłady:
  python scripts/discover.py subjects
  python scripts/discover.py variables --name bezrobotni
  python scripts/discover.py units            # kandydaci dla 18 miast z config/cities.json
Wyniki przejrzyj w BDL i potwierdź definicje w opisie wskaźnika.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from bdl_client import BdlClient  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
POWIAT_LEVEL = 5  # w BDL miasta na prawach powiatu są jednostkami poziomu "powiat" - zweryfikuj w dokumentacji


def cmd_subjects(client, args):
    data, _ = client.get("subjects", {"parent-id": args.parent_id} if args.parent_id else {})
    for s in data.get("results", []):
        print(f"{s.get('id')}\t{s.get('name')}\t(podtematy: {s.get('hasVariables')})")


def cmd_variables(client, args):
    pages = client.get_all_pages("variables/search", {"name": args.name})
    for page in pages:
        for v in page["response"].get("results", []):
            print(f"{v.get('id')}\tpoziom={v.get('level')}\t{v.get('n1')} | {v.get('n2', '')}"
                  f"\t[{v.get('measureUnitName', '')}]\ttemat={v.get('subjectId')}")


def cmd_units(client, args):
    cities = json.loads((ROOT / "config" / "cities.json").read_text(encoding="utf-8"))
    for c in cities:
        data, _ = client.get("units/search", {"name": c["city"], "level": POWIAT_LEVEL})
        print(f"\n== {c['city']}")
        for u in data.get("results", []):
            print(f"  {u.get('id')}\t{u.get('name')}\t(rodzic: {u.get('parentId')})")
    print("\nWybierz jednostkę 'miasto na prawach powiatu' (nie powiat ziemski o tej samej nazwie!)"
          " i wpisz jej id do config/cities.json.")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("subjects"); s.add_argument("--parent-id"); s.set_defaults(fn=cmd_subjects)
    v = sub.add_parser("variables"); v.add_argument("--name", required=True); v.set_defaults(fn=cmd_variables)
    u = sub.add_parser("units"); u.set_defaults(fn=cmd_units)
    args = p.parse_args()
    args.fn(BdlClient(), args)


if __name__ == "__main__":
    main()
