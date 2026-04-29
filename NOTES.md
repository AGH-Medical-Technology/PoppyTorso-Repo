## Notatki o stanie prac (problemów) 
Stan na koniec kwietnia 2026

### Co udało się zrobić
- Edycja metody inicjalizacji poppy-torso w bibliotece pypot jak aby ponowne uruchomienie tego samego kodu na tym samym kernelu nie powodowało błędów.
- Edycja metody otwarzającej ruchy w bibliotece tak aby możliwe było omijanie serwomotorów o konkretnych nazwach.  Co jest używane aby omijać spinanie serwa 'head_y' przy wykoywaniu ruchów.
- Podłączono do robota kamerkę i udało się nie zrobić i zapisać przykładowe kilka zdjęć.

Używamy biblioteki pypot (tej od twórców orginalnego projektu poppy) ale z wprowadzonymi drobnymi dodatkami zapisanej w zbiorze bibliotek robota jako pypotedited. 
Kod zedytowanej biblioteki różnież dodano na repo w folderze pypotedited.

### Co jest lub bywa nie tak:
- Hotspot się wyłącza z losowych powodów (dlaczego? jak temu przciwdziałać?)
- Błędy przy inicjalizaci poppy - opisano w for_show.ipynb
- Coś jest nie tak z serwomotorem 'head_y'

Serwo 'head_y' przy spinaniu go pochyla głowę robota do przodu (bardzo agresywnie) oraz źle odtwarza lub też odczytuje swoją pozycje. Może jakby inaczej odczytywało tą samą swoją pozycje jak jest luźne a jak jest spięte.

### Inne bardziej konktetnie rzeczy do naprawy:
- Działanie EVE eyes, tak żeby się nie psuło ich wyłączanie
- Pobieranie czasu ruchu z pliku .move 

### Co można robić dalej (zachęcam do własnych pomysłów):
- Zabawa z kamerką - przetwarzanie robionych zdjęć jakoś
- Przeniesienie niektórych działać na wątek w tle - np. to wyświetlanie oczu
- 