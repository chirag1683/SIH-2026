import React, { useState, useEffect, useMemo, useCallback } from 'react';
import Plot from 'react-plotly.js';
import { useTheme } from '../App';
import { API_BASE_URL } from '../config';

const API = API_BASE_URL;

/* ─── Interfaces ─────────────────────────────────────────────────────────── */
interface CarrierAudit {
  airline: string;
  fare: number;
  excess: number;
  status: 'COMPLIANT' | 'MARGINAL' | 'BREACH';
}

interface RcsRouteItem {
  route_id: string;
  origin: string;
  origin_name: string;
  destination: string;
  dest_name: string;
  stage_length_km: number;
  horizon: string;
  statutory_cap: number;
  actual_fare: number;
  rcs_quota_fare: number;
  excess_surcharge: number;
  excess_pct: number;
  status: 'COMPLIANT' | 'MARGINAL' | 'BREACH';
  passenger_count: number;
  potential_vgf_clawback: number;
  carriers: CarrierAudit[];
  regulatory_action: string;
}

interface RcsAuditResponse {
  total_rcs_routes: number;
  displayed_routes: number;
  compliant_count: number;
  marginal_count: number;
  breach_count: number;
  compliance_rate_pct: number;
  total_excess_surcharge_sum: number;
  horizon: string;
  filters_applied: {
    carrier: string;
    status: string;
    horizon: string;
  };
  audit_timestamp: string;
  routes: RcsRouteItem[];
}

const CARRIERS_LIST = [
  'All Airlines',
  'IndiGo (6E)',
  'Air India (AI)',
  'SpiceJet (SG)',
  'Air India Express (IX)',
  'Akasa Air (QP)'
];

const HORIZONS_LIST = ['T+1', 'T+7', 'T+15', 'T+30', 'T+45'];

const UdanRcs: React.FC = () => {
  const { dark } = useTheme();

  // Filters
  const [selectedHorizon, setSelectedHorizon] = useState('T+7');
  const [selectedCarrier, setSelectedCarrier] = useState('All Airlines');
  const [selectedStatus, setSelectedStatus]   = useState('all');
  const [searchQuery, setSearchQuery]         = useState('');

  // Data
  const [auditData, setAuditData]             = useState<RcsAuditResponse | null>(null);
  const [loading, setLoading]                 = useState(false);
  const [flaggedModalItem, setFlaggedModalItem] = useState<RcsRouteItem | null>(null);
  const [downloading, setDownloading]         = useState(false);

  const fetchRcsData = useCallback(() => {
    setLoading(true);
    const carrierParam = selectedCarrier === 'All Airlines' ? 'all' : selectedCarrier;
    const qs = `horizon=${encodeURIComponent(selectedHorizon)}&carrier=${encodeURIComponent(carrierParam)}&status=${encodeURIComponent(selectedStatus)}`;

    fetch(`${API}/api/udan/rcs-compliance?${qs}`)
      .then(res => res.ok ? res.json() : null)
      .then(data => {
        if (data && data.routes) {
          setAuditData(data);
        }
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [selectedHorizon, selectedCarrier, selectedStatus]);

  useEffect(() => {
    fetchRcsData();
  }, [fetchRcsData]);

  // Client-side search filtering
  const displayedRoutes = useMemo(() => {
    if (!auditData || !auditData.routes) return [];
    if (!searchQuery.trim()) return auditData.routes;
    const q = searchQuery.toLowerCase();
    return auditData.routes.filter(r =>
      r.route_id.toLowerCase().includes(q) ||
      r.origin_name.toLowerCase().includes(q) ||
      r.dest_name.toLowerCase().includes(q)
    );
  }, [auditData, searchQuery]);

  // Export CSV Handler
  const handleDownloadCsv = () => {
    setDownloading(true);
    const carrierParam = selectedCarrier === 'All Airlines' ? 'all' : selectedCarrier;
    const url = `${API}/api/udan/export-rcs-report?horizon=${encodeURIComponent(selectedHorizon)}&carrier=${encodeURIComponent(carrierParam)}&status=${encodeURIComponent(selectedStatus)}`;
    
    fetch(url)
      .then(res => res.blob())
      .then(blob => {
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = `moca_udan_rcs_audit_${selectedHorizon}.csv`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      })
      .catch(() => alert('Failed to download audit CSV.'))
      .finally(() => setDownloading(false));
  };

  // Status Styling Helpers
  const getStatusBadge = (status: string) => {
    if (status === 'COMPLIANT') {
      return <span className="stat-pill" style={{ background: 'rgba(16,185,129,0.15)', color: 'var(--green)', border: '1px solid rgba(16,185,129,0.4)', padding: '3px 8px', borderRadius: 4, fontWeight: 700, fontSize: '0.72rem' }}>✓ COMPLIANT</span>;
    }
    if (status === 'MARGINAL') {
      return <span className="stat-pill" style={{ background: 'rgba(245,158,11,0.15)', color: '#F59E0B', border: '1px solid rgba(245,158,11,0.4)', padding: '3px 8px', borderRadius: 4, fontWeight: 700, fontSize: '0.72rem' }}>⚠ MARGINAL</span>;
    }
    return <span className="stat-pill" style={{ background: 'rgba(239,68,68,0.15)', color: '#EF4444', border: '1px solid rgba(239,68,68,0.4)', padding: '3px 8px', borderRadius: 4, fontWeight: 700, fontSize: '0.72rem' }}>✕ STATUTORY BREACH</span>;
  };

  // Plotly chart theme base
  const plotLayout = useMemo(() => ({
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    font: { color: dark ? '#94A3B8' : '#334155', family: 'Inter, sans-serif' },
    margin: { t: 30, r: 25, b: 50, l: 60 },
    xaxis: {
      title: { text: 'Stage Length (km)', font: { size: 12, color: dark ? '#CBD5E1' : '#1E293B' } },
      gridcolor: dark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)',
      zerolinecolor: dark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
    },
    yaxis: {
      title: { text: 'Airfare (₹ INR)', font: { size: 12, color: dark ? '#CBD5E1' : '#1E293B' } },
      gridcolor: dark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)',
      zerolinecolor: dark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
    },
    legend: { orientation: 'h' as const, y: 1.12, x: 0 },
    hovermode: 'closest' as const,
  }), [dark]);

  return (
    <div className="page-content" style={{ maxWidth: 1400, margin: '0 auto', paddingBottom: 60 }}>

      {/* ── Page Header ── */}
      <div style={{ marginBottom: 24 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 6 }}>
          <span style={{
            background: 'linear-gradient(90deg, #F97316 0%, #10B981 100%)',
            color: '#fff',
            fontSize: '0.7rem',
            fontWeight: 800,
            letterSpacing: 1.2,
            padding: '2px 8px',
            borderRadius: 4,
            textTransform: 'uppercase'
          }}>
            MoCA · UDAN RCS STATUTORY AUDITOR
          </span>
          <span style={{ fontSize: '0.78rem', color: 'var(--sub)', fontFamily: 'JetBrains Mono,monospace' }}>
            AIRCRAFT RULES 1937 · RULE 135(1) TARIFF COMPLIANCE
          </span>
        </div>
        <h1 style={{ fontSize: '1.85rem', fontWeight: 800, margin: 0, letterSpacing: '-0.5px' }}>
          UDAN Scheme (RCS) Statutory Fare Cap Auditor
        </h1>
        <p style={{ color: 'var(--sub)', fontSize: '0.88rem', margin: '6px 0 0 0', maxWidth: 850 }}>
          Continuous regulatory surveillance of domestic regional connectivity routes against distance-tiered tariff caps mandated by the Ministry of Civil Aviation under the <strong>Ude Desh Ka Aam Nagrik (UDAN)</strong> framework.
        </p>
      </div>

      {/* ── 4 Executive KPI Cards ── */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: 16, marginBottom: 24 }}>
        <div className="card" style={{ padding: 18, borderLeft: '4px solid var(--cyan)' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--sub)', textTransform: 'uppercase', letterSpacing: 1 }}>
            Monitored Regional Corridors
          </div>
          <div style={{ fontSize: '2rem', fontWeight: 900, color: 'var(--text)', marginTop: 6 }}>
            {auditData ? auditData.total_rcs_routes : '—'}
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--sub)', marginTop: 4 }}>
            Stage length ≤ 1,100 km & Tier-2/3 destinations
          </div>
        </div>

        <div className="card" style={{ padding: 18, borderLeft: '4px solid var(--green)' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--sub)', textTransform: 'uppercase', letterSpacing: 1 }}>
            Statutory Compliance Rate
          </div>
          <div style={{ fontSize: '2rem', fontWeight: 900, color: 'var(--green)', marginTop: 6 }}>
            {auditData ? `${auditData.compliance_rate_pct}%` : '—'}
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--sub)', marginTop: 4 }}>
            {auditData ? `${auditData.compliant_count} Compliant · ${auditData.marginal_count} Marginal` : 'Evaluating...'}
          </div>
        </div>

        <div className="card" style={{ padding: 18, borderLeft: '4px solid #EF4444' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--sub)', textTransform: 'uppercase', letterSpacing: 1 }}>
            Active Statutory Breaches
          </div>
          <div style={{ fontSize: '2rem', fontWeight: 900, color: '#EF4444', marginTop: 6 }}>
            {auditData ? auditData.breach_count : '—'}
          </div>
          <div style={{ fontSize: '0.75rem', color: '#EF4444', marginTop: 4 }}>
            Routes exceeding legal RCS ceiling ({selectedHorizon})
          </div>
        </div>

        <div className="card" style={{ padding: 18, borderLeft: '4px solid #F59E0B' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--sub)', textTransform: 'uppercase', letterSpacing: 1 }}>
            Total Excess Surcharge Detected
          </div>
          <div style={{ fontSize: '2rem', fontWeight: 900, color: '#F59E0B', marginTop: 6 }}>
            {auditData ? `₹${Math.round(auditData.total_excess_surcharge_sum).toLocaleString('en-IN')}` : '—'}
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--sub)', marginTop: 4 }}>
            Cumulative excess ticket fare over statutory cap
          </div>
        </div>
      </div>

      {/* ── Filter & Control Bar ── */}
      <div className="card" style={{ padding: '16px 20px', marginBottom: 24, display: 'flex', flexWrap: 'wrap', gap: 16, alignItems: 'center' }}>
        {/* Horizon Filter */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          <label style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--sub)', textTransform: 'uppercase' }}>Booking Horizon</label>
          <div style={{ display: 'flex', gap: 4 }}>
            {HORIZONS_LIST.map(h => (
              <button
                key={h}
                type="button"
                onClick={() => setSelectedHorizon(h)}
                style={{
                  padding: '6px 12px',
                  borderRadius: 6,
                  fontSize: '0.78rem',
                  fontWeight: 700,
                  cursor: 'pointer',
                  border: selectedHorizon === h ? '1.5px solid var(--cyan)' : '1px solid var(--border)',
                  background: selectedHorizon === h ? 'rgba(6,182,212,0.18)' : 'transparent',
                  color: selectedHorizon === h ? 'var(--cyan)' : 'var(--text)'
                }}
              >
                {h}
              </button>
            ))}
          </div>
        </div>

        {/* Carrier Filter */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          <label style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--sub)', textTransform: 'uppercase' }}>Airline Filter</label>
          <select
            className="control-select"
            value={selectedCarrier}
            onChange={e => setSelectedCarrier(e.target.value)}
            style={{ minWidth: 160 }}
          >
            {CARRIERS_LIST.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>

        {/* Status Filter */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          <label style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--sub)', textTransform: 'uppercase' }}>Compliance Status</label>
          <select
            className="control-select"
            value={selectedStatus}
            onChange={e => setSelectedStatus(e.target.value)}
            style={{ minWidth: 150 }}
          >
            <option value="all">All Statuses</option>
            <option value="breach">Breaches Only</option>
            <option value="marginal">Marginal Only</option>
            <option value="compliant">Compliant Only</option>
          </select>
        </div>

        {/* Search corridor */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 4, flex: 1, minWidth: 180 }}>
          <label style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--sub)', textTransform: 'uppercase' }}>Search Route / City</label>
          <input
            type="text"
            className="control-select"
            placeholder="e.g. PAT, GAU, JAI, Lucknow..."
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
          />
        </div>

        {/* Download CSV Button */}
        <div style={{ marginLeft: 'auto', alignSelf: 'flex-end' }}>
          <button
            type="button"
            className="apix-btn-solid"
            onClick={handleDownloadCsv}
            disabled={downloading}
            style={{ padding: '8px 16px', fontSize: '0.82rem', whiteSpace: 'nowrap' }}
          >
            <span>{downloading ? 'Exporting...' : '📥 Export DGCA Audit Dossier (CSV)'}</span>
          </button>
        </div>
      </div>

      {/* ── Interactive Visualization: Distance vs Statutory Cap vs Actual Fare ── */}
      <div className="card" style={{ padding: 20, marginBottom: 24 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
          <div>
            <div style={{ fontSize: '0.92rem', fontWeight: 700, color: 'var(--text)' }}>
              Stage Length vs. Statutory RCS Cap vs. Actual Market Tariff
            </div>
            <div style={{ fontSize: '0.78rem', color: 'var(--sub)' }}>
              Visualizing the statutory MoCA ceiling line against observed representative airfares across booking corridors.
            </div>
          </div>
          <div style={{ fontSize: '0.75rem', fontFamily: 'JetBrains Mono,monospace', color: 'var(--cyan)' }}>
            SURVEILLANCE HORIZON: {selectedHorizon}
          </div>
        </div>

        {auditData && auditData.routes.length > 0 ? (
          <Plot
            data={[
              // Statutory ceiling step line
              {
                x: [150, 250, 250, 350, 350, 500, 500, 650, 650, 850, 850, 1100, 1100, 1200],
                y: [2250, 2250, 2750, 2750, 3300, 3300, 3800, 3800, 4400, 4400, 5100, 5100, 5800, 5800],
                mode: 'lines',
                name: 'Statutory RCS Ceiling (MoCA Mandate)',
                line: { color: '#F97316', width: 3, dash: 'solid' },
              },
              // Compliant routes
              {
                x: auditData.routes.filter(r => r.status === 'COMPLIANT').map(r => r.stage_length_km),
                y: auditData.routes.filter(r => r.status === 'COMPLIANT').map(r => r.actual_fare),
                mode: 'markers',
                name: 'Compliant Corridors (≤ Cap)',
                text: auditData.routes.filter(r => r.status === 'COMPLIANT').map(r => `${r.route_id} (${r.stage_length_km}km)<br>Actual: ₹${r.actual_fare.toLocaleString()}<br>Cap: ₹${r.statutory_cap.toLocaleString()}`),
                marker: { color: '#10B981', size: 9, opacity: 0.85 },
              },
              // Marginal routes
              {
                x: auditData.routes.filter(r => r.status === 'MARGINAL').map(r => r.stage_length_km),
                y: auditData.routes.filter(r => r.status === 'MARGINAL').map(r => r.actual_fare),
                mode: 'markers',
                name: 'Marginal Corridors (+5% to +30%)',
                text: auditData.routes.filter(r => r.status === 'MARGINAL').map(r => `${r.route_id} (${r.stage_length_km}km)<br>Actual: ₹${r.actual_fare.toLocaleString()}<br>Cap: ₹${r.statutory_cap.toLocaleString()}`),
                marker: { color: '#F59E0B', size: 9, opacity: 0.85 },
              },
              // Breach routes
              {
                x: auditData.routes.filter(r => r.status === 'BREACH').map(r => r.stage_length_km),
                y: auditData.routes.filter(r => r.status === 'BREACH').map(r => r.actual_fare),
                mode: 'markers',
                name: 'Statutory Breach Corridors (> 30% Over Cap)',
                text: auditData.routes.filter(r => r.status === 'BREACH').map(r => `${r.route_id} (${r.stage_length_km}km)<br>Actual: ₹${r.actual_fare.toLocaleString()}<br>Cap: ₹${r.statutory_cap.toLocaleString()}<br>Excess: +₹${r.excess_surcharge.toLocaleString()} (+${r.excess_pct}%)`),
                marker: { color: '#EF4444', size: 10, symbol: 'cross', line: { color: '#DC2626', width: 2 } },
              },
            ]}
            layout={{
              ...plotLayout,
              height: 380,
            }}
            config={{ responsive: true, displayModeBar: false }}
            style={{ width: '100%' }}
          />
        ) : (
          <div style={{ padding: 40, textAlign: 'center', color: 'var(--sub)' }}>Loading telemetry data...</div>
        )}
      </div>

      {/* ── Live Compliance Audit Table ── */}
      <div className="card" style={{ padding: 20 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <div>
            <div style={{ fontSize: '1rem', fontWeight: 800, color: 'var(--text)' }}>
              Regional Corridors Statutory Audit Register
            </div>
            <div style={{ fontSize: '0.78rem', color: 'var(--sub)' }}>
              Displaying {displayedRoutes.length} of {auditData ? auditData.total_rcs_routes : 0} regional connectivity pairs under active surveillance.
            </div>
          </div>
          {loading && <span style={{ color: 'var(--cyan)', fontSize: '0.8rem', fontWeight: 700 }}>↻ Synchronizing...</span>}
        </div>

        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border)', textAlign: 'left', color: 'var(--sub)' }}>
                <th style={{ padding: '10px 12px' }}>CORRIDOR</th>
                <th style={{ padding: '10px 12px' }}>STAGE LENGTH</th>
                <th style={{ padding: '10px 12px' }}>STATUTORY CAP</th>
                <th style={{ padding: '10px 12px' }}>MARKET FARE</th>
                <th style={{ padding: '10px 12px' }}>EXCESS SURCHARGE</th>
                <th style={{ padding: '10px 12px' }}>COMPLIANCE STATUS</th>
                <th style={{ padding: '10px 12px' }}>REGULATORY ACTION</th>
              </tr>
            </thead>
            <tbody>
              {displayedRoutes.map(r => (
                <tr
                  key={r.route_id}
                  style={{
                    borderBottom: '1px solid rgba(255,255,255,0.04)',
                    background: r.status === 'BREACH' ? 'rgba(239,68,68,0.03)' : 'transparent',
                    transition: 'background 0.2s ease'
                  }}
                >
                  <td style={{ padding: '12px', fontWeight: 700 }}>
                    <div style={{ color: 'var(--text)' }}>{r.route_id}</div>
                    <div style={{ fontSize: '0.72rem', color: 'var(--sub)', fontWeight: 400 }}>
                      {r.origin_name.split(',')[0]} ➔ {r.dest_name.split(',')[0]}
                    </div>
                  </td>
                  <td style={{ padding: '12px', fontFamily: 'JetBrains Mono,monospace' }}>
                    {r.stage_length_km} km
                  </td>
                  <td style={{ padding: '12px', fontFamily: 'JetBrains Mono,monospace', color: '#F97316', fontWeight: 700 }}>
                    ₹{r.statutory_cap.toLocaleString('en-IN')}
                  </td>
                  <td style={{ padding: '12px', fontFamily: 'JetBrains Mono,monospace', color: 'var(--text)', fontWeight: 700 }}>
                    ₹{r.actual_fare.toLocaleString('en-IN')}
                  </td>
                  <td style={{ padding: '12px', fontFamily: 'JetBrains Mono,monospace' }}>
                    {r.excess_surcharge > 0 ? (
                      <span style={{ color: '#EF4444', fontWeight: 700 }}>
                        +₹{r.excess_surcharge.toLocaleString('en-IN')} (+{r.excess_pct}%)
                      </span>
                    ) : (
                      <span style={{ color: 'var(--green)', fontWeight: 600 }}>₹0 (No Excess)</span>
                    )}
                  </td>
                  <td style={{ padding: '12px' }}>
                    {getStatusBadge(r.status)}
                  </td>
                  <td style={{ padding: '12px' }}>
                    {r.status === 'BREACH' ? (
                      <button
                        type="button"
                        onClick={() => setFlaggedModalItem(r)}
                        style={{
                          background: 'rgba(239,68,68,0.12)',
                          border: '1px solid rgba(239,68,68,0.4)',
                          color: '#EF4444',
                          padding: '4px 10px',
                          borderRadius: 4,
                          fontSize: '0.75rem',
                          fontWeight: 700,
                          cursor: 'pointer'
                        }}
                      >
                        ⚠️ Draft Notice
                      </button>
                    ) : (
                      <span style={{ color: 'var(--sub)', fontSize: '0.75rem' }}>{r.regulatory_action}</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* ── Official DGCA Show-Cause Notice Preview Modal ── */}
      {flaggedModalItem && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100vw',
          height: '100vh',
          background: 'rgba(0,0,0,0.75)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 9999,
          padding: 20
        }}>
          <div className="card" style={{
            maxWidth: 680,
            width: '100%',
            maxHeight: '90vh',
            overflowY: 'auto',
            padding: 28,
            border: '2px solid rgba(239,68,68,0.5)',
            boxShadow: '0 0 30px rgba(239,68,68,0.2)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border)', paddingBottom: 12, marginBottom: 16 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <span style={{ fontSize: '1.2rem' }}>🏛️</span>
                <span style={{ fontWeight: 800, fontSize: '1rem', color: 'var(--text)' }}>
                  MINISTRY OF CIVIL AVIATION · DGCA REGULATORY NOTICE
                </span>
              </div>
              <button
                type="button"
                onClick={() => setFlaggedModalItem(null)}
                style={{ background: 'none', border: 'none', color: 'var(--sub)', fontSize: '1.2rem', cursor: 'pointer' }}
              >
                ✕
              </button>
            </div>

            <div style={{ background: 'rgba(0,0,0,0.2)', padding: 16, borderRadius: 6, fontFamily: 'JetBrains Mono,monospace', fontSize: '0.78rem', lineHeight: 1.6, color: 'var(--text)' }}>
              <div style={{ fontWeight: 800, color: 'var(--cyan)', marginBottom: 8 }}>
                REF NO: DGCA/RCS-UDAN/TARIFF-AUDIT/2026/CORR-{flaggedModalItem.route_id}
              </div>
              <div><strong>MEMORANDUM:</strong> STATUTORY NOTICE UNDER RULE 135(1) OF THE AIRCRAFT RULES, 1937</div>
              <div><strong>CONCERNED OPERATOR(S):</strong> {flaggedModalItem.carriers.map(c => c.airline).join(', ')}</div>
              <div><strong>SUBJECT ROUTE:</strong> {flaggedModalItem.route_id} ({flaggedModalItem.origin_name} ➔ {flaggedModalItem.dest_name})</div>
              <div><strong>STAGE LENGTH:</strong> {flaggedModalItem.stage_length_km} KM</div>
              <div style={{ margin: '10px 0', borderTop: '1px dashed rgba(255,255,255,0.2)', paddingTop: 10 }}>
                <div>• Mandated RCS Statutory Tariff Cap: <strong>₹{flaggedModalItem.statutory_cap.toLocaleString()}</strong></div>
                <div>• Observed Spot Tariff: <strong style={{ color: '#EF4444' }}>₹{flaggedModalItem.actual_fare.toLocaleString()}</strong></div>
                <div>• Excess Surcharge Imposed: <strong style={{ color: '#EF4444' }}>+₹{flaggedModalItem.excess_surcharge.toLocaleString()} (+{flaggedModalItem.excess_pct}%)</strong></div>
                <div>• Potential Viability Gap Funding (VGF) Subsidy Clawback: <strong>₹{flaggedModalItem.potential_vgf_clawback.toLocaleString()}</strong></div>
              </div>
              <div style={{ color: 'var(--sub)' }}>
                Pursuant to statutory powers under the National Civil Aviation Policy and UDAN Scheme guidelines, the operating air carrier is hereby directed to show cause within <strong>7 calendar days</strong> why punitive tariff enforcement measures and recovery of subsidized VGF allotments should not be initiated.
              </div>
            </div>

            <div style={{ display: 'flex', gap: 12, justifyContent: 'flex-end', marginTop: 20 }}>
              <button
                type="button"
                className="apix-btn-ghost"
                onClick={() => setFlaggedModalItem(null)}
                style={{ padding: '8px 16px', fontSize: '0.82rem' }}
              >
                Close
              </button>
              <button
                type="button"
                className="apix-btn-solid"
                onClick={() => {
                  window.print();
                }}
                style={{ padding: '8px 18px', fontSize: '0.82rem' }}
              >
                🖨️ Print / Dispatch Dossier
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
};

export default UdanRcs;
