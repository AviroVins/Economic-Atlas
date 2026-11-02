# Przetwarzanie danych

### Dobór narzędzi
- Źródło i format danych: API REST GUS BDL, odpowiedzi JSON
- Narzędzie główne: Python 3.14 + pandas (skrypty w `scripts/`)
- Dlaczego pasuje do tego źródła i zadania: powtarzalny skrypt, łatwe testy, późniejszy import do PostgreSQL
- Narzędzie pomocnicze (jeśli potrzebne): VS Code Data Wrangler do podglądu CSV
- Wynik zapisany w repozytorium: `data/processed/observations.csv`

## Kroki
| Krok | Operacja | Powód | Wpływ na dane |
|---|---|---|---|
| 1 | Spłaszczenie JSON do wierszy | format tabelaryczny | wiersz = jednostka-wskaźnik-rok |
| 2 | Ujednolicenie typów (year -> int, value -> liczba) | spójność typów | wartości nienumeryczne -> puste (liczba raportowana: non_numeric_values: 0) |
| 3 | Ograniczenie do 18 miast (po `unit_id`) | zakres projektu | odrzucone pozostałe powiaty (z 24700 do 1170) |
| 4 | Usunięcie identycznych duplikatów | klucz musi być unikalny | 0 duplikatów (duplicates_dropped: 0) |
| 5 | Agregacja 12 miesięcy do średniej rocznej; brak roku, gdy brakuje któregokolwiek miesiąca | stabilniejszy wskaźnik roczny i szereg czasowy dla Lab 4 | 12 wierszy miesięcznych stóp bezrobocia agregowanych do 1 wiersza rocznego `bezrobocie_rok` (monthly_to_annual_rows: 90) |
| 6 | Flaga `is_missing`, bez uzupełniania braków | brak danych != 0 | puste wartości pozostają puste (missing_values: 0) |

## Kontrole jakości (automatyczne, `scripts/checks.py`)
| Kontrola | Warunek poprawności |
|---|---|
| Unikalny klucz | 0 powtórzeń (unit_id, indicator_code, year) |
| Znane jednostki | wszystkie unit_id należą do config/cities.json |
| Wartości nieujemne | 0 wartości < 0 |
| Spójność flagi braków | is_missing == value jest puste |

**Próba na błędnej kopii** (`data/test/observations-invalid.csv`):
- **Oczekiwany wynik:** naruszenia 3 rodzajów (powtórzony klucz, ujemna wartość, nieznana jednostka) i kod wyjścia 1.
- **Uzyskany wynik:** kod wyjścia `1`, wykryto `4` naruszenia (3 rodzaje błędów):
  - `powtórzony klucz: 062013761000/bezrobocie_rok/2019`
  - `powtórzony klucz: 062013761000/bezrobocie_rok/2019`
  - `nieznana jednostka: 000000000000`
  - `ujemna wartość: 062013761000/bezrobocie_rok/2020=-5.0`

## Podsumowanie jakości
| Kontrola | Wynik | Działanie lub ograniczenie |
|---|---|---|
| Liczba rekordów | records_raw: 24700, records_after_city_filter: 1170, monthly_to_annual_rows: 90, records_final: 180 | Ograniczenie do 18 miast (z 24700 do 1170), agregacja 12 miesięcy bezrobocia do wartości rocznej (90 wierszy); ostateczny plik zawiera 180 rekordów (90 bezrobocie_rok + 90 wynagrodzenie_wzgledne) |
| Brakujące wartości | missing_values: 0 (non_numeric_values: 0) | Brak braków danych w pobranym zakresie 2019–2023 dla 18 miast |
| Duplikaty | duplicates_dropped: 0 | Brak zduplikowanych rekordów w danych wejściowych |
| Zakresy i jednostki | Naruszeń: 0 | checks.py potwierdził 0 naruszeń (unikalny klucz, znane jednostki z config/cities.json, wartości nieujemne, spójność is_missing) |
| Powtarzalność przetwarzania | identyczne (0 różnic w Compare-Object, 181 wierszy w obu plikach, SHA-256 identyczny: 17F05B874B445F81C57DBDC8C0AF135767E8136E4D9BFAC1BCA19532B955FFCE) | Wynik Compare-Object zwrócił 0 różnic (porównano observations-run1.csv i observations.csv) |

## Ograniczenia
1. **Brak kwotowych danych o wynagrodzeniach w zł na poziomie miast**: W BDL na poziomie powiatów/miast na prawach powiatu (poziom 5) nie jest publikowane przeciętne miesięczne wynagrodzenie brutto w złotych (dostępne jest na poziomie podregionów NUTS 3 lub województw NUTS 2). Zamiast tego wykorzystano jedyny dostępny na poziomie 5 wskaźnik relatywny: przeciętne miesięczne wynagrodzenie brutto w relacji do średniej krajowej (`wynagrodzenie_wzgledne`, Polska=100, var_id: 64429).
2. **Agregacja roczna bezrobocia**: Stopa bezrobocia rejestrowanego w BDL publikowana jest w cyklu miesięcznym (`bezrobocie_01`–`bezrobocie_12`). W celu uzyskania spójnego szeregu rocznego na potrzeby indeksu wyliczono średnią arytmetyczną z 12 miesięcy (`bezrobocie_rok`). Zastosowano regułę konserwatywną: brak wartości w którymkolwiek miesiącu skutkuje brakiem wartości (`NaN`) dla całego roku.
3. **Krótki szereg czasowy (2019–2023)**: Zastosowano 5-letni zakres obserwacji, będący wspólnym, w pełni kompletnym okresem dostępności obu wskaźników dla wszystkich 18 miast. Stanowi to ograniczenie przy badaniu wieloletnich trendów ekonomicznych w kolejnych etapach (Lab 4).
