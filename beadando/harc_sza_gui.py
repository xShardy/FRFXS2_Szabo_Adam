import tkinter as tk
from tkinter import messagebox

from sza_harc_modul import VARAZSLO_MAX_HP, BOSS_MAX_HP, sza_dob_kocka


class SzaHarcJatek:
    """
    Varázsló vs. boss – körökre osztott harc cooldown rendszerrel, gyógyitallal és körnaplóval.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Varázsló vs Boss")

        # játékkal kapcsolatos változók
        self.varazslo_hp = VARAZSLO_MAX_HP
        self.boss_hp = BOSS_MAX_HP
        self.jatek_vege = False

        # spell cooldownok (0 = használható)
        self.cooldowns = {1: 0, 2: 0, 3: 0}

        # spell nevek
        self.spell_nevek = {
            1: "Szélpenge",
            2: "Jégzuhatag",
            3: "Meteorzápor"
        }

        # spell töltési idők körökben
        self.spell_cd_idok = {
            1: 0,
            2: 1,
            3: 2
        }

        # gyógyital mennyisége
        self.gyogyital_db = 2

        # körnapló (utolsó 3 esemény)
        self.turn_log = []

        # képek betöltése
        try:
            self.wizard_img = tk.PhotoImage(file="wizard.png")
            self.boss_img = tk.PhotoImage(file="boss.png")
            self.spell1_img = tk.PhotoImage(file="spell1.png")
            self.spell2_img = tk.PhotoImage(file="spell2.png")
            self.spell3_img = tk.PhotoImage(file="spell3.png")
            self.potion_img = tk.PhotoImage(file="potion.png")
        except Exception as e:
            messagebox.showerror("Hiba", f"Kép betöltési hiba: {e}")
            self.root.destroy()
            return

        # szürke ikonok elkészítése cooldown vagy elfogyott gyógyital esetére
        self.spell1_grey = self.make_grey(self.spell1_img)
        self.spell2_grey = self.make_grey(self.spell2_img)
        self.spell3_grey = self.make_grey(self.spell3_img)
        self.potion_grey = self.make_grey(self.potion_img)

        # fő keret (felső rész: varázsló – log – boss)
        main = tk.Frame(root, padx=10, pady=10)
        main.pack()

        # bal oldali panel – varázsló adatai
        left = tk.Frame(main)
        left.grid(row=0, column=0, padx=10)

        tk.Label(left, text="Varázsló", font=("Arial", 14, "bold")).pack()
        tk.Label(left, image=self.wizard_img).pack(pady=5)

        self.var_hp_label = tk.Label(left)
        self.var_hp_label.pack()

        self.var_hp_canvas = tk.Canvas(left, width=200, height=20, bg="grey20")
        self.var_hp_canvas.pack()
        self.var_hp_bar = self.var_hp_canvas.create_rectangle(0, 0, 200, 20, fill="green")

        # jobb oldali panel – boss adatai
        right = tk.Frame(main)
        right.grid(row=0, column=2, padx=10)

        tk.Label(right, text="Boss", font=("Arial", 14, "bold")).pack()
        tk.Label(right, image=self.boss_img).pack()

        self.boss_hp_label = tk.Label(right)
        self.boss_hp_label.pack()

        self.boss_hp_canvas = tk.Canvas(right, width=200, height=20, bg="grey20")
        self.boss_hp_canvas.pack()
        self.boss_hp_bar = self.boss_hp_canvas.create_rectangle(0, 0, 200, 20, fill="red")

        # középső panel – dobás és nagy üzenet
        center = tk.Frame(main)
        center.grid(row=0, column=1, padx=10)

        self.dobas_label = tk.Label(center, text="Dobás: -", font=("Arial", 16, "bold"))
        self.dobas_label.pack(pady=10)

        self.log_label = tk.Label(center, text="Válassz egy képességet!", justify="center")
        self.log_label.pack()

        # alsó panel – spellek és gyógyital
        spells_frame = tk.Frame(root, pady=10)
        spells_frame.pack()

        tk.Label(spells_frame, text="Varázsló képességei:", font=("Arial", 12, "bold")).pack()

        self.buttons_frame = tk.Frame(spells_frame)
        self.buttons_frame.pack()

        # három spell gomb
        self.spell1_btn = tk.Button(self.buttons_frame, image=self.spell1_img,
                                    command=lambda: self.varazslo_kor(1))
        self.spell1_btn.grid(row=0, column=0, padx=5)

        self.spell2_btn = tk.Button(self.buttons_frame, image=self.spell2_img,
                                    command=lambda: self.varazslo_kor(2))
        self.spell2_btn.grid(row=0, column=1, padx=5)

        self.spell3_btn = tk.Button(self.buttons_frame, image=self.spell3_img,
                                    command=lambda: self.varazslo_kor(3))
        self.spell3_btn.grid(row=0, column=2, padx=5)

        # gyógyital gomb
        self.potion_btn = tk.Button(self.buttons_frame, image=self.potion_img,
                                    command=self.hasznal_gyogyital)
        self.potion_btn.grid(row=0, column=3, padx=15)

        # gyógyital mennyiség kiírása az ikonra
        self.potion_label = tk.Label(
            self.buttons_frame,
            text=str(self.gyogyital_db),
            fg="white",
            bg="black",
            font=("Arial", 14, "bold")
        )
        self.potion_label.place(in_=self.potion_btn, relx=0.5, rely=0.5, anchor="center")

        # spell cooldown feliratok
        self.cd_labels = {
            1: tk.Label(self.buttons_frame, text="", fg="white", bg="black"),
            2: tk.Label(self.buttons_frame, text="", fg="white", bg="black"),
            3: tk.Label(self.buttons_frame, text="", fg="white", bg="black"),
        }

        self.spell_btn_map = {1: self.spell1_btn, 2: self.spell2_btn, 3: self.spell3_btn}
        self.spell_img_map = {
            1: (self.spell1_img, self.spell1_grey),
            2: (self.spell2_img, self.spell2_grey),
            3: (self.spell3_img, self.spell3_grey)
        }

        # legalul: utolsó 3 kör megjelenítése
        log_frame = tk.Frame(root, pady=10)
        log_frame.pack()

        tk.Label(log_frame, text="Utolsó 3 kör:", font=("Arial", 12, "bold")).pack(anchor="w")

        self.turn_log_label = tk.Label(
            log_frame,
            text="(Még nincs adat)",
            justify="left",
            font=("Arial", 10)
        )
        self.turn_log_label.pack(anchor="w")

        # induló frissítések
        self.update_spell_buttons()
        self.update_potion_button()
        self.update_hp_bars()
        self.update_turn_log()

    # napló kezelése
    def add_log_esemeny(self, szoveg):
        self.turn_log.append(szoveg)
        if len(self.turn_log) > 3:
            self.turn_log.pop(0)
        self.update_turn_log()

    def update_turn_log(self):
        if not self.turn_log:
            self.turn_log_label.config(text="(Még nincs adat)")
        else:
            self.turn_log_label.config(text="\n".join(self.turn_log))

    # hp csíkok frissítése
    def update_hp_bars(self):
        ar = max(self.varazslo_hp, 0) / VARAZSLO_MAX_HP
        self.var_hp_canvas.coords(self.var_hp_bar, 0, 0, 200 * ar, 20)
        self.var_hp_label.config(text=f"HP: {self.varazslo_hp}/{VARAZSLO_MAX_HP}")

        ar2 = max(self.boss_hp, 0) / BOSS_MAX_HP
        self.boss_hp_canvas.coords(self.boss_hp_bar, 0, 0, 200 * ar2, 20)
        self.boss_hp_label.config(text=f"HP: {self.boss_hp}/{BOSS_MAX_HP}")

    # nagy központi log
    def log(self, szoveg):
        self.log_label.config(text=szoveg)

    # spell gombok frissítése cooldown alapján
    def update_spell_buttons(self):
        for i in (1, 2, 3):
            btn = self.spell_btn_map[i]
            normal, grey = self.spell_img_map[i]

            if self.cooldowns[i] > 0:
                btn.config(state="disabled", image=grey)
                self.cd_labels[i].config(text=str(self.cooldowns[i]), font=("Arial", 14, "bold"))
                self.cd_labels[i].place(in_=btn, relx=0.5, rely=0.5, anchor="center")
            else:
                btn.config(state="normal", image=normal)
                self.cd_labels[i].place_forget()

    # gyógyital gomb frissítése
    def update_potion_button(self):
        if self.gyogyital_db > 0:
            self.potion_btn.config(state="normal", image=self.potion_img)
            self.potion_label.config(text=str(self.gyogyital_db))
        else:
            self.potion_btn.config(state="disabled", image=self.potion_grey)
            self.potion_label.config(text="0")

    # gyógyital használata
    def hasznal_gyogyital(self):
        if self.jatek_vege or self.gyogyital_db <= 0:
            return

        self.gyogyital_db -= 1
        self.varazslo_hp = min(self.varazslo_hp + 10, VARAZSLO_MAX_HP)

        self.log("Gyógyital → +10 HP")
        self.add_log_esemeny("Varázsló: Gyógyital (+10 HP)")

        self.update_hp_bars()
        self.update_potion_button()

        # gyógyital is körnek számít → boss jön
        self.root.after(800, self.boss_kor)

    # ikonok szürkévé alakítása
    def make_grey(self, img):
        grey = tk.PhotoImage(width=img.width(), height=img.height())
        for x in range(img.width()):
            for y in range(img.height()):
                color = img.get(x, y)
                if isinstance(color, tuple):
                    r, g, b = color
                else:
                    color = color.lstrip("#")
                    r = int(color[0:2], 16)
                    g = int(color[2:4], 16)
                    b = int(color[4:6], 16)
                avg = int((r + g + b) / 3)
                grey.put(f"#{avg:02x}{avg:02x}{avg:02x}", (x, y))
        return grey

    # varázsló köre
    def varazslo_kor(self, spell_id: int):
        if self.jatek_vege or self.cooldowns[spell_id] > 0:
            return

        nev = self.spell_nevek[spell_id]

        dobas = sza_dob_kocka(1, 20)
        self.dobas_label.config(text=f"Varázsló d20: {dobas}")

        if dobas >= 10:
            if spell_id == 1:
                sebzes = sza_dob_kocka(1, 6)
            elif spell_id == 2:
                sebzes = sza_dob_kocka(2, 4)
            else:
                sebzes = sza_dob_kocka(1, 20)

            self.boss_hp -= sebzes
            self.log(f"{nev} → találat ({sebzes} sebzés)")
            self.add_log_esemeny(f"Varázsló: {nev} ({sebzes})")
        else:
            self.log(f"{nev} → mellément")
            self.add_log_esemeny(f"Varázsló: {nev} (mellé)")

        # cooldown növelése
        self.cooldowns[spell_id] = self.spell_cd_idok[spell_id] + 1

        self.update_hp_bars()
        self.update_spell_buttons()

        if self.boss_hp <= 0:
            self.jatek_vege = True
            messagebox.showinfo("Győzelem", "A boss elbukott!")
            return

        self.root.after(800, self.boss_kor)

    # boss köre
    def boss_kor(self):
        if self.jatek_vege:
            return

        dobas = sza_dob_kocka(1, 20)
        self.dobas_label.config(text=f"Boss d20: {dobas}")

        if dobas >= 7:
            sebzes = sza_dob_kocka(1, 6)
            self.varazslo_hp -= sebzes
            self.log(f"Boss támad → {sebzes} sebzés")
            self.add_log_esemeny(f"Boss: támadás ({sebzes})")
        else:
            self.log("Boss támad → mellé")
            self.add_log_esemeny("Boss: mellé")

        self.update_hp_bars()

        if self.varazslo_hp <= 0:
            self.jatek_vege = True
            messagebox.showinfo("Vereség", "A boss legyőzött")
            return

        # kör végi cooldown csökkentés
        for i in (1, 2, 3):
            if self.cooldowns[i] > 0:
                self.cooldowns[i] -= 1

        self.update_spell_buttons()
