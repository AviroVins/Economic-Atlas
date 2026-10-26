# Atlas atrakcyjnoÅ›ci ekonomicznej polskich miast

NarzÄ™dzie analityczne porÃ³wnujÄ…ce sytuacjÄ™ ekonomicznÄ… 18 miast wojewÃ³dzkich na podstawie
publicznych danych GUS (Bank Danych Lokalnych). Indeks jest syntetycznym narzÄ™dziem porÃ³wnawczym
opracowanym na potrzeby projektu - nie jest oficjalnym wskaÅºnikiem GUS.

**ZespÃ³Å‚:** `login1`, `login2` (uzupeÅ‚niÄ‡)
**Dokumentacja:** [problem](docs/problem.md) Â· [dane i ÅºrÃ³dÅ‚a](docs/data.md) Â·
[sÅ‚ownik danych](docs/data-dictionary.md) Â· [przetwarzanie](docs/processing.md)

## Åšrodowisko (Python 3.14, VS Code)

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
python scripts/discover.py variables --name "bezrobotni"  # audyt: kandydaci wskaÅºnikÃ³w -> config/indicators.json
python scripts/fetch_bdl.py --years 2019-2023             # surowe dane -> data/raw/
python scripts/prepare_data.py data/raw data/processed/observations.csv
python scripts/checks.py data/processed/observations.csv  # kontrole jakoÅ›ci
python -m pytest                                          # testy (dane syntetyczne, bez internetu)
```

Kontrola na bÅ‚Ä™dnej kopii:
```powershell
python scripts/make_invalid_copy.py data/processed/observations.csv data/test/observations-invalid.csv
python scripts/checks.py data/test/observations-invalid.csv   # oczekiwane: naruszenia, kod wyjÅ›cia 1
```

