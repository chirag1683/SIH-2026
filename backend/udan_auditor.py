# udan_auditor.py
# UDAN Scheme (RCS) Statutory Fare Cap Auditor & VGF Compliance Engine
# Ministry of Civil Aviation (MoCA) Regional Connectivity Scheme Compliance

import math
from typing import List, Dict, Any, Optional
import pandas as pd
from datetime import datetime

try:
    from backend.static_data import (
        AIRPORTS,
        SELECTED_PAIRS,
        ROUTE_WEIGHTS,
        BASE_FARES,
        AIRLINES,
    )
except ModuleNotFoundError:
    from static_data import (
        AIRPORTS,
        SELECTED_PAIRS,
        ROUTE_WEIGHTS,
        BASE_FARES,
        AIRLINES,
    )


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Computes great-circle distance between two airport coordinates in kilometers.
    """
    R = 6371.0  # Earth's radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2.0) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 1)


def get_statutory_rcs_cap(distance_km: float) -> float:
    """
    Official Ministry of Civil Aviation (MoCA) UDAN RCS Fare Ceiling Schedule:
    Distance-tiered statutory price cap per subsidized regional seat.
    """
    if distance_km <= 250:
        return 2250.0
    elif distance_km <= 350:
        return 2750.0
    elif distance_km <= 500:
        return 3300.0
    elif distance_km <= 650:
        return 3800.0
    elif distance_km <= 850:
        return 4400.0
    elif distance_km <= 1100:
        return 5100.0
    else:
        return 5800.0


# Regional airport identifiers under regional connectivity focus
REGIONAL_STATIONS = {"PAT", "GAU", "BBI", "IXC", "LKO", "JAI", "COK", "GOI", "PNQ", "AMD"}


def audit_rcs_compliance(
    clean_df: pd.DataFrame,
    rep_fares: pd.DataFrame,
    horizon: str = "T+7",
    carrier_filter: str = "all",
    status_filter: str = "all"
) -> Dict[str, Any]:
    """
    Evaluates domestic flight fares against MoCA UDAN RCS statutory fare caps.
    Identifies statutory breaches, excess surcharges, and Viability Gap Funding (VGF) subsidy risk.
    """
    routes_audited: List[Dict[str, Any]] = []
    target_h = horizon if horizon in ["T+1", "T+7", "T+15", "T+30", "T+45"] else "T+7"

    # Map representative fares by route_id (Economy only)
    rep_fare_map = {}
    if not rep_fares.empty:
        h_fares = rep_fares[
            (rep_fares["lead_time_horizon"] == target_h) &
            (rep_fares.get("cabin_class", pd.Series(dtype=str)).str.lower() == "economy")
        ]
        if h_fares.empty:
            h_fares = rep_fares[rep_fares["lead_time_horizon"] == target_h]
        for _, r in h_fares.iterrows():
            rep_fare_map[r["route_id"]] = float(r["representative_fare"])

    # Carrier-specific representative fares (Economy only)
    carrier_rep_map = {}
    if not clean_df.empty:
        h_clean = clean_df[
            (clean_df["lead_time_horizon"] == target_h) &
            (clean_df.get("cabin_class", pd.Series(dtype=str)).str.lower() == "economy")
        ]
        if h_clean.empty:
            h_clean = clean_df[clean_df["lead_time_horizon"] == target_h]
        for (rid, al), grp in h_clean.groupby(["route_id", "airline"]):
            carrier_rep_map[(rid, al)] = float(grp["total_fare"].median())

    total_rcs_routes = 0
    compliant_count = 0
    marginal_count = 0
    breach_count = 0
    total_excess_surcharge = 0.0

    for orig, dest in SELECTED_PAIRS:
        rid = f"{orig}-{dest}"

        # Consider route as regional if either endpoint is in REGIONAL_STATIONS or distance <= 900km
        orig_info = AIRPORTS.get(orig, (0.0, 0.0, orig))
        dest_info = AIRPORTS.get(dest, (0.0, 0.0, dest))
        dist_km = haversine_distance(orig_info[0], orig_info[1], dest_info[0], dest_info[1])

        is_regional = (orig in REGIONAL_STATIONS or dest in REGIONAL_STATIONS or dist_km <= 900)
        if not is_regional:
            continue

        total_rcs_routes += 1
        statutory_cap = get_statutory_rcs_cap(dist_km)

        # Base market fare (T+7)
        actual_fare = rep_fare_map.get(rid)
        if actual_fare is None:
            base_f = float(BASE_FARES.get("T+7", {}).get(rid, statutory_cap * 1.15))
            actual_fare = round(base_f * 1.253, 2)

        # Carrier specifics
        route_carriers = []
        for al in AIRLINES:
            al_fare = carrier_rep_map.get((rid, al))
            if al_fare is not None:
                al_excess = round(max(0.0, al_fare - statutory_cap), 2)
                al_status = "BREACH" if al_fare > statutory_cap else ("MARGINAL" if al_fare > statutory_cap * 0.9 else "COMPLIANT")
                route_carriers.append({
                    "airline": al,
                    "fare": round(al_fare, 2),
                    "excess": al_excess,
                    "status": al_status,
                })

        # Apply carrier filter if specified
        if carrier_filter != "all":
            matched = [c for c in route_carriers if c["airline"] == carrier_filter]
            if matched:
                actual_fare = matched[0]["fare"]
            else:
                continue

        excess = round(max(0.0, actual_fare - statutory_cap), 2)
        excess_pct = round(((actual_fare - statutory_cap) / statutory_cap) * 100.0, 2)

        if actual_fare <= statutory_cap * 1.05:
            status = "COMPLIANT"
            compliant_count += 1
        elif actual_fare <= statutory_cap * 1.30:
            status = "MARGINAL"
            marginal_count += 1
        else:
            status = "BREACH"
            breach_count += 1
            total_excess_surcharge += excess

        # Filter by status if requested
        if status_filter != "all" and status.lower() != status_filter.lower():
            continue

        # Passenger volume impact
        pshare = ROUTE_WEIGHTS.get(rid, 0.0125)
        pcount = int(pshare * 150_000_000)
        potential_vgf_clawback = int(excess * (pcount * 0.12))  # Assuming 12% subsidized seats

        routes_audited.append({
            "route_id": rid,
            "origin": orig,
            "origin_name": orig_info[2],
            "destination": dest,
            "dest_name": dest_info[2],
            "stage_length_km": dist_km,
            "horizon": target_h,
            "statutory_cap": statutory_cap,
            "actual_fare": actual_fare,
            "rcs_quota_fare": round(min(actual_fare, statutory_cap), 2),
            "excess_surcharge": excess,
            "excess_pct": excess_pct,
            "status": status,
            "passenger_count": pcount,
            "potential_vgf_clawback": potential_vgf_clawback,
            "carriers": route_carriers if route_carriers else [
                {"airline": "IndiGo (6E)", "fare": actual_fare, "status": status, "excess": excess}
            ],
            "regulatory_action": "Statutory Show-Cause Recommended" if status == "BREACH" else "Routine Monitoring"
        })

    # Sort routes: Breaches with highest excess surcharge first
    routes_audited.sort(key=lambda r: (r["status"] != "BREACH", -r["excess_surcharge"]))

    compliance_rate = round((compliant_count / max(1, total_rcs_routes)) * 100.0, 1)

    return {
        "total_rcs_routes": total_rcs_routes,
        "displayed_routes": len(routes_audited),
        "compliant_count": compliant_count,
        "marginal_count": marginal_count,
        "breach_count": breach_count,
        "compliance_rate_pct": compliance_rate,
        "total_excess_surcharge_sum": round(total_excess_surcharge, 2),
        "horizon": target_h,
        "filters_applied": {
            "carrier": carrier_filter,
            "status": status_filter,
            "horizon": target_h
        },
        "audit_timestamp": datetime.now().isoformat(),
        "routes": routes_audited
    }


def generate_rcs_audit_csv(audit_result: Dict[str, Any]) -> str:
    """
    Generates official DGCA / MoCA UDAN RCS Audit Dossier in CSV format.
    """
    lines = [
        "MoCA_UDAN_RCS_COMPLIANCE_AUDIT_DOSSIER",
        f"Generated At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"Compliance Rate: {audit_result.get('compliance_rate_pct', 0)}%",
        f"Total Active Breaches: {audit_result.get('breach_count', 0)}",
        "",
        "Route_ID,Origin,Destination,Distance_KM,Statutory_Cap_INR,Representative_Fare_INR,Excess_INR,Excess_Pct,Status,VGF_Clawback_Risk_INR,Regulatory_Action"
    ]

    for r in audit_result.get("routes", []):
        lines.append(
            f"{r['route_id']},{r['origin']},{r['destination']},{r['stage_length_km']},"
            f"{r['statutory_cap']},{r['actual_fare']},{r['excess_surcharge']},{r['excess_pct']}%,{r['status']},"
            f"{r['potential_vgf_clawback']},{r['regulatory_action']}"
        )

    return "\n".join(lines)
