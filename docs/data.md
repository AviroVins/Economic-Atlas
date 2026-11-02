# Dane

## Plan pozyskania danych
| Element | Ustalenie zespołu |
|---|---|
| Źródło lub sposób pomiaru | GUS - Bank Danych Lokalnych, API REST (`bdl.stat.gov.pl/api/v1`) |
| Właściciel danych | Główny Urząd Statystyczny |
| Zakres danych | 18 miast wojewódzkich (poziom: powiat/miasto na prawach powiatu), 4-6 wskaźników |
| Okres i częstotliwość | 2019–2023 (roczne) |
| Jednostka obserwacji | miasto-rok-wskaźnik |
| Dobór obserwacji i liczebność próby | wszystkie 18 jednostek, wszystkie dostępne lata z wybranego zakresu |
| Sposób pobrania | `python scripts/fetch_bdl.py --years 2019-2023` (parametry: `--years 2019-2023`, `unit-level 5`; data pobrania: 2026-11-03; pobrano 13 plików `bdl_*.json` do `data/raw/`) |
| Limit, koszt lub uprawnienia | nie sprawdzono – wymaga weryfikacji w dokumentacji GUS / Swagger (zostanie dodane w późniejszym etapie) |
| Licencja i zasady publikacji | nie sprawdzono – wymaga weryfikacji w regulaminie GUS (zostanie dodane w późniejszym etapie; podawać "Źródło: GUS, BDL") |
| Osoba odpowiedzialna za pozyskanie | Maja |
| Plan awaryjny | zawęzić do wspólnych wskaźników; dane z plików eksportu BDL (CSV) zamiast API |

## Tabela źródeł
| Źródło | Co można pobrać? | Czy odpowiada potrzebom? | Dowód sprawdzenia | Braki lub ryzyko |
|---|---|---|---|---|
| GUS BDL API | wskaźniki dla powiatów/miast | tak | data/raw/sample.json | limity, poziom terytorialny |
| Geoportal / PRG (drugie źródło) | granice administracyjne | zostanie dodane w późniejszym etapie (etap mapy) | do weryfikacji w późniejszym etapie | format, układ współrzędnych |

## Opis wybranego źródła
| Element | Wynik sprawdzenia |
|---|---|
| Źródło i właściciel | GUS, BDL |
| Link lub sposób dostępu | https://bdl.stat.gov.pl/api/v1 + dokumentacja Swagger |
| Wymaganie, które źródło obsługuje | R1, R2 |
| Data pobrania | 2026-11-02 |
| Format i kodowanie | JSON, UTF-8 |
| Liczba rekordów w próbce | 380 rekordów jednostek (totalRecords=380, 4 strony w pages, 380 wartości val dla roku 2023) |
| Nazwy pól i ich znaczenie | Opakowanie: `indicator` (definicja wskaźnika), `years_requested` (żądane lata), `pages` (strony z API: `request_url`, `retrieved_at`, `rate_limit_headers`, `response`). Odpowiedź API: `totalRecords`, `links`, `variableId`, `measureUnitId`, `aggregateId`, `lastUpdate`, `results` (`id` - 12-znakowy kod jednostki BDL, `name` - nazwa powiatu/miasta, `values` z polami `year` - rok, `val` - wartość wskaźnika, `attrId` - identyfikator atrybutu/jakości); szczegółowe znaczenia do potwierdzenia w dokumentacji BDL |
| Format dat i jednostki | rok jako tekst "2023" (typ str); jednostka miary: % (measureUnitId=50) |
| Brakujące wartości lub rekordy | 0 wartości null na 380 obserwacji w próbce; brak brakujących rekordów |
| Limit zapytań, klucz i koszt | nie sprawdzono (wymaga weryfikacji w oficjalnej dokumentacji GUS / Swagger) |
| Licencja i ograniczenia wykorzystania | nie sprawdzono (wymaga weryfikacji w regulaminie / dokumentacji GUS) |
| Próba ponownego pobrania | wykonano; wynik: zawartość odpowiedzi API (response) w 100% identyczna (zgodność payloadu), różnią się wyłącznie znaczniki czasu retrieved_at w metadanych |
| Brakujące dane | 0 braków w próbce dla roku 2023 (380/380 wypełnionych wartości val) |
| Plan awaryjny | eksport CSV z BDL |
| Wybrany pomysł realizacji | skrypt Python pobierający dane z API + przetwarzanie pandas |
| Odrzucony pomysł i powód | ręczne pobieranie plików z portalu (niepowtarzalne); *(dodać kolejny: np. wszystkie miasta Polski - brak porównywalnych danych / zbyt duży zakres)* |

## Sprawdzenie ID w BDL
| ID zmiennej | Nazwa zwrócona przez API | Poziom (level) | Jednostka miary | Dostępne lata | Status weryfikacji |
|---|---|---|---|---|---|
| 461680 | styczeń - stopa bezrobocia rejestrowanego | 5 | % | 2011–2026 | Zgodny (oczekiwano poziom 5, %) |
| 461681 | luty - stopa bezrobocia rejestrowanego | 5 | % | 2011–2026 | Zgodny (oczekiwano poziom 5, %) |
| 461682 | marzec - stopa bezrobocia rejestrowanego | 5 | % | 2011–2026 | Zgodny (oczekiwano poziom 5, %) |
| 461683 | kwiecień - stopa bezrobocia rejestrowanego | 5 | % | 2011–2026 | Zgodny (oczekiwano poziom 5, %) |
| 461684 | maj - stopa bezrobocia rejestrowanego | 5 | % | 2011–2026 | Zgodny (oczekiwano poziom 5, %) |
| 461685 | czerwiec - stopa bezrobocia rejestrowanego | 5 | % | 2011–2026 | Zgodny (oczekiwano poziom 5, %) |
| 461686 | lipiec - stopa bezrobocia rejestrowanego | 5 | % | 2011–2026 | Zgodny (oczekiwano poziom 5, %) |
| 461687 | sierpień - stopa bezrobocia rejestrowanego | 5 | % | 2011–2026 | Zgodny (oczekiwano poziom 5, %) |
| 461688 | wrzesień - stopa bezrobocia rejestrowanego | 5 | % | 2011–2026 | Zgodny (oczekiwano poziom 5, %) |
| 461689 | październik - stopa bezrobocia rejestrowanego | 5 | % | 2011–2025 | Zgodny (oczekiwano poziom 5, %) |
| 461690 | listopad - stopa bezrobocia rejestrowanego | 5 | % | 2011–2025 | Zgodny (oczekiwano poziom 5, %) |
| 461691 | grudzień - stopa bezrobocia rejestrowanego | 5 | % | 2011–2025 | Zgodny (oczekiwano poziom 5, %) |
| 64429 | przeciętne miesięczne wynagrodzenia brutto w relacji do średniej krajowej (Polska=100) | 5 | % | 2002–2025 | Zgodny (oczekiwano poziom 5, %) |
