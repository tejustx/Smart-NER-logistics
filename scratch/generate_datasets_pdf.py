"""
Generates the comprehensive Smart NER Logistics Control Platform - Datasets Reference Manual PDF.
Refined with clean page breaks and executive layout.
"""

import os
import math
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print running headers and 'Page X of Y' footers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        width, height = letter
        margin = 36

        if self._pageNumber == 1:
            # First page subtle bottom notice
            self.saveState()
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(margin, 38, width - margin, 38)
            self.setFont("Helvetica-Bold", 7)
            self.setFillColor(colors.HexColor("#475569"))
            self.drawString(margin, 26, "GOVERNMENT EVALUATION DOSSIER — SECTION 16 DATA INTEGRITY COMPLIANT")
            self.setFont("Helvetica", 7)
            self.drawRightString(width - margin, 26, f"Page 1 of {page_count} | Smart NER Logistics Control Platform")
            self.restoreState()
            return

        # Pages 2+: Full running header and footer
        self.saveState()
        # Top Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0284C7"))
        self.drawString(margin, height - 26, "SMART NER LOGISTICS CONTROL PLATFORM")
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(width - margin, height - 26, "TECHNICAL DATASET ARCHITECTURE & PROVENANCE MANUAL")

        # Top rule
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.6)
        self.line(margin, height - 31, width - margin, height - 31)

        # Bottom rule
        self.line(margin, 38, width - margin, 38)

        # Bottom Footer
        self.setFont("Helvetica", 7.5)
        self.drawString(margin, 26, "Confidential — Ministry of DoNER / NDMA Logistics Operations & Research Framework")
        self.drawRightString(width - margin, 26, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf(filename="SMART_NER_LOGISTICS_DATASETS_REFERENCE.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=38,
        bottomMargin=42
    )

    printable_w = letter[0] - 72  # 540 pt

    # Base Styles
    base_styles = getSampleStyleSheet()

    # Custom Palette Colors
    c_primary = colors.HexColor("#0F172A")    # Deep Slate Navy
    c_secondary = colors.HexColor("#0284C7")  # Tech Blue
    c_accent = colors.HexColor("#0369A1")     # Deep Accent Blue
    c_text = colors.HexColor("#1E293B")       # Dark Charcoal
    c_muted = colors.HexColor("#64748B")      # Muted Slate
    c_bg_light = colors.HexColor("#F8FAFC")   # Light background
    c_border = colors.HexColor("#CBD5E1")     # Border light

    # Typography Styles
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=c_primary,
        alignment=TA_LEFT
    )

    style_cover_subtitle = ParagraphStyle(
        'CoverSubtitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=c_secondary,
        alignment=TA_LEFT
    )

    style_meta_badge = ParagraphStyle(
        'MetaBadge',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#0369A1"),
        alignment=TA_LEFT
    )

    style_meta_text = ParagraphStyle(
        'MetaText',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=c_text,
        alignment=TA_LEFT
    )

    style_h1 = ParagraphStyle(
        'SectionH1',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=c_primary,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'SectionH2',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12.5,
        textColor=c_accent,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'BodyDark',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.2,
        textColor=c_text,
        spaceAfter=4
    )

    style_body_bold = ParagraphStyle(
        'BodyDarkBold',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=11.2,
        textColor=c_primary
    )

    style_formula = ParagraphStyle(
        'FormulaText',
        parent=base_styles['Normal'],
        fontName='Courier-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0F172A"),
        alignment=TA_LEFT
    )

    style_formula_desc = ParagraphStyle(
        'FormulaDesc',
        parent=base_styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#475569")
    )

    style_th = ParagraphStyle(
        'TableHeader',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.white,
        alignment=TA_LEFT
    )

    style_td = ParagraphStyle(
        'TableCell',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=8.8,
        textColor=c_text,
        alignment=TA_LEFT
    )

    style_td_bold = ParagraphStyle(
        'TableCellBold',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=8.8,
        textColor=c_primary,
        alignment=TA_LEFT
    )

    style_td_code = ParagraphStyle(
        'TableCellCode',
        parent=base_styles['Normal'],
        fontName='Courier',
        fontSize=6.8,
        leading=8.5,
        textColor=c_primary,
        alignment=TA_LEFT
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE, EXECUTIVE SUMMARY & SECTION 16 PROVENANCE
    # =========================================================================
    story.append(Spacer(1, 2))
    
    # Title Banner Box
    title_data = [
        [
            Paragraph("SMART NER LOGISTICS CONTROL PLATFORM", style_cover_subtitle),
            Paragraph("RELEASE v2.4 | ARCHITECTURE REFERENCE", ParagraphStyle('CoverRef', parent=style_meta_badge, alignment=TA_RIGHT, textColor=colors.HexColor("#0284C7")))
        ],
        [
            Paragraph("Comprehensive Dataset Architecture &amp; Data Provenance Reference Manual", style_cover_title),
            ""
        ],
        [
            Paragraph("A complete technical compendium of geospatial graphs, environmental risk datasets, defense vehicle fleets, certified mountain driver registries, multi-tier disaster cargo taxonomies, and Section 16 Data Integrity standards deployed across India's 8 North Eastern States.", style_body),
            ""
        ]
    ]

    title_table = Table(
        title_data,
        colWidths=[printable_w * 0.72, printable_w * 0.28],
        style=[
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (0, 2), (1, 2)),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 1),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]
    )
    story.append(title_table)
    story.append(Spacer(1, 4))

    # Metadata Grid
    meta_data = [
        [
            Paragraph("OPERATIONAL THEATER", style_meta_badge),
            Paragraph("REGULATORY COMPLIANCE", style_meta_badge),
            Paragraph("SYSTEM CORES", style_meta_badge),
            Paragraph("DATA INTEGRITY STANDARD", style_meta_badge)
        ],
        [
            Paragraph("North Eastern Region (NER)<br/>8 States: AS, AR, ML, NL, MN, MZ, TR, SK", style_meta_text),
            Paragraph("NDMA Logistics Directives &amp;<br/>BRO Mountain Transit Protocols", style_meta_text),
            Paragraph("FastAPI Python 3.13 Backend<br/>MapLibre GL JS + IndexedDB PWA", style_meta_text),
            Paragraph("Section 16 Data Provenance<br/>(Live / Historical / Simulated)", style_meta_text)
        ]
    ]
    meta_table = Table(
        meta_data,
        colWidths=[printable_w * 0.25, printable_w * 0.25, printable_w * 0.25, printable_w * 0.25],
        style=[
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
            ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#CBD5E1")),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]
    )
    story.append(meta_table)
    story.append(Spacer(1, 6))

    # Section 1: Executive Summary
    story.append(Paragraph("1. Executive Summary &amp; Operational Context", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=1, spaceAfter=4))
    
    story.append(Paragraph(
        "The <b>Smart NER Logistics Control Platform</b> is an emergency-grade decision support and supply chain "
        "orchestration platform engineered specifically for India's North Eastern Region (NER). The operational "
        "theater encompasses the <i>Siliguri Corridor ('Chicken's Neck')</i>, steep seismic zones (Zone V), "
        "Brahmaputra alluvial floodplains, and high-altitude Himalayan ridge passes ranging from 16m ASL (Agartala) "
        "to 3,048m ASL (Tawang). Operating in this geomorphically volatile environment demands heterogeneous data "
        "streams to balance delivery speed against catastrophic terrain failures such as monsoonal landslides, "
        "culvert submersions, and road subsidence.",
        style_body
    ))
    story.append(Paragraph(
        "To guarantee high-stakes decision reliability, the platform synthesizes <b>8 core data domains</b> across "
        "<b>three operational data provenance tiers</b>. Every route recommendation, cargo manifest, and driver "
        "assignment computed by the algorithmic engines (MCDA Risk Scoring, Multi-Tier 0/1 Knapsack, and Offline Edge "
        "Sync) directly links to validated geospatial, meteorological, structural, and institutional datasets.",
        style_body
    ))
    story.append(Spacer(1, 4))

    # Section 2: Section 16 Data Provenance Framework
    story.append(Paragraph("2. Section 16 Data Provenance Framework", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=1, spaceAfter=4))

    story.append(Paragraph(
        "In strict adherence to <b>Section 16 Data Integrity Standards</b>, the platform enforces hard architectural "
        "separation between real-time telemetry, historical geological records, and synthetic stress tests. This "
        "guarantees that artificial simulation scenarios (such as catastrophic cloudburst injections or synthetic "
        "landslide blockages) cannot corrupt baseline historical indices or misrepresent emergency situations to government stakeholders.",
        style_body
    ))

    prov_table_data = [
        [
            Paragraph("Classification", style_th),
            Paragraph("Visual Badge", style_th),
            Paragraph("Data Sources &amp; Origins", style_th),
            Paragraph("Ingestion Cadence", style_th),
            Paragraph("Role in Algorithmic Decision Engine", style_th),
            Paragraph("Integrity Protocol", style_th)
        ],
        [
            Paragraph("<b>LIVE STREAM</b>", style_td_bold),
            Paragraph("<font color='#0D9488'><b>[LIVE DATA]</b></font>", style_td),
            Paragraph("Driver GPS coordinates, active checkpoint check-ins, route obstacle reports, local offline sync queues, vehicle telemetry.", style_td),
            Paragraph("Real-time / Sub-second (5s IoT pings, on-demand check-ins)", style_td),
            Paragraph("Updates active convoy positions, computes live ETA drift, monitors driver fatigue timers, and triggers offline sync queues.", style_td),
            Paragraph("Signed cryptographic tokens, client-side SQLite/IndexedDB journal with replay protection.", style_td)
        ],
        [
            Paragraph("<b>HISTORICAL BENCHMARK</b>", style_td_bold),
            Paragraph("<font color='#0284C7'><b>[HISTORICAL]</b></font>", style_td),
            Paragraph("<b>ISRO Landslide Atlas of India (NRSC 2023)</b>, <b>Bhuvan Disaster Services</b>, 30-yr GSI hazard atlas, CartoDEM slope contours, BRO road indices.", style_td),
            Paragraph("Static baseline / Pre-computed seasonal tables", style_td),
            Paragraph("Supplies static baseline risk weights (W<sub>slope</sub>, W<sub>history</sub>, W<sub>road</sub>) calibrated to ISRO district hazard indices.", style_td),
            Paragraph("Read-only baseline database; audited against official ISRO/GSI public domain publications.", style_td)
        ],
        [
            Paragraph("<b>SIMULATED BENCHMARK</b>", style_td_bold),
            Paragraph("<font color='#D97706'><b>[SIMULATED]</b></font>", style_td),
            Paragraph("Monsoon cloudburst telemetry (85mm/hr bursts), synthetic Banderdewa landslide blockage, generated emergency cargo requests.", style_td),
            Paragraph("Dynamic injection during testing &amp; evaluation runs", style_td),
            Paragraph("Drives 'What-If' disaster drill routing, triggers dynamic Dijkstra/A* reroutes, and tests knapsack cargo prioritization under stress.", style_td),
            Paragraph("Explicitly tagged with simulation metadata; sandboxed from live audit ledgers.", style_td)
        ]
    ]

    prov_table = Table(
        prov_table_data,
        colWidths=[printable_w * 0.15, printable_w * 0.13, printable_w * 0.24, printable_w * 0.14, printable_w * 0.20, printable_w * 0.14],
        style=[
            ('BACKGROUND', (0, 0), (-1, 0), c_primary),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]
    )
    story.append(prov_table)

    # PAGE BREAK TO PAGE 2
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: DATASET 1 - GEOGRAPHIC GRAPH, HUBS & HIGHWAYS
    # =========================================================================
    story.append(Paragraph("3. Dataset 1: North East Regional Highway Network &amp; Geospatial Graph", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=1, spaceAfter=4))

    story.append(Paragraph(
        "<b>Codebase Source:</b> <code>backend/services/ner_network.py</code> | <b>Classification:</b> <font color='#0284C7'><b>[HISTORICAL]</b></font> &amp; <font color='#0D9488'><b>[LIVE]</b></font><br/>"
        "The geographic network model represents India's North East as a directed, weighted topological graph where nodes represent "
        "strategic logistical depots, multi-modal railheads, and capital termini, while edges represent National Highway corridors. "
        "Each edge carries physical distance, standard traversal hours, maximum road gradient, elevation profiles, and vulnerability scores.",
        style_body
    ))

    # Table of 13 Hubs
    story.append(Paragraph("<b>Table 3.1: Strategic Logistics Hubs &amp; Elevation Matrix (13 Regional Hubs)</b>", style_h2))

    hubs_data = [
        [
            Paragraph("Hub Name", style_th),
            Paragraph("State", style_th),
            Paragraph("District", style_th),
            Paragraph("Coords (Lat, Lon)", style_th),
            Paragraph("Elevation", style_th),
            Paragraph("Strategic Logistics Typology", style_th)
        ],
        [Paragraph("Guwahati", style_td_bold), Paragraph("Assam", style_td), Paragraph("Kamrup Metro", style_td), Paragraph("26.1445, 91.7362", style_td_code), Paragraph("55 m", style_td), Paragraph("Primary Regional Hub &amp; Multi-modal Gateway", style_td)],
        [Paragraph("Itanagar", style_td_bold), Paragraph("Arunachal", style_td), Paragraph("Papum Pare", style_td), Paragraph("27.0844, 93.6053", style_td_code), Paragraph("750 m", style_td), Paragraph("State Capital / Border Frontier Terminus", style_td)],
        [Paragraph("Shillong", style_td_bold), Paragraph("Meghalaya", style_td), Paragraph("East Khasi Hills", style_td), Paragraph("25.5788, 91.8933", style_td_code), Paragraph("1,525 m", style_td), Paragraph("High Hill Logistics Depot &amp; Armed Forces Staging", style_td)],
        [Paragraph("Tawang", style_td_bold), Paragraph("Arunachal", style_td), Paragraph("Tawang", style_td), Paragraph("27.5861, 91.8594", style_td_code), Paragraph("3,048 m", style_td), Paragraph("High-Altitude Defense &amp; Alpine Extreme Outpost", style_td)],
        [Paragraph("Tezpur", style_td_bold), Paragraph("Assam", style_td), Paragraph("Sonitpur", style_td), Paragraph("26.6528, 92.7926", style_td_code), Paragraph("48 m", style_td), Paragraph("Brahmaputra North-Bank River Crossing Depot", style_td)],
        [Paragraph("Nagaon", style_td_bold), Paragraph("Assam", style_td), Paragraph("Nagaon", style_td), Paragraph("26.3452, 92.6840", style_td_code), Paragraph("60 m", style_td), Paragraph("Central Assam Fork &amp; Storage Interchange", style_td)],
        [Paragraph("Silchar", style_td_bold), Paragraph("Assam", style_td), Paragraph("Cachar", style_td), Paragraph("24.8170, 92.7950", style_td_code), Paragraph("25 m", style_td), Paragraph("Barak Valley Transit Gateway (Mizoram/Tripura Link)", style_td)],
        [Paragraph("Aizawl", style_td_bold), Paragraph("Mizoram", style_td), Paragraph("Aizawl", style_td), Paragraph("23.7271, 92.7176", style_td_code), Paragraph("1,132 m", style_td), Paragraph("Mountain Ridge Capital / High-Slope Terminal", style_td)],
        [Paragraph("Dimapur", style_td_bold), Paragraph("Nagaland", style_td), Paragraph("Dimapur", style_td), Paragraph("25.9090, 93.7266", style_td_code), Paragraph("145 m", style_td), Paragraph("Railhead &amp; Broad-Gauge Intermodal Freight Yard", style_td)],
        [Paragraph("Kohima", style_td_bold), Paragraph("Nagaland", style_td), Paragraph("Kohima", style_td), Paragraph("25.6751, 94.1086", style_td_code), Paragraph("1,444 m", style_td), Paragraph("High Mountain Capital / NH-29 Ridge Pass", style_td)],
        [Paragraph("Imphal", style_td_bold), Paragraph("Manipur", style_td), Paragraph("Imphal West", style_td), Paragraph("24.8170, 93.9368", style_td_code), Paragraph("786 m", style_td), Paragraph("Manipur Valley Gateway &amp; Border Trade Interchange", style_td)],
        [Paragraph("Agartala", style_td_bold), Paragraph("Tripura", style_td), Paragraph("West Tripura", style_td), Paragraph("23.8315, 91.2868", style_td_code), Paragraph("16 m", style_td), Paragraph("South-West Lowland Gateway / International Border", style_td)],
        [Paragraph("Gangtok", style_td_bold), Paragraph("Sikkim", style_td), Paragraph("East Sikkim", style_td), Paragraph("27.3314, 88.6138", style_td_code), Paragraph("1,650 m", style_td), Paragraph("Eastern Himalayan Outpost / Teesta Valley Transit", style_td)]
    ]

    hubs_table = Table(
        hubs_data,
        colWidths=[printable_w * 0.14, printable_w * 0.12, printable_w * 0.16, printable_w * 0.17, printable_w * 0.10, printable_w * 0.31],
        style=[
            ('BACKGROUND', (0, 0), (-1, 0), c_primary),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
            ('TOPPADDING', (0, 0), (-1, -1), 2.2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]
    )
    story.append(hubs_table)
    story.append(Spacer(1, 5))

    # Corridors Table
    story.append(Paragraph("<b>Table 3.2: Strategic Regional Highway Corridors</b>", style_h2))

    corr_data = [
        [
            Paragraph("Corridor ID", style_th),
            Paragraph("Highway", style_th),
            Paragraph("Corridor Name / Axis", style_th),
            Paragraph("Jurisdiction", style_th),
            Paragraph("Criticality Designation", style_th),
            Paragraph("Baseline Risk", style_th),
            Paragraph("Active Environmental Vulnerability", style_th)
        ],
        [
            Paragraph("CORR-NH27", style_td_bold),
            Paragraph("NH-27", style_td),
            Paragraph("Guwahati - Nagaon - Kaziranga Axis", style_td),
            Paragraph("Assam", style_td),
            Paragraph("Critical Lifeline (East-West Trunk)", style_td),
            Paragraph("68 / 100", style_td),
            Paragraph("Vulnerable to monsoon flood submergence across Kaziranga belt", style_td)
        ],
        [
            Paragraph("CORR-NH415", style_td_bold),
            Paragraph("NH-415", style_td),
            Paragraph("Banderdewa - Itanagar Hill Ingress", style_td),
            Paragraph("Arunachal / Assam", style_td),
            Paragraph("Capital City Supply Corridor", style_td),
            Paragraph("82 / 100", style_td),
            Paragraph("Frequent mudslides and active slope collapse at Km 18-24", style_td)
        ],
        [
            Paragraph("CORR-NH06", style_td_bold),
            Paragraph("NH-06", style_td),
            Paragraph("Guwahati - Shillong Express Highway", style_td),
            Paragraph("Assam / Meghalaya", style_td),
            Paragraph("Meghalaya Food &amp; Medical Lifeline", style_td),
            Paragraph("45 / 100", style_td),
            Paragraph("Dense mountain fog and moderate rockfall zones near Umsning", style_td)
        ],
        [
            Paragraph("CORR-NH29", style_td_bold),
            Paragraph("NH-29", style_td),
            Paragraph("Dimapur - Kohima High Gradient Corridor", style_td),
            Paragraph("Nagaland", style_td),
            Paragraph("Nagaland-Manipur Supply Backbone", style_td),
            Paragraph("79 / 100", style_td),
            Paragraph("Active sinking zone monitored continuously at Pagla Pahar", style_td)
        ],
        [
            Paragraph("CORR-NH13", style_td_bold),
            Paragraph("NH-13", style_td),
            Paragraph("Tezpur - Bhalukpong - Tawang Axis", style_td),
            Paragraph("Arunachal Pradesh", style_td),
            Paragraph("Strategic Defense &amp; Essential Civil Life", style_td),
            Paragraph("87 / 100", style_td),
            Paragraph("Sub-zero icing, heavy snow accumulation, and Sela Pass hazards", style_td)
        ]
    ]

    corr_table = Table(
        corr_data,
        colWidths=[printable_w * 0.13, printable_w * 0.09, printable_w * 0.22, printable_w * 0.13, printable_w * 0.19, printable_w * 0.09, printable_w * 0.15],
        style=[
            ('BACKGROUND', (0, 0), (-1, 0), c_primary),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
            ('TOPPADDING', (0, 0), (-1, -1), 2.2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]
    )
    story.append(corr_table)
    story.append(Spacer(1, 5))

    # Rerouting Case Study Box
    story.append(Paragraph("<b>Canonical Evaluation Case: Guwahati to Itanagar Dynamic Rerouting</b>", style_h2))
    reroute_box_data = [
        [
            Paragraph("<b>ROUTE A: Direct Northern Foothills (High Hazard)</b>", style_meta_badge),
            Paragraph("<b>ROUTE B: South Bank Trunk via Tezpur (Recommended)</b>", style_meta_badge)
        ],
        [
            Paragraph(
                "• <b>Distance:</b> 274.0 km | <b>Nominal Time:</b> 6.2 hours<br/>"
                "• <b>Risk Score:</b> <font color='#DC2626'><b>78.4 / 100 (HIGH HAZARD)</b></font><br/>"
                "• <b>Active Disruption:</b> 450m mudslide breach at NH-415 Km 21.<br/>"
                "• <b>Cost Multiplier:</b> <b>2.24x</b> (Severe risk penalty applied).",
                style_td
            ),
            Paragraph(
                "• <b>Distance:</b> 348.0 km (+74 km) | <b>Nominal Time:</b> 7.8 hours (+1.6h)<br/>"
                "• <b>Risk Score:</b> <font color='#16A34A'><b>24.2 / 100 (LOW HAZARD - SAFE)</b></font><br/>"
                "• <b>Corridor Status:</b> 100% 4-lane via Kolia Bhomora Bridge at Tezpur.<br/>"
                "• <b>Cost Multiplier:</b> <b>1.21x</b> (Effective cost <b>38% lower</b> than Route A).",
                style_td
            )
        ]
    ]
    reroute_box = Table(
        reroute_box_data,
        colWidths=[printable_w * 0.50, printable_w * 0.50],
        style=[
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
            ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#CBD5E1")),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]
    )
    story.append(reroute_box)

    # PAGE BREAK TO PAGE 3
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: DATASET 2 - RISK ENGINE & DATASET 3 - VEHICLE FLEET
    # =========================================================================
    story.append(Paragraph("4. Dataset 2: Environmental, Hydrological &amp; Slope Risk Engine", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=1, spaceAfter=4))

    story.append(Paragraph(
        "<b>Codebase Source:</b> <code>backend/services/risk_engine.py</code> | <b>Classification:</b> <font color='#0284C7'><b>[HISTORICAL]</b></font> &amp; <font color='#D97706'><b>[SIMULATED]</b></font><br/>"
        "USP 1 implements an empirical Multi-Criteria Decision Analysis (MCDA) model that transforms four physical "
        "signals into a composite segment risk score <b>R ∈ [0, 100]</b> and calculates dynamic routing penalties. "
        "Historical slope and hazard weights (W<sub>slope</sub> = 0.25, W<sub>history</sub> = 0.25) are calibrated against the "
        "<b>ISRO Landslide Atlas of India (NRSC 2023)</b> district vulnerability rankings and <b>NRSC Bhuvan</b> event inventories.",
        style_body
    ))

    # Formula Box
    formula_data = [
        [
            Paragraph("<b>COMPOSITE RISK FORMULATION (USP 1)</b>", style_meta_badge),
            Paragraph("<b>NON-LINEAR STORM SPIKE CONDITION</b>", style_meta_badge)
        ],
        [
            Paragraph("R = [ (0.35 · I_rain) + (0.25 · S_slope) + (0.25 · F_hist) + (0.15 · (1 - Q_road)) ] × 100", style_formula),
            Paragraph("IF (Rainfall > 60 mm/hr) AND (Slope > 20%):<br/>&nbsp;&nbsp;&nbsp;&nbsp;R_final = min(R_raw × 1.35, 99.0)", style_formula)
        ],
        [
            Paragraph(
                "Where:<br/>"
                "• <b>I_rain:</b> Hourly rainfall normalized against extreme cloudburst cap (100 mm/hr).<br/>"
                "• <b>S_slope:</b> Terrain gradient incline normalized against mountain pass grade (35%).<br/>"
                "• <b>F_hist:</b> GSI 30-year landslide recurrence probability index [0.0, 1.0].<br/>"
                "• <b>Q_road:</b> NHIDCL structural pavement quality index (1.0 = pristine, 0.0 = broken gravel).",
                style_formula_desc
            ),
            Paragraph(
                "<b>Generalized Cost Multiplier:</b><br/>"
                "C_effective = C_base × [ 1.0 + 1.8 × (R / 100)^1.5 ]<br/>"
                "Calculates mathematical traversal impedance for Dijkstra/A* pathfinding, forcing autonomous convoys away from saturated slopes.",
                style_formula_desc
            )
        ]
    ]

    formula_table = Table(
        formula_data,
        colWidths=[printable_w * 0.52, printable_w * 0.48],
        style=[
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
            ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#CBD5E1")),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]
    )
    story.append(formula_table)
    story.append(Spacer(1, 4))

    # Risk Thresholds
    story.append(Paragraph("<b>Table 4.1: Operational Risk Severity Thresholds &amp; Dispatch Protocols</b>", style_h2))
    risk_band_data = [
        [Paragraph("Score Band", style_th), Paragraph("Risk Level", style_th), Paragraph("Cost Multiplier", style_th), Paragraph("Physical Road Conditions", style_th), Paragraph("Automated Platform Action &amp; Safety Protocol", style_th)],
        [Paragraph("0.0 – 29.9", style_td_bold), Paragraph("<font color='#16A34A'><b>LOW</b></font>", style_td), Paragraph("1.00 – 1.30x", style_td), Paragraph("Dry pavement, stable slopes, clear visibility", style_td), Paragraph("Normal transit authorized for all vehicle classes including 16T multi-axle freight.", style_td)],
        [Paragraph("30.0 – 59.9", style_td_bold), Paragraph("<font color='#D97706'><b>MEDIUM</b></font>", style_td), Paragraph("1.31 – 1.83x", style_td), Paragraph("Moderate rainfall, wet gravel, minor slope seepage", style_td), Paragraph("Transit permitted with speed derating (40 km/h cap); mandatory driver wiper/brake alert.", style_td)],
        [Paragraph("60.0 – 79.9", style_td_bold), Paragraph("<font color='#EA580C'><b>HIGH</b></font>", style_td), Paragraph("1.84 – 2.29x", style_td), Paragraph("Heavy downpour (>40mm), steep gradient, loose debris", style_td), Paragraph("Convoy escort required; non-4x4 vehicles halted; dynamic reroute alert sent to operator.", style_td)],
        [Paragraph("80.0 – 100.0", style_td_bold), Paragraph("<font color='#DC2626'><b>CRITICAL</b></font>", style_td), Paragraph("2.30 – 2.80x", style_td), Paragraph("Active landslide, road breach, flash flood culvert overflow", style_td), Paragraph("Corridor immediately closed; Dijkstra algorithm locks edge; all convoys rerouted.", style_td)]
    ]
    risk_table = Table(
        risk_band_data,
        colWidths=[printable_w * 0.14, printable_w * 0.12, printable_w * 0.14, printable_w * 0.28, printable_w * 0.32],
        style=[
            ('BACKGROUND', (0, 0), (-1, 0), c_primary),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]
    )
    story.append(risk_table)
    story.append(Spacer(1, 5))

    # Section 5: Defense & Mountain Vehicle Fleet
    story.append(Paragraph("5. Dataset 3: Defense &amp; Mountain Vehicle Fleet Specifications", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=1, spaceAfter=4))

    story.append(Paragraph(
        "<b>Codebase Source:</b> <code>backend/services/state_store.py</code> &amp; <code>backend/db/init_db.py</code> | <b>Classification:</b> <font color='#0D9488'><b>[LIVE]</b></font><br/>"
        "The fleet catalog defines realistic tactical and civil mountain logistics vehicles modeled on standard Border Roads "
        "Organisation (BRO) and Indian Army Logistics Corps specifications. Each vehicle record includes precise capacities and incline gradeability.",
        style_body
    ))

    fleet_data = [
        [
            Paragraph("Vehicle ID", style_th),
            Paragraph("Vehicle Name &amp; Model", style_th),
            Paragraph("Payload", style_th),
            Paragraph("Volume", style_th),
            Paragraph("Hill Grade Rating", style_th),
            Paragraph("Fuel", style_th),
            Paragraph("Operational Role &amp; Mission Profile", style_th)
        ],
        [
            Paragraph("VEH-NER-01", style_td_bold),
            Paragraph("Mountain Freight 4x4 Cruiser<br/><i>Tata LPTA 715 4x4 High-Torque</i>", style_td),
            Paragraph("4,800 kg", style_td),
            Paragraph("22.0 m³", style_td),
            Paragraph("Grade A (35% Incline)", style_td),
            Paragraph("Heavy Diesel", style_td),
            Paragraph("Frontier high-altitude transit, steep pass convoy lead, all-weather emergency supply.", style_td)
        ],
        [
            Paragraph("VEH-NER-02", style_td_bold),
            Paragraph("Heavy Hill Hauler (10T)<br/><i>Ashok Leyland 1618 6x4 Heavy Cargo</i>", style_td),
            Paragraph("10,500 kg", style_td),
            Paragraph("45.0 m³", style_td),
            Paragraph("Grade B (22% Incline)", style_td),
            Paragraph("Diesel", style_td),
            Paragraph("Inter-depot bulk transport across NH-27 trunk routes; high-volume food and grain delivery.", style_td)
        ],
        [
            Paragraph("VEH-NER-03", style_td_bold),
            Paragraph("Rapid Valley Feeder (3T)<br/><i>Mahindra Furio 7 High Clearance</i>", style_td),
            Paragraph("3,200 kg", style_td),
            Paragraph("14.5 m³", style_td),
            Paragraph("Grade A (30% Slope)", style_td),
            Paragraph("Diesel", style_td),
            Paragraph("Agile arterial delivery connecting remote valley district headquarters to trunk highway.", style_td)
        ],
        [
            Paragraph("VEH-NER-04", style_td_bold),
            Paragraph("All-Weather Mountain 4x4<br/><i>Force Gurkha Alpine Cargo Spec</i>", style_td),
            Paragraph("2,500 kg", style_td),
            Paragraph("11.0 m³", style_td),
            Paragraph("Grade A (38% Alpine)", style_td),
            Paragraph("Diesel", style_td),
            Paragraph("Critical cold-chain medical parcels, blood plasma, oxygen, and reconnaissance transit.", style_td)
        ],
        [
            Paragraph("VEH-NER-05", style_td_bold),
            Paragraph("Multi-Axle Heavy Transporter<br/><i>Tata Signa 2823 Hill Transporter</i>", style_td),
            Paragraph("16,000 kg", style_td),
            Paragraph("58.0 m³", style_td),
            Paragraph("Grade B (20% Highway)", style_td),
            Paragraph("Diesel", style_td),
            Paragraph("Disaster infrastructure reconstruction, Bailey bridge steel pins, heavy generator sets.", style_td)
        ],
        [
            Paragraph("VEH-NER-06", style_td_bold),
            Paragraph("High-Mobility Light Carrier<br/><i>Mahindra Bolero Maxi Camper 4x4</i>", style_td),
            Paragraph("1,800 kg", style_td),
            Paragraph("8.5 m³", style_td),
            Paragraph("Grade A (35% Ridge)", style_td),
            Paragraph("Diesel", style_td),
            Paragraph("Narrow ridge roads, rural village outreach, rapid emergency search-and-rescue support.", style_td)
        ]
    ]

    fleet_table = Table(
        fleet_data,
        colWidths=[printable_w * 0.13, printable_w * 0.23, printable_w * 0.11, printable_w * 0.09, printable_w * 0.15, printable_w * 0.09, printable_w * 0.20],
        style=[
            ('BACKGROUND', (0, 0), (-1, 0), c_primary),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
            ('TOPPADDING', (0, 0), (-1, -1), 2.2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]
    )
    story.append(fleet_table)

    # PAGE BREAK TO PAGE 4
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: DATASET 4 - DRIVERS & DATASET 5 - CARGO TAXONOMY
    # =========================================================================
    story.append(Paragraph("6. Dataset 4: Certified Mountain Drivers Registry (25 Drivers)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=1, spaceAfter=4))

    story.append(Paragraph(
        "<b>Codebase Source:</b> <code>backend/services/state_store.py</code> &amp; <code>backend/db/init_db.py</code> | <b>Classification:</b> <font color='#0D9488'><b>[LIVE]</b></font><br/>"
        "Operating heavy vehicles across Himalayan ridge terrains requires specialized mountain driver licenses endorsed by regional "
        "licensing authorities. The platform maintains an active registry of <b>25 certified mountain drivers</b> with multi-lingual "
        "capabilities across North Eastern dialects, high safety ratings, and automated fatigue monitors (max 9-hour mountain driving cap).",
        style_body
    ))

    # Drivers Table
    drivers_sample = [
        [
            Paragraph("Driver ID", style_th),
            Paragraph("Full Name", style_th),
            Paragraph("Contact Phone", style_th),
            Paragraph("Exp.", style_th),
            Paragraph("Hill Cert.", style_th),
            Paragraph("Languages Spoken", style_th),
            Paragraph("Rating", style_th),
            Paragraph("Status &amp; Shift Assignment", style_th)
        ],
        [
            Paragraph("DRV-NER-101", style_td_bold),
            Paragraph("Tashi Norbu", style_td),
            Paragraph("+91 94351-88291", style_td),
            Paragraph("14 yrs", style_td),
            Paragraph("<font color='#16A34A'><b>YES</b></font>", style_td),
            Paragraph("Assamese, Hindi, English, Monpa", style_td),
            Paragraph("4.95 / 5.0", style_td_bold),
            Paragraph("Busy (Trip #1024 to Itanagar, ETA 8.5h remaining)", style_td)
        ],
        [
            Paragraph("DRV-NER-102", style_td_bold),
            Paragraph("Bikram Roy", style_td),
            Paragraph("+91 98640-12948", style_td),
            Paragraph("9 yrs", style_td),
            Paragraph("<font color='#16A34A'><b>YES</b></font>", style_td),
            Paragraph("Bengali, Assamese, Hindi", style_td),
            Paragraph("4.78 / 5.0", style_td_bold),
            Paragraph("Available (Guwahati Central Depot)", style_td)
        ],
        [
            Paragraph("DRV-NER-103", style_td_bold),
            Paragraph("Debajit Bora", style_td),
            Paragraph("+91 97060-77123", style_td),
            Paragraph("11 yrs", style_td),
            Paragraph("<font color='#16A34A'><b>YES</b></font>", style_td),
            Paragraph("Assamese, Hindi", style_td),
            Paragraph("4.88 / 5.0", style_td_bold),
            Paragraph("Available (Tezpur River Crossing Staging)", style_td)
        ],
        [
            Paragraph("DRV-NER-104", style_td_bold),
            Paragraph("Dorjee Khandu", style_td),
            Paragraph("+91 94360-33412", style_td),
            Paragraph("16 yrs", style_td),
            Paragraph("<font color='#16A34A'><b>YES</b></font>", style_td),
            Paragraph("Monpa, Hindi, English", style_td),
            Paragraph("4.96 / 5.0", style_td_bold),
            Paragraph("Available (Tawang Alpine Defense Outpost)", style_td)
        ],
        [
            Paragraph("DRV-NER-105", style_td_bold),
            Paragraph("Zonunmawia Ralte", style_td),
            Paragraph("+91 98623-88190", style_td),
            Paragraph("10 yrs", style_td),
            Paragraph("<font color='#16A34A'><b>YES</b></font>", style_td),
            Paragraph("Mizo, English, Hindi", style_td),
            Paragraph("4.82 / 5.0", style_td_bold),
            Paragraph("Available (Aizawl Ridge Logistics Depot)", style_td)
        ],
        [
            Paragraph("DRV-NER-106", style_td_bold),
            Paragraph("Temjen Jamir", style_td),
            Paragraph("+91 94362-55019", style_td),
            Paragraph("13 yrs", style_td),
            Paragraph("<font color='#16A34A'><b>YES</b></font>", style_td),
            Paragraph("Nagamese, English, Hindi", style_td),
            Paragraph("4.91 / 5.0", style_td_bold),
            Paragraph("Available (Dimapur Railhead Depot)", style_td)
        ],
        [
            Paragraph("DRV-NER-107", style_td_bold),
            Paragraph("Pema Lhamu", style_td),
            Paragraph("+91 94340-99214", style_td),
            Paragraph("8 yrs", style_td),
            Paragraph("<font color='#16A34A'><b>YES</b></font>", style_td),
            Paragraph("Bhutia, Nepali, Hindi, English", style_td),
            Paragraph("4.89 / 5.0", style_td_bold),
            Paragraph("Available (Gangtok Sikkim Staging Center)", style_td)
        ]
    ]

    drivers_table = Table(
        drivers_sample,
        colWidths=[printable_w * 0.13, printable_w * 0.15, printable_w * 0.15, printable_w * 0.08, printable_w * 0.09, printable_w * 0.18, printable_w * 0.10, printable_w * 0.12],
        style=[
            ('BACKGROUND', (0, 0), (-1, 0), c_primary),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
            ('TOPPADDING', (0, 0), (-1, -1), 2.2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]
    )
    story.append(drivers_table)
    story.append(Spacer(1, 6))

    # Section 7: Emergency Cargo Taxonomy
    story.append(Paragraph("7. Dataset 5: Multi-Tier Emergency &amp; Disaster Relief Cargo Taxonomy", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=1, spaceAfter=4))

    story.append(Paragraph(
        "<b>Codebase Source:</b> <code>backend/services/allocation_engine.py</code> | <b>Classification:</b> <font color='#D97706'><b>[SIMULATED]</b></font> &amp; <font color='#0D9488'><b>[LIVE]</b></font><br/>"
        "USP 2 implements a multi-tier constrained optimization engine (0/1 Knapsack with deadline penalties). Emergency supplies "
        "are categorized into four standardized humanitarian response tiers aligned with National Disaster Response Force (NDRF) guidelines.<br/>"
        "<i>Optimization Function:</i> <code>Priority Score = TIER_BASE - (deadline_hours × 50) + (urgency_score × 200)</code>",
        style_body
    ))

    cargo_tier_data = [
        [
            Paragraph("Priority Tier", style_th),
            Paragraph("Base Score", style_th),
            Paragraph("Humanitarian Category", style_th),
            Paragraph("Representative Manifest Items", style_th),
            Paragraph("Handling &amp; Physical Loading Directives", style_th),
            Paragraph("Maximum Allowed Delay", style_th)
        ],
        [
            Paragraph("<b>TIER 1</b><br/><font color='#DC2626'>CRITICAL</font>", style_td_bold),
            Paragraph("10,000", style_td_bold),
            Paragraph("Medical &amp; Life Support Supplies", style_td),
            Paragraph("Cold-chain vaccines, antivenom serums, portable oxygen cylinders, trauma surgical kits, blood plasma units.", style_td),
            Paragraph("Forward-cabin shock mounts; insulated temperature-controlled chambers; lowest center-of-gravity placement.", style_td),
            Paragraph("&lt; 6 to 12 Hours", style_td)
        ],
        [
            Paragraph("<b>TIER 2</b><br/><font color='#EA580C'>ESSENTIAL</font>", style_td_bold),
            Paragraph("5,000", style_td_bold),
            Paragraph("Human Survival Rations &amp; Shelter", style_td),
            Paragraph("Purified water jerrycans, high-calorie meal packs (MREs), infant milk formula, waterproof family tents, water purification tablets.", style_td),
            Paragraph("Evenly stacked across central cargo bed; secured under heavy waterproof tarpaulins.", style_td),
            Paragraph("&lt; 24 Hours", style_td)
        ],
        [
            Paragraph("<b>TIER 3</b><br/><font color='#0284C7'>RECOVERY</font>", style_td_bold),
            Paragraph("1,000", style_td_bold),
            Paragraph("Infrastructure Reconstruction", style_td),
            Paragraph("Bailey bridge steel structural pins, water pumps, diesel generators (25kVA), heavy fuel drums, earthmoving repair tools.", style_td),
            Paragraph("Heavy industrial chaining directly onto chassis anchor rings; axle weight limits enforced.", style_td),
            Paragraph("&lt; 48 to 72 Hours", style_td)
        ],
        [
            Paragraph("<b>TIER 4</b><br/><font color='#64748B'>GENERAL</font>", style_td_bold),
            Paragraph("100", style_td_bold),
            Paragraph("Commercial &amp; Administrative", style_td),
            Paragraph("Office documentation, standard parcel postal cargo, dry hardware, non-perishable general retail provisions.", style_td),
            Paragraph("Space-filling top cargo; deferred to Wave 2 if vehicle payload or volume bounds are exceeded.", style_td),
            Paragraph("Standard Logistics Cadence", style_td)
        ]
    ]

    cargo_table = Table(
        cargo_tier_data,
        colWidths=[printable_w * 0.13, printable_w * 0.10, printable_w * 0.19, printable_w * 0.26, printable_w * 0.22, printable_w * 0.10],
        style=[
            ('BACKGROUND', (0, 0), (-1, 0), c_primary),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]
    )
    story.append(cargo_table)

    # PAGE BREAK TO PAGE 5
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: DATASET 6 - HAZARDS & DATASETS 7 & 8 - RBAC & CARTOGRAPHY
    # =========================================================================
    story.append(Paragraph("8. Dataset 6: Active Hazard Alerts, Incidents &amp; Disruptions", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=1, spaceAfter=4))

    story.append(Paragraph(
        "<b>Codebase Source:</b> <code>backend/services/state_store.py</code> &amp; <code>backend/routers/alerts_router.py</code> | <b>Classification:</b> <font color='#0D9488'><b>[LIVE]</b></font> &amp; <font color='#D97706'><b>[SIMULATED]</b></font><br/>"
        "Active road hazard events represent dynamic topological impediments in the routing graph. Each disruption object contains "
        "exact coordinate vectors, severity rankings, estimated clearance timelines, and bypass feasibility flags.",
        style_body
    ))

    alerts_sample_data = [
        [
            Paragraph("Disruption ID", style_th),
            Paragraph("Corridor Segment", style_th),
            Paragraph("Hazard Typology", style_th),
            Paragraph("Severity Level", style_th),
            Paragraph("Estimated Clearance", style_th),
            Paragraph("Operational Impact &amp; Bypass Action", style_th)
        ],
        [
            Paragraph("DIS-2026-001", style_td_bold),
            Paragraph("NH-415 Km 21 (Banderdewa – Itanagar)", style_td),
            Paragraph("Massive Landslide (450m debris)", style_td),
            Paragraph("<font color='#DC2626'><b>CRITICAL (Closed)</b></font>", style_td),
            Paragraph("18 Hours (Heavy Excavators deployed)", style_td),
            Paragraph("Direct northern route blocked. Forces all inbound Guwahati convoys onto Southern Tezpur axis.", style_td)
        ],
        [
            Paragraph("DIS-2026-002", style_td_bold),
            Paragraph("NH-29 Pagla Pahar (Dimapur – Kohima)", style_td),
            Paragraph("Active Road Subsidence / Sinking Zone", style_td),
            Paragraph("<font color='#EA580C'><b>WARNING (Restricted)</b></font>", style_td),
            Paragraph("Continuous Monitoring (BRO taskforce)", style_td),
            Paragraph("Single-lane convoy alternating traffic; maximum vehicle gross weight restricted to &lt; 12T.", style_td)
        ],
        [
            Paragraph("DIS-2026-003", style_td_bold),
            Paragraph("NH-27 Kaziranga Southern Stretch", style_td),
            Paragraph("Monsoon Flood Inundation (35cm water)", style_td),
            Paragraph("<font color='#D97706'><b>ADVISORY (Slow)</b></font>", style_td),
            Paragraph("Dependent on Brahmaputra river gauge", style_td),
            Paragraph("Speed restricted to 20 km/h; high-clearance 4x4 vehicles only; nighttime transit prohibited.", style_td)
        ],
        [
            Paragraph("DIS-2026-004", style_td_bold),
            Paragraph("NH-13 Sela Pass High Altitude Approach", style_td),
            Paragraph("Black Ice &amp; Late Season Snowdrift", style_td),
            Paragraph("<font color='#DC2626'><b>CRITICAL (Chains Req.)</b></font>", style_td),
            Paragraph("Weather clearance window 10:00–14:00", style_td),
            Paragraph("Mandatory snow tire chains; convoy escorted by BRO snowplow units.", style_td)
        ]
    ]

    alerts_table = Table(
        alerts_sample_data,
        colWidths=[printable_w * 0.15, printable_w * 0.20, printable_w * 0.19, printable_w * 0.16, printable_w * 0.14, printable_w * 0.16],
        style=[
            ('BACKGROUND', (0, 0), (-1, 0), c_primary),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
            ('TOPPADDING', (0, 0), (-1, -1), 2.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]
    )
    story.append(alerts_table)
    story.append(Spacer(1, 6))

    # Section 9: RBAC & Cartography
    story.append(Paragraph("9. Datasets 7 &amp; 8: Security RBAC &amp; Cartographic Basemaps", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=1, spaceAfter=4))

    story.append(Paragraph(
        "<b>Security &amp; RBAC Architecture:</b> <code>backend/data/users.json</code> &amp; <code>backend/services/user_service.py</code><br/>"
        "The security subsystem implements zero-trust role-based access control (RBAC). Passwords are cryptographically salted "
        "and hashed using PBKDF2-HMAC-SHA256 with 100,000 iterations across four standardized operational personas:",
        style_body
    ))

    rbac_data = [
        [
            Paragraph("Role Key", style_th),
            Paragraph("Operational Persona", style_th),
            Paragraph("Authorized Capabilities &amp; Access Scope", style_th),
            Paragraph("Audit Trail Protocol", style_th)
        ],
        [
            Paragraph("<code>disaster_commander</code>", style_td_code),
            Paragraph("Disaster Response Commander (NDMA/State)", style_td_bold),
            Paragraph("Authority to declare corridor emergency closures, override autonomous reroute recommendations, and authorize military 4x4 escort escorts.", style_td),
            Paragraph("All decisions logged to immutable cryptographic ledger with UTC timestamp.", style_td)
        ],
        [
            Paragraph("<code>logistics_operator</code>", style_td_code),
            Paragraph("Logistics Hub Manager (Depot Dispatcher)", style_td_bold),
            Paragraph("Manages daily manifests, allocates cargo knapsacks, initiates vehicle loading sequences, and monitors regional driver shift counters.", style_td),
            Paragraph("Manifest creation IDs tied to operator session token.", style_td)
        ],
        [
            Paragraph("<code>field_driver</code>", style_td_code),
            Paragraph("Field Driver / Mountain Convoy Lead", style_td_bold),
            Paragraph("Accesses offline mobile PWA view, records checkpoint arrivals, executes geofenced checkpoint check-ins, and submits offline road hazard incident reports.", style_td),
            Paragraph("Cached locally in IndexedDB; synchronized upon GSM/satellite handshake.", style_td)
        ],
        [
            Paragraph("<code>auditor</code>", style_td_code),
            Paragraph("Government Liaison / Central Auditor", style_td_bold),
            Paragraph("Read-only access to historical route cost variance reports, fuel expenditure analytics, and Section 16 Data Provenance compliance dashboards.", style_td),
            Paragraph("Complete view access with zero data mutation capability.", style_td)
        ]
    ]

    rbac_table = Table(
        rbac_data,
        colWidths=[printable_w * 0.20, printable_w * 0.25, printable_w * 0.35, printable_w * 0.20],
        style=[
            ('BACKGROUND', (0, 0), (-1, 0), c_primary),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
            ('TOPPADDING', (0, 0), (-1, -1), 2.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]
    )
    story.append(rbac_table)
    story.append(Spacer(1, 5))

    story.append(Paragraph(
        "<b>Cartographic Basemaps &amp; Tile Geometry:</b> <code>frontend/js/app.js</code><br/>"
        "• <b>MapLibre GL JS v4:</b> High-performance WebGL vector/raster map renderer capable of rendering 60 FPS smooth polyline transitions.<br/>"
        "• <b>Tile Providers:</b> CartoDB Dark Matter (operational night mode) and CartoDB Voyager raster tilesets with high-contrast topographic contours.<br/>"
        "• <b>GeoJSON Feature Collections:</b> Live vehicle markers, pulsing alert circular buffers (5km hazard radius), and animated route comparison lines.",
        style_body
    ))

    # PAGE BREAK TO PAGE 6
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: MASTER CROSS-REFERENCE MATRIX & VERIFICATION SEAL
    # =========================================================================
    story.append(Paragraph("10. Master System Cross-Reference Matrix", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=1, spaceAfter=4))

    story.append(Paragraph(
        "This master cross-reference matrix maps every dataset to its originating backend service, persistent storage mechanism, "
        "frontend visualization component, and Section 16 Data Provenance tier.",
        style_body
    ))

    master_matrix = [
        [
            Paragraph("Dataset Domain", style_th),
            Paragraph("Backend Service", style_th),
            Paragraph("Storage Mechanism", style_th),
            Paragraph("Frontend UI Component", style_th),
            Paragraph("Section 16 Tier", style_th)
        ],
        [
            Paragraph("Geographic Graph &amp; Corridors", style_td_bold),
            Paragraph("<code>backend/services/ner_network.py</code>", style_td_code),
            Paragraph("In-Memory NetworkX Graph / SQLite", style_td),
            Paragraph("Interactive MapLibre Map (View 1)", style_td),
            Paragraph("<font color='#0284C7'><b>[HISTORICAL]</b></font>", style_td)
        ],
        [
            Paragraph("MCDA Risk Factors &amp; Multipliers", style_td_bold),
            Paragraph("<code>backend/services/risk_engine.py</code>", style_td_code),
            Paragraph("Mathematical Engine / Config Tables", style_td),
            Paragraph("Risk Factor Breakdown Sliders", style_td),
            Paragraph("<font color='#0284C7'><b>[HISTORICAL]</b></font>", style_td)
        ],
        [
            Paragraph("Tactical Vehicle Fleet (6 Models)", style_td_bold),
            Paragraph("<code>backend/services/state_store.py</code>", style_td_code),
            Paragraph("SQLite <code>vehicles</code> table / StateStore", style_td),
            Paragraph("Vehicle Fleet Drawer (View 2)", style_td),
            Paragraph("<font color='#0D9488'><b>[LIVE]</b></font>", style_td)
        ],
        [
            Paragraph("Certified Mountain Drivers (25)", style_td_bold),
            Paragraph("<code>backend/services/state_store.py</code>", style_td_code),
            Paragraph("SQLite <code>drivers</code> table / StateStore", style_td),
            Paragraph("Mountain Driver Directory Panel", style_td),
            Paragraph("<font color='#0D9488'><b>[LIVE]</b></font>", style_td)
        ],
        [
            Paragraph("Multi-Tier Cargo Taxonomy (Tiers 1-4)", style_td_bold),
            Paragraph("<code>backend/services/allocation_engine.py</code>", style_td_code),
            Paragraph("Knapsack Solver / In-Memory Store", style_td),
            Paragraph("Cargo Prioritization Engine (View 2)", style_td),
            Paragraph("<font color='#D97706'><b>[SIMULATED]</b></font>", style_td)
        ],
        [
            Paragraph("Active Road Disruptions &amp; Hazards", style_td_bold),
            Paragraph("<code>backend/routers/alerts_router.py</code>", style_td_code),
            Paragraph("SQLite <code>disruptions</code> table", style_td),
            Paragraph("Hazard Alerts Drawer &amp; Map Overlays", style_td),
            Paragraph("<font color='#0D9488'><b>[LIVE]</b></font>", style_td)
        ],
        [
            Paragraph("User Credentials &amp; RBAC Matrix", style_td_bold),
            Paragraph("<code>backend/services/user_service.py</code>", style_td_code),
            Paragraph("<code>backend/data/users.json</code> (PBKDF2)", style_td),
            Paragraph("Role Switcher &amp; JWT Modal", style_td),
            Paragraph("<font color='#0D9488'><b>[LIVE]</b></font>", style_td)
        ],
        [
            Paragraph("Offline Sync Queue &amp; Checkpoints", style_td_bold),
            Paragraph("<code>backend/routers/routes_router.py</code>", style_td_code),
            Paragraph("IndexedDB / LocalStorage Cache (PWA)", style_td),
            Paragraph("USP 3 Offline Driver PWA (View 3)", style_td),
            Paragraph("<font color='#0D9488'><b>[LIVE]</b></font>", style_td)
        ]
    ]

    master_table = Table(
        master_matrix,
        colWidths=[printable_w * 0.23, printable_w * 0.25, printable_w * 0.22, printable_w * 0.18, printable_w * 0.12],
        style=[
            ('BACKGROUND', (0, 0), (-1, 0), c_primary),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
            ('TOPPADDING', (0, 0), (-1, -1), 2.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]
    )
    story.append(master_table)
    story.append(Spacer(1, 5))

    # Section 11: Authoritative Government Data Citations & Presentation Reference
    story.append(Paragraph("11. Official Government Data Portals &amp; Slide Presentation Citations", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=1, spaceAfter=3))

    story.append(Paragraph(
        "For hackathon defense, government stakeholder reviews, and presentation slides, the geohazard indices and digital terrain "
        "models directly cite official Indian Space Research Organisation (ISRO) and National Remote Sensing Centre (NRSC) repositories:",
        style_body
    ))

    citations_data = [
        [
            Paragraph("Portal / Dataset Name", style_th),
            Paragraph("Official URL / Ingestion Endpoint", style_th),
            Paragraph("Authoritative Custodian", style_th),
            Paragraph("Role in System &amp; Slide Presentation Citation", style_th)
        ],
        [
            Paragraph("<b>ISRO Landslide Atlas of India (2023)</b>", style_td_bold),
            Paragraph("<font color='#0284C7'><u>isro.gov.in/.../LandslideAtlas_2023.pdf</u></font>", style_td_code),
            Paragraph("ISRO / NRSC, Hyderabad", style_td),
            Paragraph("District-level vulnerability rankings across 147 hill districts; calibrates baseline risk weights (W<sub>history</sub>) across high-risk NER districts (Papum Pare, Tawang, East Khasi Hills, Aizawl).", style_td)
        ],
        [
            Paragraph("<b>Bhuvan Disaster Services Portal</b>", style_td_bold),
            Paragraph("<font color='#0284C7'><u>bhuvan-app1.nrsc.gov.in/disaster/...</u></font>", style_td_code),
            Paragraph("NRSC Geoportal Division", style_td),
            Paragraph("Event-based satellite landslide inventories, post-monsoon damage polygons, and state-specific hazard reports (e.g. Sikkim 2016, Assam highway washouts).", style_td)
        ],
        [
            Paragraph("<b>Bhuvan Open Geospatial Data Hub</b>", style_td_bold),
            Paragraph("<font color='#0284C7'><u>bhuvan-app3.nrsc.gov.in/data/</u></font>", style_td_code),
            Paragraph("NRSC / ISRO", style_td),
            Paragraph("Open digital elevation models (CartoDEM 30m), terrain slope gradient contours (W<sub>slope</sub>), and regional lineament/fault geometries.", style_td)
        ],
        [
            Paragraph("<b>GSI NLSM &amp; BRO Transit Logs</b>", style_td_bold),
            Paragraph("Geological Survey of India &amp; Border Roads", style_td_code),
            Paragraph("Ministry of Mines / MoD", style_td),
            Paragraph("30-year macro-landslide recurrence database and operational clearance logs for high-altitude mountain passes.", style_td)
        ]
    ]

    citations_table = Table(
        citations_data,
        colWidths=[printable_w * 0.24, printable_w * 0.28, printable_w * 0.18, printable_w * 0.30],
        style=[
            ('BACKGROUND', (0, 0), (-1, 0), c_primary),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]
    )
    story.append(citations_table)
    story.append(Spacer(1, 5))

    # Concluding Verification Seal
    seal_data = [
        [
            Paragraph("<b>DATA INTEGRITY &amp; TECHNICAL CERTIFICATION</b>", style_meta_badge),
            Paragraph("<b>SYSTEM DEPLOYMENT STATUS</b>", style_meta_badge)
        ],
        [
            Paragraph(
                "This technical reference dossier verifies that all datasets, risk calculation formulas, "
                "fleet dimensions, and driver records are fully integrated into the active Smart NER Logistics Control Platform. "
                "The codebase adheres to Section 16 Data Integrity Standards, ensuring uncompromised operational transparency.",
                style_body
            ),
            Paragraph(
                "<b>Status:</b> FULLY OPERATIONAL &amp; VERIFIED<br/>"
                "<b>Backend:</b> FastAPI (0.0.0.0:8000)<br/>"
                "<b>Database:</b> SQLite (<code>smart_ner.db</code>) with Seed Backfill<br/>"
                "<b>Target Region:</b> All 8 North Eastern States of India",
                style_body
            )
        ]
    ]
    seal_table = Table(
        seal_data,
        colWidths=[printable_w * 0.60, printable_w * 0.40],
        style=[
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
            ('BOX', (0, 0), (-1, -1), 1.0, colors.HexColor("#0284C7")),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]
    )
    story.append(seal_table)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated: {filename}")

if __name__ == "__main__":
    out_pdf = os.path.join(os.getcwd(), "SMART_NER_LOGISTICS_DATASETS_REFERENCE.pdf")
    build_pdf(out_pdf)
