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
| 2 | Ujednolicenie typów (year -> int, value -> liczba) | spójność typów | wartości nienumeryczne -> puste (liczba raportowana) |
| 3 | Ograniczenie do 18 miast (po `unit_id`) | zakres projektu | odrzucone pozostałe powiaty |
| 4 | Usunięcie identycznych duplikatów | klucz musi być unikalny | *(uzupełnić liczbę po uruchomieniu)* |
| 5 | Flaga `is_missing`, bez uzupełniania braków | brak danych != 0 | puste wartości pozostają puste |

## Kontrole jakości (automatyczne, `scripts/checks.py`)
| Kontrola | Warunek poprawności |
|---|---|
| Unikalny klucz | 0 powtórzeń (unit_id, indicator_code, year) |
| Znane jednostki | wszystkie unit_id należą do config/cities.json |
| Wartości nieujemne | 0 wartości < 0 |
| Spójność flagi braków | is_missing == value jest puste |

**Próba na błędnej kopii** (`data/test/observations-invalid.csv`): oczekiwany wynik: *(uzupełnić)*; uzyskany: *(uzupełnić)*.

## Podsumowanie jakości
| Kontrola | Wynik | Działanie lub ograniczenie |
|---|---|---|
| Liczba rekordów | przed: ? po: ? | |
| Brakujące wartości | | |
| Duplikaty | | |
| Zakresy i jednostki | | |
| Powtarzalność przetwarzania | | porównanie dwóch uruchomień na tej samej próbce |

## Ograniczenia
*(decyzja, której nie można jeszcze podjąć z powodu braków danych - np. dostępność wynagrodzeń na poziomie miasta)*
