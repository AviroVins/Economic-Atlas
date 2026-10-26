# Słownik danych

## Plik: `data/processed/observations.csv` (wynik przetwarzania)
| Pole | Znaczenie | Typ | Jednostka / format | Przykładowa wartość | Czy może być puste? |
|---|---|---|---|---|---|
| city | Nazwa miasta (z config/cities.json) | TEXT | brak | Kraków | nie |
| unit_id | Identyfikator jednostki w BDL | TEXT | 12 znaków | *(uzupełnić z próbki)* | nie |
| indicator_code | Kod wskaźnika projektu | TEXT | brak | PRZYKLAD_bezrobocie | nie |
| year | Rok, którego dotyczy wartość | INTEGER | YYYY | 2023 | nie |
| value | Wartość wskaźnika | REAL | zależna od wskaźnika | *(z próbki)* | tak - brak danych |
| is_missing | Czy wartość jest nieznana | BOOLEAN | true/false (pole utworzone w transformacji: `value` jest puste) | false | nie |

## Plik: `data/raw/bdl_*.json` (dane wejściowe)
Opakowanie: `indicator` (z config/indicators.json), `pages[].response.results[]` = odpowiedź API.
| Pole | Znaczenie | Typ | Jednostka / format | Przykładowa wartość | Czy może być puste? |
|---|---|---|---|---|---|
| results[].id | Identyfikator jednostki terytorialnej BDL | TEXT | | *(z próbki)* | nie |
| results[].name | Nazwa jednostki | TEXT | | | nie |
| results[].values[].year | Rok | TEXT | "YYYY" | "2023" | nie |
| results[].values[].val | Wartość | REAL | zależna od wskaźnika | | tak *(potwierdzić w dokumentacji)* |
| results[].values[].attrId | Identyfikator atrybutu/jakości wartości | INTEGER | | *(sprawdzić znaczenie w dokumentacji GUS)* | |

*Znaczenie pól potwierdzić w dokumentacji GUS - nie zakładać na podstawie samej nazwy.*
