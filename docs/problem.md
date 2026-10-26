# Problem projektu

## Użytkownik i decyzja
Osoba rozważająca przeprowadzkę, studia lub pracę w innym mieście wojewódzkim (także student/absolwent
zaczynający karierę). Decyzja: **które miasta warto rozważyć w pierwszej kolejności ze względu na
sytuację ekonomiczną**, zanim użytkownik zacznie szczegółową, własną analizę. *(doprecyzować na zajęciach)*

## Obecna trudność
Dane o wynagrodzeniach, bezrobociu, przedsiębiorczości i finansach samorządów są rozproszone;
użytkownik sam zestawia wskaźniki, a rankingi opierają się na różnych, często niejawnych kryteriach.

## Zakres problemu
Pierwsza wersja: 18 miast wojewódzkich, 4-6 wskaźników ekonomicznych z GUS BDL, wspólny zakres lat.
Poza zakresem: logowanie, dane płatne, wszystkie miasta Polski, ocena jakości życia.

## Potrzebne dane
Zob. tabela potrzeb informacyjnych poniżej oraz [docs/data.md](data.md).

## Założenia i pytania otwarte
- Które wskaźniki BDL są dostępne dla miast na prawach powiatu w tych samych latach? (audyt)
- Czy wynagrodzenia są dostępne na poziomie miasta, czy tylko wyżej? (audyt)
- Czy prowadzący wymaga konkretnego silnika bazy (Oracle PL/SQL vs PostgreSQL)? (zapytać)
- Czy modele AI mają być elementem produktu, czy narzędziem pomocniczym? (zapytać)

## Wymagania
| ID | Wymaganie | Kryterium sprawdzenia | Źródło lub uzasadnienie | Status | Osoba |
|----|-----------|-----------------------|-------------------------|--------|-------|
| R1 | Użytkownik powinien zobaczyć porównanie 18 miast według jawnie opisanych wskaźników | Dla każdej z 18 jednostek istnieje wartość lub jawne oznaczenie braku | rozmowa / założenie projektu | założenie | login |
| R2 | Każda wartość powinna mieć źródło, rok i jednostkę | Każdy rekord w `observations.csv` da się powiązać z wskaźnikiem BDL, rokiem i jednostką | docs/data-dictionary.md | założenie | login |
| R3 | Braki danych powinny być jawnie oznaczone, a nie traktowane jak zero | Kontrola `is_missing` zgodna z pustą wartością - 0 naruszeń | docs/processing.md | założenie | login |
| R4 | Wynik indeksu powinien dać się odtworzyć z opisanej metody | Ponowne uruchomienie procedury daje identyczny wynik | docs/processing.md | założenie | login |
| R5 | Użytkownik powinien widzieć, z czego wynika wynik miasta | Składowe indeksu i wagi dostępne dla każdego miasta | założenie projektu | założenie | login |

## Potrzeby informacyjne
| Informacja | Do czego jest potrzebna? | Minimalny zakres | Format lub częstotliwość | Czy jest dostępna? |
|------------|--------------------------|------------------|--------------------------|--------------------|
| Bezrobocie (rejestrowane) | składowa indeksu | 18 miast, min. 5 lat | roczne, API BDL | do sprawdzenia |
| Podmioty gospodarcze na mieszkańca | składowa indeksu | 18 miast, min. 5 lat | roczne, API BDL | do sprawdzenia |
| Przeciętne wynagrodzenie w mieście | składowa indeksu | 18 miast, min. 5 lat | roczne | **częściowo / nie - sprawdzić poziom terytorialny** |
| Dochody/wydatki samorządu na mieszkańca | składowa indeksu | 18 miast, min. 5 lat | roczne, API BDL | do sprawdzenia |
| Granice województw i miast (GeoJSON) | mapa (później) | 16 województw, 18 punktów | jednorazowo | do sprawdzenia |
