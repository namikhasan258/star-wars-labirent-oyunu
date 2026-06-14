# 🌌 Star Wars: Escape The Death Star 🚀

Bu proje, Pygame kütüphanesi kullanılarak geliştirilmiş, arcade tarzı dinamik bir 2D labirentten kaçış oyunudur. Oyuncu, Death Star'dan (Ölüm Yıldızı) kaçmaya çalışan Luke Skywalker veya Master Yoda karakterlerini kontrol ederek düşmanları atlatmalı, haritadaki güç kristallerini ve ekipmanları toplayarak çıkış kapısına ulaşmalıdır.


## 👨‍💻 Geliştirici / Prepared By
**Namık Hasan**

## 🛠️ Özellikler & Güncel Mekanikler

* **Çift Kontrol Desteği:** Oyunu hem **Yön Tuşları** hem de **WASD** tuş kombinasyonuyla oynayabilirsiniz.
* **Karakter Seçimi:** Farklı hız ve can havuzuna sahip iki ikonik karakter (Luke Skywalker & Master Yoda).
* **Işın Kılıcı Modu (L):** Haritadan ışın kılıcını aldığınızda düşmanlar korku moduna geçer ve kaçarlar. Bu moddayken düşmanların üzerine giderek kılıç darbesi vurabilirsiniz.
* **Kalkan Modu (S):** Aktif olduğunda oyuncuyu anomalilerden korur ve düşmanları geri iter.
* **Çekiç Mekaniği (H / SPACE):** Duvarları parçalayarak haritada kendinize yeni yollar açabilirsiniz.
* **Dinamik Anomaliler (Karlık):** Haritada rastgele zamanlarda beliren ve oyuncuya hasar veren tehlikeli alanlar.
* **Gelişmiş Ses Efektleri:** Çekiç kullanımı, kılıç savurma/darbe anları ve kalkan çarpışmaları için özel ses tetikleyicileri.

---

## 🎮 Kontroller

| Aksiyon | Tuş Kombinasyonu |
| :--- | :--- |
| **Hareket** | `Yön Tuşları` |
| **Çekiç Kullanımı** | `SPACE` (Boşluk Tuşu) |
| **Kılıç Savurma Sesi** | `E` (Işın kılıcı aktifken) |
| **Bomba Bırakma** | `B` |
| **Oyunu Duraklatma** | `P` |
| **Ana Menüye Dönüş** | `M` |

---

## 💻 Kurulum ve Çalıştırma

### 1. Gereksinimler
Oyunun çalışması için bilgisayarınızda Python ve **Pygame** kütüphanesinin kurulu olması gerekir.

```bash
pip install pygame

2. Ses Dosyalarının Eklenmesi 🎵
Proje boyutunu hafif tutmak amacıyla ses dosyaları bu depoya dahil edilmemiştir. Oyunu sesli oynamak için ana dizine (kodun yanına) aşağıdaki .wav dosyalarını kendi efektlerinizle eklemeniz gerekmektedir:

cekic.wav

kilic.wav

hasar.wav

item.wav

kazan.wav

kayip.wav

3. Oyunu Başlatma
Proje klasöründe terminali açıp aşağıdaki komutu yürütün:

Bash
python star-wars-labirent-oyunu.py


