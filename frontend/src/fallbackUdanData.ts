// Client-side fallback seed & computation engine for UDAN RCS Statutory Fare Cap Auditor
// Guarantees 100% instant zero-latency rendering on Vercel and offline mobile/desktop

export interface CarrierAudit {
  airline: string;
  fare: number;
  excess: number;
  status: 'COMPLIANT' | 'MARGINAL' | 'BREACH';
}

export interface RcsRouteItem {
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

export interface RcsAuditResponse {
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

export const AIRPORTS_MAP: Record<string, { lat: number; lon: number; name: string }> = {
  DEL: { lat: 28.5562, lon: 77.1000, name: "Indira Gandhi International, Delhi" },
  BOM: { lat: 19.0896, lon: 72.8656, name: "Chhatrapati Shivaji Maharaj, Mumbai" },
  BLR: { lat: 13.1986, lon: 77.7066, name: "Kempegowda International, Bengaluru" },
  HYD: { lat: 17.2403, lon: 78.4294, name: "Rajiv Gandhi International, Hyderabad" },
  MAA: { lat: 12.9941, lon: 80.1709, name: "Chennai International, Chennai" },
  CCU: { lat: 22.6547, lon: 88.4467, name: "Netaji Subhash Chandra Bose, Kolkata" },
  AMD: { lat: 23.0734, lon: 72.6347, name: "Sardar Vallabhbhai Patel, Ahmedabad" },
  COK: { lat: 10.1520, lon: 76.4019, name: "Cochin International, Kochi" },
  PNQ: { lat: 18.5822, lon: 73.9197, name: "Pune Airport, Pune" },
  GOI: { lat: 15.3808, lon: 73.8314, name: "Dabolim / Mopa, Goa" },
  LKO: { lat: 26.7606, lon: 80.8893, name: "Chaudhary Charan Singh, Lucknow" },
  JAI: { lat: 26.8242, lon: 75.8122, name: "Jaipur International, Jaipur" },
  ATQ: { lat: 31.7096, lon: 74.7973, name: "Sri Guru Ram Dass Jee, Amritsar" },
  GAU: { lat: 26.1061, lon: 91.5859, name: "Lokpriya Gopinath Bordoloi, Guwahati" },
  BBI: { lat: 20.2444, lon: 85.8178, name: "Biju Patnaik International, Bhubaneswar" },
  IXC: { lat: 30.6735, lon: 76.7886, name: "Shaheed Bhagat Singh, Chandigarh" },
  IXB: { lat: 26.6812, lon: 88.3286, name: "Bagdogra Airport, Siliguri" },
  PAT: { lat: 25.5913, lon: 85.0880, name: "Jayprakash Narayan, Patna" },
  TRV: { lat: 8.4821,  lon: 76.9201, name: "Thiruvananthapuram International, Trivandrum" },
  VTZ: { lat: 17.7211, lon: 83.2245, name: "Visakhapatnam Airport, Vizag" },
};

export const RCS_PAIRS: [string, string][] = [
  ["AMD","PNQ"], ["PNQ","AMD"],
  ["DEL","LKO"], ["LKO","DEL"],
  ["DEL","JAI"], ["JAI","DEL"],
  ["DEL","IXC"], ["IXC","DEL"],
  ["BOM","GOI"], ["GOI","BOM"],
  ["BOM","PNQ"], ["PNQ","BOM"],
  ["BOM","AMD"], ["AMD","BOM"],
  ["BLR","COK"], ["COK","BLR"],
  ["BLR","HYD"], ["HYD","BLR"],
  ["BLR","PNQ"], ["PNQ","BLR"],
  ["BLR","GOI"], ["GOI","BLR"],
  ["HYD","MAA"], ["MAA","HYD"],
  ["HYD","PNQ"], ["PNQ","HYD"],
  ["HYD","GOI"], ["GOI","HYD"],
  ["HYD","VTZ"], ["VTZ","HYD"],
  ["MAA","COK"], ["COK","MAA"],
  ["MAA","TRV"], ["TRV","MAA"],
  ["CCU","BBI"], ["BBI","CCU"],
  ["CCU","PAT"], ["PAT","CCU"],
  ["CCU","GAU"], ["GAU","CCU"],
  ["CCU","IXB"], ["IXB","CCU"],
  ["DEL","ATQ"], ["ATQ","DEL"],
  ["DEL","PAT"], ["PAT","DEL"],
  ["DEL","GAU"], ["GAU","DEL"],
  ["DEL","BBI"], ["BBI","DEL"],
  ["BOM","JAI"], ["JAI","BOM"],
  ["BOM","LKO"], ["LKO","BOM"],
  ["BOM","IXC"], ["IXC","BOM"],
  ["BOM","PAT"], ["PAT","BOM"],
  ["BOM","COK"], ["COK","BOM"],
  ["HYD","COK"], ["COK","HYD"]
];

function haversineDist(lat1: number, lon1: number, lat2: number, lon2: number): number {
  const R = 6371.0;
  const dLat = (lat2 - lat1) * Math.PI / 180.0;
  const dLon = (lon2 - lon1) * Math.PI / 180.0;
  const a = Math.sin(dLat / 2.0) ** 2 +
            Math.cos(lat1 * Math.PI / 180.0) * Math.cos(lat2 * Math.PI / 180.0) *
            Math.sin(dLon / 2.0) ** 2;
  const c = 2.0 * Math.atan2(Math.sqrt(a), Math.sqrt(1.0 - a));
  return Math.round(R * c * 10) / 10;
}

export function getStatutoryCap(distKm: number): number {
  if (distKm <= 250) return 2250;
  if (distKm <= 350) return 2750;
  if (distKm <= 500) return 3300;
  if (distKm <= 650) return 3800;
  if (distKm <= 850) return 4400;
  if (distKm <= 1100) return 5100;
  return 5800;
}

const CARRIERS_DEF = [
  { name: 'IndiGo (6E)', mult: 1.0 },
  { name: 'Air India (AI)', mult: 1.08 },
  { name: 'SpiceJet (SG)', mult: 0.94 },
  { name: 'Air India Express (IX)', mult: 0.92 },
  { name: 'Akasa Air (QP)', mult: 0.96 }
];

export function getFallbackRcsData(
  horizon: string = 'T+7',
  carrierFilter: string = 'all',
  statusFilter: string = 'all'
): RcsAuditResponse {
  const hMult: Record<string, number> = {
    'T+1': 2.14,
    'T+7': 1.42,
    'T+15': 1.18,
    'T+30': 1.05,
    'T+45': 0.95
  };
  const multiplier = hMult[horizon] || 1.42;

  let totalRcsRoutes = 0;
  let compliantCount = 0;
  let marginalCount = 0;
  let breachCount = 0;
  let totalExcessSurcharge = 0;
  const routes: RcsRouteItem[] = [];

  RCS_PAIRS.forEach(([orig, dest], idx) => {
    const origInfo = AIRPORTS_MAP[orig] || { lat: 28.5, lon: 77.1, name: `${orig} Airport` };
    const destInfo = AIRPORTS_MAP[dest] || { lat: 19.1, lon: 72.8, name: `${dest} Airport` };
    const dist = haversineDist(origInfo.lat, origInfo.lon, destInfo.lat, destInfo.lon);
    const cap = getStatutoryCap(dist);

    totalRcsRoutes++;

    // Realistic pseudo-random variation based on route index
    const variance = 0.92 + ((idx * 7) % 25) / 100.0;
    const baseFare = Math.round(cap * multiplier * variance);
    let actualFare = baseFare;

    // Build carrier audits
    const carriers: CarrierAudit[] = CARRIERS_DEF.map(c => {
      const cFare = Math.round(baseFare * c.mult);
      const cExcess = Math.max(0, cFare - cap);
      const cStatus: 'COMPLIANT' | 'MARGINAL' | 'BREACH' =
        cFare <= cap * 1.05 ? 'COMPLIANT' : cFare <= cap * 1.30 ? 'MARGINAL' : 'BREACH';
      return {
        airline: c.name,
        fare: cFare,
        excess: cExcess,
        status: cStatus
      };
    });

    if (carrierFilter !== 'all') {
      const matched = carriers.find(c => c.airline.toLowerCase().includes(carrierFilter.toLowerCase()));
      if (matched) {
        actualFare = matched.fare;
      } else {
        return;
      }
    }

    const excess = Math.max(0, actualFare - cap);
    const excessPct = Math.round(((actualFare - cap) / cap) * 10000) / 100;

    let status: 'COMPLIANT' | 'MARGINAL' | 'BREACH' = 'BREACH';
    if (actualFare <= cap * 1.05) {
      status = 'COMPLIANT';
      compliantCount++;
    } else if (actualFare <= cap * 1.30) {
      status = 'MARGINAL';
      marginalCount++;
    } else {
      status = 'BREACH';
      breachCount++;
      totalExcessSurcharge += excess;
    }

    if (statusFilter !== 'all' && status.toLowerCase() !== statusFilter.toLowerCase()) {
      return;
    }

    const paxCount = Math.round(180000 + ((idx * 13) % 50) * 10000);
    const potentialClawback = Math.round(excess * (paxCount * 0.12));

    let directive = 'Route tariff conforms to MoCA RCS ceiling.';
    if (status === 'MARGINAL') {
      directive = 'Fare near ceiling (+5% to +30%). Informal tariff surveillance active.';
    } else if (status === 'BREACH') {
      directive = 'STATUTORY VIOLATION: Excessive fare gouging. Formal DGCA Show-Cause Notice warranted.';
    }

    routes.push({
      route_id: `${orig}-${dest}`,
      origin: orig,
      origin_name: origInfo.name,
      destination: dest,
      dest_name: destInfo.name,
      stage_length_km: dist,
      horizon: horizon,
      statutory_cap: cap,
      actual_fare: actualFare,
      rcs_quota_fare: cap,
      excess_surcharge: excess,
      excess_pct: excessPct,
      status: status,
      passenger_count: paxCount,
      potential_vgf_clawback: potentialClawback,
      carriers: carriers,
      regulatory_action: directive
    });
  });

  const compRate = totalRcsRoutes > 0 ? Math.round((compliantCount / totalRcsRoutes) * 1000) / 10 : 0;

  return {
    total_rcs_routes: totalRcsRoutes,
    displayed_routes: routes.length,
    compliant_count: compliantCount,
    marginal_count: marginalCount,
    breach_count: breachCount,
    compliance_rate_pct: compRate,
    total_excess_surcharge_sum: totalExcessSurcharge,
    horizon: horizon,
    filters_applied: {
      carrier: carrierFilter,
      status: statusFilter,
      horizon: horizon
    },
    audit_timestamp: new Date().toISOString(),
    routes: routes
  };
}
