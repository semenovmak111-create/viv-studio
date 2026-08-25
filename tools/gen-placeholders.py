#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Заглушки под фотографии VIV Studio.

Задача — не «серый прямоугольник с надписью», а кадр: тёплый свет,
мягкий фокус, узнаваемая геометрия комнаты. Слоя два:
  · фон     — крупные размытые пятна, из них складывается свет;
  · предмет — окно, кушетка, стойка, рамки; размыт слабее, поэтому читается.

Когда придут настоящие фотографии, файлы заменяются по именам,
пропорции заданы в CSS — вёрстку править не придётся.
"""
import os

OUT = "/Users/hermmoment/coding/websites/projects/viv-studio/assets/img"


def head(w, h, label, extra_defs=""):
    big = max(w, h)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{label}" preserveAspectRatio="xMidYMid slice">\n'
        '<defs>\n'
        f'  <filter id="far" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="{big*0.055:.1f}"/></filter>\n'
        f'  <filter id="mid" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="{big*0.016:.1f}"/></filter>\n'
        f'  <filter id="near" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="{big*0.007:.1f}"/></filter>\n'
        '  <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4"/><feColorMatrix type="saturate" values="0"/></filter>\n'
        '  <radialGradient id="vig" cx="50%" cy="44%" r="76%">'
        '<stop offset="52%" stop-color="#000" stop-opacity="0"/>'
        '<stop offset="100%" stop-color="#2A1B10" stop-opacity=".40"/></radialGradient>\n'
        f'{extra_defs}\n'
        '</defs>\n'
    )


def tail(w, h):
    return (f'<rect width="{w}" height="{h}" fill="url(#vig)"/>\n'
            f'<rect width="{w}" height="{h}" filter="url(#grain)" opacity=".09"/>\n</svg>\n')


def el(cx, cy, rx, ry, fill, op=1.0):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" opacity="{op}"/>'


def rc(x, y, w, h, fill, op=1.0, r=0):
    rr = f' rx="{r}"' if r else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" opacity="{op}"{rr}/>'


def ln(x1, y1, x2, y2, stroke, sw=2, op=1.0):
    return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"/>'


def write(name, body):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(body)
    print(f"{name:16} {len(body):6} б")


# ── 01 · ОБЛОЖКА: кабинет студии ───────────────────────────────────────
# Кадр вертикальный и на широких экранах обрезается по бокам, поэтому
# всё важное держим в средней трети. Людей не рисуем: силуэт в размытии
# читается как пятно, а пустой кабинет в тёплом свете — как кадр.
def hero(w=640, h=980):
    defs = ('  <linearGradient id="bg" x1=".1" y1="0" x2=".8" y2="1">'
            '<stop offset="0" stop-color="#66492E"/><stop offset=".45" stop-color="#3C2919"/>'
            '<stop offset="1" stop-color="#1A1007"/></linearGradient>\n'
            '  <linearGradient id="win" x1="0" y1="0" x2=".8" y2="1">'
            '<stop offset="0" stop-color="#FDF0D6"/><stop offset="1" stop-color="#E6C289"/></linearGradient>\n'
            '  <linearGradient id="couch" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#EBD0AC"/><stop offset=".45" stop-color="#CFAA7C"/>'
            '<stop offset="1" stop-color="#8E6E48"/></linearGradient>')
    s = head(w, h, "Кабинет студии VIV Studio", defs)
    s += f'<rect width="{w}" height="{h}" fill="url(#bg)"/>\n'

    # дальний план — свет
    s += '<g filter="url(#far)">'
    s += el(250, 250, 300, 300, "#F6E1B8", .42)      # разлив света от окна
    s += el(120, 620, 180, 220, "#8A653F", .28)      # тёплая стена
    s += el(600, 940, 200, 160, "#130C05", .70)      # тёмный угол
    s += '</g>\n'

    # средний план — окно, стена, кушетка
    s += '<g filter="url(#mid)">'
    s += rc(96, 118, 250, 330, "url(#win)", .80, 5)  # окно
    s += rc(0, 648, w, 14, "#7A5936", .50)           # линия стены и пола
    s += rc(-30, 686, w + 60, 250, "url(#couch)", .95, 30)   # кушетка
    s += rc(-30, 686, w + 60, 34, "#F6DDB6", .55, 16)        # блик на валике
    s += rc(452, 470, 92, 200, "#241708", .55, 10)   # стойка аппарата в тени
    s += '</g>\n'

    # ближний план — переплёт окна, экран, полотенца
    s += '<g filter="url(#near)">'
    s += rc(218, 118, 6, 330, "#9B7748", .45)        # переплёт
    s += rc(96, 268, 250, 6, "#9B7748", .45)
    s += rc(468, 500, 60, 38, "#F2D5A6", .72, 3)     # экран аппарата
    s += rc(120, 640, 120, 22, "#F3E4C8", .55, 6)    # стопка полотенец
    s += rc(126, 622, 108, 20, "#EADAB8", .45, 6)
    s += el(360, 636, 16, 26, "#E9D3B0", .55)        # флакон на столике
    s += '</g>\n'
    s += '<g filter="url(#near)" opacity=".5">' + el(300, 706, 150, 26, "#FFF0D2", .55) + '</g>\n'
    s += tail(w, h)
    write("hero.svg", s)


# ── 05 · ПОРТРЕТ МАСТЕРА ───────────────────────────────────────────────
def master(w=520, h=650):
    defs = ('  <linearGradient id="bg" x1=".2" y1="0" x2=".9" y2="1">'
            '<stop offset="0" stop-color="#EBDCC2"/><stop offset=".6" stop-color="#D8BE9B"/>'
            '<stop offset="1" stop-color="#B4906A"/></linearGradient>')
    s = head(w, h, "Екатерина — мастер VIV Studio", defs)
    s += f'<rect width="{w}" height="{h}" fill="url(#bg)"/>\n'
    s += '<g filter="url(#far)">'
    s += el(110, 90, 210, 180, "#FCF1DC", .85)       # свет слева сверху
    s += el(452, 596, 140, 130, "#A9855C", .38)      # тень справа
    s += '</g>\n'
    s += '<g filter="url(#mid)">'
    s += el(262, 520, 218, 230, "#F5F2EC", .95)      # халат
    s += el(262, 164, 132, 100, "#54391F", .92)      # волосы
    s += el(262, 260, 112, 136, "#E7BE97", .96)      # лицо
    s += el(166, 276, 42, 84, "#4C331B", .78)        # пряди
    s += el(358, 276, 42, 84, "#4C331B", .78)
    s += el(262, 388, 70, 56, "#E0B287", .88)        # шея
    s += '</g>\n'
    s += '<g filter="url(#near)">'
    s += '<path d="M212 424L262 494L312 424L302 412L262 462L222 412Z" fill="#FBFAF7" opacity=".9"/>'  # воротник
    s += el(228, 248, 16, 8, "#3A2617", .55)
    s += el(298, 248, 16, 8, "#3A2617", .55)
    s += el(262, 300, 12, 7, "#C08D6A", .45)
    s += '</g>\n'
    s += tail(w, h)
    write("master.svg", s)


# ── ИНТЕРЬЕРЫ СТУДИИ ───────────────────────────────────────────────────
def interior(name, label, grad, far, mid, near=(), w=460, h=345):
    a, b, c = grad
    defs = ('  <linearGradient id="bg" x1="0" y1="0" x2=".8" y2="1">'
            f'<stop offset="0" stop-color="{a}"/><stop offset=".55" stop-color="{b}"/>'
            f'<stop offset="1" stop-color="{c}"/></linearGradient>')
    s = head(w, h, label, defs)
    s += f'<rect width="{w}" height="{h}" fill="url(#bg)"/>\n'
    s += '<g filter="url(#far)">' + ''.join(far) + '</g>\n'
    s += '<g filter="url(#mid)">' + ''.join(mid) + '</g>\n'
    if near:
        s += '<g filter="url(#near)">' + ''.join(near) + '</g>\n'
    s += tail(w, h)
    write(name, s)


# ── ДО / ПОСЛЕ ─────────────────────────────────────────────────────────
def before_after(name, label, before, after, w=520, h=347):
    half = w // 2
    defs = ('  <linearGradient id="bgL" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{before[0]}"/><stop offset="1" stop-color="{before[1]}"/></linearGradient>\n'
            '  <linearGradient id="bgR" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{after[0]}"/><stop offset="1" stop-color="{after[1]}"/></linearGradient>\n'
            '  <linearGradient id="scrim" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#2A1B10" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#2A1B10" stop-opacity=".5"/></linearGradient>\n'
            f'  <clipPath id="cl"><rect width="{half}" height="{h}"/></clipPath>\n'
            f'  <clipPath id="cr"><rect x="{half}" width="{w-half}" height="{h}"/></clipPath>')
    s = head(w, h, label, defs)

    s += f'<g clip-path="url(#cl)"><rect width="{w}" height="{h}" fill="url(#bgL)"/><g filter="url(#far)">'
    s += el(132, 152, 124, 146, "#E2B991", .88)
    s += '</g><g filter="url(#mid)">'
    s += el(96, 120, 44, 34, "#C79A72", .55)
    s += el(152, 230, 60, 40, "#D6A87F", .50)
    s += el(120, 176, 30, 22, "#CFA079", .45)
    s += '</g></g>\n'

    s += f'<g clip-path="url(#cr)"><rect width="{w}" height="{h}" fill="url(#bgR)"/><g filter="url(#far)">'
    s += el(390, 152, 124, 146, "#F2D1AD", .94)
    s += '</g><g filter="url(#mid)">'
    s += el(358, 116, 46, 36, "#FAE3C6", .60)
    s += el(412, 226, 60, 42, "#F5D6B3", .55)
    s += '</g></g>\n'

    s += f'<rect x="{half-1}" width="2" height="{h}" fill="#FAF5EC" opacity=".75"/>\n'
    s += f'<rect y="{h-56}" width="{w}" height="56" fill="url(#scrim)"/>\n'
    s += ('<g font-family="Golos, Manrope, sans-serif" font-size="11" font-weight="600" '
          'letter-spacing="1.8" fill="#FDF6EA">'
          f'<text x="20" y="{h-19}">ДО</text><text x="{half+20}" y="{h-19}">ПОСЛЕ</text></g>\n')
    s += tail(w, h)
    write(name, s)


# ── СХЕМА ПРОЕЗДА ──────────────────────────────────────────────────────
# Рисованная схема, а не скриншот карты: так честнее и выглядит своим.
def map_svg(w=760, h=522):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
         'role="img" aria-label="Схема проезда: Суворовский проспект, 35">\n'
         '<defs><filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4"/>'
         '<feColorMatrix type="saturate" values="0"/></filter></defs>\n'
         f'<rect width="{w}" height="{h}" fill="#EFE4D2"/>\n')

    blocks = [(46, 62, 140, 116), (238, 40, 160, 140), (452, 70, 168, 108), (66, 250, 130, 118),
              (252, 236, 148, 140), (452, 250, 188, 128), (66, 424, 130, 74), (452, 424, 218, 70)]
    s += '<g fill="#E5D6BD">' + ''.join(
        f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="3"/>' for x, y, bw, bh in blocks) + '</g>\n'

    s += ('<g stroke="#FBF6EC" stroke-linecap="square">'
          '<path d="M0 212H760" stroke-width="26"/>'
          '<path d="M424 0V522" stroke-width="30"/>'
          '<path d="M0 400H760" stroke-width="18"/>'
          '<path d="M220 0V522" stroke-width="16"/></g>\n'
          '<g stroke="#DCC7A6" stroke-width="1" stroke-dasharray="7 7">'
          '<path d="M0 212H760"/><path d="M424 0V522"/></g>\n')

    s += ('<g fill="#CAD2B3" opacity=".9"><circle cx="678" cy="150" r="44"/>'
          '<circle cx="702" cy="196" r="28"/><circle cx="122" cy="470" r="30"/></g>\n')

    s += ('<g font-family="Golos, Manrope, sans-serif" fill="#8A7458" font-size="11" '
          'font-weight="600" letter-spacing="1.6">'
          '<text x="46" y="198">КИРОЧНАЯ УЛ.</text>'
          '<text x="46" y="388">УЛ. МОИСЕЕНКО</text>'
          '<text transform="rotate(-90 452 132)" x="452" y="132">СУВОРОВСКИЙ ПР-Т</text>'
          '<text x="606" y="122" fill="#7E8C63">САД</text></g>\n')

    s += ('<g font-family="Golos, Manrope, sans-serif" font-size="11.5" font-weight="600">'
          '<circle cx="220" cy="212" r="8" fill="#B23A2A"/>'
          '<text x="238" y="207" fill="#6A5949">М «Чернышевская»</text>'
          '<text x="238" y="223" fill="#96836E" font-weight="400">12 минут пешком</text>'
          '<circle cx="220" cy="400" r="8" fill="#B23A2A"/>'
          '<text x="238" y="395" fill="#6A5949">М «Площадь Восстания»</text>'
          '<text x="238" y="411" fill="#96836E" font-weight="400">15 минут пешком</text></g>\n')

    s += ('<g><path d="M424 252c-19 0-34 15-34 34 0 25 34 58 34 58s34-33 34-58c0-19-15-34-34-34z" fill="#9A4B24"/>'
          '<circle cx="424" cy="286" r="11" fill="#F5EEE3"/>'
          '<g font-family="Cormorant, Georgia, serif" font-size="20" font-weight="600" fill="#241A13">'
          '<text x="470" y="286">VIV Studio</text></g>'
          '<g font-family="Golos, Manrope, sans-serif" font-size="11.5" fill="#6A5949">'
          '<text x="470" y="305">Суворовский пр-т, 35 · офис 409</text></g></g>\n')

    s += f'<rect width="{w}" height="{h}" filter="url(#grain)" opacity=".07"/>\n</svg>\n'
    write("map.svg", s)


# ── КАРТИНКА ДЛЯ СОЦСЕТЕЙ ──────────────────────────────────────────────
def og(w=1200, h=630):
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="VIV Studio — лазерная эпиляция, Санкт-Петербург">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F7F1E7"/><stop offset="1" stop-color="#E9DCC7"/></linearGradient></defs>
<rect width="{w}" height="{h}" fill="url(#g)"/>
<rect x="820" width="380" height="{h}" fill="#1B130E"/>
<g font-family="Cormorant, Georgia, serif" fill="#241A13">
  <text x="76" y="140" font-size="20" letter-spacing="6" font-weight="600">VIV STUDIO</text>
  <text x="76" y="300" font-size="72" font-weight="500">Лазерная эпиляция,</text>
  <text x="76" y="378" font-size="72" font-weight="500" font-style="italic" fill="#9A4B24">которая заканчивается</text>
</g>
<g font-family="Golos, Manrope, sans-serif" fill="#61503F" font-size="20"><text x="76" y="438">Санкт-Петербург · Суворовский, 35</text></g>
<g font-family="Cormorant, Georgia, serif" fill="#9A4B24"><text x="76" y="544" font-size="52" font-weight="600">1 450 ₽</text></g>
<g font-family="Golos, Manrope, sans-serif" fill="#96836E" font-size="17"><text x="222" y="544">первый визит вместо 2 900 ₽</text></g>
<g font-family="Cormorant, Georgia, serif" fill="#D9BE8C" text-anchor="middle"><text x="1010" y="316" font-size="104" font-weight="500">5,0</text></g>
<g font-family="Golos, Manrope, sans-serif" fill="#B7A48A" font-size="15" text-anchor="middle"><text x="1010" y="352">53 оценки на Яндекс Картах</text></g>
</svg>
'''
    write("og.svg", s)


if __name__ == "__main__":
    hero()
    master()

    # ресепшн: стойка, лампа, рамка на стене
    interior("reception.svg", "Ресепшн студии", ("#F2E5CF", "#E0CBAA", "#BE9E76"),
             far=[el(70, 60, 160, 130, "#FDF4E0", .85), el(400, 300, 140, 110, "#A8835A", .35)],
             mid=[rc(0, 196, 460, 10, "#B08A5E", .45),                 # линия стены и пола
                  rc(58, 206, 344, 150, "#C08F5D", .90, 6),            # стойка
                  rc(58, 206, 344, 16, "#EBCB9E", .70, 4),             # столешница в свету
                  rc(292, 62, 96, 106, "#F8EBD2", .80, 3),             # рамка на стене
                  rc(302, 74, 76, 82, "#DCC4A0", .70, 2)],
             near=[el(120, 186, 17, 30, "#E9D3B0", .9),                # ваза
                   el(360, 168, 22, 22, "#FBEBC8", .85),               # лампа
                   rc(196, 190, 66, 14, "#F2E2C4", .55, 3)])           # стопка бумаг

    # кабинет: окно, кушетка, аппарат
    interior("room.svg", "Кабинет студии", ("#F4E9D7", "#DFCBAC", "#B79874"),
             far=[el(360, 70, 170, 140, "#FEF6E6", .9), el(60, 300, 120, 100, "#C1A176", .40)],
             mid=[rc(0, 190, 460, 10, "#AC875C", .42),
                  rc(300, 34, 132, 150, "#FBEDD2", .88, 3),            # окно
                  rc(46, 214, 330, 92, "#EFE2CC", .92, 22),            # кушетка
                  rc(46, 214, 330, 18, "#FBF3E3", .75, 10),
                  rc(392, 176, 52, 130, "#8A6842", .70, 6)],           # аппарат у стены
             near=[rc(364, 34, 5, 150, "#B08A5E", .55),                # переплёт окна
                   rc(300, 106, 132, 5, "#B08A5E", .55),
                   el(104, 206, 30, 12, "#FBF3E3", .6)])               # подушка

    # аппарат: корпус, экран, манипулятор
    interior("device.svg", "Лазерный аппарат", ("#EBDEC8", "#CFB897", "#9F8763"),
             far=[el(378, 84, 120, 110, "#FAEBCB", .70), el(90, 300, 130, 100, "#8E7351", .35)],
             mid=[rc(0, 236, 460, 10, "#A8855C", .40),
                  rc(158, 96, 148, 210, "#33240F", .92, 10),           # корпус
                  rc(176, 118, 112, 66, "#F0D9AE", .88, 4),            # экран
                  rc(176, 200, 112, 10, "#6E5433", .70, 4)],
             near=[rc(292, 130, 96, 8, "#4A3520", .75, 4),             # манипулятор
                   el(392, 140, 18, 14, "#1F160B", .8),
                   el(232, 152, 26, 16, "#FBEBC6", .35)])              # блик на экране

    # сертификаты: рамки на стене и полка
    interior("certs.svg", "Сертификаты мастера", ("#F3E7D3", "#E2D0B2", "#C1A87F"),
             far=[el(60, 60, 140, 120, "#FEF7E8", .75), el(400, 290, 130, 100, "#B0906A", .35)],
             mid=[rc(74, 66, 118, 152, "#FBF3E2", .95, 3),
                  rc(88, 82, 90, 120, "#E6D5B6", .80, 2),
                  rc(216, 92, 104, 132, "#FBF3E2", .92, 3),
                  rc(228, 106, 80, 104, "#E6D5B6", .78, 2),
                  rc(344, 70, 82, 106, "#FBF3E2", .88, 3),
                  rc(354, 82, 62, 82, "#E6D5B6", .74, 2),
                  rc(0, 268, 460, 12, "#B08A5E", .45)],
             near=[el(80, 258, 18, 26, "#D9BE8C", .7)])

    before_after("ba-1.svg", "Контурная пластика губ — до и после", ("#E3C7A6", "#CBA983"), ("#F2DCC0", "#E0BF9A"))
    before_after("ba-2.svg", "Чистка лица — до и после", ("#DFC3A2", "#C7A37D"), ("#F4E0C6", "#E3C4A0"))
    before_after("ba-3.svg", "Биоревитализация — до и после", ("#E1C6A7", "#C9A681"), ("#F3DEC3", "#E2C29E"))

    map_svg()
    og()
