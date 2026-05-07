"""
Power System Intelligence Service
Handles industry/machinery classification, fault analysis, and cascading effects
"""

from datetime import datetime
from enum import Enum
import json


class PowerSystemIndustry(Enum):
    """Power system industries in the industry classification."""
    GENERATION = "Generation"
    TRANSMISSION = "Transmission"
    DISTRIBUTION = "Distribution"


class MachineryType(Enum):
    """Machinery types in power systems."""
    GENERATOR = "Generator"
    TRANSFORMER = "Transformer"
    SWITCHGEAR = "Switchgear"
    TRANSMISSION_LINE = "Transmission Line"
    BREAKER = "Circuit Breaker"
    MOTOR = "Induction Motor"
    CAPACITOR_BANK = "Capacitor Bank"
    RELAY = "Protection Relay"


# Industry -> Machinery mapping
INDUSTRY_MACHINERY_MAP = {
    "Generation": [
        MachineryType.GENERATOR.value,
        MachineryType.TRANSFORMER.value,
        MachineryType.SWITCHGEAR.value,
        MachineryType.CAPACITOR_BANK.value,
        MachineryType.RELAY.value,
    ],
    "Transmission": [
        MachineryType.TRANSMISSION_LINE.value,
        MachineryType.TRANSFORMER.value,
        MachineryType.SWITCHGEAR.value,
        MachineryType.BREAKER.value,
        MachineryType.RELAY.value,
        MachineryType.CAPACITOR_BANK.value,
    ],
    "Distribution": [
        MachineryType.TRANSFORMER.value,
        MachineryType.SWITCHGEAR.value,
        MachineryType.BREAKER.value,
        MachineryType.CAPACITOR_BANK.value,
        MachineryType.MOTOR.value,
    ],
}

# Fault types by machinery
MACHINERY_FAULT_MAP = {
    "Generator": {
        "faults": [
            {"type": "Stator Winding Fault", "code": "SWF", "severity": "critical"},
            {"type": "Rotor Winding Fault", "code": "RWF", "severity": "high"},
            {"type": "Air Gap Eccentricity", "code": "AGE", "severity": "high"},
            {"type": "Phase-to-Ground Fault", "code": "PGF", "severity": "critical"},
        ],
        "cascading_risk": "high"
    },
    "Transformer": {
        "faults": [
            {"type": "Core Loss", "code": "CL", "severity": "medium"},
            {"type": "Copper Loss", "code": "CPL", "severity": "medium"},
            {"type": "Oil Breakdown", "code": "OB", "severity": "critical"},
            {"type": "Winding Short Circuit", "code": "WSC", "severity": "critical"},
            {"type": "Phase-to-Phase Fault", "code": "PPF", "severity": "high"},
        ],
        "cascading_risk": "critical"
    },
    "Transmission Line": {
        "faults": [
            {"type": "Line-to-Ground (LG)", "code": "LG", "severity": "medium"},
            {"type": "Line-to-Line (LL)", "code": "LL", "severity": "high"},
            {"type": "Line-to-Line-to-Ground (LLG)", "code": "LLG", "severity": "high"},
            {"type": "Three-Phase Fault (LLL)", "code": "LLL", "severity": "critical"},
        ],
        "cascading_risk": "critical"
    },
    "Switchgear": {
        "faults": [
            {"type": "Contact Erosion", "code": "CE", "severity": "medium"},
            {"type": "Arc Tracking", "code": "AT", "severity": "high"},
            {"type": "Insulation Breakdown", "code": "IB", "severity": "critical"},
            {"type": "Trip Failure", "code": "TF", "severity": "critical"},
        ],
        "cascading_risk": "high"
    },
    "Circuit Breaker": {
        "faults": [
            {"type": "Contact Wear", "code": "CW", "severity": "medium"},
            {"type": "Spring Failure", "code": "SF", "severity": "high"},
            {"type": "Trip Unit Failure", "code": "TUF", "severity": "critical"},
            {"type": "Arc Extinguishing Failure", "code": "AEF", "severity": "critical"},
        ],
        "cascading_risk": "high"
    },
    "Induction Motor": {
        "faults": [
            {"type": "Stator Winding Fault", "code": "SWF", "severity": "high"},
            {"type": "Rotor Bar Breakage", "code": "RBB", "severity": "high"},
            {"type": "Bearing Fault", "code": "BF", "severity": "medium"},
            {"type": "Phase Loss", "code": "PL", "severity": "high"},
        ],
        "cascading_risk": "medium"
    },
    "Capacitor Bank": {
        "faults": [
            {"type": "Capacitor Rupture", "code": "CR", "severity": "high"},
            {"type": "Dielectric Breakdown", "code": "DB", "severity": "critical"},
            {"type": "Fuse Failure", "code": "FF", "severity": "medium"},
        ],
        "cascading_risk": "high"
    },
    "Protection Relay": {
        "faults": [
            {"type": "Relay Misoperation", "code": "RM", "severity": "critical"},
            {"type": "Setting Drift", "code": "SD", "severity": "high"},
            {"type": "Communication Failure", "code": "CF", "severity": "high"},
        ],
        "cascading_risk": "critical"
    },
}

# Cascading effects mapping
CASCADING_EFFECTS_MAP = {
    "Generation": {
        "Generator": {
            "Stator Winding Fault": ["Transformer", "Switchgear", "Transmission Line"],
            "Phase-to-Ground Fault": ["Transformer", "Switchgear", "Circuit Breaker"],
        },
        "Transformer": {
            "Oil Breakdown": ["Switchgear", "Generator", "Transmission Line"],
            "Winding Short Circuit": ["Generator", "Switchgear", "Circuit Breaker"],
        },
    },
    "Transmission": {
        "Transmission Line": {
            "Three-Phase Fault (LLL)": ["Transformer", "Switchgear", "Circuit Breaker"],
            "Line-to-Line-to-Ground (LLG)": ["Switchgear", "Circuit Breaker", "Relay"],
        },
        "Transformer": {
            "Oil Breakdown": ["Transmission Line", "Switchgear", "Circuit Breaker"],
            "Winding Short Circuit": ["Transmission Line", "Switchgear"],
        },
        "Switchgear": {
            "Trip Failure": ["Transmission Line", "Circuit Breaker", "Relay"],
        },
    },
    "Distribution": {
        "Transformer": {
            "Winding Short Circuit": ["Motor", "Switchgear", "Circuit Breaker"],
        },
        "Motor": {
            "Stator Winding Fault": ["Transformer", "Switchgear"],
            "Phase Loss": ["Transformer", "Circuit Breaker"],
        },
    },
}


class PowerSystemIntelligenceEngine:
    """Main intelligence engine for power system fault analysis."""

    @staticmethod
    def get_industries():
        """Return list of available industries."""
        return [industry.value for industry in PowerSystemIndustry]

    @staticmethod
    def get_machinery_by_industry(industry):
        """Get available machinery for a given industry."""
        return INDUSTRY_MACHINERY_MAP.get(industry, [])

    @staticmethod
    def get_faults_by_machinery(machinery_type):
        """Get possible faults for a given machinery type."""
        return MACHINERY_FAULT_MAP.get(machinery_type, {})

    @staticmethod
    def analyze_cascading_effects(industry, machinery_type, fault_type):
        """Analyze cascading effects of a fault."""
        if industry not in CASCADING_EFFECTS_MAP:
            return []
        
        industry_map = CASCADING_EFFECTS_MAP[industry]
        if machinery_type not in industry_map:
            return []
        
        machinery_map = industry_map[machinery_type]
        return machinery_map.get(fault_type, [])

    @staticmethod
    def get_cascading_visualization(industry, machinery_type, fault_type):
        """Generate cascading effect visualization data."""
        cascading_effects = PowerSystemIntelligenceEngine.analyze_cascading_effects(
            industry, machinery_type, fault_type
        )
        
        primary_fault_info = MACHINERY_FAULT_MAP.get(machinery_type, {})
        for fault in primary_fault_info.get("faults", []):
            if fault["type"] == fault_type:
                primary_severity = fault.get("severity", "medium")
                break
        else:
            primary_severity = "medium"

        cascade_data = {
            "root_cause": {
                "industry": industry,
                "machinery": machinery_type,
                "fault": fault_type,
                "severity": primary_severity,
            },
            "cascading_effects": [],
            "total_affected_systems": 1 + len(cascading_effects),
        }

        for idx, affected_machinery in enumerate(cascading_effects):
            affected_faults = MACHINERY_FAULT_MAP.get(affected_machinery, {}).get("faults", [])
            cascade_data["cascading_effects"].append({
                "level": idx + 1,
                "affected_machinery": affected_machinery,
                "possible_faults": [f["type"] for f in affected_faults[:2]],
                "cascade_risk": MACHINERY_FAULT_MAP.get(affected_machinery, {}).get("cascading_risk", "medium"),
            })

        return cascade_data

    @staticmethod
    def generate_alert_notification(industry, machinery_type, fault_type, fault_code, confidence=95):
        """Generate an alert notification for a detected fault."""
        severity_levels = {
            "critical": 1,
            "high": 2,
            "medium": 3,
            "low": 4,
        }
        
        fault_info = MACHINERY_FAULT_MAP.get(machinery_type, {})
        fault_details = None
        for f in fault_info.get("faults", []):
            if f["type"] == fault_type:
                fault_details = f
                break

        severity = fault_details.get("severity", "medium") if fault_details else "medium"

        alert = {
            "alert_id": f"ALERT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "alert_level": severity.upper(),
            "priority": severity_levels.get(severity, 3),
            "industry": industry,
            "machinery": machinery_type,
            "fault_type": fault_type,
            "fault_code": fault_code,
            "confidence": confidence,
            "message": f"CRITICAL ALERT: {fault_type} detected in {machinery_type} ({industry} sector)",
            "recommended_action": PowerSystemIntelligenceEngine._get_recommended_action(fault_type),
            "estimated_impact": "System may experience cascading failures if not addressed immediately",
        }
        return alert

    @staticmethod
    def _get_recommended_action(fault_type):
        """Get recommended action based on fault type."""
        actions = {
            "Stator Winding Fault": "Isolate affected equipment immediately. Check winding insulation.",
            "Rotor Winding Fault": "Stop the machine. Inspect rotor windings for damage.",
            "Phase-to-Ground Fault": "Activate protective relays. Isolate faulted phase.",
            "Oil Breakdown": "Shut down transformer immediately. Drain and replace oil.",
            "Winding Short Circuit": "De-energize equipment. Check all windings.",
            "Line-to-Ground (LG)": "Monitor system. Engage protection relays if persistent.",
            "Three-Phase Fault (LLL)": "Immediate circuit isolation required. Maximum cascading risk.",
            "Trip Failure": "Manual disconnection required. Service switchgear.",
        }
        return actions.get(fault_type, "Perform diagnostic and preventive maintenance.")

    @staticmethod
    def generate_iso_compliance_report(industry, machinery_type, fault_type, alert_id):
        """Generate ISO 55001 (Asset Management) compliant report."""
        report = {
            "report_id": f"ISO-RPT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "report_date": datetime.now().isoformat(),
            "compliance_standard": "ISO 55001:2024 (Asset Management)",
            "audit_trail": {
                "alert_id": alert_id,
                "industry_segment": industry,
                "asset_type": machinery_type,
                "fault_classification": fault_type,
            },
            "asset_management_lifecycle": {
                "plan": "Predictive maintenance scheduled quarterly",
                "acquire": "Equipment sourced from certified vendors",
                "use": "Operating within design parameters",
                "maintain": "Preventive maintenance per schedule",
                "dispose": "End-of-life recycling per regulations",
            },
            "risk_assessment": {
                "risk_level": "HIGH",
                "mitigation_required": True,
                "mitigation_steps": [
                    "Immediate equipment isolation",
                    "Diagnostic testing within 24 hours",
                    "Root cause analysis within 48 hours",
                    "Corrective action implementation",
                    "Verification testing before re-commissioning",
                ],
            },
            "documentation": {
                "incident_logged": True,
                "maintenance_record_updated": True,
                "compliance_status": "UNDER_INVESTIGATION",
                "next_review_date": "7 days",
            },
            "legal_and_regulatory": {
                "regulatory_body": "National Grid Authority / Local Authority",
                "compliance_requirement": "Mandatory incident reporting within 24 hours",
                "penalties_for_non_compliance": "Significant fines and operational restrictions",
            },
        }
        return report


class ComplianceAlertService:
    """Service for generating and managing compliance alerts."""

    @staticmethod
    def format_alert_for_display(alert):
        """Format alert for dashboard display."""
        return {
            "alert_id": alert["alert_id"],
            "timestamp": alert["timestamp"],
            "level": alert["alert_level"],
            "priority": alert["priority"],
            "title": f"{alert['fault_code']}: {alert['fault_type']}",
            "machinery": alert["machinery"],
            "industry": alert["industry"],
            "confidence": f"{alert['confidence']}%",
            "message": alert["message"],
            "action": alert["recommended_action"],
        }

    @staticmethod
    def format_report_for_download(report):
        """Format report for PDF/document download."""
        formatted = f"""
========================================
ISO 55001 COMPLIANCE INCIDENT REPORT
========================================

Report ID: {report['report_id']}
Date: {report['report_date']}
Standard: {report['compliance_standard']}

--- INCIDENT DETAILS ---
Alert ID: {report['audit_trail']['alert_id']}
Industry: {report['audit_trail']['industry_segment']}
Equipment: {report['audit_trail']['asset_type']}
Fault Type: {report['audit_trail']['fault_classification']}

--- ASSET MANAGEMENT LIFECYCLE ---
Plan: {report['asset_management_lifecycle']['plan']}
Acquire: {report['asset_management_lifecycle']['acquire']}
Use: {report['asset_management_lifecycle']['use']}
Maintain: {report['asset_management_lifecycle']['maintain']}
Dispose: {report['asset_management_lifecycle']['dispose']}

--- RISK ASSESSMENT ---
Risk Level: {report['risk_assessment']['risk_level']}
Mitigation Required: {report['risk_assessment']['mitigation_required']}

Mitigation Steps:
"""
        for i, step in enumerate(report['risk_assessment']['mitigation_steps'], 1):
            formatted += f"{i}. {step}\n"
        
        formatted += f"""
--- COMPLIANCE STATUS ---
Incident Logged: {report['documentation']['incident_logged']}
Records Updated: {report['documentation']['maintenance_record_updated']}
Status: {report['documentation']['compliance_status']}
Next Review: {report['documentation']['next_review_date']}

--- LEGAL & REGULATORY ---
Regulatory Body: {report['legal_and_regulatory']['regulatory_body']}
Requirement: {report['legal_and_regulatory']['compliance_requirement']}
Penalties: {report['legal_and_regulatory']['penalties_for_non_compliance']}

========================================
"""
        return formatted
