import os, sys
import fitz # PyMuPDF
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

ARTIFACT_DIR = r"C:\Users\tejas\.gemini\antigravity-ide\brain\eb4d8ea1-cab3-4c8f-8c8e-e48f9c594c61"
SWITCHER_IMG_PATH = os.path.join(ARTIFACT_DIR, r".user_uploaded\media_1789073864464.png")
OUTPUT_PDF = r"c:\Users\tejas\OneDrive\Documents\replit\SIH_JURY_DEFENSE_BASEMAP_OPTIONS_EXPLAINED.pdf"

class NumberedCanvas(canvas.Canvas):
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

        # Running Header (pages 2+)
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#0284C7"))
            self.drawString(margin, height - 24, "SMART NER LOGISTICS CONTROL PLATFORM")
            self.setFont("Helvetica", 7.5)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(width - margin, height - 24, "SIH JURY DEFENSE: GIS BASEMAP ARCHITECTURE & OPERATIONAL USE CASES")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(margin, height - 28, width - margin, height - 28)
            self.restoreState()

        # Running Footer (all pages)
        self.saveState()
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(margin, 30, width - margin, 30)
        self.setFont("Helvetica-Bold", 7)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(margin, 20, "SMART INDIA HACKATHON (SIH) - PROBLEM STATEMENT PS 26002")
        self.setFont("Helvetica", 7)
        self.drawRightString(width - margin, 20, f"Page {self._pageNumber} of {page_count} | Jury Technical Defense Dossier")
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=34,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=21,
        textColor=colors.HexColor('#0F172A'),
        alignment=TA_LEFT
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#475569'),
        alignment=TA_LEFT
    )
    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#0369A1'),
        spaceBefore=6,
        spaceAfter=3
    )
    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12.5,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=4,
        spaceAfter=2
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.2,
        textColor=colors.HexColor('#334155'),
        alignment=TA_JUSTIFY
    )
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.8,
        textColor=colors.HexColor('#334155'),
        leftIndent=8
    )
    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#0F172A')
    )
    table_hdr_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.white,
        alignment=TA_CENTER
    )
    table_cell_style = ParagraphStyle(
        'TD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor('#1E293B')
    )
    table_cell_bold = ParagraphStyle(
        'TDBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor('#0F172A')
    )

    story = []

    # ==========================================
    # PAGE 1: Title, Banner, Pitch, Section 1
    # ==========================================
    story.append(Paragraph("SMART NER LOGISTICS CONTROL PLATFORM", ParagraphStyle('SuperTitle', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.HexColor('#0284C7'))))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Jury Defense Brief: GIS Basemap Architecture & Operational Use Cases", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Why and When to Use Vector Dark, Satellite Recon, Topo Terrain, and Vector Light in High-Altitude North Eastern Freight Operations", subtitle_style))
    story.append(Spacer(1, 5))

    # Metadata & Switcher Image row
    meta_html = (
        "<b>Domain:</b> North Eastern Region (NER) Mountain Freight & Disaster Logistics<br/>"
        "<b>Problem Statement:</b> SIH PS 26002 (Resilient Multimodal Routing)<br/>"
        "<b>Technology:</b> MapLibre GL JS &plus; ArcGIS Server Keyless REST Tiles"
    )
    meta_p = Paragraph(meta_html, table_cell_style)

    if os.path.exists(SWITCHER_IMG_PATH):
        # 653x62 -> scale to width 260, height 24.7
        switcher_img = Image(SWITCHER_IMG_PATH, width=270, height=25.6)
    else:
        switcher_img = Paragraph("<b>[Basemap Layer Switcher]</b>", table_cell_style)

    header_table = Table([[meta_p, switcher_img]], colWidths=[260, 280])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 6))

    # 30-Second Pitch
    pitch_text = (
        "<b>30-Second Executive Pitch for the Jury:</b><br/>"
        "<i>\"In the North Eastern Region, freight logistics is not city delivery on flat plains—it is high-altitude, "
        "disaster-prone mountain transport subject to cloudbursts, slope landslides, river washouts, and extreme lighting variations. "
        "A single basemap cannot simultaneously serve a 24/7 disaster control room, a driver navigating noon sunlight glare, and an "
        "engineer analyzing 35° mountain slope hazards. We decoupled our mapping engine into four specialized GIS basemap modes, "
        "each purpose-built for a distinct operational role, lighting environment, and physical hazard profile.\"</i>"
    )
    pitch_box = Table([[Paragraph(pitch_text, callout_style)]], colWidths=[540])
    pitch_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#E0F2FE')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#0284C7')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(pitch_box)
    story.append(Spacer(1, 6))

    # Section 1: Detailed Breakdown
    story.append(Paragraph("1. Detailed Breakdown: Operational Role of Each Basemap Layer", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor('#0284C7'), spaceBefore=1, spaceAfter=5))

    # Vector Dark
    story.append(Paragraph("A. Vector Dark (ArcGIS Dark Gray Canvas)", h2_style))
    story.append(Paragraph("<b>Operational Role:</b> Tactical 24/7 Command Center & Night Dispatch Operations.", body_style))
    story.append(Paragraph("&bull; <b>WHY:</b> Mutes background map clutter into neutral charcoal (#111827) so that <b>critical dynamic signals—emerald safe corridors (#10B981), rose hazard lines (#F43F5E), and roadblock pins—stand out with maximum visual contrast</b> while eliminating ocular fatigue during 12-hour shifts.", bullet_style))
    story.append(Paragraph("&bull; <b>WHEN:</b> Night shifts (20:00–06:00 IST) in regional headquarters (Guwahati/Shillong) and active multi-truck convoy telemetry monitoring.", bullet_style))
    story.append(Spacer(1, 4))

    # Satellite Recon
    story.append(Paragraph("B. Satellite Recon (ArcGIS World Imagery / High-Res Orbital Imagery)", h2_style))
    story.append(Paragraph("<b>Operational Role:</b> Ground-Truth Physical Terrain Verification & Geological Hazard Inspection.", body_style))
    story.append(Paragraph("&bull; <b>WHY:</b> Digital road lines do not tell the dispatcher if a highway hugs an eroding riverbed gorge or passes under active rock faces. Sub-meter orbital imagery reveals <b>landslide scars, riverbank siltation, gorge narrows, and actual road cuttings</b>.", bullet_style))
    story.append(Paragraph("&bull; <b>WHEN:</b> Pre-dispatch route validation (e.g. Bhalukpong river gorge vs. Sela tunnel bypass) and post-cloudburst corridor clearance checks.", bullet_style))
    story.append(Spacer(1, 4))

    # Topo Terrain
    story.append(Paragraph("C. Topo Terrain (ArcGIS World Topographic Map / Elevation & Contours)", h2_style))
    story.append(Paragraph("<b>Operational Role:</b> Slope Gradient Analysis, Mountain Pass Altitude Assessment, & Watershed Runoff Triage.", body_style))
    story.append(Paragraph("&bull; <b>WHY:</b> Landslide susceptibility in the Himalayas correlates directly with <b>slope angles (>35°) and elevation variance (180 ft plains to 13,700 ft passes)</b>. Topo Terrain provides continuous contour lines, elevation intervals, and watershed ridgelines.", bullet_style))
    story.append(Paragraph("&bull; <b>WHEN:</b> Monsoon season (May–September) to identify rain-induced toe-erosion zones, winter pass freeze-ups, and multi-axle truck hairpin feasibility.", bullet_style))
    story.append(Spacer(1, 4))

    # Vector Light
    story.append(Paragraph("D. Vector Light (ArcGIS World Street Map / High-Visibility Day Ops)", h2_style))
    story.append(Paragraph("<b>Operational Role:</b> High-Ambient-Light Readability, Administrative Jurisdiction, & Inter-Agency Hand-Off.", body_style))
    story.append(Paragraph("&bull; <b>WHY:</b> Dark screens suffer severe reflective glare in direct sunlight. Vector Light delivers maximum photometric luminance while highlighting <b>district boundaries, police checkpoints, toll plazas, National Highway markers (NH-13, NH-15, NH-27), and named towns</b>.", bullet_style))
    story.append(Paragraph("&bull; <b>WHEN:</b> Daytime dispatch on driver tablets/loading docks and inter-agency coordination with Border Roads Organisation (BRO), Assam Rifles, and NDRF.", bullet_style))

    # ==========================================
    # PAGE 2: Decision Matrix Table & Domain Need
    # ==========================================
    story.append(PageBreak())

    story.append(Paragraph("2. Operational Decision Matrix: When to Select Each Basemap", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor('#0284C7'), spaceBefore=1, spaceAfter=6))
    story.append(Paragraph("The following matrix maps operational roles directly to environmental triggers and supported decisions:", body_style))
    story.append(Spacer(1, 4))

    matrix_data = [
        [
            Paragraph("<b>Basemap Mode</b>", table_hdr_style),
            Paragraph("<b>Target User & Environment</b>", table_hdr_style),
            Paragraph("<b>Environmental Trigger</b>", table_hdr_style),
            Paragraph("<b>Operational Decision Supported</b>", table_hdr_style),
            Paragraph("<b>Key Technical Feature</b>", table_hdr_style)
        ],
        [
            Paragraph("<b>Vector Dark</b>", table_cell_bold),
            Paragraph("Central Command Center<br/>(Guwahati / Shillong HQ)", table_cell_style),
            Paragraph("Night operations (20:00–06:00 IST), low-light triage rooms", table_cell_style),
            Paragraph("Active fleet dispatch, real-time alert triage, multi-truck convoy tracking", table_cell_style),
            Paragraph("Suppressed street noise, maximum neon contrast for risk heatmaps", table_cell_style)
        ],
        [
            Paragraph("<b>Satellite Recon</b>", table_cell_bold),
            Paragraph("Geological Risk Officer & Relief Dispatch Lead", table_cell_style),
            Paragraph("Pre-dispatch hazard scan, post-cloudburst corridor check", table_cell_style),
            Paragraph("Validating gorge vs. ridge routes, checking riverbank erosion & rock scars", table_cell_style),
            Paragraph("Sub-meter orbital imagery, true physical ground verification", table_cell_style)
        ],
        [
            Paragraph("<b>Topo Terrain</b>", table_cell_bold),
            Paragraph("Civil Infrastructure Engineer & Route Safety Analyst", table_cell_style),
            Paragraph("Monsoon rains (>75mm/24h), winter freeze at >10,000 ft altitude", table_cell_style),
            Paragraph("Assessing slope gradient (>35°), mountain pass viability, hairpin curvature", table_cell_style),
            Paragraph("Continuous elevation contours, shaded relief, watershed basins", table_cell_style)
        ],
        [
            Paragraph("<b>Vector Light</b>", table_cell_bold),
            Paragraph("Warehouse Field Supervisor & Truck Driver in Transit", table_cell_style),
            Paragraph("Bright daylight, high-glare tablet screens, outdoor terminals", table_cell_style),
            Paragraph("Identifying police checkpoints, administrative district borders, toll plazas", table_cell_style),
            Paragraph("Maximum photometric luminance, clear highway milestones & town labels", table_cell_style)
        ]
    ]

    col_widths = [75, 105, 110, 130, 120]
    matrix_table = Table(matrix_data, colWidths=col_widths, repeatRows=1)
    matrix_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0284C7')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(matrix_table)
    story.append(Spacer(1, 10))

    # Section 3: Domain Justification
    story.append(Paragraph("3. Domain Justification: Why Single-Basemap Systems Fail in Mountain Logistics", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor('#0284C7'), spaceBefore=1, spaceAfter=6))
    story.append(Paragraph(
        "Standard mainland logistics platforms (e.g., Delhivery, Blue Dart, Amazon) rely exclusively on a single Google Maps or OSM "
        "street basemap because highway topology in flat plains is uniform. In India's North Eastern Region, this approach leads to "
        "critical operational blind spots due to three geographic realities:",
        body_style
    ))
    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>1. Extreme Elevation Variance:</b> A 150-km journey in Arunachal Pradesh spans from 180 ft (Brahmaputra plain) to 13,700 ft (Sela Pass). A street basemap does not convey that the truck is climbing into sub-zero oxygen-depleted terrain. Topo Terrain makes this elevation transition instantly readable for engine load and brake wear calculation.", bullet_style))
    story.append(Paragraph("<b>2. Gorge vs. Ridge Road Vulnerability:</b> Two highways between the same origin and destination can have identical driving distances but completely different risk regimes. For example, Old NH-13 runs through the narrow Kameng riverbed gorge (subject to flash flood washouts), while the OKSRT Defense Road travels along reinforced ridges and tunnels. Satellite Recon allows dispatchers to verify this in seconds.", bullet_style))
    story.append(Paragraph("<b>3. Multi-Agency Maintenance & Jurisdictions:</b> Mountain highways are maintained by multiple overlapping entities—the Border Roads Organisation (Project Vartak / Project Pushpak), State PWDs, and the NHIDCL. Vector Light provides the administrative clarity required to coordinate convoys across state boundaries and police checkpoints.", bullet_style))

    # ==========================================
    # PAGE 3: Tech Architecture, Cheatsheet & Summary
    # ==========================================
    story.append(PageBreak())

    story.append(Paragraph("4. Technical Architecture & Engineering Integrity", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor('#0284C7'), spaceBefore=1, spaceAfter=6))
    story.append(Paragraph("&bull; <b>Zero API-Key Dependency:</b> All four basemap styles leverage public, high-availability ArcGIS REST services directly from <code>server.arcgisonline.com</code>. This eliminates third-party token expiry, rate-limiting watermarks, or black-tile error screens during jury demonstrations.", bullet_style))
    story.append(Paragraph("&bull; <b>3D WebGL Vector Persistence:</b> Built with MapLibre GL JS utilizing a 35° perspective pitch angle. Route polylines (Route A high-risk and Route B recommended) dynamically persist across style switches via automated lifecycle listeners (<code>style.load</code> / <code>waitForMapStyle</code>).", bullet_style))
    story.append(Paragraph("&bull; <b>Low-Bandwidth & Offline Readiness:</b> Basemap tiles and route vector GeoJSONs are structured to be cached via client-side Service Workers and IndexedDB, ensuring mission-critical continuity when convoys transit zero-connectivity Himalayan valleys.", bullet_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("5. Quick Verbal Cheatsheet: Exact 1-Sentence Answers for the Jury", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor('#0284C7'), spaceBefore=1, spaceAfter=6))

    cheat_data = [
        [
            Paragraph("<b>If the Judge asks:</b>", table_cell_bold),
            Paragraph("<b>Deliver this exact 1-sentence answer:</b>", table_cell_bold)
        ],
        [
            Paragraph("<i>\"Why do you need Vector Dark?\"</i>", table_cell_style),
            Paragraph("\"Vector Dark is built for 24/7 disaster control rooms—it suppresses street clutter and eye fatigue so that glowing red landslide hazard zones and green safe corridors stand out with maximum clarity during night shifts.\"", table_cell_style)
        ],
        [
            Paragraph("<i>\"Why is Satellite Recon necessary?\"</i>", table_cell_style),
            Paragraph("\"Satellite Recon gives ground-truth physical verification—before sending a 20-ton medical convoy, dispatchers can physically verify actual rock scars, river widths, and gorge washouts that schematic road lines cannot show.\"", table_cell_style)
        ],
        [
            Paragraph("<i>\"Why do you have Topo Terrain?\"</i>", table_cell_style),
            Paragraph("\"Topo Terrain reveals elevation contours and slope angles (>35°)—allowing engineers to predict monsoon toe-erosion in river valleys and avoid freezing or vehicle stalling at 13,700-ft mountain passes.\"", table_cell_style)
        ],
        [
            Paragraph("<i>\"Why keep Vector Light?\"</i>", table_cell_style),
            Paragraph("\"Vector Light is designed for high-glare daytime tablets in loading docks and for coordination with police, BRO, and district authorities who need standard highway milestones, toll plazas, and administrative borders.\"", table_cell_style)
        ]
    ]

    cheat_table = Table(cheat_data, colWidths=[150, 390])
    cheat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(cheat_table)
    story.append(Spacer(1, 10))

    # Summary Callout Box
    concl_text = (
        "<b>Key Takeaway for SIH Evaluators:</b><br/>"
        "By decoupling the GIS basemap into these four modes, our platform ensures <b>zero cognitive overload</b>: "
        "planners view only the terrain and infrastructure layers strictly relevant to their immediate operational decision—whether "
        "it is slope risk during a cloudburst, physical gorge verification before dispatch, or daylight route briefing with local authorities."
    )
    concl_box = Table([[Paragraph(concl_text, callout_style)]], colWidths=[540])
    concl_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0FDF4')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#16A34A')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(concl_box)

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print("SUCCESS: Perfectly built 3-page PDF at:", OUTPUT_PDF)

    # Convert pages to PNG for visual inspection
    pdf_doc = fitz.open(OUTPUT_PDF)
    print(f"Total pages generated: {len(pdf_doc)}")
    for i, page in enumerate(pdf_doc):
        pix = page.get_pixmap(dpi=150)
        img_out = os.path.join(ARTIFACT_DIR, f"basemap_guide_page_{i+1}.png")
        pix.save(img_out)
        print(f"Saved page {i+1} preview to: {img_out}")

if __name__ == "__main__":
    build_pdf()
