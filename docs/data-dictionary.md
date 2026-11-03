# Słownik danych

## Plik: `data/processed/observations.csv` (wynik przetwarzania)
| Pole | Znaczenie | Typ | Jednostka / format | Przykładowa wartość | Czy może być puste? |
|---|---|---|---|---|---|
| city | Nazwa miasta (z config/cities.json) | TEXT | brak | Białystok | nie |
| unit_id | Identyfikator jednostki w BDL | TEXT | 12 cyfr (kod TERYT/BDL) | 062013761000 | nie |
| indicator_code | Kod wskaźnika projektu | TEXT | brak | bezrobocie_rok | nie |
| year | Rok, którego dotyczy wartość | INTEGER | YYYY | 2023 | nie |
| value | Wartość wskaźnika | REAL | % | 5.208333 | tak - brak danych |
| is_missing | Czy wartość jest nieznana | BOOLEAN | true/false (pole utworzone w transformacji: `value` jest puste) | false | nie |

## Wartości pola `indicator_code`
| Kod wskaźnika | Znaczenie | Typ | Jednostka | Przykładowa wartość | Czy może być puste? |
|---|---|---|---|---|---|
| bezrobocie_01 | Stopa bezrobocia rejestrowanego - styczeń (var_id 461680) | REAL | % | 3.1 | tak |
| bezrobocie_02 | Stopa bezrobocia rejestrowanego - luty (var_id 461681) | REAL | % | 3.1 | tak |
| bezrobocie_03 | Stopa bezrobocia rejestrowanego - marzec (var_id 461682) | REAL | % | 3.0 | tak |
| bezrobocie_04 | Stopa bezrobocia rejestrowanego - kwiecień (var_id 461683) | REAL | % | 2.9 | tak |
| bezrobocie_05 | Stopa bezrobocia rejestrowanego - maj (var_id 461684) | REAL | % | 2.8 | tak |
| bezrobocie_06 | Stopa bezrobocia rejestrowanego - czerwiec (var_id 461685) | REAL | % | 2.8 | tak |
| bezrobocie_07 | Stopa bezrobocia rejestrowanego - lipiec (var_id 461686) | REAL | % | 2.8 | tak |
| bezrobocie_08 | Stopa bezrobocia rejestrowanego - sierpień (var_id 461687) | REAL | % | 2.8 | tak |
| bezrobocie_09 | Stopa bezrobocia rejestrowanego - wrzesień (var_id 461688) | REAL | % | 2.8 | tak |
| bezrobocie_10 | Stopa bezrobocia rejestrowanego - październik (var_id 461689) | REAL | % | 2.8 | tak |
| bezrobocie_11 | Stopa bezrobocia rejestrowanego - listopad (var_id 461690) | REAL | % | 2.7 | tak |
| bezrobocie_12 | Stopa bezrobocia rejestrowanego - grudzień (var_id 461691) | REAL | % | 2.8 | tak |
| bezrobocie_rok | Średnioroczna stopa bezrobocia rejestrowanego (średnia z 12 miesięcy; brak, jeśli brakuje choćby 1 miesiąca) | REAL | % | 5.208333 | tak |
| wynagrodzenie_wzgledne | Przeciętne miesięczne wynagrodzenia brutto w relacji do średniej krajowej (Polska=100, var_id 64429) | REAL | % | 99.4 | tak |

## Plik: `data/raw/bdl_*.json` (dane wejściowe)
Opakowanie: `indicator` (z config/indicators.json), `pages[].response.results[]` = odpowiedź API.
| Pole | Znaczenie | Typ | Jednostka / format | Przykładowa wartość | Czy może być puste? |
|---|---|---|---|---|---|
| results[].id | Identyfikator jednostki terytorialnej BDL | TEXT | 12 cyfr | 011212001000 | nie |
| results[].name | Nazwa jednostki | TEXT | tekst | Powiat bocheński | nie |
| results[].values[].year | Rok | TEXT | "YYYY" | "2023" | nie |
| results[].values[].val | Wartość | REAL | zależna od wskaźnika (%) | 3.1 | tak |
| results[].values[].attrId | Identyfikator atrybutu/jakości wartości | INTEGER | kod numeryczny | 1 | nie |

*Znaczenie pól potwierdzić w dokumentacji GUS - nie zakładać na podstawie samej nazwy.*
