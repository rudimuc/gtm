#!/usr/bin/env python3
"""Erzeugt druckbare PDFs (A4) aus unterlagen/aufgabe-*.md und unterlagen/hilfekarte.md.

Aufruf:  python3 scripts/pdf-erstellen.py        (benötigt: pip install reportlab)
Ergebnis: unterlagen/pdf/aufgabe-1.pdf, aufgabe-2.pdf, aufgabe-3.pdf, hilfekarte.pdf
          und unterlagen/pdf/aufgabenblaetter-komplett.pdf (alle zusammen, je Blatt eine eigene Seite)
Unterstützt wird nur der Markdown-Teil, der in diesen Dateien vorkommt (Überschriften, Listen, **fett**, *kursiv*, `code`, ---).
"""
import re, sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                PageBreak, HRFlowable, KeepTogether, Table, TableStyle)

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "unterlagen"
OUT = SRC / "pdf"
BLAETTER = ["aufgabe-1", "aufgabe-2", "aufgabe-3", "hilfekarte"]
DARK, ACC, GREY = colors.HexColor("#1f2937"), colors.HexColor("#c2410c"), colors.HexColor("#6b7280")

body = ParagraphStyle("body", fontName="Helvetica", fontSize=10.5, leading=15, textColor=DARK, spaceAfter=5)
h1 = ParagraphStyle("h1", parent=body, fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=ACC, spaceAfter=6)
h2 = ParagraphStyle("h2", parent=body, fontName="Helvetica-Bold", fontSize=13.5, leading=18, spaceBefore=10, spaceAfter=5)
item = ParagraphStyle("item", parent=body, leftIndent=20, bulletIndent=2, spaceAfter=4)
sub = ParagraphStyle("sub", parent=body, leftIndent=40, bulletIndent=22, spaceAfter=2, fontSize=10)


def inline(text):
    parts = re.split(r"(`[^`]+`)", text)
    out = []
    for p in parts:
        if p.startswith("`") and p.endswith("`") and len(p) > 1:
            c = p[1:-1].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            out.append(f'<font face="Courier" size="9.5" color="#9a3412">{c}</font>')
        else:
            t = p.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
            t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", t)
            out.append(t)
    return "".join(out)


def parse(md, kopf):
    story, cur = [], None  # cur: [style, bullet, text]

    def flush():
        nonlocal cur
        if cur:
            story.append(Paragraph(cur[2], cur[0], bulletText=cur[1]))
            cur = None

    for raw in md.splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush(); continue
        if line.startswith("# "):
            flush(); story.append(Paragraph(inline(line[2:]), h1))
            if kopf:
                story.append(Table([[Paragraph("Gruppe: ________________", body), Paragraph("Instanz: gtm ___", body)]],
                                   colWidths=[9 * cm, 7 * cm], style=TableStyle([("BOTTOMPADDING", (0, 0), (-1, -1), 8)])))
            story.append(HRFlowable(width="100%", thickness=1, color=ACC, spaceAfter=8))
        elif line.startswith("## "):
            flush(); story.append(Paragraph(inline(line[3:]), h2))
        elif line.strip() == "---":
            flush(); story.append(HRFlowable(width="100%", thickness=0.6, color=GREY, spaceBefore=8, spaceAfter=8))
        elif (m := re.match(r"^(\d+)\.\s+(.*)", line)):
            flush(); cur = [item, m.group(1) + ".", inline(m.group(2))]
        elif (m := re.match(r"^- (.*)", line)):
            flush(); cur = [item, "•", inline(m.group(1))]
        elif (m := re.match(r"^\s{2,}- (.*)", line)):
            flush(); cur = [sub, "–", inline(m.group(1))]
        elif line.startswith("   ") and cur:
            cur[2] += "<br/>" + inline(line.strip())
        elif line.startswith("> "):
            flush(); story.append(Paragraph(inline(line[2:]), body))
        else:
            flush(); story.append(Paragraph(inline(line.strip()), body))
    flush()
    return story


def seite(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8.5); canvas.setFillColor(GREY)
    canvas.drawString(2 * cm, 1.2 * cm, "n8n-Workshop im Tribe-Meeting")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Seite {doc.page}")
    canvas.restoreState()


def bauen(pfad, namen):
    doc = BaseDocTemplate(str(pfad), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=2 * cm,
                          title="n8n-Workshop: " + ", ".join(namen), author="n8n-Workshop")
    doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")], onPage=seite)])
    story = []
    for i, n in enumerate(namen):
        if i:
            story.append(PageBreak())
        story += parse((SRC / f"{n}.md").read_text(encoding="utf-8"), kopf=n.startswith("aufgabe"))
    doc.build(story)
    print("geschrieben:", pfad.relative_to(ROOT))


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for n in BLAETTER:
        bauen(OUT / f"{n}.pdf", [n])
    bauen(OUT / "aufgabenblaetter-komplett.pdf", BLAETTER)
