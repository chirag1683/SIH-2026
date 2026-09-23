import os
from playwright.sync_api import sync_playwright

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>UDAN-STAT: Complete Dashboard & Feature Comprehensive Guide</title>
<style>
  @page {
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
    @bottom-right {
      content: counter(page);
    }
  }
  body {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    line-height: 1.55;
    font-size: 11pt;
    margin: 0;
    padding: 0;
  }
  .header-box {
    border-bottom: 3px solid #0284c7;
    padding-bottom: 12px;
    margin-bottom: 20px;
  }
  .tagline {
    font-size: 9pt;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #0284c7;
    text-transform: uppercase;
  }
  h1 {
    font-size: 24pt;
    color: #0f172a;
    margin: 4px 0 6px 0;
    font-weight: 800;
  }
  .subtitle {
    font-size: 13pt;
    color: #475569;
    font-weight: 500;
    margin-bottom: 10px;
  }
  .meta-badge-row {
    display: flex;
    gap: 10px;
    margin-top: 8px;
  }
  .badge {
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 8.5pt;
    font-weight: 600;
    color: #334155;
  }
  .badge-accent {
    background: #e0f2fe;
    border-color: #7dd3fc;
    color: #0369a1;
  }
  .badge-gold {
    background: #fef3c7;
    border-color: #fde68a;
    color: #92400e;
  }
  
  .section-card {
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 18px;
    background: #ffffff;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    page-break-inside: avoid;
  }
  .section-card.highlight {
    border-left: 4px solid #0284c7;
  }
  .section-card.gold-highlight {
    border-left: 4px solid #f59e0b;
    background: #fafaf9;
  }
  
  h2 {
    font-size: 14pt;
    color: #0f172a;
    margin: 0 0 8px 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .route-badge {
    font-size: 9pt;
    font-family: monospace;
    background: #0f172a;
    color: #38bdf8;
    padding: 2px 7px;
    border-radius: 4px;
    font-weight: normal;
  }
  
  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 8px;
  }
  .sub-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 10px 12px;
    border-radius: 6px;
  }
  .sub-box-title {
    font-size: 9.5pt;
    font-weight: 700;
    color: #0369a1;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
  }
  
  ul {
    margin: 4px 0 6px 0;
    padding-left: 18px;
  }
  li {
    margin-bottom: 4px;
    font-size: 9.8pt;
  }
  
  .jury-quote {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-left: 4px solid #16a34a;
    padding: 8px 12px;
    border-radius: 4px;
    margin-top: 10px;
    font-size: 9.5pt;
    color: #14532d;
  }
  .jury-quote strong {
    color: #15803d;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 9pt;
  }
  th {
    background: #0f172a;
    color: #ffffff;
    text-align: left;
    padding: 6px 10px;
    font-weight: 600;
  }
  td {
    padding: 6px 10px;
    border-bottom: 1px solid #e2e8f0;
  }
  tr:nth-child(even) td {
    background: #f8fafc;
  }

  .page-break {
    page-break-after: always;
  }
</style>
</head>
<body>

  <!-- COVER / HEADER -->
  <div class="header-box">
    <div class="tagline">Ministry of Civil Aviation (MoCA) & Directorate General of Civil Aviation (DGCA)</div>
    <h1>UDAN-STAT</h1>
    <div class="subtitle">Unified Domestic Airfare & Network Sovereign Tariff Analytics Platform</div>
    <div class="meta-badge-row">
      <span class="badge badge-accent">SIH 2026 Idea Submission</span>
      <span class="badge badge-gold">Complete System & Dashboard Dossier</span>
      <span class="badge">React 19 • FastAPI • SQLite/PostgreSQL</span>
      <span class="badge">Sub-45ms Verified Query Latency</span>
    </div>
  </div>

  <!-- EXECUTIVE SUMMARY -->
  <div class="section-card highlight">
    <h2>Executive Summary & System Purpose</h2>
    <p style="margin: 4px 0 8px 0; font-size: 10pt;">
      <strong>UDAN-STAT</strong> is a sovereign regulatory intelligence platform engineered for the Ministry of Civil Aviation (MoCA) and DGCA to eliminate regulatory blindspots in Indian domestic aviation. It replaces arbitrary manual spot-checks with an empirical, tamper-proof mathematical framework:
    </p>
    <ul>
      <li><strong>National Airfare Price Index:</strong> Modified Laspeyres index dynamically weighted by DGCA quarterly Form A/B passenger matrices across 80 scheduled domestic corridors covering ~92% scheduled capacity.</li>
      <li><strong>Statutory UDAN RCS Auditor:</strong> First-of-its-kind Geodesic distance auditor benchmarking regional fares against MoCA statutory caps (₹2,250 – ₹5,800) with 1-click Show-Cause Notice dispatching under Rule 135 of Aircraft Rules, 1937.</li>
      <li><strong>Antitrust & Macroeconomic Simulation:</strong> HHI monopoly detection and Aviation Turbine Fuel (ATF) shock elasticity modeling safeguarding ₹4,500+ Cr of consumer welfare.</li>
    </ul>
  </div>

  <!-- DASHBOARD 1 -->
  <div class="section-card">
    <h2>1. Executive Landing & Intelligence Overview <span class="route-badge">Route: /</span></h2>
    <p><strong>Primary Objective:</strong> Acts as the ministerial executive gate providing senior policymakers with an instantaneous 10-second pulse of national airfare inflation and surge velocity.</p>
    <div class="grid-2">
      <div class="sub-box">
        <div class="sub-box-title">Key Visual Components</div>
        <ul>
          <li><strong>Sovereign Flash KPIs:</strong> National Benchmark Index (124.50), 24h Surge Velocity, 80 Corridors, 92% Domestic Seat Capacity.</li>
          <li><strong>Multi-Horizon Carousel:</strong> Compares T+1 emergency pricing against T+30/T+45 advance purchase tiers.</li>
          <li><strong>Sovereign Module Grid:</strong> 7 direct navigational pathways into analytical sub-engines.</li>
        </ul>
      </div>
      <div class="sub-box">
        <div class="sub-box-title">Underlying Mechanics</div>
        <ul>
          <li>Aggregates weighted median pricing across all active carrier feeds.</li>
          <li>Translates complex statistical spreads into high-level ministerial alerts.</li>
        </ul>
      </div>
    </div>
    <div class="jury-quote">
      <strong>Jury Defense Line:</strong> "Sir, the Landing Cockpit replaces subjective complaints with an objective, real-time national indicator of domestic airfare inflation."
    </div>
  </div>

  <!-- DASHBOARD 2 -->
  <div class="section-card">
    <h2>2. National Airfare Price Index Calculator <span class="route-badge">Route: /dashboard</span></h2>
    <p><strong>Primary Objective:</strong> The computational core computing India's official weighted Laspeyres domestic airfare price index.</p>
    <div class="grid-2">
      <div class="sub-box">
        <div class="sub-box-title">Key Visual Components</div>
        <ul>
          <li><strong>Flight Control Panel:</strong> Cabin class filter (Economy / Business) and 5 Active Fleet toggles (6E, AI, SG, QP, IX).</li>
          <li><strong>Lead-Horizon Spreads:</strong> T+1 (+50.8%), T+7 (+24.5%), T+15 (+18.8%), T+30 (+11.5%), T+45 (+6.1%).</li>
          <li><strong>Plotly 30-Day Forward Trajectory:</strong> Historical vs forward price index projection against Base 100.00 parity.</li>
          <li><strong>Route Network Comparison:</strong> Metro trunks vs Tier-2 regional network indices.</li>
        </ul>
      </div>
      <div class="sub-box">
        <div class="sub-box-title">Mathematical Formula</div>
        <p style="font-family: monospace; font-size: 8.5pt; margin: 4px 0;">APIx_t = Σ [ w_r × ( P(r,t) / P(r,0) ) ] × 100</p>
        <p style="font-size: 8.5pt; color: #64748b;">Where w_r is DGCA quarterly passenger share, P(r,t) is clean median fare, and Base Sept 2022 = 100.00.</p>
      </div>
    </div>
    <div class="jury-quote">
      <strong>Jury Defense Line:</strong> "We do not take raw averages. The index is passenger-weighted via DGCA Form A/B so high-volume trunk routes accurately drive the macroeconomic score."
    </div>
  </div>

  <div class="page-break"></div>

  <!-- DASHBOARD 3 -->
  <div class="section-card">
    <h2>3. Mathematical & Statistical Methodology <span class="route-badge">Route: /methodology</span></h2>
    <p><strong>Primary Objective:</strong> Mathematical defense engine demonstrating data sanitization and proof against arithmetic mean skew.</p>
    <div class="grid-2">
      <div class="sub-box">
        <div class="sub-box-title">Key Visual Components</div>
        <ul>
          <li><strong>Interactive IQR Outlier Sanitizer:</strong> Live tool calculating Q1 (25th %), Q3 (75th %), IQR, and Upper Bound.</li>
          <li><strong>Mean vs Median Scatter Comparison:</strong> Proof showing how 1 predatory ₹18,500 ticket skews arithmetic mean by 42% while Median remains truthful.</li>
          <li><strong>80-Route Passenger Weight Ledger:</strong> Full DGCA normalized passenger share table (Σ w_r = 1.0).</li>
        </ul>
      </div>
      <div class="sub-box">
        <div class="sub-box-title">Two-Stage Statistical Defense</div>
        <ul>
          <li><strong>Stage 1:</strong> Trim unrepresentative fares outside [Q1 - 1.5·IQR, Q3 + 1.5·IQR].</li>
          <li><strong>Stage 2:</strong> Compute robust statistical median P(r,t) across clean distribution.</li>
        </ul>
      </div>
    </div>
    <div class="jury-quote">
      <strong>Jury Defense Line:</strong> "Sir, statistical IQR bounds eliminate promotional flash sales and predatory surge spikes before computing medians, guaranteeing mathematical integrity."
    </div>
  </div>

  <!-- DASHBOARD 4 -->
  <div class="section-card">
    <h2>4. Antitrust & HHI Monopoly Cockpit <span class="route-badge">Route: /analysts</span></h2>
    <p><strong>Primary Objective:</strong> Regulatory surveillance tool for the Competition Commission of India (CCI) to detect route monopolies and cartelization.</p>
    <div class="grid-2">
      <div class="sub-box">
        <div class="sub-box-title">Key Visual Components</div>
        <ul>
          <li><strong>Herfindahl-Hirschman (HHI) Scorecard:</strong> Color-coded market concentration status across 80 corridors.</li>
          <li><strong>Concentration Thresholds:</strong> &lt;1500 (Competitive), 1500-2500 (Moderate), &gt;2500 (High Monopoly Risk).</li>
          <li><strong>Duopoly Radar:</strong> Identifies corridors dominated by IndiGo + Air India (~90% combined market share).</li>
        </ul>
      </div>
      <div class="sub-box">
        <div class="sub-box-title">Regulatory Focus</div>
        <ul>
          <li>Flags artificial capacity throttling (ASKM drops) preceding holiday fare surges.</li>
          <li>Equips regulators to prevent predatory monopoly pricing.</li>
        </ul>
      </div>
    </div>
    <div class="jury-quote">
      <strong>Jury Defense Line:</strong> "HHI monitoring allows DGCA and CCI to proactively intervene on monopoly routes before passengers are subjected to exploitative pricing."
    </div>
  </div>

  <!-- DASHBOARD 5 -->
  <div class="section-card gold-highlight">
    <h2>5. UDAN RCS Statutory Fare Cap Compliance Auditor <span class="route-badge">Route: /udan-rcs</span></h2>
    <p><strong>Primary Objective:</strong> Flagship statutory engine monitoring regional corridors against distance-tiered legal fare caps mandated under the UDAN (Ude Desh Ka Aam Nagrik) Scheme.</p>
    
    <div class="grid-2">
      <div class="sub-box">
        <div class="sub-box-title">Key Features & Metrics</div>
        <ul>
          <li><strong>4 Regulatory KPIs:</strong> Monitored Corridors (62), Statutory Compliance Rate (%), Active Breaches Count, Total Excess Surcharge (₹1,76,738+).</li>
          <li><strong>Plotly Step-Line Chart:</strong> MoCA distance ceiling step-line vs live observed carrier airfares.</li>
          <li><strong>VGF Clawback Estimator:</strong> Calculates public subsidy recovery from airlines violating fare caps.</li>
        </ul>
      </div>
      <div class="sub-box">
        <div class="sub-box-title">1-Click Legal Notice & Export</div>
        <ul>
          <li><strong>DGCA Show-Cause Notice:</strong> 1-Click modal auto-drafting official legal notice citing <em>Rule 135 of Aircraft Rules, 1937</em> with exact route evidence.</li>
          <li><strong>CSV Dossier Export:</strong> Instant download of MoCA regulatory audit report.</li>
        </ul>
      </div>
    </div>

    <table style="margin-top: 10px;">
      <tr>
        <th>Stage Length (Distance Tier)</th>
        <th>Statutory RCS Fare Cap</th>
        <th>Compliance Rule</th>
        <th>Enforcement Action</th>
      </tr>
      <tr>
        <td>≤ 250 km</td>
        <td>₹2,250</td>
        <td>Actual Fare ≤ Cap</td>
        <td>Tag COMPLIANT (Green)</td>
      </tr>
      <tr>
        <td>251 – 350 km</td>
        <td>₹2,750</td>
        <td>Actual Fare ≤ Cap × 1.10</td>
        <td>Tag MARGINAL (Warning)</td>
      </tr>
      <tr>
        <td>351 – 500 km</td>
        <td>₹3,300</td>
        <td>Actual Fare &gt; Cap × 1.10</td>
        <td>Tag BREACH → Calculate VGF Clawback</td>
      </tr>
      <tr>
        <td>501 – 650 km</td>
        <td>₹3,800</td>
        <td>Haversine Great-Circle</td>
        <td>Generate Rule 135 Show-Cause Notice</td>
      </tr>
      <tr>
        <td>651 – 850 km</td>
        <td>₹4,400</td>
        <td>Airport GPS Lat/Long</td>
        <td>Flag to DGCA Tariff Cell</td>
      </tr>
      <tr>
        <td>851 – 1,100 km</td>
        <td>₹5,100</td>
        <td>Single Seat Outlier Filtered</td>
        <td>Clawback Viability Gap Funding</td>
      </tr>
      <tr>
        <td>&gt; 1,100 km</td>
        <td>₹5,800</td>
        <td>Economy Class Strict Filter</td>
        <td>Export Regulatory Audit Dossier</td>
      </tr>
    </table>

    <div class="jury-quote">
      <strong>Jury Defense Line:</strong> "Sir, this feature makes our solution truly unique. It protects taxpayers' ₹1,000+ Crore Viability Gap Funding by auditing whether airlines are charging predatory rates on subsidized UDAN routes."
    </div>
  </div>

  <div class="page-break"></div>

  <!-- DASHBOARD 6 -->
  <div class="section-card">
    <h2>6. ATF Fuel Shock Elasticity Simulator <span class="route-badge">Route: /simulation</span></h2>
    <p><strong>Primary Objective:</strong> Macroeconomic cost pass-through simulator modeling the financial impact of crude oil and jet fuel volatility on ticket prices.</p>
    <div class="grid-2">
      <div class="sub-box">
        <div class="sub-box-title">Key Visual Components</div>
        <ul>
          <li><strong>Fuel Fluctuation Slider:</strong> Interactive slider from -30% to +50% crude price shocks.</li>
          <li><strong>Elasticity Toggles:</strong> Low (η = 0.40), Medium (η = 0.65), High (η = 0.85).</li>
          <li><strong>Consumer Financial Exposure Metric:</strong> Quantifies national consumer burden in ₹ Crores.</li>
          <li><strong>Route Sensitivity Matrix:</strong> Plots fuel sensitivity across 10 representative trunk corridors.</li>
        </ul>
      </div>
      <div class="sub-box">
        <div class="sub-box-title">Economic Rationale</div>
        <ul>
          <li>ATF constitutes 35–40% of airline operational costs in India.</li>
          <li>Models legitimate fuel surcharge adjustments vs illegitimate predatory gouging.</li>
        </ul>
      </div>
    </div>
    <div class="jury-quote">
      <strong>Jury Defense Line:</strong> "When global crude jumps 20%, our simulator tells regulators exactly how much fare increase is mathematically justified versus artificial price hiking."
    </div>
  </div>

  <!-- DASHBOARD 7 -->
  <div class="section-card">
    <h2>7. Carrier Fleet & Capacity Intelligence <span class="route-badge">Route: /fleet</span></h2>
    <p><strong>Primary Objective:</strong> Operational aircraft inventory, fuel efficiency benchmarks, and capacity allocation across scheduled domestic carriers.</p>
    <div class="grid-2">
      <div class="sub-box">
        <div class="sub-box-title">Key Visual Components</div>
        <ul>
          <li><strong>Carrier Profiles:</strong> IndiGo (A320neo, A321neo), Air India (A350, B777), SpiceJet (B737, Q400), Akasa Air (B737 MAX 8), AI Express.</li>
          <li><strong>Seat Density vs Fares:</strong> Single-class high-density vs full-service dual-class yield comparison.</li>
          <li><strong>Fuel Burn Benchmarks:</strong> LEAP-1A / GTF engine efficiency differentials.</li>
        </ul>
      </div>
      <div class="sub-box">
        <div class="sub-box-title">Operational Context</div>
        <ul>
          <li>Correlates aircraft seating capacity with route-level yield curves.</li>
        </ul>
      </div>
    </div>
    <div class="jury-quote">
      <strong>Jury Defense Line:</strong> "Fleet intelligence tracks how aircraft upgrades directly alter an airline's baseline cost structure and pricing dynamics."
    </div>
  </div>

  <!-- DASHBOARD 8 & 9 -->
  <div class="section-card">
    <h2>8. Regulatory Citations & Standards <span class="route-badge">Route: /references</span></h2>
    <p><strong>Primary Objective:</strong> Documents legal anchors, statistical guidelines, and Survey of India cartographic compliance.</p>
    <ul>
      <li><strong>Statutory Mandate:</strong> Rule 135, Aircraft Rules (1937) — Tariff filing & prevention of predatory pricing.</li>
      <li><strong>Official Data Feeds:</strong> DGCA Monthly Traffic Form A/B, MOSPI CPI Transport Sub-Index Manual, ICAO Doc 9626.</li>
      <li><strong>Sovereign Cartography:</strong> 100% Survey of India (SoI) compliant territorial boundaries.</li>
    </ul>
  </div>

  <div class="section-card">
    <h2>9. Sovereign Gov API Gateway <span class="route-badge">Route: /gov-api</span></h2>
    <p><strong>Primary Objective:</strong> Enterprise integration portal for National Informatics Centre (NIC) and MoCA automated systems.</p>
    <ul>
      <li><strong>REST Endpoints:</strong> <code>/api/index</code>, <code>/api/udan/rcs-compliance</code>, <code>/api/udan/export-rcs-report</code>.</li>
      <li><strong>Performance SLA:</strong> Verified sub-45ms response latency with OpenAPI 3.0 Swagger specifications.</li>
    </ul>
  </div>

  <!-- JURY DEFENSE CHEAT SHEET -->
  <div class="section-card highlight">
    <h2>🏆 3-Minute Master Pitch for Judges & Evaluators</h2>
    <ol style="margin: 4px 0; padding-left: 18px; font-size: 9.8pt;">
      <li><strong>The Problem:</strong> Under the guise of dynamic pricing, airlines exploit emergency travelers and regional routes with 2.14x surge spikes while the government lacked a reproducible real-time price index.</li>
      <li><strong>The Innovation (UDAN-STAT):</strong> We created India's first Laspeyres airfare index weighted by DGCA Form A/B passenger distributions across 80 corridors, backed by statistical IQR outlier filtering.</li>
      <li><strong>The Differentiator (UDAN RCS Auditor):</strong> Our Haversine geodesic engine monitors regional routes against statutory fare caps (₹2,250–₹5,800), detects Viability Gap Funding (VGF) subsidy clawbacks, and auto-generates legal notices under Rule 135 of Aircraft Rules, 1937.</li>
      <li><strong>Readiness:</strong> 100% sovereign open-source stack (React 19 + FastAPI + SQLite/Postgres), live deployed on Vercel with zero commercial API licensing overhead.</li>
    </ol>
  </div>

</body>
</html>
"""

def generate_pdf():
    html_file = "d:/SIH 2026/temp_feature_guide.html"
    pdf_file  = "d:/SIH 2026/UDAN_STAT_Comprehensive_Feature_and_Dashboard_Guide.pdf"

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("HTML created. Converting to PDF with Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file:///{os.path.abspath(html_file)}")
        page.wait_for_timeout(1000)
        page.pdf(
            path=pdf_file,
            format="A4",
            print_background=True,
            margin={"top": "14mm", "bottom": "14mm", "left": "14mm", "right": "14mm"}
        )
        browser.close()

    if os.path.exists(html_file):
        os.remove(html_file)

    print(f"PDF successfully generated at: {pdf_file}")

if __name__ == "__main__":
    generate_pdf()
