# Körökre osztott harcrendszer – Python / Tkinter

**Hallgató neve:** Szabó Ádám   
**Beadandó:** Körökre osztott harcrendszer grafikus felülettel, saját modulokkal, osztályokkal és eseménykezeléssel.

**Megjegyzés:** A feladat tartalmaz kommenteket, mivel nem egy ültő helyemben készítettem el. 


## Feladat leírása

A program egy egyszerű, körökre osztott harcrendszert valósít meg, ahol a játékos egy varázslót irányít, aki 3 különböző képességgel támadhat a boss ellen.

A harc működése:

- A varázsló és a boss felváltva cselekszenek.
- A varázsló d20-al dob, és 10 vagy nagyobb dobás esetén eltalálja a bosst.
- A boss d20-al dob, és 7 vagy nagyobb dobás esetén találja el a varázslót.
- A varázslónak három spell áll rendelkezésére, mindegyik más sebzéssel és cooldownnal.
- A varázsló használhat **gyógyitalt** is, amely +10 életerőt tölt vissza (maximum 65-ig), és két alkalommal használható.
- A GUI-n megjelenik:
  - varázsló és boss képe,
  - HP csíkok,
  - dobás eredménye,
  - központi log üzenet,
  - az utolsó 3 kör eseménye (körnapló),
  - spell ikonok, melyeken a cooldown visszaszámolása látszik,
  - gyógyital ikon, mennyiségi kijelzéssel.

A program grafikus felületét a **Tkinter** modul biztosítja.



## Modulok

A projekt két Python modulból áll:

### **1. `harc_sza_gui.py`**
A teljes grafikus felületet és a játék logikáját tartalmazza.

Fő funkciói:
- GUI inicializálása
- HP csíkok frissítése
- Eseménykezelés (spell gomb, gyógyital gomb)
- Cooldown rendszer
- Körnapló frissítése (utolsó 3 esemény)
- Boss és varázsló körének lekezelése
- Képek szürkére alakítása cooldown esetére

Tartalmazza a következő fontos metódusokat:
- `varazslo_kor()`
- `boss_kor()`
- `hasznal_gyogyital()`
- `update_spell_buttons()`
- `update_hp_bars()`
- `add_log_esemeny()`
- `make_grey()`



### **2. `sza_harc_modul.py`**
A saját készítésű modul, benne:

- **Saját függvény:**  
  `sza_dob_kocka(kockak_szama, oldalak)`  
  → általános dobókocka függvény (pl. 1d6, 2d4, 1d20).

- **Konstansok:**  
  `VARAZSLO_MAX_HP` (65)  
  `BOSS_MAX_HP` (100)

Ez a modul felel az összes dobás és HP-érték elkülönített kezeléséért.



## Osztályok

### **`SzaHarcJatek`**
A játék fő osztálya, amely kezeli:

- Tkinter ablak létrehozása
- GUI minden eleme (képek, gombok, HP csíkok, logok)
- játékmenet logikája
- spell cooldown rendszer
- varázsló és boss körének levezénylése
- körnapló frissítése

Az osztály szerepe:

- összefogja a játék állapotát,
- eseményvezérelt működést biztosít (gombnyomás → esemény),
- elkülöníti a GUI-t a matematikai logikától (ami a modulban van).



## Futtatás

A program indítása:

```bash
python3 harc_sza_gui.py
