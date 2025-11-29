import random

# állandók
VARAZSLO_MAX_HP = 65
BOSS_MAX_HP = 100

def sza_dob_kocka(kockak_szama, oldalak):

    return sum(random.randint(1, oldalak) for _ in range(kockak_szama))
