import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_clean_process_flowchart(output_path="d:/SIH 2026/process_flowchart.png"):
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor('#060B18') # Sovereign Deep Slate/Navy
    ax.set_facecolor('#060B18')
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    # Color Palette
    C_TITLE     = '#38BDF8' # Sky Blue
    C_CARD_BG   = '#0F1A30' # Card Base
    C_BORDER    = '#1E3A8A' # Blue Border
    C_CYAN      = '#00F0FF'
    C_DEC_BG    = '#2D154B' # Decision Diamond
    C_DEC_BORDER= '#C084FC'
    C_GREEN     = '#10B981' # Yes / Compliant
    C_RED       = '#EF4444' # No / Outlier / Breach
    C_GOLD      = '#F59E0B' # Regional Warning
    C_TEXT      = '#F8FAFC'
    C_MUTED     = '#94A3B8'

    # Title Header
    ax.text(50, 97, "METHODOLOGY & OPERATIONAL PROCESS FLOW CHART",
            ha='center', va='center', fontsize=17, fontweight='bold', color=C_CYAN)
    ax.text(50, 94.2, "How UDAN-STAT Works: Step-by-Step Data Flow, Statistical Sanitization & Statutory Enforcement",
            ha='center', va='center', fontsize=10.5, color=C_MUTED)

    # Helper: Box
    def draw_box(x, y, w, h, title, subtitle="", border_col=C_BORDER, bg_col=C_CARD_BG, font_sz=9.5, sub_sz=7.8):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.25,rounding_size=0.5",
                                      edgecolor=border_col, facecolor=bg_col, linewidth=1.4)
        ax.add_patch(rect)
        if subtitle:
            ax.text(x + w/2, y + h*0.64, title, ha='center', va='center', fontsize=font_sz, fontweight='bold', color=C_TEXT)
            ax.text(x + w/2, y + h*0.28, subtitle, ha='center', va='center', fontsize=sub_sz, color=C_MUTED, multialignment='center')
        else:
            ax.text(x + w/2, y + h/2, title, ha='center', va='center', fontsize=font_sz, fontweight='bold', color=C_TEXT, multialignment='center')

    # Helper: Diamond
    def draw_diamond(cx, cy, r_w, r_h, text, border_col=C_DEC_BORDER, bg_col=C_DEC_BG):
        pts = [[cx, cy + r_h], [cx + r_w, cy], [cx, cy - r_h], [cx - r_w, cy]]
        poly = patches.Polygon(pts, closed=True, edgecolor=border_col, facecolor=bg_col, linewidth=1.5)
        ax.add_patch(poly)
        ax.text(cx, cy, text, ha='center', va='center', fontsize=8.0, fontweight='bold', color=C_TEXT, multialignment='center')

    # Helper: Arrow
    def draw_arrow(x1, y1, x2, y2, color=C_TITLE, text="", text_offset_y=0.0, text_offset_x=0.0, fontsize=8.0):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(facecolor=color, edgecolor=color, width=1.4, headwidth=5.5, shrink=0.02))
        if text:
            mx, my = (x1 + x2) / 2 + text_offset_x, (y1 + y2) / 2 + text_offset_y
            ax.text(mx, my, text, ha='center', va='center', fontsize=fontsize, fontweight='bold', color=color)

    # =========================================================================
    # 1. TOP SECTION: DATA INGESTION & IQR FILTER (Y = 90 down to 59)
    # =========================================================================
    # 3 Raw Inputs
    draw_box(4, 85, 18, 6.5, "1. Live Flight Fares", "80 Corridors × 5 Horizons\n(T+1 to T+45 Booking Lead)", border_col='#0284C7')
    draw_box(24, 85, 18, 6.5, "2. DGCA Traffic Matrix", "Form A/B Passenger Volume\nQuarterly Weights (wr)", border_col='#0284C7')
    draw_box(44, 85, 18, 6.5, "3. Airport Coordinates", "Verified AAI GPS Lat/Long\nfor Geodesic Distance", border_col='#0284C7')

    # Converge into Step 1
    draw_box(68, 85, 28, 6.5, "Step 1: Normalization Engine", "Deduplicate by Flight #, Date, Origin/Dest,\nFilter strictly to Economy Cabin Class", border_col=C_CYAN)
    
    draw_arrow(22, 88.25, 24, 88.25)
    draw_arrow(42, 88.25, 44, 88.25)
    draw_arrow(62, 88.25, 68, 88.25)

    # Arrow Down to Step 2
    draw_arrow(82, 85, 82, 79)

    # Step 2: Compute IQR Distribution
    draw_box(68, 72.5, 28, 6.5, "Step 2: IQR Computation", "Calculate Q1 (25th %), Q3 (75th %),\nand IQR = Q3 - Q1 for Route Basket", border_col='#60A5FA')

    # Arrow Left to IQR Decision Diamond
    draw_arrow(68, 75.75, 54, 75.75)

    # Decision Diamond 1: Outlier Bounds
    draw_diamond(44, 75.75, 9.5, 4.0, "Is Fare within Bounds?\n[Q1 - 1.5·IQR,\nQ3 + 1.5·IQR]")

    # If NO -> Discard Outlier (arrow UP-LEFT)
    draw_arrow(44, 79.75, 44, 82.5, color=C_RED)
    draw_arrow(44, 82.5, 24, 82.5, color=C_RED, text="NO (Outlier)", text_offset_y=1.2, text_offset_x=2.5)
    draw_box(4, 79.5, 19, 5.0, "Discard Outlier Fare", "Strips Flash Promos & Predatory Gouges", border_col=C_RED, bg_col='#310F15')

    # If YES -> Step 3 Representative Median (arrow DOWN)
    draw_arrow(44, 71.75, 44, 66, color=C_GREEN, text="YES", text_offset_x=2.0)
    draw_box(28, 59.5, 32, 6.5, "Step 3: Representative Median Price P(r,t)", "Extracts Central Tendency Price for each Route & Horizon\nEliminates Single-Seat Pricing Distortion", border_col=C_GREEN)

    # Divider Line
    div_line = patches.Rectangle((4, 56.5), 92, 0.15, facecolor='#1E293B', edgecolor='none')
    ax.add_patch(div_line)
    ax.text(50, 57.5, "PARALLEL DUAL REGULATORY ENGINES", ha='center', va='center', fontsize=9.0, fontweight='bold', color='#64748B')

    # Arrow from Step 3 down to Split
    draw_arrow(44, 59.5, 44, 54.5)
    draw_arrow(44, 54.5, 24, 54.5)
    draw_arrow(44, 54.5, 74, 54.5)

    # =========================================================================
    # 2. BOTTOM LEFT: PIPELINE A - LASPEYRES PRICE INDEX (X: 4 to 46, Y = 52 to 5)
    # =========================================================================
    # Container Box for Left Column
    c_left = patches.FancyBboxPatch((4, 5), 44, 47, boxstyle="round,pad=0.3,rounding_size=0.6",
                                    edgecolor='#0284C7', facecolor='#0B1528', linewidth=1.2)
    ax.add_patch(c_left)
    ax.text(26, 49.5, "PIPELINE A: NATIONAL LASPEYRES PRICE INDEX", ha='center', va='center', fontsize=11, fontweight='bold', color=C_CYAN)

    draw_arrow(24, 54.5, 24, 47)

    draw_box(7, 39, 38, 7.5, "A1. Route Price Relatives & Weighting",
             "Calculate: Price Relative = P(r,t) / P(r,0)\nWeight by DGCA Passenger Traffic Share (w_r)", border_col='#0284C7')

    draw_arrow(26, 39, 26, 33)

    draw_box(7, 25, 38, 8.0, "A2. Modified Laspeyres Index Formula",
             "APIx_t = Σ [ w_r × ( P(r,t) / P(r,0) ) ] × 100\nBase Period Normalized: Sept 2022 = 100.00", border_col='#38BDF8')

    draw_arrow(26, 25, 26, 19)

    draw_box(7, 8, 38, 10.5, "A3. Sovereign Economic Intelligence Output",
             "• Multi-Horizon Trajectory (T+1 Last-minute vs T+45 Advance)\n• ATF Fuel Shock Elasticity Simulator (η = 0.55 - 0.80)\n• Seamless Data Feed for MOSPI CPI Transport Sub-Index", border_col=C_CYAN)

    # =========================================================================
    # 3. BOTTOM RIGHT: PIPELINE B - UDAN RCS STATUTORY COMPLIANCE (X: 52 to 96, Y = 52 to 5)
    # =========================================================================
    c_right = patches.FancyBboxPatch((52, 5), 44, 47, boxstyle="round,pad=0.3,rounding_size=0.6",
                                     edgecolor=C_GOLD, facecolor='#0B1528', linewidth=1.2)
    ax.add_patch(c_right)
    ax.text(74, 49.5, "PIPELINE B: UDAN RCS STATUTORY AUDITOR", ha='center', va='center', fontsize=11, fontweight='bold', color=C_GOLD)

    draw_arrow(74, 54.5, 74, 47)

    draw_box(55, 39.5, 38, 7.0, "B1. Haversine Geodesic Distance Engine",
             "Calculates Great-Circle Stage Length between Airports (km)\nMaps to MoCA Statutory Fare Cap Tier (₹2,250 to ₹5,800)", border_col=C_GOLD)

    draw_arrow(74, 39.5, 74, 34)

    # Decision Diamond 2: Actual Fare > Statutory Cap?
    draw_diamond(74, 30.5, 10.5, 3.5, "Actual Fare > Statutory Cap?\n( P(r,t) > Statutory_Cap )")

    # If NO -> Compliant (Left branch inside box)
    draw_arrow(63.5, 30.5, 55, 30.5, color=C_GREEN, text="NO", text_offset_y=1.0)
    draw_box(55, 20.5, 15, 7.5, "Tag: COMPLIANT", "Airfare within legal\nRCS distance ceiling", border_col=C_GREEN, bg_col='#05291B', font_sz=8.5, sub_sz=7.2)

    # If YES -> Breach (Right branch inside box)
    draw_arrow(84.5, 30.5, 87.5, 30.5, color=C_RED, text="YES", text_offset_y=1.0)
    draw_box(74, 20.5, 19, 7.5, "Tag: STATUTORY BREACH", "Excess = P(r,t) - Cap\nAssess VGF Subsidy Clawback", border_col=C_RED, bg_col='#310F15', font_sz=8.5, sub_sz=7.2)

    # From Breach down to DGCA Notice
    draw_arrow(83.5, 20.5, 83.5, 16.5)

    draw_box(55, 8, 38, 8.5, "B2. Regulatory Enforcement & Action",
             "★ 1-Click DGCA Show-Cause Notice citing Rule 135 (Aircraft Rules 1937)\n★ Live Corridor Audit Register & Downloadable MoCA CSV Dossier", border_col=C_RED, bg_col='#260B11')

    # Save
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Clean Process Flowchart successfully saved to: {output_path}")

if __name__ == "__main__":
    generate_clean_process_flowchart()
