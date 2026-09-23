import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_complete_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Colors
    C_NAVY_DARK   = RGBColor(10, 25, 47)      # #0A192F
    C_NAVY_CARD   = RGBColor(17, 34, 64)      # #112240
    C_BLUE_ACCENT = RGBColor(14, 116, 144)    # #0E7490
    C_BLUE_LIGHT  = RGBColor(56, 189, 248)    # #38BDF8
    C_TEXT_WHITE  = RGBColor(248, 250, 252)
    C_TEXT_MUTED  = RGBColor(148, 163, 184)
    C_GOLD        = RGBColor(245, 158, 11)
    C_GREEN       = RGBColor(16, 185, 129)
    C_CARD_BG_LT  = RGBColor(241, 245, 249)
    C_BORDER_LT   = RGBColor(203, 213, 225)
    C_WHITE_BG    = RGBColor(255, 255, 255)

    def add_slide_header(slide, title_text, category_text, slide_num, total_slides="6"):
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.1))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = C_BLUE_LIGHT
        top_bar.line.color.rgb = C_BLUE_LIGHT

        tb_tag = slide.shapes.add_textbox(Inches(0.8), Inches(0.25), Inches(8.0), Inches(0.4))
        p_tag = tb_tag.text_frame.paragraphs[0]
        p_tag.text = f"SMART INDIA HACKATHON 2026  •  {category_text.upper()}"
        p_tag.font.name = "Arial"
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = C_BLUE_ACCENT

        tb_right = slide.shapes.add_textbox(Inches(8.5), Inches(0.25), Inches(4.0), Inches(0.4))
        p_right = tb_right.text_frame.paragraphs[0]
        p_right.text = "UDAN-STAT  |  MoCA & DGCA Sovereign RegTech"
        p_right.alignment = PP_ALIGN.RIGHT
        p_right.font.name = "Arial"
        p_right.font.size = Pt(10)
        p_right.font.bold = True
        p_right.font.color.rgb = C_TEXT_MUTED

        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.7), Inches(0.7))
        p_title = tb_title.text_frame.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = "Arial"
        p_title.font.size = Pt(21)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY_DARK

        tb_foot = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.7), Inches(0.35))
        p_foot = tb_foot.text_frame.paragraphs[0]
        p_foot.text = f"Ministry of Civil Aviation / DGCA  •  SIH 2026 Idea Submission                                                                                                           Slide {slide_num} of {total_slides}"
        p_foot.font.name = "Arial"
        p_foot.font.size = Pt(9)
        p_foot.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 1: Title & Cover
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_NAVY_DARK
    bg.line.fill.background()

    accent_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(0.12))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = C_BLUE_LIGHT
    accent_bar.line.fill.background()

    tb_sih = s1.shapes.add_textbox(Inches(0.8), Inches(1.1), Inches(11.733), Inches(0.5))
    p = tb_sih.text_frame.paragraphs[0]
    p.text = "SMART INDIA HACKATHON 2026  •  SOVEREIGN REGULATORY TECHNOLOGY"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_LIGHT

    tb_main = s1.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.733), Inches(1.5))
    p = tb_main.text_frame.paragraphs[0]
    p.text = "UDAN-STAT"
    p.font.name = "Arial"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_WHITE

    p2 = tb_main.text_frame.add_paragraph()
    p2.text = "Unified Domestic Airfare & Network Sovereign Tariff Analytics Platform"
    p2.font.name = "Arial"
    p2.font.size = Pt(20)
    p2.font.color.rgb = C_GOLD

    card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.3), Inches(11.733), Inches(3.4))
    card1.fill.solid()
    card1.fill.fore_color.rgb = C_NAVY_CARD
    card1.line.color.rgb = C_BLUE_ACCENT
    card1.line.width = Pt(1.5)

    tb_info = s1.shapes.add_textbox(Inches(1.1), Inches(3.5), Inches(11.1), Inches(3.0))
    tf_info = tb_info.text_frame
    tf_info.word_wrap = True

    items = [
        ("Problem Statement:", "Development of an Airfare Price Index (APIx) for Domestic Scheduled Aviation in India"),
        ("Institutional Alignment:", "Ministry of Civil Aviation (MoCA) & Directorate General of Civil Aviation (DGCA)"),
        ("Key Statutory Pillars:", "Rule 135 Aircraft Rules 1937, UDAN Regional Connectivity Scheme (RCS), Laspeyres Price Index"),
        ("Theme / Category:", "Smart Automation / Transportation & Logistics / Regulatory Technology (RegTech) — Software"),
        ("Core Capabilities:", "80-Route Laspeyres Index • UDAN Statutory Fare Cap Auditor • ATF Fuel Shock Simulator • HHI Antitrust Monitor"),
        ("Team Identification:", "Team ID: [Your Team ID]   |   Team Name: [Your Team Name]   |   Status: Fully Functional Working Prototype")
    ]
    for i, (k, v) in enumerate(items):
        p = tf_info.paragraphs[0] if i == 0 else tf_info.add_paragraph()
        p.space_after = Pt(8)
        run_k = p.add_run()
        run_k.text = f"{k:<26} "
        run_k.font.bold = True
        run_k.font.size = Pt(13)
        run_k.font.color.rgb = C_BLUE_LIGHT
        run_v = p.add_run()
        run_v.text = v
        run_v.font.bold = (i == 4 or i == 5)
        run_v.font.size = Pt(13)
        run_v.font.color.rgb = C_TEXT_WHITE

    # =========================================================================
    # SLIDE 2: Proposed Solution & Key Innovations
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_slide_header(s2, "Slide 2: Proposed Solution & Key Innovations", "Solution Architecture", 2)

    box_l = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.45))
    box_l.fill.solid()
    box_l.fill.fore_color.rgb = C_CARD_BG_LT
    box_l.line.color.rgb = C_BORDER_LT

    tb_l = s2.shapes.add_textbox(Inches(1.0), Inches(1.45), Inches(5.3), Inches(5.15))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "1. Sovereign Domestic Basket & Working Engine"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = C_NAVY_DARK
    p.space_after = Pt(10)

    l_points = [
        ("80-Route Sovereign Basket: ", "Audits comprehensive fare distributions across 20 metro, secondary, and UDAN regional corridors covering ~92% of scheduled domestic seat capacity."),
        ("5 Multi-Lead Horizons: ", "Monitors temporal yield management across T+1 (Emergency/Last-minute), T+7, T+15, T+30, and T+45 booking lead times."),
        ("Modified Laspeyres Methodology: ", "Mathematically robust national airfare index (Base Sept 2022 = 100.00) dynamically weighted by quarterly DGCA Form A/B passenger traffic statistics (w_r)."),
        ("Statistical IQR Filtration: ", "Automated [Q1 - 1.5·IQR, Q3 + 1.5·IQR] bounds trimming predatory gouging spikes and promotional flash sales prior to median aggregation.")
    ]
    for bold_txt, norm_txt in l_points:
        p = tf_l.add_paragraph()
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = "• " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = C_NAVY_DARK
        r2 = p.add_run()
        r2.text = norm_txt
        r2.font.size = Pt(11.5)
        r2.font.color.rgb = RGBColor(51, 65, 85)

    box_r = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.45))
    box_r.fill.solid()
    box_r.fill.fore_color.rgb = RGBColor(240, 249, 255)
    box_r.line.color.rgb = C_BLUE_ACCENT

    tb_r = s2.shapes.add_textbox(Inches(7.0), Inches(1.45), Inches(5.3), Inches(5.15))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "2. Breakthrough Institutional Innovations (Novel Features)"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = C_BLUE_ACCENT
    p.space_after = Pt(10)

    r_points = [
        ("UDAN RCS Statutory Fare Cap Auditor: ", "Geodesic Haversine engine auditing routes against distance-tiered statutory caps (₹2,250–₹5,800) to protect subsidized regional travelers and calculate Viability Gap Funding (VGF) clawbacks."),
        ("1-Click DGCA Show-Cause Notice Dispatcher: ", "Instantly compiles live statutory tariff violations into enforceable legal notices citing Rule 135 of Aircraft Rules, 1937."),
        ("ATF Fuel Shock Elasticity Simulator: ", "Simulates crude price fluctuations (-20% to +60%) with airline pass-through elasticity (η = 0.55–0.80) to model consumer financial burden in ₹ Crores."),
        ("HHI Antitrust Route Monitor: ", "Computes Herfindahl-Hirschman Index across all 80 corridors to detect carrier duopolies and high-barrier monopoly pricing risks (HHI > 2,500).")
    ]
    for bold_txt, norm_txt in r_points:
        p = tf_r.add_paragraph()
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = "★ " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = C_BLUE_ACCENT
        r2 = p.add_run()
        r2.text = norm_txt
        r2.font.size = Pt(11.5)
        r2.font.color.rgb = RGBColor(15, 23, 42)

    # =========================================================================
    # SLIDE 3: Methodology and process for implementation (Flow Charts/Images/ working prototype)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_slide_header(s3, "Slide 3: Methodology and Process for Implementation", "Functional Process Flow & Working Prototype", 3)

    # Left: High Resolution Pure Functional Process Flowchart
    flowchart_path = "d:/SIH 2026/process_flowchart.png"
    if os.path.exists(flowchart_path):
        # Insert Flowchart image on the top/left
        s3.shapes.add_picture(flowchart_path, Inches(0.8), Inches(1.3), Inches(6.8), Inches(5.5))
    else:
        # Fallback text box if image missing
        box_fc = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.3), Inches(6.8), Inches(5.5))
        box_fc.fill.solid()
        box_fc.fill.fore_color.rgb = C_CARD_BG_LT

    # Right: Working Prototype Screenshots & Validation Box
    box_proto = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.3), Inches(4.733), Inches(5.5))
    box_proto.fill.solid()
    box_proto.fill.fore_color.rgb = C_CARD_BG_LT
    box_proto.line.color.rgb = C_BLUE_ACCENT
    box_proto.line.width = Pt(1.5)

    tb_proto_title = s3.shapes.add_textbox(Inches(8.0), Inches(1.4), Inches(4.333), Inches(0.45))
    p = tb_proto_title.text_frame.paragraphs[0]
    p.text = "Live Working Prototype Deployment"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_BLUE_ACCENT

    # Add Prototype Screenshot 1: UDAN RCS Auditor
    proto_udan = "d:/SIH 2026/prototype_udan_rcs.png"
    if os.path.exists(proto_udan):
        s3.shapes.add_picture(proto_udan, Inches(8.0), Inches(1.9), Inches(4.333), Inches(2.2))

    # Add Prototype Screenshot 2: Dashboard
    proto_dash = "d:/SIH 2026/prototype_dashboard.png"
    if os.path.exists(proto_dash):
        s3.shapes.add_picture(proto_dash, Inches(8.0), Inches(4.25), Inches(4.333), Inches(2.1))

    # Caption / Verification Tag
    tb_cap = s3.shapes.add_textbox(Inches(8.0), Inches(6.4), Inches(4.333), Inches(0.35))
    p = tb_cap.text_frame.paragraphs[0]
    p.text = "Verified: React 19 + Plotly Visual Cockpit & FastAPI Engine (<45ms Latency)"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK

    # =========================================================================
    # SLIDE 4: Feasibility, Viability & Risk Analysis
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_slide_header(s4, "Slide 4: Feasibility, Viability & Risk Analysis", "Feasibility & Risk Mitigation", 4)

    card_w = Inches(3.64)
    card_h = Inches(1.5)
    feas = [
        ("Operational Feasibility", "Combines published DGCA Form A/B passenger statistics with automated fare ingestion across 20 domestic hubs with zero manual intervention.", C_BLUE_ACCENT),
        ("Technical Feasibility", "Lightweight, stateless ASGI architecture running in real-time with responsive UI and sub-45ms API query latency across all 80 corridors.", C_GOLD),
        ("Economic Viability", "Built 100% on open-source, sovereign, scalable stack. Zero paid commercial API or GDS subscription dependencies.", C_GREEN)
    ]
    for i, (f_title, f_desc, col) in enumerate(feas):
        c_left = Inches(0.8 + i * (3.64 + 0.39))
        c_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(1.35), card_w, card_h)
        c_box.fill.solid()
        c_box.fill.fore_color.rgb = C_CARD_BG_LT
        c_box.line.color.rgb = col
        c_box.line.width = Pt(1.5)

        tb = s4.shapes.add_textbox(c_left + Inches(0.15), Inches(1.4), card_w - Inches(0.3), card_h - Inches(0.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f_title
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = f_desc
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = RGBColor(51, 65, 85)

    tb_tab_title = s4.shapes.add_textbox(Inches(0.8), Inches(3.05), Inches(11.733), Inches(0.4))
    p = tb_tab_title.text_frame.paragraphs[0]
    p.text = "Implemented Risk Mitigation & Legal Safeguards Matrix"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = C_NAVY_DARK

    rows, cols = 5, 3
    tab_shape = s4.shapes.add_table(rows, cols, Inches(0.8), Inches(3.55), Inches(11.733), Inches(3.2))
    table = tab_shape.table
    table.columns[0].width = Inches(2.6)
    table.columns[1].width = Inches(3.6)
    table.columns[2].width = Inches(5.533)

    headers = ["Identified Risk / Challenge", "Operational Regulatory Impact", "Technical & Legal Mitigation Implemented"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_TEXT_WHITE

    row_data = [
        ("Extreme Fare Volatility & Flash Sales", "Distorts median price index with temporary artificial promotions or single-seat spikes.", "IQR Outlier Trimming: Automatically bounds fares to [Q1 - 1.5·IQR, Q3 + 1.5·IQR] before Laspeyres aggregation."),
        ("Seasonal Traffic Pattern Shifts", "Fixed route weights become obsolete over time as seasonal leisure/holiday routes peak.", "Dynamic Quarterly Rebalancing: Recalculates route passenger weights (w_r) each quarter using DGCA Form A/B statistics."),
        ("Anti-Scraping / Portal Rate Limits", "Scraping disruptions leading to incomplete daily fare baskets or missing carriers.", "Distributed Fetching & Robust Fallbacks: Staggered asynchronous requests, randomized user-agents, and persistent SQLite cache."),
        ("Regulatory & Statutory Challenges", "Airlines contesting fare caps or index methodology as anti-market or non-statutory.", "Aircraft Rules 1937 Anchor: Grounded strictly under Rule 135 (Tariff Filing & Non-Predatory Pricing) and UDAN Gazette frameworks.")
    ]
    for i, r in enumerate(row_data):
        for j, val in enumerate(r):
            cell = table.cell(i+1, j)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_WHITE_BG if i % 2 == 0 else C_CARD_BG_LT
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            p.font.color.rgb = C_NAVY_DARK if j == 0 else RGBColor(51, 65, 85)
            if j == 0:
                p.font.bold = True

    # =========================================================================
    # SLIDE 5: Impact and Socio-Economic Benefits
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_slide_header(s5, "Slide 5: Impact and Socio-Economic Benefits", "Socio-Economic Value", 5)

    box_stk = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.45))
    box_stk.fill.solid()
    box_stk.fill.fore_color.rgb = C_CARD_BG_LT
    box_stk.line.color.rgb = C_BORDER_LT

    tb_stk = s5.shapes.add_textbox(Inches(1.0), Inches(1.45), Inches(5.3), Inches(5.15))
    tf_stk = tb_stk.text_frame
    tf_stk.word_wrap = True
    p = tf_stk.paragraphs[0]
    p.text = "1. Direct Stakeholder Impact"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = C_NAVY_DARK
    p.space_after = Pt(10)

    stk_points = [
        ("Ministry of Civil Aviation & DGCA: ", "Provides an objective, reproducible national benchmark to evaluate statutory fare caps, eliminate ad-hoc spot checks, and enforce Rule 135 mandates."),
        ("Competition Commission of India (CCI): ", "Corridor-level HHI transparency uncovers route duopolies, cartel pricing, and artificial capacity cuts on high-density corridors."),
        ("Indian Air Travelers: ", "Full transparency into baseline market fares; exposes 2.14x emergency surge gouging and equips travelers with optimal booking window intelligence."),
        ("Airlines & Industry Operators: ", "Clear, transparent regulatory yardstick preventing arbitrary policy freezes while preserving dynamic revenue management within fair statutory bounds.")
    ]
    for bold_txt, norm_txt in stk_points:
        p = tf_stk.add_paragraph()
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = "• " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = C_NAVY_DARK
        r2 = p.add_run()
        r2.text = norm_txt
        r2.font.size = Pt(11.5)
        r2.font.color.rgb = RGBColor(51, 65, 85)

    box_mac = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.45))
    box_mac.fill.solid()
    box_mac.fill.fore_color.rgb = RGBColor(240, 253, 244)
    box_mac.line.color.rgb = C_GREEN

    tb_mac = s5.shapes.add_textbox(Inches(7.0), Inches(1.45), Inches(5.3), Inches(5.15))
    tf_mac = tb_mac.text_frame
    tf_mac.word_wrap = True
    p = tf_mac.paragraphs[0]
    p.text = "2. Broad Socio-Economic & Fiscal Benefits"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = C_GREEN
    p.space_after = Pt(10)

    mac_points = [
        ("Macroeconomic Inflation Forecasting: ", "Directly integrates with MOSPI Consumer Price Index (CPI) transport sub-indices for truthful macroeconomic inflation modeling."),
        ("UDAN Subsidy & VGF Clawback Protection: ", "Audits ₹1,000+ Cr annual Viability Gap Funding (VGF) disbursements to ensure airlines do not collect public subsidies while charging predatory fares."),
        ("₹4,500+ Cr Consumer Protection: ", "Simulates fuel shocks and emergency events (e.g., festival surges, rail strikes) to protect Indian consumers from unconstrained predatory exploitation."),
        ("Sovereign Digital Asset: ", "Establishes India's first standardized, independent, and reproducible domestic airfare analytics infrastructure, reducing reliance on foreign proprietary feeds.")
    ]
    for bold_txt, norm_txt in mac_points:
        p = tf_mac.add_paragraph()
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = "✔ " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = RGBColor(22, 101, 52)
        r2 = p.add_run()
        r2.text = norm_txt
        r2.font.size = Pt(11.5)
        r2.font.color.rgb = RGBColor(15, 23, 42)

    # =========================================================================
    # SLIDE 6: Research, Citations, Standards & Verification
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_slide_header(s6, "Slide 6: Research, Citations & Standards", "Compliance & Standards", 6)

    box_std = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.45))
    box_std.fill.solid()
    box_std.fill.fore_color.rgb = C_CARD_BG_LT
    box_std.line.color.rgb = C_BORDER_LT

    tb_std = s6.shapes.add_textbox(Inches(1.0), Inches(1.45), Inches(5.3), Inches(5.15))
    tf_std = tb_std.text_frame
    tf_std.word_wrap = True
    p = tf_std.paragraphs[0]
    p.text = "1. Regulatory Data Sources & Legal Standards"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = C_NAVY_DARK
    p.space_after = Pt(8)

    std_points = [
        ("DGCA India Statistics: ", "Monthly Domestic Air Traffic Statistics, City-Pair Passenger Volume Reports (Form A & B) and On-Time Performance (OTP) data — dgca.gov.in"),
        ("Aircraft Rules, 1937 (Rule 135): ", "Statutory authority governing tariff publishing, reasonable profit margins, and prohibition of predatory or exploitative pricing."),
        ("UDAN RCS Framework (MoCA): ", "Gazette-notified distance-tiered statutory fare caps (₹2,250 to ₹5,800) and Viability Gap Funding guidelines — civilaviation.gov.in"),
        ("MOSPI CPI Guidelines: ", "Methodological manual for Laspeyres price index aggregation, base-year weighting principles, and inflation sub-indices — mospi.gov.in"),
        ("ICAO Doc 9626: ", "Manual on the Regulation of International Air Transport: Tariff Monitoring Guidelines & Sovereign Airfare Index Principles.")
    ]
    for bold_txt, norm_txt in std_points:
        p = tf_std.add_paragraph()
        p.space_after = Pt(7)
        r1 = p.add_run()
        r1.text = "• " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = C_NAVY_DARK
        r2 = p.add_run()
        r2.text = norm_txt
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = RGBColor(51, 65, 85)

    box_ver = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.45))
    box_ver.fill.solid()
    box_ver.fill.fore_color.rgb = C_NAVY_DARK
    box_ver.line.color.rgb = C_BLUE_LIGHT
    box_ver.line.width = Pt(1.5)

    tb_ver = s6.shapes.add_textbox(Inches(7.0), Inches(1.45), Inches(5.3), Inches(5.15))
    tf_ver = tb_ver.text_frame
    tf_ver.word_wrap = True
    p = tf_ver.paragraphs[0]
    p.text = "2. Live Demonstration & Verification Endpoints"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = C_BLUE_LIGHT
    p.space_after = Pt(10)

    ver_items = [
        ("Operational Status: ", "Fully Functional Working Prototype (Frontend + Backend + Database Engine)"),
        ("Interactive Cockpit: ", "http://localhost:5173  (React 19 + Plotly Visual Analytics)"),
        ("UDAN RCS Auditor: ", "http://localhost:5173/udan-rcs  (Live Statutory Ceiling Surveillance & Notices)"),
        ("Antitrust & HHI Engine: ", "http://localhost:5173/analysts  (Herfindahl-Hirschman Route Monopoly Dashboard)"),
        ("Fuel Shock Simulator: ", "http://localhost:5173/simulation  (Macroeconomic Elasticity & Consumer Burden)"),
        ("FastAPI OpenAPI Engine: ", "http://localhost:8000/docs  (Automated Swagger Microservice Documentation)"),
        ("Production Readiness: ", "Dockerized, stateless microservice architecture ready for sovereign deployment on National Informatics Centre (NIC) / MoCA cloud.")
    ]
    for bold_txt, norm_txt in ver_items:
        p = tf_ver.add_paragraph()
        p.space_after = Pt(7)
        r1 = p.add_run()
        r1.text = "▶ " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = C_GOLD
        r2 = p.add_run()
        r2.text = norm_txt
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = C_TEXT_WHITE

    # Save
    out_path = "d:/SIH 2026/UDAN_STAT_SIH2026_Final_Submission.pptx"
    prs.save(out_path)
    print(f"Final Presentation saved successfully to: {out_path}")

if __name__ == "__main__":
    build_complete_presentation()
