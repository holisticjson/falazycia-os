## Główne Zasady / Ramy Logiczne (Frameworki)

*   **Myślenie > narzędzie:** Najpierw decydujesz, co ma się stać na ekranie. Dopiero potem wybierasz narzędzie.
*   **Maska = kontrola:** AI potrafi zrobić cuda, ale lubi zmieniać cały kadr. Gdy zależy Ci na realizmie, wytnij tylko to, co chcesz zabrać z AI.
*   **Jedna „kotwica” stylu:** Trzymaj stałą paletę kolorów i rodzaj światła. Dzięki temu różne modele wyglądają jak jedna produkcja.
*   **Prototyp zanim „dowożenie”:** Najpierw wersja szybka (PixVerse/Runway/CapCut), potem wersja premium (Veo/Kling + grading + sound).
*   **Dźwięk sprzedaje obraz:** Bez muzyki i SFX nawet najlepszy efekt wygląda płasko. Dźwięk to mnożnik jakości.
*   **AI MASTER 3 uczy procesu i łączenia:** Kurs nie uczy pojedynczego narzędzia, lecz tego, jak łączyć je w spójny proces.
*   **Dwa tryby korzystania z przewodnika:**
    *   **Tryb 1 (szybki):** Sprawdzasz tabelę „Mapa narzędzi” i podejmujesz decyzję w minutę.
    *   **Tryb 2 (deep):** Bierzesz konkretny workflow i odtwarzasz go krok po kroku.
*   **Pułapki i Ograniczenia (ogólne):**
    *   **ChatGPT (LLM):**
        *   Łatwo wpaść w „ładne, ale generyczne” – zawsze dodawaj kontekst, styl i ograniczenia.
        *   LLM nie „widzi” świata – dla precyzyjnej zgodności wizualnej, łącz z Gemini/Photoshop.
    *   **Sora (obraz/wideo):** Ma tendencję do ruszania każdego piksela – słabsza do wieloetapowego retuszu.
    *   **Midjourney:** Mniej „chirurgiczny” w lokalnych poprawkach niż Gemini/Photoshop.
    *   **Gemini / NanoBanana:** Nie jest to „magiczny przycisk” – im lepsza referencja i opis, tym lepsza kontrola.
    *   **Photoshop:** Łatwo utknąć w perfekcjonizmie – rób wersje robocze i dopiero potem „dowoź” jakość.
    *   **Topaz Photo AI:** Zbyt agresywne ustawienia mogą robić „plastik” – porównuj wersje.
    *   **Magnific:** Może odjechać od oryginału – świetne, gdy chcesz styl, słabsze, gdy chcesz 100% wierności.
    *   **Higgsfield:** To nie zastępuje montażu – efekt trzeba wkomponować.
    *   **Veo (Veo 3.1):** Czasami ignoruje fragment prompta – nie masz 100% kontroli.
    *   **Kling (Kling 2.6):** Brak ścieżki lektorskiej/lipsyncu – to narzędzie od obrazu, nie od mówienia.
    *   **Runway:** Model często zmienia cały kadr, nie lokalnie – maskowanie to obowiązek.
    *   **PixVerse:** Czasem mniej „filmowe” niż Veo/Kling – dobry jako szybki szkic.
    *   **HeyGen:** Restrykcje wizerunkowe i prawne – narzędzie pilnuje bezpieczeństwa (nie zrobisz nielegalnych „ambasadorów”).
    *   **ElevenLabs:** Jakość rośnie wraz z jakością tekstu i intencją – pisz tekst jak do człowieka, nie jak do robota.
    *   **Suno:** Nie zawsze to „final” – traktuj jako ghost-producenta: wybierasz najlepszy szkic i dopracowujesz.
    *   **Descript:** Traktuj jako narzędzie do przyspieszania, nie „zastępnik” pełnego montażu.
    *   **Wtyczka „YouTube Summary”:** Sprawdzaj kontekst – streszczenia są świetne, ale czasem warto zajrzeć do źródła.
    *   **ComfyUI:** Na starcie: brakujące nody i błędy są normalne – trzeba doinstalować komponenty.

## Gotowe Schematy, Prompty i Szablony

### Szybkie wybory - które narzędzie do czego?

*   **Chcę hiperrealistyczny key visual / kampanię:** `Midjourney -> Gemini (retusz) -> Topaz/Magnific`
*   **Chcę styl/plakat/klimat artystyczny:** `Sora -> Photoshop (napisy/logotypy) -> Topaz`
*   **Chcę realistyczny packshot produktu:** `Gemini/NanoBanana -> Photoshop -> Topaz`
*   **Chcę filmowy klip z ruchem kamery:** `Veo lub Kling -> Premiere/DaVinci (montaż)`
*   **Chcę morfing A->B (przemiana):** `Sora (klatki) -> Kling Frame-to-Frame -> montaż`
*   **Chcę dodać efekt (np. wybuch):** `Higgsfield -> montaż + SFX`
*   **Chcę awatara mówiącego w wielu językach:** `ChatGPT (skrypt) -> ElevenLabs -> HeyGen -> montaż`
*   **Chcę muzykę do reels/filmu:** `Suno (szkice) -> montaż / miks (głośności)`
*   **Chcę robić za free lokalnie:** `ComfyUI -> (opcjonalnie) Topaz/Magnific`

### Wejście/Wyjście dla narzędzi (Input/Output Frameworks)

*   **ChatGPT (LLM):**
    *   **Wejście:** opis celu + kontekst + przykłady.
    *   **Wyjście:** scenariusze, prompty, checklisty, warianty.
*   **Sora (obraz/wideo):**
    *   **Wejście:** prompt + ewentualnie obraz referencyjny.
    *   **Wyjście:** obraz lub klip, często mocno „artystycznie” interpretowany.
*   **Midjourney:**
    *   **Wejście:** prompt + referencje.
    *   **Wyjście:** obrazy w stylistyce kampanii, gotowe jako baza do dalszej pracy.
*   **Gemini / NanoBanana:**
    *   **Wejście:** obraz + instrukcje.
    *   **Wyjście:** wersje zdjęcia o wysokiej spójności.
*   **Photoshop:**
    *   **Wejście:** klatki/obrazy.
    *   **Wyjście:** gotowe assety (PNG/PSD) do montażu i animacji.
*   **Topaz Photo AI:**
    *   **Wejście:** obraz.
    *   **Wyjście:** wyższa jakość, większa rozdzielczość, czystszy detal.
*   **Magnific (przez Freepik):**
    *   **Wejście:** obraz.
    *   **Wyjście:** wersja o mocniej „wymyślonych” detalach i teksturach.
*   **Higgsfield:**
    *   **Wejście:** klatka/klip + preset/prompt.
    *   **Wyjście:** klip z efektem do użycia na timeline.
*   **Veo (Veo 3.1):**
    *   **Wejście:** prompt (i ewentualnie referencje).
    *   **Wyjście:** klip wideo.
*   **Kling (Kling 2.6):**
    *   **Wejście:** prompt + obrazy (frame-to-frame / reference).
    *   **Wyjście:** klip.
*   **Runway:**
    *   **Wejście:** klip/obraz + prompt.
    *   **Wyjście:** nowy klip.
*   **PixVerse:**
    *   **Wejście:** obraz/prompt.
    *   **Wyjście:** krótki klip.
*   **HeyGen:**
    *   **Wejście:** wideo/zdjęcie + audio/tekst + asset produktu.
    *   **Wyjście:** gotowy klip z awatarem/lipsyncem.
*   **ElevenLabs:**
    *   **Wejście:** tekst + ustawienia głosu.
    *   **Wyjście:** audio WAV/MP3.
*   **Suno:**
    *   **Wejście:** tekst (lub opis) + styl.
    *   **Wyjście:** utwór, warianty aranżu.
*   **Descript:**
    *   **Wejście:** materiał wideo/audio.
    *   **Wyjście:** oczyszczona wersja, poprawki dialogu, eksport.
*   **Wtyczka „YouTube Summary”:**
    *   **Wejście:** link/strona filmu.
    *   **Wyjście:** transkrypt + streszczenie.
*   **ComfyUI:**
    *   **Wejście:** modele + workflow.
    *   **Wyjście:** obrazy/wideo/audio lokalnie.

### Szablony promptów i briefów

#### Szablon 1: prompt do wideo (Veo/Kling/Sora 2)

```
Opis sceny: [co widzimy, gdzie, pora dnia].
Postać/obiekt: [kto/co, wygląd, strój].
Akcja: [co się dzieje].
Kamera: [typ ujęcia, ruch, obiektyw, tempo].
Światło: [kierunek, miękkość, klimat].
Styl: [filmowy/komercyjny/dokumentalny], [referencje].
Ograniczenia: [czego NIE robić].
```
*   **TIP:** Największa różnica w jakości: konkret kamery i światła. Zawsze dopisuj ruch kamery i rodzaj światła.

#### Szablon 2: brief reklamy produktu (ChatGPT)

```
Produkt: [nazwa, kategoria, cena].
Odbiorca: [dla kogo, co go boli].
Obietnica: [co zmienia się po zakupie].
Dowód: [dlaczego to działa - funkcja, fakt, demo].
Estetyka: [premium/minimal/energetyczna], [paleta], [światło].
Format: [Reels 15s / 30s / 60s], [pion/poziom].
CTA: [co dokładnie ma zrobić widz].
```
*   **TIP:** Poproś ChatGPT o 3 wersje: spokojną, dynamiczną i „premium”. Potem wybierasz jedną i dopiero wtedy dopieszczasz.

## Konkretne Instrukcje "Krok po Kroku"

### Reklama produktu w 60-90 minut

*   **Cel:** Zrobić krótką reklamę (5-10 s) z packshotem, ruchem kamery, efektem i dopiętym dźwiękiem.
*   **Kroki:**
    1.  **ChatGPT:** brief reklamy + 3 warianty prompta (kamera, światło, emocja).
    2.  **Gemini/NanoBanana:** dopracuj packshot (tło, refleksy, kolor, etykieta).
    3.  **Topaz** lub **Magnific:** podbij jakość kluczowego kadru.
    4.  **Veo** lub **Kling:** wygeneruj ujęcie wideo (text-to-video lub image-to-video).
    5.  **Higgsfield:** dołóż efekt (np. wybuch, światło, motion).
    6.  **ElevenLabs:** lektor + 2 wersje intonacji.
    7.  **Suno** lub **Artlist:** podkład + dopasowanie tempa.
    8.  **Premiere/DaVinci/CapCut:** montaż, color matching, eksport.
*   **TIP:** **Maskuj:** AI robi tło/efekt, a to co ma być „Twoje” (twarz/produkt/napisy) trzymaj pod kontrolą w Photoshopie lub na timeline.

### Transformacja „przed/po” (morfing)

*   **Cel:** Płynne przejście z jednego wyglądu/sceny w drugi (np. zwykły kadr -> cyberpunk).
*   **Kroki:**
    9.  **Sora:** wygeneruj klatkę A i klatkę B (start i meta).
    10. **Kling Frame-to-Frame:** zrób morfing A -> B z filmowym ruchem.
    11. **Premiere/DaVinci:** dodaj dźwięk przejścia + speed ramp (jeśli potrzebujesz).
*   **TIP:** Najlepszy morfing wychodzi, gdy klatki A i B mają podobną kompozycję (pozycja postaci, kąt kamery).

### Vlog ze zdjęć, które zaczynają żyć

*   **Cel:** Zmontować story/reels z animowanych zdjęć (uczucie „żywej fotografii").
*   **Kroki:**
    12. **Midjourney** lub **Gemini:** przygotuj spójny zestaw zdjęć w jednym stylu.
    13. **PixVerse:** animuj każde zdjęcie krótkim ruchem (2-4 s).
    14. **CapCut/Premiere:** montaż pod muzykę, napisy, rytm.
    15. **Suno/Artlist:** muzyka, a na końcu mastering głośności.
*   **TIP:** Najpierw rytm (montaż), dopiero potem „fajne efekty”.

### „Wysadzanie” sceny w stylu filmu akcji

*   **Cel:** Dodać mocny efekt (wybuch, pył, uderzenie) do istniejącego ujęcia.
*   **Kroki:**
    16. **Higgsfield:** wybierz preset efektu i wygeneruj klip pod Twoje ujęcie.
    17. **Premiere/DaVinci:** color match, blend mode, maska, tracking jeśli trzeba.
    18. **Z-Artist / biblioteka SFX:** dopasuj dźwięk (impact, rumble, debris).
*   **TIP:** Bez dźwięku efekt wygląda jak „naklejka”. Najpierw sound design, potem dopieszczaj obraz.

### Reklama, w której mówisz awatarem (wiele języków)

*   **Cel:** Nagranie, które sprzedaje, ale Ty nie nagrywasz od nowa każdej wersji językowej.
*   **Kroki:**
    19. **ChatGPT:** skrypt + 3 warianty (krótki, normal, dynamiczny).
    20. **ElevenLabs:** głos (lub dubbing) w wybranych językach.
    21. **HeyGen:** avatar + lipsync + eksport wideo.
    22. **Premiere/CapCut:** B-roll z Veo/Kling + napisy + CTA.
*   **TIP:** Najpierw dopracuj jedną wersję „master”, dopiero potem tłumacz i klonuj format.

### Fashion / kampania z jednym spójnym lookiem

*   **Cel:** Spójne wizualnie kadry w stylu kampanii premium.
*   **Kroki:**
    23. **Midjourney:** wygeneruj key visual + 6 wariantów kadru.
    24. **Gemini:** lokalny retusz (światło, tekstura, tło).
    25. **Topaz/Magnific:** finalna jakość.
    26. **Kling** lub **Runway:** animacja (ruch kamery, delikatny motion).
    27. **Premiere/DaVinci:** color grading i montaż.
*   **TIP:** Trzymaj 1-2 „kotwice stylu”: paleta kolorów i rodzaj światła. Reszta może się zmieniać.

### Multi-elements: Ty + produkt + konkretne miejsce

*   **Cel:** Realistyczny kadr, w którym łączysz kilka elementów (np. Twoje zdjęcie + produkt + Nowy Jork).
*   **Kroki:**
    28. **Gemini/NanoBanana:** połącz elementy w jednym spójnym kadrze (światło, perspektywa).
    29. **Photoshop:** dopnij maski i drobne poprawki.
    30. **Veo / Kling:** zrób krótkie ujęcie z ruchem kamery.
    31. **Premiere:** dodaj napisy i dźwięk.
*   **TIP:** Największa różnica w realizmie to: cień pod produktem + spójny kierunek światła.

### Klip muzyczny AI w 1 wieczór

*   **Cel:** Utwór + kilka ujęć pod beat i klimat.
*   **Kroki:**
    32. **Suno:** wygeneruj 5 wersji utworu; wybierz najlepszą.
    33. **ChatGPT:** lista ujęć (storyboard 6-10 scen).
    34. **Veo/Kling/Sora 2:** wygeneruj klipy do każdej sceny.
    35. **Premiere:** montaż na beat, przejścia, mastering głośności.
*   **TIP:** Zanim wygenerujesz 10 ujęć, zrób 2 i sprawdź, czy styl się trzyma.

### Praca „za free” lokalnie: ComfyUI

*   **Cel:** Generować bez limitów, na własnym sprzęcie.
*   **Kroki:**
    36. Zainstaluj **ComfyUI** i pobierz podstawowe modele (zgodnie z lekcją).
    37. Uruchom gotowy workflow i przejdź go krok po kroku.
    38. Doinstaluj brakujące nody, gdy pojawi się błąd.
    39. Eksportuj obrazy/klipy i dopnij jakość **Topaz/Magnific**.
*   **TIP:** Traktuj **ComfyUI** jak „studio”: raz złożysz workflow, potem tylko wymieniasz wejścia.

### Color matching, czyli „żeby to wyglądało jak jedno”

*   **Cel:** Połączyć AI ujęcia i realne ujęcia w spójną całość.
*   **Kroki:**
    40. Wybierz ujęcie referencyjne (najlepsze światło).
    41. Na pozostałych ujęciach: dopasuj ekspozycję, kontrast i temperaturę.
    42. Dodaj wspólne „spoiwo”: ziarno, lekka winieta, delikatny LUT.
*   **TIP:** Najpierw wyrównaj jasność (exposure), dopiero potem kolor. Inaczej będziesz gonić własny ogon.

### Krótkie video z obrazów (prototyp reklamy)

*   **Cel:** Szybki prototyp: czy pomysł działa zanim zrobisz finalną wersję.
*   **Kroki:**
    43. **Midjourney/Nano Banana Pro:** 3 kluczowe kadry kampanii.
    44. **PixVerse/Runway:** animuj kadry w krótkie klipy.
    45. **CapCut:** zmontuj w 15-30 s, dodaj napisy, muzykę.
*   **TIP:** Prototyp ma być brzydki, ale czytelny. Liczy się przekaz, nie perfekcja.

### Workflow „bezpieczna twarz”

*   **Cel:** Maksymalny realizm: AI robi tło/ubranie/efekt, a twarz zostaje Twoja.
*   **Kroki:**
    46. Wygeneruj ujęcie/klip w **Runway/Kling/Sora 2** (nie przejmuj się twarzą).
    47. W **Photoshopie** lub w montażu: wytnij i podmień twarz z realnego ujęcia (maskowanie).
    48. Dopasuj kolor i dodaj lekki motion blur/ziarno.
*   **TIP:** To jest najszybsza droga do „wow”: realizm bierze się z kontrolowanych detali.

### Postprodukcja - checklista końcowa

*   Czy jasność/kontrast są spójne między ujęciami? (najpierw exposure, potem kolor)
*   Czy jest wspólne „spoiwo”: ziarno / delikatny LUT / winieta?
*   Czy wideo ma rytm? (cięcia pod beat i intencję)
*   Czy napisy są czytelne na telefonie? (test na małym ekranie)
*   Czy audio ma porządek: lektor na wierzchu, muzyka niżej, SFX punktowo?
*   Czy CTA jest jasne i pojawia się wystarczająco wcześnie?
*   Czy eksport jest ustawiony pod platformę (pion/poziom, bitrate, fps)?