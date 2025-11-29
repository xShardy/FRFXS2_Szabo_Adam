# Körökre osztott harcrendszer – Python / Tkinter

**Hallgató neve:** Szabó Ádám  
**Beadandó:** Körökre osztott harcrendszer grafikus felülettel, saját modulokkal, osztályokkal és eseménykezeléssel.

**Megjegyzés:** A feladat egy több részből álló grafikus alkalmazás, és nem egy ültő helyben készült el, ezért a kódban kommentek találhatók.



## Feladat leírása

A program egy egyszerű, körökre osztott harcrendszert valósít meg, ahol a játékos egy varázslót irányít, aki három különböző képességgel támadhat a boss ellen.

A harc működése:

- A varázsló és a boss felváltva cselekszenek.
- A varázsló d20-al dob, és 10 vagy nagyobb dobás esetén eltalálja a bosst.
- A boss d20-al dob, és 7 vagy nagyobb dobás esetén találja el a varázslót.
- A varázslónak három spell áll rendelkezésére, mindegyik más sebzéssel és cooldownnal.
- A varázsló használhat **gyógyitalt**, amely +10 életerőt tölt vissza (maximum 65-ig), és két alkalommal használható.
- A grafikus felületen megjelenik:
  - varázsló és boss képe,
  - HP csíkok,
  - dobások eredménye,
  - központi log üzenet,
  - külön körnapló, amely az utolsó 3 kör eseményét mutatja,
  - spell ikonok cooldown visszaszámlálással,
  - gyógyital ikon mennyiségi kijelzéssel.

A grafikus felületet a **Tkinter** modul biztosítja.



## Modulok

### **1. `main.py`**
A program indítófájlja.

Feladatai:
- létrehozza az alap Tkinter ablakot (`root`),
- létrehozza a program példányát (`app`),
- elindítja a grafikus főciklust.

A fájl nem tartalmaz játékmeneti logikát.



### **2. `harc_sza_gui.py`**
A teljes grafikus felületet és a játék logikáját tartalmazza.

Fő funkciói:
- GUI elemek inicializálása és elhelyezése,
- HP csíkok frissítése,
- varázsló körének kezelése,
- boss körének kezelése,
- cooldown rendszer működtetése,
- gyógyital használata,
- dobások eredményének megjelenítése,
- körnapló frissítése (utolsó 3 esemény),
- képek szürkére alakítása cooldown alatt.

Fontos metódusai:
- `varazslo_kor()`
- `boss_kor()`
- `hasznal_gyogyital()`
- `update_spell_buttons()`
- `update_potion_button()`
- `update_hp_bars()`
- `add_log_esemeny()`
- `update_turn_log()`
- `make_grey()`



### **3. `sza_harc_modul.py`**
A saját készítésű segédmodul.

Tartalma:
- `VARAZSLO_MAX_HP = 65`  
- `BOSS_MAX_HP = 100`  
- `sza_dob_kocka(kockak_szama, oldalak)` – saját függvény dobókockák dobásához.

Ez a modul végzi a kockadobásokat és tárolja a HP konstansokat.

## Osztályok

### **`SzaHarcJatek`**
A program fő osztálya, amely a teljes grafikus felületet és játékmenetet vezérli.

Feladatai:
- Tkinter GUI létrehozása és kezelése,
- képek, gombok és HP csíkok megjelenítése,
- a varázsló és a boss köreinek feldolgozása,
- spell cooldown rendszer működtetése,
- dobások és sebzések kezelése,
- gyógyital használata,
- körnapló frissítése,
- gombnyomások kezelése (eseménykezelés).

Az osztály elkülöníti a grafikus réteget a matematikai/kockadobási logikától.


## Futtatás

A program indítása a főmodul segítségével történik:

```bash
python3 main.py
