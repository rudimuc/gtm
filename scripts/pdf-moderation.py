#!/usr/bin/env python3
"""Moderationsblatt für die 30-Minuten-Einführung (A4, mit Grafiken).

Aufruf:  python3 scripts/pdf-moderation.py      (benötigt: pip install reportlab)
Ergebnis: unterlagen/pdf/moderation-einfuehrung.pdf
"""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
                                KeepTogether, Table, TableStyle, HRFlowable)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon, Circle, Group
from reportlab.graphics import renderPDF

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "unterlagen" / "pdf" / "moderation-einfuehrung.pdf"
W = 17 * cm  # Inhaltsbreite

DARK = colors.HexColor("#1f2937"); GREY = colors.HexColor("#6b7280"); LIGHT = colors.HexColor("#f3f4f6")
ACC = colors.HexColor("#c2410c"); ACC_L = colors.HexColor("#ffedd5")
BLUE = colors.HexColor("#1d4ed8"); BLUE_L = colors.HexColor("#dbeafe")
GREEN = colors.HexColor("#15803d"); GREEN_L = colors.HexColor("#dcfce7")
RED = colors.HexColor("#b91c1c"); RED_L = colors.HexColor("#fee2e2")
PURPLE = colors.HexColor("#6d28d9"); PURPLE_L = colors.HexColor("#ede9fe")

body = ParagraphStyle("b", fontName="Helvetica", fontSize=10.8, leading=14.8, textColor=DARK, spaceAfter=3)
small = ParagraphStyle("s", parent=body, fontSize=8.5, leading=11, textColor=GREY)
bul = ParagraphStyle("bul", parent=body, leftIndent=14, bulletIndent=2, spaceAfter=3.5)
title = ParagraphStyle("t", parent=body, fontName="Helvetica-Bold", fontSize=22, leading=26, textColor=ACC, spaceAfter=2)
h2 = ParagraphStyle("h2", parent=body, fontName="Helvetica-Bold", fontSize=13, leading=16, spaceBefore=8, spaceAfter=4)


def B(items, style=bul):
    return [Paragraph(t, style, bulletText="•") for t in items]


def blockkopf(zeit, text, farbe=ACC):
    t = Table([[Paragraph(f'<font color="white"><b>{zeit}</b></font>', ParagraphStyle("z", parent=body, alignment=1, spaceAfter=0)),
                Paragraph(f"<b>{text}</b>", ParagraphStyle("k", parent=body, fontSize=13, leading=16, spaceAfter=0))]],
              colWidths=[2.6 * cm, W - 2.6 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, 0), farbe), ("BACKGROUND", (1, 0), (1, 0), LIGHT),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                           ("LEFTPADDING", (1, 0), (1, 0), 8)]))
    return t


# ---------- Zeichenhelfer ----------
def box(d, x, y, w, h, fill, stroke, text="", size=9, bold=True, color=DARK, lines=None):
    d.add(Rect(x, y, w, h, rx=6, ry=6, fillColor=fill, strokeColor=stroke, strokeWidth=1.2))
    ls = lines or ([text] if text else [])
    n = len(ls); lh = size + 2
    for i, l in enumerate(ls):
        d.add(String(x + w / 2, y + h / 2 + (n - 1) * lh / 2 - i * lh - size * 0.33, l, fontName="Helvetica-Bold" if (bold and i == 0) else "Helvetica",
                     fontSize=size, fillColor=color, textAnchor="middle"))


def pfeil(d, x1, y1, x2, y2, farbe=DARK, w=1.6):
    d.add(Line(x1, y1, x2, y2, strokeColor=farbe, strokeWidth=w))
    import math
    a = math.atan2(y2 - y1, x2 - x1); s = 6
    d.add(Polygon([x2, y2, x2 - s * math.cos(a - 0.4), y2 - s * math.sin(a - 0.4), x2 - s * math.cos(a + 0.4), y2 - s * math.sin(a + 0.4)],
                  fillColor=farbe, strokeColor=farbe, strokeWidth=0.5))


def txt(d, x, y, s, size=8.5, color=GREY, anchor="middle", bold=False, font=None):
    d.add(String(x, y, s, fontName=font or ("Helvetica-Bold" if bold else "Helvetica"), fontSize=size, fillColor=color, textAnchor=anchor))


def zeitleiste():
    d = Drawing(482, 78)
    seg = [(3, "Idee", BLUE), (5, "Oberfläche", BLUE), (5, "Trigger", BLUE), (8, "Datenfluss", ACC), (5, "REST + Logik", BLUE), (4, "Agent + Fragen", PURPLE)]
    sc = 482 / 30.0; x = 0; t = 0
    for m, name, c in seg:
        d.add(Rect(x, 32, m * sc - 2, 30, fillColor=c, strokeColor=colors.white, strokeWidth=0))
        txt(d, x + (m * sc - 2) / 2, 43, name, size=8 if m < 5 else 9, color=colors.white, bold=True)
        txt(d, x, 18, f"{t}", size=8.5, anchor="start"); x += m * sc; t += m
    txt(d, 482, 18, "30 min", size=8.5, anchor="end")
    txt(d, 3.5 * sc * 0 + 241, 3, "Fragen jederzeit erlaubt, Flipchart für Zurückgestelltes. Datenfluss bekommt die meiste Zeit.", size=8.5, color=GREY)
    return d


def bild_ablauf():
    d = Drawing(482, 118)
    xs = [0, 130, 260, 390]; wb = 92
    namen = [("AUSLÖSER", "Trigger", GREEN_L, GREEN), ("SCHRITT", "Node", BLUE_L, BLUE), ("SCHRITT", "Node", BLUE_L, BLUE), ("ERGEBNIS", "Antwort", ACC_L, ACC)]
    bsp = ["Formular wird", "abgeschickt", "Daten holen", "(HTTP Request)", "Entscheiden", "(IF)", "Text anzeigen", "(Form Ending)"]
    for i, (x, (a, b, f, s)) in enumerate(zip(xs, namen)):
        box(d, x, 50, wb, 52, f, s, lines=[a, b], size=10)
        txt(d, x + wb / 2, 34, bsp[2 * i], size=8.5); txt(d, x + wb / 2, 23, bsp[2 * i + 1], size=8.5)
        if i < 3:
            pfeil(d, x + wb + 3, 76, xs[i + 1] - 3, 76)
    txt(d, 241, 4, "Eine Linie = Datenfluss: Jeder Schritt bekommt die Daten des vorigen.", size=8.5, color=DARK)
    return d


def bild_node():
    d = Drawing(482, 132)
    cols = [("EINGABE", "Daten vom vorigen Node", "Von hier Felder in die", "Einstellungen ziehen", BLUE_L, BLUE),
            ("EINSTELLUNGEN", "Was der Node tut", "z. B. URL, Bedingung,", "Feldnamen", ACC_L, ACC),
            ("AUSGABE", "Ergebnis dieses Nodes", "Hier prüfen. Mit Pin", "festhalten (Testdaten)", GREEN_L, GREEN)]
    for i, (h, a, b, c, f, s) in enumerate(cols):
        x = i * 164
        box(d, x, 38, 154, 82, f, s, lines=[h, a, b, c], size=9)
    d.add(Rect(0, 0, 482, 26, rx=5, ry=5, fillColor=LIGHT, strokeColor=LIGHT))
    txt(d, 241, 9, "Doppelklick auf einen Node öffnet dieses Fenster.   Oben: Execute step   |   Rechts oben: Publish   |   Executions: Verlauf", size=8.5, color=DARK)
    return d


def bild_items():
    d = Drawing(482, 112)
    box(d, 0, 30, 205, 72, LIGHT, GREY, lines=["Ein Item (eine Zeile Daten)", '{ "Name": "Anna",', '  "Abteilung": "IT-Support",', '  "Dringlichkeit": "hoch" }'], size=9)
    pfeil(d, 212, 66, 262, 66, ACC)
    box(d, 270, 44, 212, 44, ACC_L, ACC, lines=["Expression im Feld", "{{ $json.Name }}"], size=10)
    txt(d, 376, 28, "ergibt:  Anna", size=9, color=DARK, bold=True)
    txt(d, 376, 12, "Tipp: Feld aus der Eingabe ins Feld ziehen, statt zu tippen", size=8, color=GREY)
    return d


def bild_regel():
    d = Drawing(482, 190)
    xs = [0, 132, 264, 396]; wb = 86
    labels = [("Anfrage-Formular", GREEN_L, GREEN), ("HTTP Request", BLUE_L, BLUE), ("IF", BLUE_L, BLUE), ("Antwort", ACC_L, ACC)]
    inh = [["$json = Formular:", "Name, Abteilung,", "Dringlichkeit, Nachricht"], ["$json = Antwort der API:", "mitarbeiter[ ... ]", "(Formular ist weg!)"],
           ["$json = weiter die", "API-Antwort"], ["$json = API-Antwort,", "nicht das Formular"]]
    for i, (x, (n, f, s)) in enumerate(zip(xs, labels)):
        box(d, x, 80, wb, 36, f, s, text=n, size=9.5)
        for j, l in enumerate(inh[i]):
            txt(d, x + wb / 2, 66 - j * 10, l, size=7.6, color=DARK if i != 1 else RED, bold=(i == 1 and j == 0))
        if i < 3:
            pfeil(d, x + wb + 2, 98, xs[i + 1] - 2, 98)
    # Rückgriff vom IF zum Formular
    yb = 150
    d.add(Line(xs[2] + wb / 2, 116, xs[2] + wb / 2, yb, strokeColor=ACC, strokeWidth=1.6))
    d.add(Line(xs[2] + wb / 2, yb, xs[0] + wb / 2, yb, strokeColor=ACC, strokeWidth=1.6))
    pfeil(d, xs[0] + wb / 2, yb, xs[0] + wb / 2, 118, ACC)
    box(d, 70, 158, 342, 26, ACC_L, ACC, text="Frühere Werte:   {{ $('Anfrage-Formular').item.json.Dringlichkeit }}", size=9, color=DARK)
    d.translate(0, -34); d.height = 156
    return d


def bild_agent():
    d = Drawing(482, 170)
    box(d, 0, 98, 84, 38, GREEN_L, GREEN, lines=["Chat", "(Auslöser)"], size=9.5)
    pfeil(d, 86, 117, 146, 117)
    box(d, 148, 84, 186, 66, PURPLE_L, PURPLE, lines=["AI Agent", "denkt, wählt Tools,", "formuliert die Antwort"], size=11)
    pfeil(d, 336, 117, 396, 117)
    box(d, 398, 98, 84, 38, ACC_L, ACC, lines=["Antwort", "im Chat"], size=9.5)
    plug = [("Modell", "OpenRouter", 150, BLUE_L, BLUE), ("Memory", "Window Buffer", 227, BLUE_L, BLUE), ("Tools", "(mehrere)", 304, GREEN_L, GREEN)]
    for n, s, x, f, c in plug:
        box(d, x - 8 if n != "Modell" else 148, 20, 76, 36, f, c, lines=[n, s], size=9)
    xs = [186, 263, 340]
    for (n, s, x, f, c), px in zip(plug, [186, 265, 344]):
        d.add(Line(px, 84, px, 58, strokeColor=c, strokeWidth=1.4))
        d.add(Circle(px, 70, 7, fillColor=colors.white, strokeColor=c, strokeWidth=1.4))
        txt(d, px, 66.5, "+", size=11, color=c, bold=True)
    txt(d, 420, 52, "Tools in Aufgabe 2:", size=8.5, color=DARK, bold=True, anchor="middle")
    for i, l in enumerate(["Mitarbeiter suchen", "Abteilungen auflisten", "MCP: Räume, Wetter"]):
        txt(d, 420, 40 - i * 11, l, size=8, color=GREY)
    txt(d, 241, 4, "Anschlüsse unten, jeweils über das Plus-Zeichen verbinden (nicht rechts am Pfeil).", size=8.5, color=DARK)
    return d


def seite(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8.5); canvas.setFillColor(GREY)
    canvas.drawString(2 * cm, 1.1 * cm, "Moderationsblatt: n8n-Einführung (30 Min.)  |  nur für dich, nicht für die Teilnehmenden")
    canvas.drawRightString(A4[0] - 2 * cm, 1.1 * cm, f"Seite {doc.page}")
    canvas.restoreState()


def sp(h=6):
    return Spacer(1, h)


def story():
    s = []
    # ----- Seite 1 -----
    s += [Paragraph("n8n-Einführung in 30 Minuten", title),
          Paragraph("Moderationsblatt: Stichpunkte, Bilder zum Nachzeichnen, Live-Schritte", ParagraphStyle("u", parent=body, textColor=GREY, fontSize=10.5)),
          HRFlowable(width="100%", thickness=1.2, color=ACC, spaceBefore=4, spaceAfter=8), zeitleiste(), sp(8)]
    s += [Paragraph("Ziel", h2)] + B(["Jede Gruppe kann danach <b>Aufgabe 1 anfangen</b>, ohne zu raten. Alles andere bleibt weg.",
                                      "Live in einer eigenen Instanz bauen (kein Foliensatz). <b>Jeden Klick laut benennen.</b>"])
    s += [Paragraph("Vorher erledigen", h2)] + B([
        "Eigene Instanz (oder die Reserve) offen, <b>Browser-Zoom 125 bis 150 %</b>, nur ein Tab sichtbar.",
        "Neuen, leeren Workflow vorbereiten. <b>Plan B:</b> <font face='Courier' size='9'>solutions/aufgabe-1-loesung.json</font> per Drag-and-drop in den Canvas ziehen.",
        "Alles einmal durchgespielt: Formular, HTTP Request, IF, Form Ending, Agent-Chat mit echtem Modell.",
        "Zugangszettel und Hilfekarte gedruckt, Flipchart und Stifte bereit, <b>RAM-Tracking gestartet</b>.",
        "Teilnehmende auf <b>privaten Geräten</b> (Firmen-VPN blockiert den Live-Kanal von n8n)."])
    s += [Paragraph("Nicht zeigen", h2)] + B(["Credentials anlegen (ist vorbereitet), Sub-Workflows im Detail, Code-Node, Community-Nodes.",
                                               "Alles, was nicht für Aufgabe 1 und 2 nötig ist."])
    s += [sp(4), Paragraph("Was die Teilnehmenden hinterher können sollen", h2)] + B([
        "Einen <b>Trigger</b> setzen und testen, die Ausgabe eines Nodes lesen.",
        "Mit <font face='Courier' size='9'>{{ $json.feld }}</font> auf Daten zugreifen, auch auf frühere Nodes.",
        "Eine <b>REST-Schnittstelle</b> per HTTP Request abfragen.",
        "Mit <b>IF</b> verzweigen und das Ergebnis mit <b>Form Ending</b> anzeigen.",
        "Einem <b>Agenten</b> Modell, Memory und Tools über das Plus-Zeichen geben."]) + [PageBreak()]

    # ----- Seite 2: 0-13 -----
    s += [blockkopf("0 bis 3", "Was ist ein Workflow?", BLUE), sp(4), bild_ablauf(), sp(2)]
    s += B(["<b>Sagen:</b> n8n verbindet Systeme. Statt zu programmieren, zieht man Bausteine und Linien.",
            "<b>Sagen:</b> Immer gleich: <b>ein Auslöser, dann Schritte, am Ende ein Ergebnis.</b>",
            "<b>Zeigen:</b> Auf dem leeren Canvas das Plus, Trigger-Auswahl (nur anschauen)."])
    s += [sp(16), blockkopf("3 bis 8", "Die Oberfläche", BLUE), sp(4), bild_node(), sp(2)]
    s += B(["<b>Zeigen:</b> Node hinzufügen (Plus), Node öffnen (Doppelklick), <i>Execute workflow</i>, <i>Executions</i>, Schalter <i>Publish</i>.",
            "<b>Test oder Produktion:</b> Beim Testen siehst du die Daten. Produktiv läuft der Workflow von selbst, die Production-URL gilt nur, wenn er <b>aktiv</b> ist.",
            "<b>Merksatz:</b> Links kommt rein, rechts kommt raus, in der Mitte stellst du ein."])
    s += [sp(16), blockkopf("8 bis 13", "Trigger", GREEN), sp(4)]
    s += B(["<b>Live bauen:</b> Formular-Trigger, Felder <i>Name</i> und <i>Dringlichkeit</i>, <i>Execute step</i>, Formular im Test-Tab ausfüllen.",
            "Die Ausgabe zeigen: Die Eingaben des Formulars sind jetzt Daten.",
            "<b>Pin</b> zeigen: Testdaten festhalten, kein Formular mehr ausfüllen.",
            "Kurz nennen: <b>Webhook</b> (andere Systeme rufen an), <b>Chat</b> (kommt in Aufgabe 2), <b>Zeitplan</b>."]) + [PageBreak()]

    # ----- Seite 3: 13-26 -----
    s += [blockkopf("13 bis 21", "Datenfluss: der wichtigste Block", ACC), sp(4), bild_items(), sp(2)]
    s += B(["<b>Item</b> = eine Zeile Daten (JSON). Jeder Node bekommt Items und gibt Items weiter.",
            "<b>Live:</b> <i>Edit Fields</i> anhängen, Feld ziehen, <font face='Courier' size='9'>{{ $json.Name }}</font> entsteht von selbst. Ausgabe prüfen.",
            "<b>Fehler absichtlich zeigen:</b> <font face='Courier' size='9'>$json.name</font> statt <font face='Courier' size='9'>Name</font> tippen, den roten Node lesen.",
            "Danach ein Problem aufbauen, das später in Aufgabe 1 vorkommt (nächstes Bild)."])
    s += [sp(4), bild_regel(), sp(2)]
    s += B(["<b>Merksatz:</b> <font face='Courier' size='9'>$json</font> ist immer das, was der <b>Node direkt davor</b> geliefert hat.",
            "Für <b>frühere</b> Nodes: <font face='Courier' size='9'>$('Node-Name').item.json.feld</font>. Dies ist die häufigste Stolperstelle in Aufgabe 1."])
    s += [sp(16), blockkopf("21 bis 26", "REST und Logik", BLUE), sp(4)]
    s += B(["<b>HTTP Request:</b> Methode <b>GET</b>, URL <font face='Courier' size='9'>http://tools:5678/webhook/mitarbeiter</font>, Query-Parameter <font face='Courier' size='9'>abteilung</font>. Antwort ist JSON.",
            "<b>IF</b> mit zwei Ausgängen (true/false), an jeden ein <i>Edit Fields</i>, das <font face='Courier' size='9'>antwort</font> baut.",
            "<b>Form Ending</b> an beide Zweige, <i>Completion Message</i> = <font face='Courier' size='9'>{{ $json.antwort }}</font> (als Expression).",
            "<b>Durchspielen:</b> Formular einmal mit <i>hoch</i>, einmal mit <i>normal</i>. Jeder Zweig zeigt seinen Text."]) + [PageBreak()]

    # ----- Seite 4: 26-30 + Tipps -----
    s += [blockkopf("26 bis 30", "Ausblick: Agent, dann Fragen", PURPLE), sp(4), bild_agent(), sp(2)]
    s += B(["<b>Aufgabe 2 öffnen, nicht bauen.</b> Im Chat fragen: <i>Wer arbeitet im IT-Support?</i>",
            "<b>Ausführung öffnen:</b> Welches Tool hat der Agent mit welchen Eingaben aufgerufen? Das ist der Aha-Moment.",
            "Hilfekarte zeigen (fünf Stolperstellen), Zugangszettel verteilen.",
            "Offene Fragen vom Flipchart abarbeiten."])
    s += [sp(10), Paragraph("Die fünf Stolperstellen (Hilfekarte)", h2)]
    t = Table([[Paragraph("<b>1  Ausdrücke</b><br/>Feldname genau wie in der Ausgabe, Groß-/Kleinschreibung beachten.", small),
                Paragraph("<b>2  Pinning</b><br/>Testdaten festhalten, kein erneutes Ausfüllen.", small),
                Paragraph("<b>3  Credential</b><br/>Beim Chat-Modell <i>OpenRouter (Workshop)</i> wählen.", small)],
               [Paragraph("<b>4  Verbinden</b><br/>Am Agenten alles über das Plus-Zeichen unten, nicht rechts.", small),
                Paragraph("<b>5  Test oder Produktion</b><br/>Production-URL nur bei aktivem (publizierten) Workflow.", small),
                Paragraph("<b>Hilft nichts?</b><br/>Executions öffnen, roten Node lesen, Team fragen, dann dich.", small)]],
              colWidths=[W / 3] * 3)
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.6, GREY), ("INNERGRID", (0, 0), (-1, -1), 0.6, GREY), ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    s += [t, sp(10), Paragraph("Danach: Workshop (75 Min.)", h2)]
    s += B(["0 bis 5 Ankommen und Anmelden.  5 bis 10 Neustart mit Beispiel.  <b>10 bis 40 Aufgabe 1.</b>  <b>40 bis 65 Aufgabe 2.</b>  65 bis 75 Showcase.",
            "Schnelle Gruppen machen Aufgabe 3. Alles Weitere zu Pannen: <font face='Courier' size='9'>unterlagen/betrieb-runbook.md</font>."])
    return s


def main():
    OUT.parent.mkdir(exist_ok=True)
    doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.7 * cm, bottomMargin=1.9 * cm,
                          title="Moderationsblatt n8n-Einführung", author="n8n-Workshop")
    doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")], onPage=seite)])
    doc.build(story())
    print("geschrieben:", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
