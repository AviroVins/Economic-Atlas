# Atlas atrakcyjności ekonomicznej polskich miast

Narzędzie analityczne porównujące sytuację ekonomiczną 18 miast wojewódzkich na podstawie
publicznych danych GUS (Bank Danych Lokalnych). Indeks jest syntetycznym narzędziem porównawczym
opracowanym na potrzeby projektu - nie jest oficjalnym wskaźnikiem GUS.

**Zespół:** `login1`, `login2` (uzupełnić)
**Dokumentacja:** [problem](docs/problem.md) · [dane i źródła](docs/data.md) ·
[słownik danych](docs/data-dictionary.md) · [przetwarzanie](docs/processing.md)

## Środowisko (Python 3.14, VS Code)

```powershell
python -m venv .EA
.EA\Scripts\Activate.ps1          # macOS/Linux: source .EA/bin/activate
python -m pip install -r requirements.txt
```
W VS Code: Ctrl+Shift+P -> *Python: Select Interpreter* -> wybierz `.EA`.
Opcjonalnie: skopiuj `.env.example` do `.env` i wpisz `BDL_CLIENT_ID` (klucz nie trafia do repozytorium).

## Uruchomienie przetwarzania

```powershell
python scripts/discover.py units                          # audyt: kandydaci id miast -> config/cities.json
python scripts/discover.py variables --name "bezrobotni"  # audyt: kandydaci wskaźników -> config/indicators.json
python scripts/fetch_bdl.py --years 2019-2023             # surowe dane -> data/raw/
python scripts/prepare_data.py data/raw data/processed/observations.csv
python scripts/checks.py data/processed/observations.csv  # kontrole jakości
python -m pytest                                          # testy (dane syntetyczne, bez internetu)
```

Kontrola na błędnej kopii:
```powershell
python scripts/make_invalid_copy.py data/processed/observations.csv data/test/observations-invalid.csv
python scripts/checks.py data/test/observations-invalid.csv   # oczekiwane: naruszenia, kod wyjścia 1
```
