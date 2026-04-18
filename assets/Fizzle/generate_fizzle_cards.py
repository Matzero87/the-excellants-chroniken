from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from PIL import Image

OUT_PATH = '/home/marcel/Schreibtisch/DnD-Website/Fizzle_Gadget_Karten_duplex.pdf'
BANNER_PATH = '/home/marcel/Schreibtisch/DnD-Website/banner.jpg'
FIZZLE_PATH = '/home/marcel/Schreibtisch/DnD-Website/assets/Fizzle/Fizzle.PNG'
WERKSTATT = '/home/marcel/Schreibtisch/DnD-Website/assets/Fizzle/Fizzles Werkstatt/'

PAGE_W, PAGE_H = A4
CARD_W = 63 * mm
CARD_H = 88 * mm
COLS = 3
ROWS = 3
LEFT = (PAGE_W - COLS * CARD_W) / 2
BOTTOM = (PAGE_H - ROWS * CARD_H) / 2

GOLD = HexColor('#c9a85d')
GOLD_DARK = HexColor('#8b6a2d')
PARCHMENT = HexColor('#efe1b8')
PARCHMENT_DARK = HexColor('#dbc79d')
INK = HexColor('#2b2116')
RED = HexColor('#8d2e24')
STEEL = HexColor('#46505a')
SMOKE = HexColor('#6d6254')
BLUE = HexColor('#2b6f7f')
GREEN = HexColor('#486b34')
BORDER = HexColor('#5f4721')

cards = [
    {
        'name': 'Funkenherz Mk. II',
        'kind': 'Gadget',
        'action': 'Aktion',
        'tagline': 'Fast stabil. Angeblich.',
        'desc': 'Pulsierendes Geraet aus Kupfer und Glas. Glimmt und knistert unruhig.',
        'effect': 'Geworfen oder aktiviert: 1W6 Feuerschaden an ein Ziel oder kleinen Bereich.',
        'great': '2W6 Feuerschaden. Ziel steht kurz in Flammen oder wird erschreckt.',
        'fail': 'Ueberladen: 1W4 Schaden an Fizzle oder nur Rauch und dramatisches Zischen.',
        'flavor': 'Fizzles erste „wirklich funktionierende" Erfindung. Laut ihm.',
        'accent': RED,
        'image': WERKSTATT + 'FunkenHerz MK.II.PNG',
        'back_title': 'Fizzles Werkstatt'
    },
    {
        'name': 'Greifklau 3000',
        'kind': 'Gadget',
        'action': 'Aktion',
        'tagline': 'Praezisionswerkzeug. Wohl kaum.',
        'desc': 'Mechanischer Greifarm mit Magnetkern und ausfahrbaren Fingern an einem Lederhandschuh.',
        'effect': 'Zieht kleine Gegenstaende heran oder stoert ein Ziel in Griffweite auf Distanz.',
        'great': 'Gegner kurz festgehalten oder entwaffnet. Objekte aus der Distanz manipulieren.',
        'fail': 'Bleibt haengen, zieht dich falsch oder greift etwas voellig Falsches.',
        'flavor': 'Fizzle nennt es Praezisionswerkzeug. Alle anderen nennen es gefaehrlich.',
        'accent': STEEL,
        'image': WERKSTATT + 'Greifklau.PNG',
        'back_title': 'Greifen. Reissen. Hoffen.'
    },
    {
        'name': 'Uberdruck-Regulator',
        'kind': 'Gadget',
        'action': 'Aktion',
        'tagline': 'Mobilitaet durch kontrollierte Explosionen.',
        'desc': 'Roehrenfoermiges Geraet mit Ventilen und einem viel zu grossen Hebel. Zischt bedrohlich.',
        'effect': 'Stosswelle draengt Gegner zurueck oder schafft Distanz.',
        'great': 'Gegner stark zurueckgestossen oder gefallen. Du repositionierst dich sofort.',
        'fail': 'Druck entlaedt sich falsch: du fliegst selbst oder ein lauter Knall verraet dich.',
        'flavor': 'Fuer Fizzle ist das die Zukunft der Mobilitaet.',
        'accent': BLUE,
        'image': WERKSTATT + '\u00dcberdruck-Regulator.PNG',
        'back_title': 'Druck macht Tempo'
    },
    {
        'name': 'Rauchkapsel',
        'kind': 'Gadget',
        'action': 'Bonusaktion/Aktion',
        'tagline': 'Mehr Laerm als Nutzen. Oft beides.',
        'desc': 'Kleine Glas- oder Metallkapseln mit uebertriebenem Innendruck.',
        'effect': 'Auf einen Punkt geworfen: 3 m Radius stark verdeckt. Gegner haben Nachteil.',
        'great': 'Zusaetzlich Furcht oder Verwirrung fuer 1 Runde bei unvorbereiteten Feinden.',
        'fail': 'Fizzle steht selbst im Rauch oder der Knall zieht sofort Aufmerksamkeit an.',
        'flavor': 'Kann auch Fizzle einnebeln. Zaehlt nicht als Konstruktionsfehler.',
        'accent': SMOKE,
        'image': WERKSTATT + 'Rauchkapsel.PNG',
        'back_title': 'Nebel ist nur Taktik'
    },
    {
        'name': 'Federfalle',
        'kind': 'Gadget',
        'action': 'Aktion (vorbereitet)',
        'tagline': 'Eine konzeptionelle Falle.',
        'desc': 'Zusammenklappbares Geraet aus Federn, Zaehnraedern und fragwuerdigen Entscheidungen.',
        'effect': 'Bei Ausloesung: DEX-Save. Bei Fehlschlag festgesetzt und 1W6 Schaden.',
        'great': 'Haelt zwei Gegner fest oder laenger als erwartet.',
        'fail': 'Loest sofort aus. Sehr oft auf Fizzle.',
        'flavor': '\u201eDas ist eine konzeptionelle Falle!\u201c \u2014 Fizzle',
        'accent': GREEN,
        'image': WERKSTATT + 'Federfalle.PNG',
        'back_title': 'Schnapp. Aua. Wissenschaft.'
    },
    {
        'name': 'Magnetgeraet',
        'kind': 'Gadget',
        'action': 'Aktion',
        'tagline': 'Zieht Metall an. Leider alles.',
        'desc': 'Ueberladener Magnet mit Kurbelmechanismus.',
        'effect': 'Metalltraeger: STR-Save. Bei Fehlschlag faellt die Waffe oder Bewegung halbiert sich.',
        'great': 'Gegner komplett festgezogen oder entwaffnet.',
        'fail': 'Zieht Fizzle zum Gegner oder reisst saemtliches Metall im Umkreis los.',
        'flavor': 'Inklusive Fizzle. Vor allem inklusive Fizzle.',
        'accent': STEEL,
        'image': WERKSTATT + 'Magnetgerät.PNG',
        'back_title': 'Pol des Problems'
    },
    {
        'name': 'Mini-Flammenwerfer',
        'kind': 'Gadget',
        'action': 'Aktion (Kegel)',
        'tagline': 'Kuechenunfall, aber bewaffnet.',
        'desc': 'Eine Mischung aus Flammenwerfer und Kuechenunfall.',
        'effect': '5 m Kegel, 2W8 Feuerschaden, DEX-Save halbiert.',
        'great': 'Ziel brennt weiter und nimmt 1W6 pro Runde.',
        'fail': 'Rueckstoss: Fizzle brennt fuer 1W6 oder Boden bleibt gefaehrlich entflammt.',
        'flavor': 'Kaum jemand darf in Innenraeumen experimentieren. Fizzle schon gar nicht.',
        'accent': RED,
        'image': WERKSTATT + 'Mini-Flammenwerfer.PNG',
        'back_title': 'Mehr Hitze, weniger Plan'
    },
    {
        'name': 'Denkerhelm (Beta)',
        'kind': 'Ausrüstung',
        'action': 'Ausrüstung',
        'tagline': 'Erhoeht Konzentration. Oder Ideen.',
        'desc': 'Helm mit drehenden Zaehnraedern und blinkenden Lichtern.',
        'effect': 'Verbessert Konzentration oder liefert absurde Eingebungen; im Zweifel beides.',
        'great': 'Wahrer Moment der Genialitaet: Bonus auf INT-basierte Idee oder Analyse.',
        'fail': 'Absurde Idee statt Konzentration.',
        'flavor': '\u201eIch bin mir ziemlich sicher, dass ich damit schlauer werde.\u201c \u2014 Fizzle',
        'accent': GOLD_DARK,
        'image': WERKSTATT + 'Denkerhelm.PNG',
        'back_title': 'Genie unter Spannung'
    },
    {
        'name': 'A.V.A.',
        'kind': 'Begleiterin',
        'action': 'Reaktion/Support',
        'tagline': 'Vielleicht loyal. Definitiv bewaffnet.',
        'desc': 'Autonome Verteidigungs-Assistentin. Oder Adaptive Vernichtungs-Aparatur.',
        'effect': 'Stellt sich im Schutzmodus vor Fizzle, blockt Angriffe oder reagiert schneller.',
        'great': 'Schutzmodus verhindert Treffer oder verschafft Verbuendeten Deckung/Vorteil.',
        'fail': 'Reagiert eigensinnig, falsch priorisiert oder nur mit beleidigtem KRRRRT.',
        'flavor': 'Sie wirkt fast lebendig. Das beruhigt niemanden.',
        'accent': BLUE,
        'image': WERKSTATT + 'AvA.PNG',
        'back_title': 'KRRRRT'
    },
]


def fit_text(c, text, font_name, max_size, min_size, width):
    size = max_size
    while size >= min_size:
        if stringWidth(text, font_name, size) <= width:
            return size
        size -= 0.3
    return min_size


def draw_crop_marks(c, x, y, w, h, mark=4*mm):
    c.setStrokeColor(HexColor('#888888'))
    c.setLineWidth(0.35)
    c.line(x - mark, y, x - 1*mm, y)
    c.line(x, y - mark, x, y - 1*mm)
    c.line(x + w + 1*mm, y, x + w + mark, y)
    c.line(x + w, y - mark, x + w, y - 1*mm)
    c.line(x - mark, y + h, x - 1*mm, y + h)
    c.line(x, y + h + 1*mm, x, y + h + mark)
    c.line(x + w + 1*mm, y + h, x + w + mark, y + h)
    c.line(x + w, y + h + 1*mm, x + w, y + h + mark)


def draw_image_cover(c, path, x, y, w, h, anchor='center'):
    img = Image.open(path)
    iw, ih = img.size
    target_ratio = w / h
    img_ratio = iw / ih
    if img_ratio > target_ratio:
        new_h = ih
        new_w = int(ih * target_ratio)
        left = (iw - new_w) // 2
        box = (left, 0, left + new_w, ih)
    else:
        new_w = iw
        new_h = int(iw / target_ratio)
        top = max(0, (ih - new_h) // 3 if anchor == 'top' else (ih - new_h) // 2)
        box = (0, top, iw, min(ih, top + new_h))
    cropped = img.crop(box)
    c.drawImage(ImageReader(cropped), x, y, width=w, height=h, mask='auto')


def _wrap_text(text, font, size, max_width):
    from reportlab.pdfbase.pdfmetrics import stringWidth as sw
    words = text.split()
    lines = []
    current = ''
    for w in words:
        test = (current + ' ' + w).strip()
        if sw(test, font, size) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def _draw_text_lines(c, text, font, size, color, x, y, max_width, leading):
    lines = _wrap_text(text, font, size, max_width)
    c.setFillColor(color)
    c.setFont(font, size)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return len(lines) * leading


def draw_front(c, card, x, y):
    """
    Layout after removing flavor text — more breathing room.
    
    Header bar: 5–12mm from top (7mm height), title at 9.5mm
    Kind/Action: 14.5mm from top  
    Art: starts at 17mm from top, 22mm height, bottom at 39mm from top
    Tagline ribbon: below art
    Text sections: below tagline, down to 4mm from bottom
    """
    # outer card
    c.setFillColor(PARCHMENT)
    c.setStrokeColor(BORDER)
    c.setLineWidth(1.0)
    c.roundRect(x, y, CARD_W, CARD_H, 4*mm, fill=1, stroke=1)

    # inner frame
    inset = 2.2*mm
    c.setStrokeColor(GOLD_DARK)
    c.setLineWidth(0.7)
    c.roundRect(x+inset, y+inset, CARD_W-2*inset, CARD_H-2*inset, 3*mm, fill=0, stroke=1)

    # header bar — title plus kind/action inside the same frame
    header_h = 10*mm
    header_y = y + CARD_H - 14*mm
    c.setFillColor(card['accent'])
    c.roundRect(x+inset, header_y, CARD_W-2*inset, header_h, 2*mm, fill=1, stroke=0)

    title_size = fit_text(c, card['name'], 'Times-Bold', 9.2, 6.8, CARD_W-14*mm)
    c.setFillColor(white)
    c.setFont('Times-Bold', title_size)
    c.drawCentredString(x + CARD_W/2, header_y + 6.3*mm, card['name'])

    c.setStrokeColor(HexColor('#ead9b2'))
    c.setLineWidth(0.25)
    c.line(x + 4.5*mm, header_y + 3.8*mm, x + CARD_W - 4.5*mm, header_y + 3.8*mm)

    c.setFillColor(HexColor('#f7ecd2'))
    c.setFont('Times-Bold', 5.4)
    c.drawString(x + 4.5*mm, header_y + 1.4*mm, card['kind'].upper())
    c.setFont('Times-Italic', 5.2)
    c.drawRightString(x + CARD_W - 4.5*mm, header_y + 1.4*mm, card['action'])

    # art frame — narrower and a touch taller to avoid over-cropping portrait art
    art_w = 34*mm
    art_h = 25*mm
    art_x = x + (CARD_W - art_w) / 2
    art_y = header_y - 2.4*mm - art_h
    c.setFillColor(PARCHMENT_DARK)
    c.roundRect(art_x, art_y, art_w, art_h, 1.5*mm, fill=1, stroke=0)
    draw_image_cover(c, card['image'], art_x, art_y, art_w, art_h, anchor='top')
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.5)
    c.roundRect(art_x, art_y, art_w, art_h, 1.5*mm, fill=0, stroke=1)

    # tagline ribbon — below art
    c.setFillColor(GOLD)
    c.roundRect(x+6*mm, art_y-4.2*mm, CARD_W-12*mm, 4.2*mm, 1.2*mm, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont('Times-Italic', 6.0)
    c.drawCentredString(x + CARD_W/2, art_y - 2.8*mm, card['tagline'])

    # Text sections
    text_x = x + 3.5*mm
    text_w = CARD_W - 7*mm
    cursor = art_y - 7*mm
    bottom_limit = y + 5*mm

    sections = [
        ('Beschreibung', card['desc']),
        ('Effekt', card['effect']),
        ('Voller Erfolg', card['great']),
        ('Fehlschlag', card['fail']),
    ]

    BODY_FONT = 'Times-Roman'
    BODY_SIZE = 6.0
    BODY_LEADING = 8.0
    LABEL_FONT = 'Times-Bold'
    LABEL_SIZE = 6.5
    SECTION_GAP = 2.2 * mm
    LABEL_BODY_GAP = 2.5 * mm

    for label, body in sections:
        if cursor < bottom_limit + 3*mm:
            break
        c.setFillColor(card['accent'])
        c.setFont(LABEL_FONT, LABEL_SIZE)
        c.drawString(text_x, cursor, label)
        cursor -= LABEL_BODY_GAP

        h = _draw_text_lines(c, body, BODY_FONT, BODY_SIZE, INK, text_x, cursor, text_w, BODY_LEADING)
        cursor -= h + SECTION_GAP

    draw_crop_marks(c, x, y, CARD_W, CARD_H)


def draw_back(c, card, x, y):
    c.setFillColor(HexColor('#120f0c'))
    c.setStrokeColor(BORDER)
    c.setLineWidth(1.0)
    c.roundRect(x, y, CARD_W, CARD_H, 4*mm, fill=1, stroke=1)

    # banner background
    draw_image_cover(c, BANNER_PATH, x+1.2*mm, y+1.2*mm, CARD_W-2.4*mm, CARD_H-2.4*mm, anchor='center')

    # dark overlay for readability
    c.setFillColor(HexColor('#120f0c'))
    c.setFillAlpha(0.52)
    c.roundRect(x+1.2*mm, y+1.2*mm, CARD_W-2.4*mm, CARD_H-2.4*mm, 3.2*mm, fill=1, stroke=0)
    c.setFillAlpha(1)

    # ornate border
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.9)
    c.roundRect(x+2.3*mm, y+2.3*mm, CARD_W-4.6*mm, CARD_H-4.6*mm, 3*mm, fill=0, stroke=1)
    c.setStrokeColor(GOLD_DARK)
    c.setLineWidth(0.4)
    c.roundRect(x+3.5*mm, y+3.5*mm, CARD_W-7*mm, CARD_H-7*mm, 2.3*mm, fill=0, stroke=1)

    # center medallion with fizzle portrait
    med_w = 30*mm
    med_h = 30*mm
    med_x = x + (CARD_W - med_w)/2
    med_y = y + CARD_H/2 - med_h/2 + 2*mm
    c.setFillColor(HexColor('#2a1f17'))
    c.circle(x + CARD_W/2, y + CARD_H/2 + 2*mm, 16.5*mm, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.0)
    c.circle(x + CARD_W/2, y + CARD_H/2 + 2*mm, 16.5*mm, fill=0, stroke=1)
    c.setLineWidth(0.4)
    c.circle(x + CARD_H/2, y + CARD_H/2 + 2*mm, 14.8*mm, fill=0, stroke=1)
    draw_image_cover(c, FIZZLE_PATH, med_x, med_y, med_w, med_h, anchor='top')

    # top/bottom text
    c.setFillColor(GOLD)
    c.setFont('Times-Bold', 11)
    c.drawCentredString(x + CARD_W/2, y + CARD_H - 12*mm, 'FIZZLES')
    c.setFont('Times-Bold', 9.5)
    c.drawCentredString(x + CARD_H/2, y + CARD_H - 16.8*mm, 'WERKSTATT')

    c.setFont('Times-Italic', 7.0)
    c.drawCentredString(x + CARD_W/2, y + 17*mm, card['back_title'])

    c.setFont('Times-Roman', 6.4)
    c.setFillColor(PARCHMENT)
    c.drawCentredString(x + CARD_W/2, y + 11.5*mm, 'Die Excellants')
    c.drawCentredString(x + CARD_W/2, y + 8*mm, 'Erfindungen, die fast funktionieren.')

    # corner ornaments
    c.setFillColor(GOLD)
    for dx in (7*mm, CARD_W-7*mm):
        for dy in (7*mm, CARD_H-7*mm):
            c.circle(x+dx, y+dy, 1.1*mm, fill=1, stroke=0)

    draw_crop_marks(c, x, y, CARD_W, CARD_H)


def positions():
    pts = []
    for row in range(ROWS):
        for col in range(COLS):
            x = LEFT + col * CARD_W
            y = PAGE_H - BOTTOM - (row + 1) * CARD_H
            pts.append((x, y, row, col))
    return pts


def build_pdf():
    c = canvas.Canvas(OUT_PATH, pagesize=A4)
    pts = positions()

    # fronts
    for i, card in enumerate(cards):
        x, y, _, _ = pts[i]
        draw_front(c, card, x, y)
    c.showPage()

    # backs mirrored by columns for duplex printing
    for i, card in enumerate(cards):
        _, _, row, col = pts[i]
        mirrored_col = COLS - 1 - col
        x = LEFT + mirrored_col * CARD_W
        y = PAGE_H - BOTTOM - (row + 1) * CARD_H
        draw_back(c, card, x, y)
    c.showPage()
    c.save()
    return OUT_PATH


if __name__ == '__main__':
    path = build_pdf()
    print(path)