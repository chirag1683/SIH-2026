import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_methodology_flowchart(output_path="d:/SIH 2026/methodology_flowchart.png"):
    # 16:9 aspect ratio at high DPI
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor('#0B132B') # Dark navy background
    ax.set_facecolor('#0B132B')

    # Turn off axes
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    # Color Palette
    C_BLUE_TOP   = '#1C2541'
    C_CARD_BG    = '#162238'
    C_CYAN       = '#00F0FF'
    C_TEAL       = '#38BDF8'
    C_GOLD       = '#F59E0B'
    C_GREEN      = '#10B981'
    C_PURPLE     = '#818CF8'
    C_TEXT_MAIN  = '#F8FAFC'
    C_TEXT_MUTED = '#94A3B8'
    C_BORDER     = '#334155'

    # Title Banner
    ax.text(50, 95.5, "UDAN-STAT: END-TO-END METHODOLOGY & IMPLEMENTATION PIPELINE",
            ha='center', va='center', fontsize=18, fontweight='bold', color=C_CYAN, fontfamily='sans-serif')
    ax.text(50, 92.5, "Ministry of Civil Aviation (MoCA) & DGCA Sovereign Regulatory Intelligence Architecture",
            ha='center', va='center', fontsize=11, color=C_TEXT_MUTED, fontfamily='sans-serif')

    # Define 5 Pipeline Stages (Columns)
    stages = [
        {
            "num": "STAGE 01",
            "title": "MULTI-SOURCE INGESTION",
            "color": C_TEAL,
            "x": 3, "w": 17,
            "items": [
                ("Live Scraping Engine", "80 Scheduled Corridors\n5 Horizons (T+1 to T+45)"),
                ("DGCA Statistics", "Monthly Form A & B\nCity-Pair Pax Weights (wr)"),
                ("MoPNG ATF Feeds", "Daily Aviation Fuel Prices\nRefinery & Tax Indices"),
                ("Airport Geodesics", "Verified AAI Lat/Long\nGreat-Circle GPS Coordinates")
            ]
        },
        {
            "num": "STAGE 02",
            "title": "IQR SANITIZATION",
            "color": C_GOLD,
            "x": 22.5, "w": 17,
            "items": [
                ("Flight Normalization", "Origin, Dest, Carrier,\nFlight #, Cabin Class"),
                ("Statistical IQR Filter", "Lower: Q1 - 1.5·IQR\nUpper: Q3 + 1.5·IQR"),
                ("Noise Elimination", "Flash Sales Trimming &\nPredatory Surge Isolation"),
                ("Representative Median", "Pr,t Robust Median Pricing\nEliminates Single-Seat Skew")
            ]
        },
        {
            "num": "STAGE 03",
            "title": "ANALYTICAL ENGINES",
            "color": C_PURPLE,
            "x": 42, "w": 18.5,
            "items": [
                ("Modified Laspeyres", "APIxt = Σ [wr × (Pr,t/Pr,0)]\nBase: Sept 2022 = 100.00"),
                ("UDAN RCS Cap Auditor", "Haversine Distance (km)\nTiered Caps (₹2,250–₹5,800)"),
                ("VGF Clawback Engine", "Viability Gap Subsidy\nClawback Penalty Calc"),
                ("HHI Antitrust & ATF", "Market Herfindahl (HHI)\nFuel Elasticity (η=0.55–0.80)")
            ]
        },
        {
            "num": "STAGE 04",
            "title": "PERSISTENCE & API",
            "color": C_GREEN,
            "x": 63, "w": 16.5,
            "items": [
                ("SQLAlchemy ORM", "PostgreSQL Enterprise &\nPortable SQLite Storage"),
                ("Relational Schema", "raw_fares, rep_fares,\nroute_weights, rcs_audit"),
                ("FastAPI REST Engine", "Asynchronous ASGI Server\n< 45ms Query Latency"),
                ("OpenAPI Specs", "Automated Swagger Docs\n& Export Data Feeds")
            ]
        },
        {
            "num": "STAGE 05",
            "title": "REGULATORY COCKPIT",
            "color": C_CYAN,
            "x": 82, "w": 15.5,
            "items": [
                ("React 19 + Vite HUD", "Interactive Sovereign UI\n4 Glassmorphic Themes"),
                ("Plotly Visualizations", "Cap vs Fare Step Chart &\nHorizon Dynamic Curves"),
                ("DGCA Show-Cause", "1-Click Formal Notice\nCiting Rule 135 (1937)"),
                ("Executive Dossiers", "Official CSV Audit Report\n& MoCA Brief Export")
            ]
        }
    ]

    for stage in stages:
        sx = stage["x"]
        sw = stage["w"]
        col = stage["color"]

        # Stage Header Box
        hdr_rect = patches.FancyBboxPatch((sx, 83), sw, 6.5, boxstyle="round,pad=0.5,rounding_size=1.2",
                                          edgecolor=col, facecolor='#111C35', linewidth=1.5)
        ax.add_patch(hdr_rect)

        ax.text(sx + sw/2, 87.2, stage["num"], ha='center', va='center', fontsize=9, fontweight='bold', color=col)
        ax.text(sx + sw/2, 84.8, stage["title"], ha='center', va='center', fontsize=10, fontweight='bold', color=C_TEXT_MAIN)

        # Stage Column Container
        body_rect = patches.FancyBboxPatch((sx, 8), sw, 73, boxstyle="round,pad=0.5,rounding_size=1.2",
                                           edgecolor=C_BORDER, facecolor=C_CARD_BG, linewidth=1.0)
        ax.add_patch(body_rect)

        # Draw Cards inside stage
        card_y = 66
        for title, desc in stage["items"]:
            # Small item card
            c_rect = patches.FancyBboxPatch((sx + 0.8, card_y), sw - 1.6, 13.5,
                                            boxstyle="round,pad=0.4,rounding_size=1.0",
                                            edgecolor=col if "Auditor" in title or "Laspeyres" in title or "IQR" in title else '#24344D',
                                            facecolor='#0D182A', linewidth=1.2 if ("Auditor" in title or "Laspeyres" in title) else 0.8)
            ax.add_patch(c_rect)

            ax.text(sx + sw/2, card_y + 10.5, title, ha='center', va='center',
                    fontsize=9.5, fontweight='bold', color=C_TEXT_MAIN)
            ax.text(sx + sw/2, card_y + 5.2, desc, ha='center', va='center',
                    fontsize=8.2, color=C_TEXT_MUTED, multialignment='center')

            card_y -= 15.5

    # Connect Stages with Flow Arrows
    arrow_points = [
        (20.3, 45, 22.2, 45),
        (39.8, 45, 41.7, 45),
        (60.8, 45, 62.7, 45),
        (79.8, 45, 81.7, 45)
    ]
    for x1, y1, x2, y2 in arrow_points:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(facecolor=C_CYAN, edgecolor=C_CYAN, width=2.5, headwidth=8, shrink=0.05))

    # Bottom Legend / Statutory Anchor Box
    bot_rect = patches.FancyBboxPatch((3, 1.5), 94.5, 5, boxstyle="round,pad=0.4,rounding_size=0.8",
                                      edgecolor=C_CYAN, facecolor='#0B1E3B', linewidth=1.2)
    ax.add_patch(bot_rect)

    statutory_text = "STATUTORY & REGULATORY ANCHOR: Rule 135, Aircraft Rules (1937) • National Civil Aviation Policy (NCAP 2016) • UDAN RCS Gazette Notifications • Survey of India Sovereign Cartography"
    ax.text(50, 4.0, statutory_text, ha='center', va='center', fontsize=9.5, fontweight='bold', color=C_CYAN)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Flowchart successfully generated and saved to: {output_path}")

if __name__ == "__main__":
    draw_methodology_flowchart()
