# Dane

## Plan pozyskania danych
| Element | Ustalenie zespołu |
|---|---|
| Źródło lub sposób pomiaru | GUS - Bank Danych Lokalnych, API REST (`bdl.stat.gov.pl/api/v1`) |
| Właściciel danych | Główny Urząd Statystyczny |
| Zakres danych | 18 miast wojewódzkich (poziom: powiat/miasto na prawach powiatu), 4-6 wskaźników |
| Okres i częstotliwość | uzupełnić po audycie (roczne) |
| Jednostka obserwacji | miasto-rok-wskaźnik |
| Dobór obserwacji i liczebność próby | wszystkie 18 jednostek, wszystkie dostępne lata z wybranego zakresu |
| Sposób pobrania | `python scripts/fetch_bdl.py --years ...` (parametry zapisane w pliku surowym) |
| Limit, koszt lub uprawnienia | uzupełnić z dokumentacji GUS (limity zapytań, klucz opcjonalny?) |
| Licencja i zasady publikacji | uzupełnić z dokumentacji GUS; podawać "Źródło: GUS, BDL" |
| Osoba odpowiedzialna za pozyskanie | login |
| Plan awaryjny | zawęzić do wspólnych wskaźników; dane z plików eksportu BDL (CSV) zamiast API |

## Tabela źródeł
| Źródło | Co można pobrać? | Czy odpowiada potrzebom? | Dowód sprawdzenia | Braki lub ryzyko |
|---|---|---|---|---|
| GUS BDL API | wskaźniki dla powiatów/miast | do sprawdzenia | data/sample.json | limity, poziom terytorialny |
| Geoportal / PRG (drugie źródło) | granice administracyjne | do sprawdzenia | (link/plik) | format, układ współrzędnych |

## Opis wybranego źródła
| Element | Wynik sprawdzenia |
|---|---|
| Źródło i właściciel | GUS, BDL |
| Link lub sposób dostępu | https://bdl.stat.gov.pl/api/v1 + dokumentacja Swagger |
| Wymaganie, które źródło obsługuje | R1, R2 |
| Data pobrania | |
| Format i kodowanie | JSON, UTF-8 |
| Liczba rekordów w próbce | |
| Nazwy pól i ich znaczenie | zob. data-dictionary.md |
| Format dat i jednostki | rok jako tekst "2023"; jednostka zależna od wskaźnika |
| Brakujące wartości lub rekordy | |
| Limit zapytań, klucz i koszt | |
| Licencja i ograniczenia wykorzystania | |
| Próba ponownego pobrania | wykonano / nie wykonano; wynik: |
| Brakujące dane | |
| Plan awaryjny | eksport CSV z BDL |
| Wybrany pomysł realizacji | skrypt Python pobierający dane z API + przetwarzanie pandas |
| Odrzucony pomysł i powód | ręczne pobieranie plików z portalu (niepowtarzalne); *(dodać kolejny: np. wszystkie miasta Polski - brak porównywalnych danych / zbyt duży zakres)* |
