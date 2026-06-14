import pygame
import sys
import copy
import os
import heapq
import random
import math
import urllib.request
import urllib.parse
import json
import threading

KARE_BOYUT = 40
FPS = 60

BEYAZ = (255, 255, 255)
SIYAH = (8, 8, 10)
KIRMIZI = (255, 60, 60)
YESIL = (40, 230, 110)
MAVI = (0, 180, 255)
SARI = (255, 215, 0)
GRI = (30, 30, 36)
MOR = (150, 50, 250)
TURUNCU = (255, 120, 0)
ACIK_GRI = (90, 95, 105)
CYAN = (0, 255, 240)
GÖLGE_RENK = (20, 20, 25)

JSONBIN_BIN_ID = "BURAYA_BIN_ID"
JSONBIN_API_KEY = "BURAYA_API_KEY"

# --- HARİTALAR ---
HARITA_1 = [
    "WWWWWWWWWWWWWWWWWWWWWWWW",
    "W  L     W            W",
    "W WWWW W W WWWWWWWWWW W",
    "W W    W     W   S    W W",
    "W W WWWW W W WWWWWW W W",
    "W   W    W          W W",
    "W WWW WWWWWWWW WWWW W W",
    "W   W W   H  W W    W W",
    "WWW W W WWWW W W WWWW W",
    "W   W        W W W    W",
    "W WWWWWWWWWW W W W WWWW",
    "W L          W     H  E",
    "WWWWWWWWWWWWWWWWWWWWWWWW"
]

HARITA_2 = [
    "WWWWWWWWWWWWWWWWWWWWWWWW",
    "W      W  L    W      W",
    "W WWWW W WWWWW W WWWW W",
    "W W  S W       W W  H W",
    "W W WWWWWWWWWWWW W WW W",
    "W W          L   W    W",
    "W WWWWWW WWWWWWW WWWW W",
    "W      W W     W W    W",
    "WWWWWW W W WWW W W WW W",
    "W    W   W W S W W    W",
    "W WW WWWWW W WWW WWWWWW",
    "W  H         W       E",
    "WWWWWWWWWWWWWWWWWWWWWWWW"
]

HARITA_3 = [
    "WWWWWWWWWWWWWWWWWWWWWWWW",
    "W L W      W    L     W",
    "W W WWWWWW W WWWWWWWW W",
    "W W      W W W      W W",
    "W WWWWWW W W W WWWW W W",
    "W      W   W   W  H W W",
    "WWWWWW W WWWWWWW WW W W",
    "W    W W W     W    W W",
    "W WW W W W WWW WWWWWW W",
    "W  W   W S W W        W",
    "WW WWWWW W W WWWWWWWWWW",
    "W  S   H W           E",
    "WWWWWWWWWWWWWWWWWWWWWWWW"
]

TUM_HARITALAR = [HARITA_1, HARITA_2, HARITA_3]

DUSMAN_BASLANGIC = [
    [("KyloRen", 22, 1), ("Stormtrooper", 11, 5), ("DarthVader", 22, 9)],
    [("KyloRen", 22, 1), ("Stormtrooper", 12, 6), ("DarthVader", 22, 10)],
    [("KyloRen", 22, 1), ("Stormtrooper", 11, 6), ("DarthVader", 21, 9)],
]

KALKAN_SURESI = 8000
ISIN_SURESI = 6000
KARLIK_SURE = 2000
KARLIK_ARALIK = 8000


class Lokasyon:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, o):
        return isinstance(o, Lokasyon) and self.x == o.x and self.y == o.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, o):
        return False


def a_star(harita, bas, hed):
    sat = len(harita);
    sut = len(harita[0])
    op = [];
    heapq.heappush(op, (0, bas))
    cf = {};
    g = {bas: 0}
    f = {bas: abs(bas.x - hed.x) + abs(bas.y - hed.y)}
    while op:
        _, cur = heapq.heappop(op)
        if cur == hed:
            yol = []
            while cur in cf:
                yol.append(cur);
                cur = cf[cur]
            yol.reverse();
            return yol
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nb = Lokasyon(cur.x + dx, cur.y + dy)
            if 0 <= nb.y < sat and 0 <= nb.x < sut:
                if nb.x >= len(harita[nb.y]) or harita[nb.y][nb.x] == 'W':
                    continue
                ng = g[cur] + 1
                if nb not in g or ng < g[nb]:
                    cf[nb] = cur;
                    g[nb] = ng
                    f[nb] = ng + abs(nb.x - hed.x) + abs(nb.y - hed.y)
                    if nb not in [i[1] for i in op]:
                        heapq.heappush(op, (f[nb], nb))
    return None


class Parcacik:
    def __init__(self, x, y, renk):
        self.x = x;
        self.y = y;
        self.renk = renk
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-3, 0.5)
        self.omur = random.randint(20, 45)
        self.r = random.randint(2, 5)

    def guncelle(self):
        self.x += self.vx;
        self.y += self.vy
        self.vy += 0.12;
        self.omur -= 1

    def draw(self, screen):
        if self.omur > 0:
            alpha = max(0, int(255 * self.omur / 45))
            s = pygame.Surface((self.r * 2, self.r * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.renk, alpha), (self.r, self.r), self.r)
            screen.blit(s, (int(self.x) - self.r, int(self.y) - self.r))


def parcacik_patla(liste, x, y, renk, adet=18):
    for _ in range(adet):
        liste.append(Parcacik(x, y, renk))


def sesler_olustur():

    ses_sozlugu = {}

    ses_dosyalari = {
        "item": "sound",
        "hasar": "hasar",
        "kilac": "kilic",
        "kazan": "kazanma",
        "cekic": "cekic",
        "bomba": "bomba"
    }

    for anahtar, dosya_adi in ses_dosyalari.items():
        bulundu = False
        for uzanti in [".wav", ".mp3", ".WAV", ".MP3"]:
            tam_yol = f"{dosya_adi}{uzanti}"
            if os.path.exists(tam_yol):
                try:
                    ses_sozlugu[anahtar] = pygame.mixer.Sound(tam_yol)
                    ses_sozlugu[anahtar].set_volume(0.4)
                    bulundu = True
                    break
                except Exception as e:
                    print(f"Hata: {tam_yol} yüklenemedi -> {e}")

        if not bulundu:
            print(f"Bilgi: Opsiyonel/Zorunlu '{dosya_adi}' ses dosyası tam yüklenemedi, es geçiliyor.")

    return ses_sozlugu


class Karakter:
    def __init__(self, ad, tur, konum, gorsel):
        self.ad = ad;
        self.tur = tur
        self.grid_x = konum.x;
        self.grid_y = konum.y
        self.px = konum.x * KARE_BOYUT;
        self.py = konum.y * KARE_BOYUT
        self.orijinal = Lokasyon(konum.x, konum.y)
        self.hiz = 4
        try:
            img = pygame.image.load(gorsel)
            self.image = pygame.transform.scale(img, (KARE_BOYUT, KARE_BOYUT))
        except Exception:
            self.image = pygame.Surface((KARE_BOYUT, KARE_BOYUT))
            self.image.fill(YESIL if tur == "İyi" else KIRMIZI)

    def smooth(self):
        tx = self.grid_x * KARE_BOYUT;
        ty = self.grid_y * KARE_BOYUT
        self.px = self.px + min(self.hiz, tx - self.px) if self.px < tx else self.px - min(self.hiz, self.px - tx)
        self.py = self.py + min(self.hiz, ty - self.py) if self.py < ty else self.py - min(self.hiz, self.py - ty)

    def draw(self, sc):
        sc.blit(self.image, (self.px, self.py))

    def reset(self):
        self.grid_x = self.orijinal.x;
        self.grid_y = self.orijinal.y
        self.px = self.grid_x * KARE_BOYUT;
        self.py = self.grid_y * KARE_BOYUT

    @property
    def konum(self):
        return Lokasyon(self.grid_x, self.grid_y)

    def tam_mi(self):
        return self.px == self.grid_x * KARE_BOYUT and self.py == self.grid_y * KARE_BOYUT


class KyloRen(Karakter):
    def __init__(self, k):
        super().__init__("Kylo Ren", "Kötü", k, "kylo.png")
        self.gecikme = 280;
        self.son = pygame.time.get_ticks()
        self.can = 2;
        self.max_can = 2

    def hareket(self, harita, op, korku):
        if not self.tam_mi(): return
        if korku:
            best = self.konum;
            bm = -1
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = self.grid_x + dx, self.grid_y + dy
                if 0 <= ny < len(harita) and 0 <= nx < len(harita[ny]) and harita[ny][nx] != 'W':
                    m = abs(nx - op.x) + abs(ny - op.y)
                    if m > bm: bm = m; best = Lokasyon(nx, ny)
            self.grid_x = best.x;
            self.grid_y = best.y
        else:
            yol = a_star(harita, self.konum, op)
            if yol: self.grid_x = yol[0].x; self.grid_y = yol[0].y


class Stormtrooper(Karakter):
    def __init__(self, k):
        super().__init__("Stormtrooper", "Kötü", k, "somtr.png")
        self.gecikme = 320;
        self.son = pygame.time.get_ticks()
        self.can = 1;
        self.max_can = 1

    def hareket(self, harita, op, korku):
        if not self.tam_mi(): return
        mes = abs(self.grid_x - op.x) + abs(self.grid_y - op.y)
        if korku or mes > 4:
            yonler = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            random.shuffle(yonler)
            for dx, dy in yonler:
                nx, ny = self.grid_x + dx, self.grid_y + dy
                if 0 <= ny < len(harita) and 0 <= nx < len(harita[ny]) and harita[ny][nx] != 'W':
                    self.grid_x = nx;
                    self.grid_y = ny;
                    break
        else:
            yol = a_star(harita, self.konum, op)
            if yol: self.grid_x = yol[0].x; self.grid_y = yol[0].y


class DarthVader(Karakter):
    def __init__(self, k):
        super().__init__("Darth Vader", "Kötü", k, "dart.png")
        self.gecikme = 450;
        self.son = pygame.time.get_ticks()
        self.can = 3;
        self.max_can = 3

    def hareket(self, harita, op, korku):
        if not self.tam_mi(): return
        if korku:
            self.gecikme = 600
            best = self.konum;
            bm = -1
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = self.grid_x + dx, self.grid_y + dy
                if 0 <= ny < len(harita) and 0 <= nx < len(harita[ny]) and harita[ny][nx] != 'W':
                    m = abs(nx - op.x) + abs(ny - op.y)
                    if m > bm: bm = m; best = Lokasyon(nx, ny)
            self.grid_x = best.x;
            self.grid_y = best.y
        else:
            self.gecikme = 450
            dx = op.x - self.grid_x;
            dy = op.y - self.grid_y
            ax = 1 if dx > 0 else -1 if dx < 0 else 0
            ay = 1 if dy > 0 else -1 if dy < 0 else 0
            nx, ny = self.grid_x + ax, self.grid_y + ay
            if 0 <= ny < len(harita) and 0 <= nx < len(harita[ny]):
                if harita[ny][nx] == 'W':
                    if ny != 0 and ny != len(harita) - 1 and nx != 0 and nx != len(harita[ny]) - 1:
                        harita[ny] = harita[ny][:nx] + ' ' + harita[ny][nx + 1:]
                        self.grid_x = nx;
                        self.grid_y = ny
                else:
                    self.grid_x = nx;
                    self.grid_y = ny


class Oyuncu(Karakter):
    def __init__(self, ad, can, k, gorsel):
        super().__init__(ad, "İyi", k, gorsel)
        self.can = can;
        self.max_can = can
        self.isin = 0;
        self.kalkan = 0
        self.cekic = 0;
        self.son_yon = (0, 1)
        self.puan = 0

    @property
    def kalkan_aktif(self): return self.kalkan > 0


class OnlineSkor:
    def __init__(self):
        self.skorlar = []
        self.yuklu = False
        self.hata = False

    def yukle(self):
        def _yukle():
            try:
                url = f"https://api.jsonbin.io/v3/b/{JSONBIN_BIN_ID}/latest"
                req = urllib.request.Request(url, headers={
                    "X-Master-Key": JSONBIN_API_KEY,
                    "Content-Type": "application/json"
                })
                with urllib.request.urlopen(req, timeout=5) as r:
                    data = json.loads(r.read())
                    self.skorlar = data.get("record", {}).get("scores", [])
                    self.yuklu = True
            except Exception:
                self.hata = True
                self.yuklu = True

        threading.Thread(target=_yukle, daemon=True).start()

    def kaydet(self, ad, sure, bolum, zorluk):
        def _kaydet():
            try:
                url = f"https://api.jsonbin.io/v3/b/{JSONBIN_BIN_ID}"
                req = urllib.request.Request(url + "/latest", headers={"X-Master-Key": JSONBIN_API_KEY})
                with urllib.request.urlopen(req, timeout=5) as r:
                    mevcut = json.loads(r.read()).get("record", {}).get("scores", [])
                mevcut.append({"ad": ad, "sure": round(sure, 2), "bolum": bolum, "zorluk": zorluk})
                mevcut.sort(key=lambda x: x["sure"])
                mevcut = mevcut[:20]
                payload = json.dumps({"scores": mevcut}).encode()
                put = urllib.request.Request(url, data=payload, method="PUT",
                                             headers={"X-Master-Key": JSONBIN_API_KEY,
                                                      "Content-Type": "application/json"})
                urllib.request.urlopen(put, timeout=5)
                self.skorlar = mevcut
            except Exception:
                pass

        threading.Thread(target=_kaydet, daemon=True).start()


class Oyun:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.hw = len(HARITA_1[0]) * KARE_BOYUT
        self.hh = len(HARITA_1) * KARE_BOYUT
        self.screen = pygame.display.set_mode((self.hw, self.hh + 55))
        pygame.display.set_caption("Star Wars: Labirentten Kaçış ULTRA+")

        self.clock = pygame.time.Clock()
        self.fb = pygame.font.Font(None, 46)
        self.fm = pygame.font.Font(None, 24)
        self.fk = pygame.font.Font(None, 18)
        self.fkk = pygame.font.Font(None, 14)

        self.sis_surf = pygame.Surface((self.hw, self.hh), pygame.SRCALPHA)
        self.parcalar = []

        self.sesler = sesler_olustur()

        self.online = OnlineSkor()
        self.online.yukle()

        self.state = "baslangic"
        self.zorluk = "Normal"
        self.bolum = 0
        self.oyuncu = None
        self.dusmanlar = []
        self.harita = []
        self.bombalar = {}
        self.karlik_hucre = None
        self.karlik_timer = 0
        self.karlik_aktif = 0

        self.toplam_item = 0
        self.toplanan_item = 0
        self.baslangic_z = 0
        self.toplam_dur_z = 0
        self.dur_bas_z = 0
        self.gecen = 0
        self.duraklama = False
        self.en_iyi = self.lokal_yukle()
        self.ad_girisi = ""
        self.ad_girisi_mod = False

        self.menü_yıldızları = []
        for _ in range(60):
            self.menü_yıldızları.append({
                "x": random.randint(0, self.hw),
                "y": random.randint(0, self.hh + 55),
                "hiz": random.uniform(0.3, 1.8),
                "r": random.randint(1, 3)
            })

        self.zorluk_ayar = {
            "Kolay": {"hiz_kats": 0.6, "sis_r": 180, "dusman_hp": 0.5},
            "Normal": {"hiz_kats": 1.0, "sis_r": 130, "dusman_hp": 1.0},
            "Zor": {"hiz_kats": 1.4, "sis_r": 90, "dusman_hp": 2.0},
        }

    def ses(self, ad):
        s = self.sesler.get(ad)
        if s:
            try:
                s.play()
            except Exception:
                pass

    def lokal_yukle(self):
        if os.path.exists("skorlar.txt"):
            try:
                return float(open("skorlar.txt").read().strip())
            except Exception:
                pass
        return float('inf')

    def lokal_kaydet(self, s):
        if s < self.en_iyi:
            open("skorlar.txt", "w").write(f"{s:.2f}")
            self.en_iyi = s

    def zorluk_gecikme(self, base):
        return int(base / self.zorluk_ayar[self.zorluk]["hiz_kats"])

    def bolum_baslat(self):
        idx = self.bolum
        self.harita = copy.deepcopy(TUM_HARITALAR[idx])
        self.toplam_item = sum(r.count('L') + r.count('S') + r.count('H') for r in self.harita)
        self.toplanan_item = 0
        self.bombalar = {}
        self.parcalar = []
        self.karlik_hucre = None
        self.karlik_timer = pygame.time.get_ticks()
        self.karlik_aktif = 0

        hp_kats = self.zorluk_ayar[self.zorluk]["dusman_hp"]
        self.dusmanlar = []
        for ad, x, y in DUSMAN_BASLANGIC[idx]:
            lok = Lokasyon(x, y)
            if ad == "KyloRen":
                d = KyloRen(lok)
                d.gecikme = self.zorluk_gecikme(280)
                d.can = d.max_can = max(1, int(2 * hp_kats))
            elif ad == "Stormtrooper":
                d = Stormtrooper(lok)
                d.gecikme = self.zorluk_gecikme(320)
                d.can = d.max_can = max(1, int(1 * hp_kats))
            else:
                d = DarthVader(lok)
                d.gecikme = self.zorluk_gecikme(450)
                d.can = d.max_can = max(1, int(3 * hp_kats))
            self.dusmanlar.append(d)

        if self.oyuncu:
            self.oyuncu.reset()
            self.oyuncu.isin = 0
            self.oyuncu.kalkan = 0
            self.oyuncu.cekic = 0

        self.baslangic_z = pygame.time.get_ticks()
        self.toplam_dur_z = 0
        self.duraklama = False
        self.state = "oyun"

    def oyunu_sifirla(self):
        if self.oyuncu:
            self.oyuncu.can = self.oyuncu.max_can
            self.oyuncu.puan = 0
        self.bolum = 0
        self.bolum_baslat()

    def harita_ciz(self):
        simdi = pygame.time.get_ticks()
        for y, row in enumerate(self.harita):
            for x, c in enumerate(row):
                rect = pygame.Rect(x * KARE_BOYUT, y * KARE_BOYUT, KARE_BOYUT, KARE_BOYUT)
                karlik = (self.karlik_hucre == (x, y) and simdi - self.karlik_aktif < KARLIK_SURE)

                if c == 'W':
                    pygame.draw.rect(self.screen, MAVI, rect)
                    pygame.draw.rect(self.screen, SIYAH, rect, 1)
                elif c == 'E':
                    renk = YESIL if self.toplanan_item == self.toplam_item else KIRMIZI
                    pygame.draw.rect(self.screen, renk, rect)
                    lbl = self.fk.render("ÇIKIŞ", True, BEYAZ)
                    self.screen.blit(lbl, lbl.get_rect(center=rect.center))
                elif c == 'L':
                    pygame.draw.rect(self.screen, SIYAH, rect)
                    pygame.draw.polygon(self.screen, SARI,
                                        [(rect.centerx, rect.top + 10), (rect.left + 12, rect.bottom - 10),
                                         (rect.right - 12, rect.bottom - 10)])
                elif c == 'S':
                    pygame.draw.rect(self.screen, SIYAH, rect)
                    pygame.draw.circle(self.screen, MAVI, rect.center, 8)
                elif c == 'H':
                    pygame.draw.rect(self.screen, SIYAH, rect)
                    pygame.draw.rect(self.screen, MOR, (rect.left + 12, rect.top + 10, 16, 12))
                    pygame.draw.rect(self.screen, BEYAZ, (rect.centerx - 2, rect.top + 22, 4, 10))
                else:
                    pygame.draw.rect(self.screen, SIYAH, rect)

                if karlik:
                    s = pygame.Surface((KARE_BOYUT, KARE_BOYUT), pygame.SRCALPHA)
                    s.fill((0, 0, 0, 200))
                    self.screen.blit(s, rect.topleft)

        for (bx, by), kalan in list(self.bombalar.items()):
            brect = pygame.Rect(bx * KARE_BOYUT, by * KARE_BOYUT, KARE_BOYUT, KARE_BOYUT)
            pygame.draw.circle(self.screen, KIRMIZI, brect.center, 8)
            pygame.draw.circle(self.screen, SARI, brect.center, 5)
            t = self.fkk.render(f"{int(kalan / 1000) + 1}", True, BEYAZ)
            self.screen.blit(t, t.get_rect(center=brect.center))

    def sis_ciz(self):
        self.sis_surf.fill((12, 12, 16, 245))
        cx = self.oyuncu.px + KARE_BOYUT // 2
        cy = self.oyuncu.py + KARE_BOYUT // 2
        r = self.zorluk_ayar[self.zorluk]["sis_r"]
        if self.oyuncu.isin > 0: r = int(r * 1.4)
        pygame.draw.circle(self.sis_surf, (0, 0, 0, 0), (cx, cy), r)
        self.screen.blit(self.sis_surf, (0, 0))

    def mini_harita_ciz(self):
        mw, mh = len(self.harita[0]) * 3, len(self.harita) * 3
        surf = pygame.Surface((mw + 2, mh + 2), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 160))
        for y, row in enumerate(self.harita):
            for x, c in enumerate(row):
                if c == 'W':
                    renk = (40, 120, 250, 200)
                elif c == 'E':
                    renk = (50, 200, 100, 230)
                elif c in ['L', 'S', 'H']:
                    renk = (240, 200, 20, 230)
                else:
                    renk = (30, 30, 35, 80)
                pygame.draw.rect(surf, renk, (1 + x * 3, 1 + y * 3, 3, 3))
        pygame.draw.rect(surf, (50, 255, 50, 255), (1 + self.oyuncu.grid_x * 3, 1 + self.oyuncu.grid_y * 3, 3, 3))
        for d in self.dusmanlar:
            if d.can > 0: pygame.draw.rect(surf, (255, 50, 50, 255), (1 + d.grid_x * 3, 1 + d.grid_y * 3, 3, 3))
        self.screen.blit(surf, (self.hw - mw - 8, 4))

    def ui_ciz(self):
        uy = self.hh
        pygame.draw.rect(self.screen, GRI, (0, uy, self.hw, 55))
        self.screen.blit(self.fm.render("CAN:", True, BEYAZ), (10, uy + 18))
        for i in range(self.oyuncu.max_can):
            renk = YESIL if i < self.oyuncu.can else ACIK_GRI
            pygame.draw.circle(self.screen, renk, (58 + i * 19, uy + 28), 7)

        ks = f"Kalkan:{int(self.oyuncu.kalkan / 1000)}s" if self.oyuncu.kalkan_aktif else "Kalkan:Yok"
        ik = f"Kılıç:{int(self.oyuncu.isin / 1000)}s" if self.oyuncu.isin > 0 else "Kılıç:Yok"
        inv = self.fk.render(f"{ik} | {ks} | Çekiç:{self.oyuncu.cekic}  [P=Dur M=Menü]", True, BEYAZ)
        self.screen.blit(inv, (155, uy + 10))

        self.screen.blit(self.fm.render(f"PUAN:{self.oyuncu.puan}", True, CYAN), (155, uy + 30))
        self.screen.blit(self.fm.render(f"ÖĞE:{self.toplanan_item}/{self.toplam_item}", True, SARI),
                         (self.hw // 2 + 10, uy + 18))
        self.screen.blit(self.fm.render(f"SÜRE:{self.gecen:.1f}s", True, TURUNCU), (self.hw - 130, uy + 18))
        self.screen.blit(self.fk.render(f"BÖLÜM {self.bolum + 1}/3  [{self.zorluk}]", True, ACIK_GRI),
                         (self.hw - 130, uy + 38))

        if self.en_iyi != float('inf'):
            self.screen.blit(self.fk.render(f"REKOR:{self.en_iyi:.1f}s", True, SARI), (155, uy + 42))

    def dusman_can_ciz(self):
        for d in self.dusmanlar:
            if d.can <= 0: continue
            bw = KARE_BOYUT - 4;
            bh = 4
            bx = d.px + 2;
            by = d.py - 7
            pygame.draw.rect(self.screen, KIRMIZI, (bx, by, bw, bh))
            dolu = int(bw * d.can / d.max_can)
            pygame.draw.rect(self.screen, YESIL, (bx, by, dolu, bh))

    def karlik_guncelle(self, simdi):
        if simdi - self.karlik_timer > KARLIK_ARALIK:
            adaylar = []
            for y, row in enumerate(self.harita):
                for x, c in enumerate(row):
                    if c == ' ' and (x, y) != (self.oyuncu.grid_x, self.oyuncu.grid_y): adaylar.append((x, y))
            if adaylar:
                self.karlik_hucre = random.choice(adaylar)
                self.karlik_aktif = simdi
                self.karlik_timer = simdi

    def bomba_guncelle(self, dt, simdi):
        patla = []
        for pos in list(self.bombalar):
            self.bombalar[pos] -= dt
            if self.bombalar[pos] <= 0: patla.append(pos)
        for pos in patla:
            del self.bombalar[pos]
            bx, by = pos
            cx = bx * KARE_BOYUT + KARE_BOYUT // 2
            cy = by * KARE_BOYUT + KARE_BOYUT // 2
            parcacik_patla(self.parcalar, cx, cy, (255, 100, 0), 25)
            self.ses("bomba")
            for d in self.dusmanlar:
                if abs(d.grid_x - bx) <= 2 and abs(d.grid_y - by) <= 2: d.son = simdi + 3000

    def input_isle(self):
        if not self.oyuncu.tam_mi(): return
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT]:
            dx = -1; self.oyuncu.son_yon = (-1, 0)
        elif keys[pygame.K_RIGHT]:
            dx = 1; self.oyuncu.son_yon = (1, 0)
        elif keys[pygame.K_UP]:
            dy = -1; self.oyuncu.son_yon = (0, -1)
        elif keys[pygame.K_DOWN]:
            dy = 1; self.oyuncu.son_yon = (0, 1)
        if dx or dy:
            nx = self.oyuncu.grid_x + dx;
            ny = self.oyuncu.grid_y + dy
            if 0 <= ny < len(self.harita) and 0 <= nx < len(self.harita[ny]) and self.harita[ny][nx] != 'W':
                self.oyuncu.grid_x = nx;
                self.oyuncu.grid_y = ny

    def puan_hesapla(self, sure, kalan_can, bolum_no):
        baz = 5000
        sure_bonus = max(0, int(3000 - sure * 40))
        can_bonus = kalan_can * 500
        bolum_bonus = bolum_no * 1000
        return baz + sure_bonus + can_bonus + bolum_bonus

    def bitis_ekrani(self, kazandi):
        overlay = pygame.Surface((self.hw, self.hh + 55), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        if kazandi:
            t = self.fb.render(f"BÖLÜM {self.bolum + 1} TAMAMLANDI!", True, YESIL)
        else:
            t = self.fb.render("KARANLIK TARAF KAZANDI!", True, KIRMIZI)
        self.screen.blit(t, t.get_rect(center=(self.hw // 2, self.hh // 2 - 60)))
        t2 = self.fm.render(f"Süre: {self.gecen:.2f}s  |  Puan: {self.oyuncu.puan}", True, SARI)
        self.screen.blit(t2, t2.get_rect(center=(self.hw // 2, self.hh // 2 - 10)))

        if kazandi and self.bolum < 2:
            t3 = self.fm.render("Sonraki bölüm için N'ye bas", True, BEYAZ)
            self.screen.blit(t3, t3.get_rect(center=(self.hw // 2, self.hh // 2 + 30)))
        else:
            t3 = self.fm.render("Tekrar: R   Menü: M   Çıkış: Q", True, BEYAZ)
            self.screen.blit(t3, t3.get_rect(center=(self.hw // 2, self.hh // 2 + 30)))

        pygame.display.flip()
        bekle = True
        while bekle:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
                if ev.type == pygame.KEYDOWN:
                    if kazandi and self.bolum < 2 and ev.key == pygame.K_n:
                        self.bolum += 1;
                        self.bolum_baslat();
                        bekle = False
                    elif ev.key == pygame.K_r:
                        self.oyuncu.can = self.oyuncu.max_can;
                        self.oyuncu.puan = 0;
                        self.bolum = 0;
                        self.bolum_baslat();
                        bekle = False
                    elif ev.key == pygame.K_m:
                        self.state = "baslangic";
                        self.oyuncu = None;
                        bekle = False
                    elif ev.key == pygame.K_q:
                        pygame.quit(); sys.exit()

    def duraklama_ciz(self):
        ov = pygame.Surface((self.hw, self.hh + 55), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 160));
        self.screen.blit(ov, (0, 0))
        t = self.fb.render("DURAKLATILDI", True, SARI)
        self.screen.blit(t, t.get_rect(center=(self.hw // 2, self.hh // 2 - 20)))
        t2 = self.fm.render("P=Devam   M=Menü", True, BEYAZ)
        self.screen.blit(t2, t2.get_rect(center=(self.hw // 2, self.hh // 2 + 25)))

    def skor_tablosu_ciz(self):
        self.screen.fill(SIYAH)
        t = self.fb.render("ONLINE SKOR TABLOSU", True, SARI)
        self.screen.blit(t, t.get_rect(center=(self.hw // 2, 40)))
        if not self.online.yuklu:
            t2 = self.fm.render("Yükleniyor...", True, ACIK_GRI)
            self.screen.blit(t2, t2.get_rect(center=(self.hw // 2, self.hh // 2)))
        elif self.online.hata or JSONBIN_BIN_ID == "BURAYA_BIN_ID":
            t2 = self.fm.render("API anahtarı girilmemiş / bağlantı hatası", True, KIRMIZI)
            self.screen.blit(t2, t2.get_rect(center=(self.hw // 2, self.hh // 2)))
        else:
            for i, s in enumerate(self.online.skorlar[:10]):
                renk = SARI if i == 0 else BEYAZ
                satir = f"{i + 1:2}. {s['ad']:<12} {s['sure']:6.2f}s  Bölüm:{s['bolum']}  [{s['zorluk']}]"
                t2 = self.fm.render(satir, True, renk)
                self.screen.blit(t2, (60, 90 + i * 32))
        t3 = self.fm.render("ESC = Geri", True, ACIK_GRI)
        self.screen.blit(t3, t3.get_rect(center=(self.hw // 2, self.hh - 30)))
        pygame.display.flip()

    def baslangic_ciz(self):
        self.screen.fill(SIYAH)
        mx = self.hw // 2
        mouse_pos = pygame.mouse.get_pos()

        for yildiz in self.menü_yıldızları:
            yildiz["y"] += yildiz["hiz"]
            if yildiz["y"] > self.hh + 55:
                yildiz["y"] = 0
                yildiz["x"] = random.randint(0, self.hw)
            pygame.draw.circle(self.screen, (200, 210, 255), (int(yildiz["x"]), int(yildiz["y"])), yildiz["r"])

        baslik_golge = self.fb.render("STAR WARS LABİRENT ULTRA+", True, GÖLGE_RENK)
        baslik_asil = self.fb.render("STAR WARS LABİRENT ULTRA+", True, SARI)
        self.screen.blit(baslik_golge, baslik_golge.get_rect(center=(mx + 3, 63)))
        self.screen.blit(baslik_asil, baslik_asil.get_rect(center=(mx, 60)))

        zt = self.fm.render("Zorluk Modu:", True, CYAN)
        self.screen.blit(zt, (mx - 180, 125))

        for i, (z, renk) in enumerate([("Kolay", YESIL), ("Normal", SARI), ("Zor", KIRMIZI)]):
            bx = mx - 60 + i * 85
            by = 120
            b_rect = pygame.Rect(bx, by, 75, 28)

            secili = (self.zorluk == z)
            if b_rect.collidepoint(mouse_pos) or secili:
                pygame.draw.rect(self.screen, renk, b_rect, border_radius=6)
                pygame.draw.rect(self.screen, BEYAZ, b_rect, 2, border_radius=6)
                lt = self.fk.render(z, True, SIYAH)
            else:
                pygame.draw.rect(self.screen, GRI, b_rect, border_radius=6)
                lt = self.fk.render(z, True, renk)

            self.screen.blit(lt, lt.get_rect(center=b_rect.center))

        butonlar = [
            {"id": "luke", "y": 175, "renk": MAVI, "metin": "Luke Skywalker  (3 Can)"},
            {"id": "yoda", "y": 240, "renk": YESIL, "metin": "Master Yoda  (6 Can)"},
            {"id": "skor", "y": 305, "renk": MOR, "metin": "Online Skor Tablosu"}
        ]

        for b in butonlar:
            rect = pygame.Rect(mx - 150, b["y"], 300, 48)
            is_hover = rect.collidepoint(mouse_pos)

            pygame.draw.rect(self.screen, GÖLGE_RENK, (rect.x + 3, rect.y + 3, rect.width, rect.height),
                             border_radius=8)

            if is_hover:
                pygame.draw.rect(self.screen, b["renk"], rect, border_radius=8)
                text_renk = SIYAH
            else:
                pygame.draw.rect(self.screen, GRI, rect, border_radius=8)
                pygame.draw.rect(self.screen, b["renk"], rect, 2, border_radius=8)
                text_renk = BEYAZ

            btn_text = self.fm.render(b["metin"], True, text_renk)
            self.screen.blit(btn_text, btn_text.get_rect(center=rect.center))

        if self.en_iyi != float('inf'):
            rk_text = self.fm.render(f"🏆 Kişisel En İyi Skor: {self.en_iyi:.2f}s", True, TURUNCU)
            self.screen.blit(rk_text, rk_text.get_rect(center=(mx, 385)))

        kontrol = self.fk.render("Yön Tuşları: Hareket  |  SPACE: Çekiç Duvar Kırma  |  B: Bomba Bırak  |  P: Duraklat",
                                 True, ACIK_GRI)
        self.screen.blit(kontrol, kontrol.get_rect(center=(mx, 425)))

    def ad_girisi_ciz(self):
        ov = pygame.Surface((self.hw, self.hh + 55), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 200));
        self.screen.blit(ov, (0, 0))
        t = self.fb.render("TEBRİKLER!", True, YESIL)
        self.screen.blit(t, t.get_rect(center=(self.hw // 2, self.hh // 2 - 80)))
        t2 = self.fm.render(f"Toplam Puan: {self.oyuncu.puan}", True, SARI)
        self.screen.blit(t2, t2.get_rect(center=(self.hw // 2, self.hh // 2 - 35)))
        t3 = self.fm.render("Adınızı girin (Enter=Kaydet):", True, BEYAZ)
        self.screen.blit(t3, t3.get_rect(center=(self.hw // 2, self.hh // 2 + 10)))
        pygame.draw.rect(self.screen, GRI, (self.hw // 2 - 120, self.hh // 2 + 35, 240, 36), border_radius=6)
        tad = self.fm.render(self.ad_girisi + "_", True, SARI)
        self.screen.blit(tad, tad.get_rect(center=(self.hw // 2, self.hh // 2 + 53)))

    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            simdi = pygame.time.get_ticks()

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit();
                    sys.exit()

                if self.ad_girisi_mod:
                    if ev.type == pygame.KEYDOWN:
                        if ev.key == pygame.K_RETURN and self.ad_girisi.strip():
                            self.online.kaydet(self.ad_girisi.strip(), self.gecen, self.bolum + 1, self.zorluk)
                            self.ad_girisi_mod = False
                            self.state = "skor_tablosu"
                        elif ev.key == pygame.K_BACKSPACE:
                            self.ad_girisi = self.ad_girisi[:-1]
                        elif ev.key != pygame.K_RETURN and len(self.ad_girisi) < 10:
                            if ev.unicode.isalnum() or ev.unicode in [' ', '_', '-']:
                                self.ad_girisi += ev.unicode

                elif self.state == "baslangic":
                    if ev.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        merkez_x = self.hw // 2

                        for i, z in enumerate(["Kolay", "Normal", "Zor"]):
                            bx = merkez_x - 60 + i * 85
                            if bx <= mx <= bx + 75 and 120 <= my <= 148:
                                self.zorluk = z
                                self.ses("item")

                        if merkez_x - 150 <= mx <= merkez_x + 150 and 175 <= my <= 223:
                            self.oyuncu = Oyuncu("Luke Skywalker", 3, Lokasyon(1, 1), "luke.png")
                            self.oyunu_sifirla()

                        elif merkez_x - 150 <= mx <= merkez_x + 150 and 240 <= my <= 288:
                            self.oyuncu = Oyuncu("Master Yoda", 6, Lokasyon(1, 1), "master.png")
                            self.oyunu_sifirla()

                        elif merkez_x - 150 <= mx <= merkez_x + 150 and 305 <= my <= 353:
                            self.state = "skor_tablosu"
                            self.online.yukle()

                elif self.state == "oyun" and not self.duraklama:
                    if ev.type == pygame.KEYDOWN:
                        if ev.key == pygame.K_p:
                            self.duraklama = True
                            self.dur_bas_z = pygame.time.get_ticks()
                        elif ev.key == pygame.K_m:
                            self.state = "baslangic"
                        elif ev.key == pygame.K_SPACE:
                            if self.oyuncu.cekic > 0:
                                sx, sy = self.oyuncu.son_yon
                                tx = self.oyuncu.grid_x + sx
                                ty = self.oyuncu.grid_y + sy
                                if 0 <= ty < len(self.harita) and 0 <= tx < len(self.harita[ty]):
                                    if ty != 0 and ty != len(self.harita) - 1 and tx != 0 and tx != len(
                                            self.harita[ty]) - 1:
                                        if self.harita[ty][tx] == 'W':
                                            self.harita[ty] = self.harita[ty][:tx] + ' ' + self.harita[ty][tx + 1:]
                                            self.oyuncu.cekic -= 1
                                            self.ses("cekic")
                                            parcacik_patla(self.parcalar, tx * KARE_BOYUT + 20, ty * KARE_BOYUT + 20,
                                                           MAVI, 15)

                        elif ev.key == pygame.K_b:
                            pos = (self.oyuncu.grid_x, self.oyuncu.grid_y)
                            if pos not in self.bombalar:
                                self.bombalar[pos] = 2000
                                self.ses("item")

                elif self.state == "oyun" and self.duraklama:
                    if ev.type == pygame.KEYDOWN:
                        if ev.key == pygame.K_p:
                            self.duraklama = False
                            self.toplam_dur_z += (pygame.time.get_ticks() - self.dur_bas_z)
                        elif ev.key == pygame.K_m:
                            self.state = "baslangic"

                elif self.state == "skor_tablosu":
                    if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                        self.state = "baslangic"

            # ─── UPDATE & DRAW DÖNGÜSÜ ───
            if self.state == "baslangic":
                self.baslangic_ciz()

            elif self.state == "skor_tablosu":
                self.skor_tablosu_ciz()

            elif self.state == "oyun":
                if not self.duraklama:
                    self.gecen = (simdi - self.baslangic_z - self.toplam_dur_z) / 1000.0

                    if self.oyuncu.isin > 0:   self.oyuncu.isin -= dt
                    if self.oyuncu.kalkan > 0: self.oyuncu.kalkan -= dt

                    self.input_isle()
                    self.oyuncu.smooth()
                    for d in self.dusmanlar: d.smooth()

                    self.bomba_guncelle(dt, simdi)
                    self.karlik_guncelle(simdi)

                    if self.oyuncu.tam_mi():
                        cell = self.harita[self.oyuncu.grid_y][self.oyuncu.grid_x]
                        if cell in ['L', 'S', 'H']:
                            if cell == 'L':
                                self.oyuncu.isin = ISIN_SURESI
                                self.oyuncu.puan += 150
                                self.ses("kilac")
                            elif cell == 'S':
                                self.oyuncu.kalkan = KALKAN_SURESI
                                self.oyuncu.puan += 100
                                self.ses("item")
                            elif cell == 'H':
                                self.oyuncu.cekic += 2
                                self.oyuncu.puan += 120
                                self.ses("item")

                            self.harita[self.oyuncu.grid_y] = self.harita[self.oyuncu.grid_y][
                                                              :self.oyuncu.grid_x] + ' ' + self.harita[
                                                                                               self.oyuncu.grid_y][
                                                                                           self.oyuncu.grid_x + 1:]
                            self.toplanan_item += 1
                            parcacik_patla(self.parcalar, self.oyuncu.px + 20, self.oyuncu.py + 20, SARI, 10)

                    korku_aktif = self.oyuncu.isin > 0
                    for d in self.dusmanlar:
                        if d.can > 0 and simdi - d.son >= d.gecikme:
                            d.hareket(self.harita, self.oyuncu.konum, korku_aktif)
                            d.son = simdi

                    for p in self.parcalar[:]:
                        p.guncelle()
                        if p.omur <= 0: self.parcalar.remove(p)

                    for d in self.dusmanlar:
                        if d.can > 0 and self.oyuncu.konum == d.konum:
                            if self.oyuncu.isin > 0:
                                d.can -= 1
                                self.oyuncu.puan += 300
                                self.ses("kilac")
                                parcacik_patla(self.parcalar, d.px + 20, d.py + 20, KIRMIZI, 20)
                                if d.can <= 0:
                                    self.oyuncu.puan += 500
                                else:
                                    d.reset()
                            elif self.oyuncu.kalkan_aktif:
                                self.oyuncu.kalkan = 0
                                self.ses("hasar")
                                d.reset()
                                parcacik_patla(self.parcalar, self.oyuncu.px + 20, self.oyuncu.py + 20, MAVI, 15)
                            else:
                                self.oyuncu.can -= 1
                                self.ses("hasar")
                                parcacik_patla(self.parcalar, self.oyuncu.px + 20, self.oyuncu.py + 20, KIRMIZI, 25)
                                if self.oyuncu.can <= 0:
                                    self.bitis_ekrani(False)
                                else:
                                    self.oyuncu.reset()
                                    for emy in self.dusmanlar: emy.reset()

                    if self.harita[self.oyuncu.grid_y][
                        self.oyuncu.grid_x] == 'E' and self.toplanan_item == self.toplam_item:
                        bolum_puani = self.puan_hesapla(self.gecen, self.oyuncu.can, self.bolum + 1)
                        self.oyuncu.puan += bolum_puani
                        self.ses("kazan")
                        if self.bolum == 2:
                            self.lokal_kaydet(self.gecen)
                            self.ad_girisi_mod = True
                        else:
                            self.bitis_ekrani(True)

                self.harita_ciz()
                self.oyuncu.draw(self.screen)

                if self.oyuncu.isin > 0:
                    pygame.draw.circle(self.screen, TURUNCU, (self.oyuncu.px + 20, self.oyuncu.py + 20), 22, 3)
                elif self.oyuncu.kalkan_aktif:
                    pygame.draw.circle(self.screen, MAVI, (self.oyuncu.px + 20, self.oyuncu.py + 20), 22, 2)

                for d in self.dusmanlar:
                    if d.can > 0: d.draw(self.screen)
                for p in self.parcalar: p.draw(self.screen)

                self.sis_ciz()
                self.dusman_can_ciz()
                self.mini_harita_ciz()
                self.ui_ciz()

                if self.duraklama: self.duraklama_ciz()
                if self.ad_girisi_mod: self.ad_girisi_ciz()

            pygame.display.flip()


if __name__ == "__main__":
    oyun = Oyun()
    oyun.run()