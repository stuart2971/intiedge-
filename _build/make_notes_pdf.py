# -*- coding: utf-8 -*-
"""Generate the IntiEdge website project notes PDF."""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image,
    KeepTogether, HRFlowable
)

NAVY = HexColor("#0B2A63")
TEAL = HexColor("#118DA3")
BLUE = HexColor("#148EEA")
DARK = HexColor("#1A1A1A")
LIGHT = HexColor("#F5F7FA")
DIVIDER = HexColor("#DCE5F0")
GRAY = HexColor("#5A6B85")

BASE = r"C:\Users\stuar\OneDrive\Documents\Side Hustles\Shelly Moffat"
OUT = os.path.join(BASE, "IntiEdge Website Project Notes.pdf")
LOGO = os.path.join(BASE, "branding", "logo.png")

styles = getSampleStyleSheet()

h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName="Helvetica-Bold",
                    fontSize=20, textColor=NAVY, spaceBefore=0, spaceAfter=10)
h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                    fontSize=14, textColor=NAVY, spaceBefore=18, spaceAfter=6)
h3 = ParagraphStyle("H3", parent=styles["Heading3"], fontName="Helvetica-Bold",
                    fontSize=11.5, textColor=TEAL, spaceBefore=10, spaceAfter=4)
body = ParagraphStyle("Body", parent=styles["Normal"], fontName="Helvetica",
                      fontSize=10, leading=14.5, textColor=DARK, spaceAfter=6)
bullet = ParagraphStyle("Bullet", parent=body, leftIndent=16, bulletIndent=6,
                        spaceAfter=3)
small = ParagraphStyle("Small", parent=body, fontSize=8.5, textColor=GRAY)
cover_sub = ParagraphStyle("CoverSub", parent=body, fontSize=13, leading=18,
                           textColor=GRAY)
quote = ParagraphStyle("Quote", parent=body, leftIndent=18, rightIndent=18,
                       fontName="Helvetica-Oblique", textColor=NAVY,
                       borderPadding=8, spaceBefore=6, spaceAfter=10)


def b(text):
    return Paragraph(text, bullet, bulletText="•")


def hr():
    return HRFlowable(width="100%", thickness=0.75, color=DIVIDER,
                      spaceBefore=4, spaceAfter=10)


def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setFillColor(NAVY)
        canvas.rect(0, letter[1] - 0.42 * inch, letter[0], 0.42 * inch,
                    stroke=0, fill=1)
        canvas.setFillColor(white)
        canvas.setFont("Helvetica-Bold", 8.5)
        canvas.drawString(0.75 * inch, letter[1] - 0.28 * inch,
                          "IntiEdge Partners Inc. - Website Project Notes")
        canvas.setFont("Helvetica", 8.5)
        canvas.drawRightString(letter[0] - 0.75 * inch,
                               letter[1] - 0.28 * inch,
                               "Prepared June 11, 2026")
    canvas.setFillColor(GRAY)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(letter[0] / 2, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def kv_table(rows, col1=2.1, col2=4.4):
    t = Table(rows, colWidths=[col1 * inch, col2 * inch])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("TEXTCOLOR", (0, 0), (0, -1), NAVY),
        ("TEXTCOLOR", (1, 0), (1, -1), DARK),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [white, LIGHT]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, DIVIDER),
    ]))
    return t


def grid_table(data, widths, header=True):
    t = Table(data, colWidths=[w * inch for w in widths], repeatRows=1)
    style = [
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (-1, -1), DARK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.5, DIVIDER),
    ]
    if header:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
        ]
    t.setStyle(TableStyle(style))
    return t


story = []

# ---------------- COVER ----------------
story.append(Spacer(1, 1.2 * inch))
story.append(Image(LOGO, width=2.2 * inch, height=2.2 * inch))
story.append(Spacer(1, 0.4 * inch))
story.append(Paragraph("Website Project Notes", ParagraphStyle(
    "CoverTitle", parent=h1, fontSize=30, leading=36, alignment=TA_LEFT)))
story.append(Paragraph(
    "IntiEdge Partners Inc. &mdash; everything learned from the client files,"
    " discovery notes, and design direction.", cover_sub))
story.append(Spacer(1, 0.35 * inch))
story.append(kv_table([
    ["Client", "Shelly Moffat (Nasution-Moffat), EMBA - Founder & Principal"],
    ["Business", "IntiEdge Partners Inc. - finance, operations & AI advisory"],
    ["Location", "London, Ontario, Canada"],
    ["Contact", "shelly@intiedge.com  |  1-226-678-3324"],
    ["Web / Social", "www.intiedge.com  |  linkedin.com/in/shellymoffat"],
    ["Prepared by", "Web design & development (Stuart) - June 11, 2026"],
]))
story.append(PageBreak())

# ---------------- 1. BUSINESS ----------------
story.append(Paragraph("1. The Business", h1))
story.append(hr())
story.append(Paragraph(
    "IntiEdge Partners Inc. is a solo consulting practice founded by Shelly "
    "Moffat. The name comes from <b>\"inti\" = core</b> (captured in the "
    "discovery meeting notes) - the firm works on the core of a business: "
    "finance, operations, and the systems that connect them. The tagline is "
    "<b>\"Purposeful Growth.\"</b>", body))
story.append(Paragraph(
    "Positioning (from the brand playbook): <b>Finance Leadership &bull; "
    "Operational Excellence &bull; AI-Enabled Growth</b>. The site should "
    "feel like <b>60% executive advisory, 25% technology/AI, 15% finance</b> "
    "- deliberately NOT a traditional accounting firm. Reference brands named "
    "in the playbook: Deloitte Private, McKinsey, fractional-CFO / executive "
    "advisory firms.", body))
story.append(Paragraph("Core differentiator", h3))
story.append(Paragraph(
    "“Unlike many consultants who provide recommendations and leave, "
    "IntiEdge combines strategic advice with hands-on execution.” "
    "Advise + implement, across finance + operations + technology + AI + "
    "people - most advisors specialize in only one of these.", quote))

story.append(Paragraph("Three service pillars", h3))
story.append(grid_table([
    ["Finance Leadership & CFO Advisory", "Operations & Process Improvement",
     "AI-Enabled Business Transformation"],
    ["Fractional CFO\nInterim Controller\nFinancial Reporting & Analysis\n"
     "Budgeting & Forecasting\nCash Flow Management\nKPI Development & Dashboards\n"
     "Audit & Governance Support",
     "Process Mapping & Optimization\nWorkflow Redesign\nOrganizational "
     "Effectiveness\nPerformance Management\nOperational Reporting\n"
     "Business Scalability",
     "AI Readiness Assessment\nReporting Automation\nAI-Assisted Financial "
     "Analysis\nProcess Documentation\nKnowledge Management\nWorkflow "
     "Automation\nERP & Systems Optimization"],
], [2.17, 2.17, 2.17]))

story.append(Paragraph("Target clients - two distinct audiences", h3))
story.append(grid_table([
    ["", "Audience A - Executive / Mid-Market", "Audience B - Small Business Owner"],
    ["Who", "CEOs, Presidents, CFOs, boards, PE-owned companies",
     "Owner-operators of growing small businesses"],
    ["Tone", "Professional, corporate, credentialed",
     "Plain-spoken, relatable, low-pressure"],
    ["Lead message", "\"Helping growing organizations improve profitability, "
     "strengthen operations, and build scalable systems\"",
     "\"Feeling like your business has become harder to manage as it grows?\""],
    ["Pain points", "Limited performance visibility; inefficient processes; "
     "growth outpacing systems & controls; tech investments not delivering; "
     "leadership gaps & resource constraints",
     "Not sure which customers/services are profitable; slow reports; manual "
     "tasks; too many spreadsheets; growing but disorganized; needs executive "
     "support without an executive hire"],
], [0.85, 2.83, 2.83]))
story.append(Paragraph(
    "Key design tension from our June 10 call: the site must feel "
    "<b>approachable to small businesses while remaining credible to large/"
    "corporate buyers</b>. The discovery notes phrase it as "
    "“modern/sophisticated but small businesses can relate.”", body))
story.append(PageBreak())

# ---------------- 2. THE FOUNDER ----------------
story.append(Paragraph("2. The Founder - Shelly Moffat, EMBA", h1))
story.append(hr())
story.append(Paragraph(
    "Full name Shelly Nasution-Moffat; brand materials use <b>Shelly Moffat, "
    "EMBA</b> (playbook explicitly says EMBA, not MBA - she graduates from "
    "Ivey Business School in 2026). Position her as: “Executive MBA "
    "graduate, senior finance and operations leader, and founder of IntiEdge "
    "Partners Inc.”", body))
story.append(Paragraph("Career snapshot (from the three resumes)", h3))
story.append(kv_table([
    ["Experience", "15+ years across SaaS, logistics, manufacturing, "
     "construction, retail, professional services, and not-for-profit"],
    ["Most recent", "Director of Finance, InvestorCOM Holdings ULC "
     "(May 2024 - Jan 2026)"],
    ["Prior roles", "Financial Controller, MAC Group (10 operating cos.); "
     "Controller, Ingersoll Products; Accounting & HR Manager, Global "
     "Warranty; Manager of Finance, Corporate Investigation Services"],
    ["Education", "EMBA, Ivey Business School (2026); BA Sociology, Western; "
     "BA Economics, Univ. of Trisakti, Indonesia; CPA in progress"],
    ["Certifications", "CHRL, PCP, CDP, Mental Health for HR, JHSC I & II"],
    ["Technology", "Sage Intacct, QuickBooks, MS Dynamics/NAV, Power BI, "
     "BambooHR, ADP, Ceridian, Stripe, HubSpot, Salesforce"],
]))
story.append(Paragraph("Proof points worth surfacing on the website", h3))
story.append(b("Cut invoicing cycle time 65% and AP processing time 50% "
               "through automation (InvestorCOM)."))
story.append(b("Reduced OPEX 14% at a manufacturer (Ingersoll Products)."))
story.append(b("Unified reporting across 10 operating companies with Power "
               "BI dashboards (MAC Group)."))
story.append(b("Secured SR&ED and CanExport government funding."))
story.append(b("Administered payroll for 200+ employees; full-cycle "
               "accounting + HR for seven entities."))
story.append(Paragraph("Personal purpose statement", h3))
story.append(Paragraph(
    "“Lead with kindness, grow continuously, and elevate people and "
    "organizations through purposeful leadership.” - this is where the "
    "“Purposeful Growth” tagline comes from, and it should inform "
    "the warm, human side of the About page.", quote))
story.append(Paragraph(
    "Three resume variants exist (strategy / finance / operations angles) - "
    "useful as source copy for service-specific credibility, not for "
    "publishing wholesale.", body))

# ---------------- 3. BRAND ----------------
story.append(Paragraph("3. Brand Identity", h1))
story.append(hr())
story.append(Paragraph("Official colours (confirmed with Stuart, June 11: "
                       "use this palette - the playbook also contains an "
                       "older draft palette that is superseded)", h3))
story.append(grid_table([
    ["Role", "Name", "HEX", "Usage"],
    ["Primary", "IntiEdge Navy", "#0B2A63",
     "\"Inti\" wordmark, logo circles, tagline, headings"],
    ["Secondary", "IntiEdge Teal", "#118DA3", "Capital \"E\", highlights"],
    ["Accent", "IntiEdge Blue", "#148EEA",
     "\"dge\" wordmark, right-side logo bars, CTAs - THE blue to keep"],
    ["Gradient", "Teal to Blue", "#118DA3 → #148EEA",
     "Buttons, accent lines, CTA sections, icons"],
    ["Background", "White / Light Gray", "#FFFFFF / #F5F7FA",
     "Page background / alternating sections"],
    ["Text", "Dark", "#1A1A1A", "Body text"],
    ["Divider", "Light blue-gray", "#DCE5F0", "Section dividers"],
], [1.0, 1.35, 1.5, 2.66]))
story.append(Paragraph("Typography", h3))
story.append(b("Logo: geometric sans-serif; closest match <b>Montserrat "
               "SemiBold/Bold</b> (free Google font)."))
story.append(b("Tagline: Montserrat Medium, ALL CAPS, letter-spacing +250 "
               "to +300."))
story.append(b("Website pairing: <b>Montserrat Bold headings + Open Sans "
               "(or Source Sans Pro) body</b>."))
story.append(Paragraph("Brand personality", h3))
story.append(Paragraph(
    "Professional + Modern + Strategic + Approachable + Technology-enabled. "
    "NOT: corporate bureaucracy, accounting firm, startup-gimmicky.", body))
story.append(Paragraph("Logo notes", h3))
story.append(b("Circular mark: navy C-form ring + navy core dot, with "
               "teal-to-blue horizontal bars forming the right half "
               "(an abstract E). Wordmark: \"Inti\" navy, \"Edge\" "
               "teal-to-blue gradient."))
story.append(b("Supplied logo.png sits on an off-white background (not "
               "transparent) - needs background removal or careful placement "
               "on light surfaces for web use."))
story.append(PageBreak())

# ---------------- 4. WEBSITE PLAN ----------------
story.append(Paragraph("4. Website Plan (from the brand playbook)", h1))
story.append(hr())
story.append(Paragraph(
    "Navigation: <b>Home &middot; Services &middot; Approach &middot; About "
    "Shelly &middot; Why IntiEdge &middot; AI Enablement &middot; Contact</b>",
    body))
story.append(grid_table([
    ["Page", "Planned content"],
    ["Home", "Headline: \"Transforming Finance, Operations, and Growth "
     "Through Practical Expertise and AI-Enabled Innovation.\" Sub: "
     "\"IntiEdge Partners helps growing organizations improve visibility, "
     "streamline operations, strengthen decision-making, and build scalable "
     "foundations for sustainable growth.\""],
    ["Services", "Three pillars with service lists (see section 1)."],
    ["Approach", "4-phase methodology: 1) Discover & Assess (wks 1-2), "
     "2) Design & Prioritize (wks 2-4), 3) Implement & Enable (months 2-4), "
     "4) Sustain & Optimize (ongoing). Early wins within 30-60 days."],
    ["About Shelly", "EMBA positioning, 15+ years, industries served, "
     "professional photo (photos/proposal.jpeg), purpose statement."],
    ["Why IntiEdge", "The bridge story: Finance + Operations + Technology + "
     "AI + People & Process - most advisors specialize in one."],
    ["AI Enablement", "Dedicated page, strongly recommended in playbook. "
     "Title: \"AI for Practical Business Results.\" Message: AI is not about "
     "replacing people - work smarter, decide better, reduce admin burden. "
     "Differentiator vs. traditional advisory firms."],
    ["Contact", "Large CTA: \"Let's Start the Conversation\" with button "
     "\"Book a Discovery Call.\" 30-minute complimentary discovery meeting - "
     "no obligation, no pressure."],
], [1.25, 5.26]))
story.append(Paragraph("Website goals (from handwritten discovery notes)", h3))
story.append(b("Generate leads and build credibility."))
story.append(b("Book complimentary meetings - mention \"30 min "
               "complimentary\" explicitly."))
story.append(b("Possible online payment capability (raised with a "
               "question mark - confirm scope)."))
story.append(b("Personalized / shows personality; testimonials wanted."))
story.append(b("Scalable as the business grows."))
story.append(b("Emails go to the company email; quotes/invoices to the "
               "company; ads for the website as marketing were discussed."))

# ---------------- 5. PRICING ----------------
story.append(Paragraph("5. Pricing & Engagement Model", h1))
story.append(hr())
story.append(Paragraph(
    "From marketing/feestructure.png - shared with prospects only after a "
    "project is discussed; decide deliberately whether pricing appears on "
    "the public site (see section 8).", body))
story.append(Paragraph("Hourly advisory rates", h3))
story.append(grid_table([
    ["Service", "Rate"],
    ["Advisory / Consulting", "$175 - $225 / hour"],
    ["Fractional CFO / Interim Controller", "$150 - $200 / hour"],
    ["Operations Advisory", "$175 - $225 / hour"],
    ["AI & Process Transformation", "$175 - $225 / hour"],
    ["Recommended starting rate", "$195 / hour"],
], [3.5, 3.0]))
story.append(Paragraph("Monthly retainers (fractional finance leadership)", h3))
story.append(grid_table([
    ["Package", "Monthly fee", "Includes"],
    ["Essential", "$2,500 - $3,500", "Monthly meetings, reporting review, "
     "email support, up to 5 hrs advisory"],
    ["Growth", "$4,000 - $6,000", "Essential + budget & forecast support, "
     "KPI monitoring, up to 10 hrs"],
    ["Strategic", "$7,500 - $10,000+", "Growth + strategic planning, board "
     "reporting support, up to 20 hrs"],
], [1.2, 1.6, 3.7]))
story.append(Paragraph("Fixed-fee projects", h3))
story.append(grid_table([
    ["Project", "Investment range"],
    ["Finance Transformation Assessment (review + 90-day roadmap)",
     "$2,500 - $4,000"],
    ["KPI & Dashboard Development", "$3,000 - $7,500"],
    ["Process Improvement Review", "$2,500 - $5,000"],
    ["AI Readiness Assessment", "$2,500 - $5,000"],
], [4.3, 2.2]))
story.append(Paragraph(
    "Value line used in collateral: “You're not just paying for time. "
    "You're investing in expertise, experience, and results that drive your "
    "business forward.” Engagement models: hourly (ad-hoc), fixed-fee "
    "(defined deliverables), retainer (ongoing), fractional leadership "
    "(part-time executive).", body))
story.append(PageBreak())

# ---------------- 6. SALES PROCESS ----------------
story.append(Paragraph("6. Sales Process & Existing Collateral", h1))
story.append(hr())
story.append(Paragraph(
    "A consultative sequence (recommended by \"Sandra\" in the playbook) "
    "that the website should mirror - lead with problems and conversation, "
    "reveal capability and pricing progressively:", body))
story.append(grid_table([
    ["Stage", "Material", "File"],
    ["1. First touch", "One-page sales brochure (per audience)",
     "brochures/executive.*, brochures/smallbusiness.*"],
    ["2. Interest established", "General Advisory capability statement",
     "services/advisory.png"],
    ["3. Targeted proposal", "Finance Leadership & CFO Advisory one-pager",
     "services/cfo.png"],
    ["3. Targeted proposal", "Operations & Growth one-pager",
     "services/operations.png"],
    ["4. After discovery", "Engagement timeline / roadmap",
     "marketing/timeline.png"],
    ["5. After project discussion", "Fee structure & engagement options",
     "marketing/feestructure.png"],
], [1.7, 2.7, 2.1]))
story.append(Paragraph(
    "Supporting items: Vistaprint business cards (curved navy/blue wave "
    "motif), branded email signature (name, title, three service areas, "
    "contact row). Recurring footer mantra across collateral: "
    "<b>“Clarity. Strategy. Execution. Results that matter.”</b> "
    "Recurring trust markers: practical insights, hands-on execution, "
    "measurable results, trusted partner.", body))

# ---------------- 7. DESIGN DIRECTION ----------------
story.append(Paragraph("7. Design Direction for the Mockups", h1))
story.append(hr())
story.append(Paragraph("From the June 10 client call", h3))
story.append(b("Establish <b>approachability for small businesses</b> while "
               "looking <b>professional/credible for big businesses</b>."))
story.append(b("Keep the IntiEdge Blue (#148EEA) and official palette."))
story.append(b("Use her existing logo. No emojis anywhere in the designs."))
story.append(Paragraph("Reference sites the designer (Stuart) likes", h3))
story.append(grid_table([
    ["Site", "What to take from it"],
    ["bcg.com/canada", "Bold editorial hero, confident typography, "
     "insight-led content hierarchy"],
    ["protiviti.com/ca-en", "Clean corporate polish, strong service "
     "taxonomy, calm blue palette"],
    ["slalom.com/us/en", "Warmer, human, photography-forward consulting "
     "feel - approachable end of the spectrum"],
    ["bain.com", "Premium restraint, results-first messaging, authoritative "
     "simplicity"],
], [1.7, 4.8]))
story.append(Paragraph("Mockup plan (agreed with Stuart, June 11)", h3))
story.append(b("10 distinct homepage styles, delivered as self-contained "
               "HTML files."))
story.append(b("Official palette anchors every style; structure and layout "
               "MAY vary per style (confirmed: structural variation "
               "allowed)."))
story.append(b("Range deliberately spans corporate-formal to warm-"
               "approachable so Shelly can pick where on the spectrum "
               "IntiEdge sits."))

# ---------------- 8. GAPS ----------------
story.append(Paragraph("8. Open Questions, Gaps & Risks", h1))
story.append(hr())
story.append(Paragraph("To confirm with Shelly", h3))
story.append(b("Online payments: in scope for v1? (Raised with a question "
               "mark in discovery notes; invoices currently go to the "
               "company.)"))
story.append(b("Testimonials: she wants them, but none exist in the files "
               "yet - need 2-3 client quotes, even informal ones."))
story.append(b("Booking mechanics: which calendar tool for \"Book a "
               "Discovery Call\" (Calendly, MS Bookings, etc.)?"))
story.append(b("Domain/email: intiedge.com is referenced everywhere - "
               "confirm it is registered and where DNS/hosting will live."))
story.append(b("Publish pricing or keep it sales-collateral only? Collateral "
               "sequence implies keeping it off the public site."))
story.append(b("Name presentation: resumes say \"Shelly Nasution-Moffat\"; "
               "brand materials say \"Shelly Moffat.\" Confirm public name."))
story.append(b("\"10+ solutions\" and \"general industry... contract\" in "
               "the handwritten notes are ambiguous - clarify on next call."))
story.append(Paragraph("Asset gaps / risks", h3))
story.append(b("Logo file is low-resolution PNG on an off-white background "
               "- no vector (SVG/AI) or transparent version supplied. "
               "Recommend recreating as SVG before launch."))
story.append(b("Both headshots appear AI-generated or heavily retouched and "
               "differ from each other; for a trust-based personal brand, a "
               "real photo session is strongly recommended."))
story.append(b("No favicon, no social/OG images, no case studies, no "
               "written client results yet."))
story.append(b("She \"doesn't know her audience\" yet (discovery notes) - "
               "the dual-audience design must avoid splitting focus so much "
               "that neither audience converts."))

story.append(Spacer(1, 18))
story.append(hr())
story.append(Paragraph(
    "Sources: IntiEdge Folder Contents.pdf; branding/website.docx (brand & "
    "website playbook); notes/meetingnotes.jpeg (handwritten discovery "
    "notes); brochures/executive.docx + smallbusiness.docx; services/*.png; "
    "marketing/feestructure.png + timeline.png + cards + signature; "
    "resumes/strategy.pdf, finance.pdf, operations.pdf, purpose.pdf; "
    "photos/*; client call June 10, 2026.", small))

doc = SimpleDocTemplate(OUT, pagesize=letter,
                        leftMargin=0.75 * inch, rightMargin=0.75 * inch,
                        topMargin=0.75 * inch, bottomMargin=0.75 * inch,
                        title="IntiEdge Website Project Notes",
                        author="Stuart Fong")
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print("Wrote", OUT)
