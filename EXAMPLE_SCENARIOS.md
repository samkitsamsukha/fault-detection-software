# Power System Intelligence Portal - Example Scenarios

This document shows real examples of what the portal outputs for different fault scenarios.

---

## Scenario 1: Transmission Line Three-Phase Fault

### User Selections:
- **Industry**: Transmission
- **Machinery**: Transmission Line
- **Fault**: Three-Phase Fault (LLL)

### Portal Output:

#### STEP 4: Cascading Effects Visualization
```
═══════════════════════════════════════════════════════════════
ROOT CAUSE ANALYSIS
═══════════════════════════════════════════════════════════════
Fault Type: Three-Phase Fault (LLL)
Equipment: Transmission Line (Transmission sector)
Severity: CRITICAL
Code: LLL
═══════════════════════════════════════════════════════════════

⚠️ 4 System(s) At Risk

├─ Level 1 Impact: Switchgear
│  Cascade Risk: HIGH
│  Possible Faults: Trip Failure, Insulation Breakdown
│
├─ Level 2 Impact: Circuit Breaker  
│  Cascade Risk: HIGH
│  Possible Faults: Arc Extinguishing Failure, Spring Failure
│
├─ Level 3 Impact: Protection Relay
│  Cascade Risk: CRITICAL
│  Possible Faults: Relay Misoperation, Communication Failure
│
└─ Level 4 Impact: Transformer
   Cascade Risk: CRITICAL
   Possible Faults: Winding Short Circuit, Oil Breakdown
```

#### STEP 5: Alert Notification
```
═══════════════════════════════════════════════════════════════
⚠️ CRITICAL ALERT - LLL: Three-Phase Fault
═══════════════════════════════════════════════════════════════
Alert ID: ALERT-20260507143456
Timestamp: 2026-05-07 14:34:56

Alert Level: 🔴 CRITICAL
Priority: P1 (Highest)

Industry Sector: Transmission
Equipment: Transmission Line
Fault Type: Three-Phase Fault (LLL)
Confidence: 95%

Message: CRITICAL ALERT: Three-Phase Fault (LLL) detected in 
Transmission Line (Transmission sector)

Recommended Action:
→ Immediate circuit isolation required. Maximum cascading risk.

System Impact:
→ System may experience cascading failures if not addressed 
  immediately
═══════════════════════════════════════════════════════════════
```

#### STEP 5: ISO 55001 Compliance Report
```
════════════════════════════════════════════════════════════════
ISO 55001 COMPLIANCE INCIDENT REPORT
════════════════════════════════════════════════════════════════

Report ID: ISO-RPT-20260507143456
Date: 2026-05-07 14:34:56
Compliance Standard: ISO 55001:2024 (Asset Management)

--- INCIDENT DETAILS ---
Alert ID: ALERT-20260507143456
Industry: Transmission
Equipment: Transmission Line
Fault Type: Three-Phase Fault (LLL)
Confidence: 95%

--- ASSET MANAGEMENT LIFECYCLE ---
Plan: Quarterly predictive maintenance
Acquire: Certified vendors only
Use: Operating within design specifications
Maintain: According to maintenance schedule
Dispose: Per environmental regulations

--- RISK ASSESSMENT ---
Risk Level: HIGH
Mitigation Required: Yes

Mitigation Steps:
1. Immediate equipment isolation
2. Diagnostic testing within 24 hours
3. Root cause analysis within 48 hours
4. Corrective action implementation
5. Verification testing before re-commissioning

--- COMPLIANCE STATUS ---
Incident Logged: Yes
Records Updated: Yes
Status: UNDER_INVESTIGATION
Next Review: 7 days

--- LEGAL & REGULATORY ---
Regulatory Body: National Grid Authority
Requirement: Mandatory incident reporting within 24 hours
Penalties: Significant fines and operational restrictions

════════════════════════════════════════════════════════════════
Generated: 2026-05-07 14:34:56
```

---

## Scenario 2: Generator Stator Winding Fault

### User Selections:
- **Industry**: Generation
- **Machinery**: Generator
- **Fault**: Stator Winding Fault

### Portal Output:

#### STEP 4: Cascading Effects
```
═══════════════════════════════════════════════════════════════
ROOT CAUSE ANALYSIS
═══════════════════════════════════════════════════════════════
Fault Type: Stator Winding Fault
Equipment: Generator (Generation sector)
Severity: CRITICAL
Code: SWF
═══════════════════════════════════════════════════════════════

⚠️ 3 System(s) At Risk

├─ Level 1 Impact: Transformer
│  Cascade Risk: CRITICAL
│  Possible Faults: Winding Short Circuit, Oil Breakdown
│
├─ Level 2 Impact: Switchgear
│  Cascade Risk: HIGH
│  Possible Faults: Trip Failure, Contact Erosion
│
└─ Level 3 Impact: Transmission Line
   Cascade Risk: CRITICAL
   Possible Faults: Line-to-Line Fault, Three-Phase Fault
```

#### STEP 5: Alert
```
Alert ID: ALERT-20260507150322
Alert Level: 🔴 CRITICAL
Confidence: 95%

Recommended Action:
→ Isolate affected equipment immediately. Check winding insulation.

System Impact:
→ Power generation capacity reduced. Risk of widespread outage.
```

#### Mitigation Steps:
```
1. Immediate equipment isolation
2. Diagnostic testing within 24 hours
3. Root cause analysis within 48 hours
4. Corrective action implementation
5. Verification testing before re-commissioning
```

---

## Scenario 3: Distribution Transformer Oil Breakdown

### User Selections:
- **Industry**: Distribution
- **Machinery**: Transformer
- **Fault**: Oil Breakdown

### Portal Output:

#### STEP 4: Cascading Effects
```
ROOT CAUSE: Oil Breakdown in Transformer (Distribution sector)
Severity: CRITICAL

⚠️ 3 System(s) At Risk

├─ Level 1 Impact: Motor
│  Cascade Risk: HIGH
│  Possible Faults: Phase Loss, Stator Winding Fault
│
├─ Level 2 Impact: Switchgear
│  Cascade Risk: HIGH
│  Possible Faults: Contact Erosion, Trip Failure
│
└─ Level 3 Impact: Circuit Breaker
   Cascade Risk: HIGH
   Possible Faults: Spring Failure, Trip Unit Failure
```

#### Alert Details:
```
Alert ID: ALERT-20260507152145
Alert Level: 🔴 CRITICAL
Priority: P1

Recommended Action:
→ Shut down transformer immediately. Drain and replace oil.

System Impact:
→ Distribution network segment offline. Customer service disruption.

Confidence: 95%
```

---

## Scenario 4: Transmission Switchgear Trip Failure

### User Selections:
- **Industry**: Transmission
- **Machinery**: Switchgear
- **Fault**: Trip Failure

### Portal Output:

#### STEP 4: Cascading Effects
```
ROOT CAUSE: Trip Failure in Switchgear (Transmission sector)
Severity: CRITICAL

⚠️ 3 System(s) At Risk

├─ Level 1 Impact: Transmission Line
│  Cascade Risk: CRITICAL
│  Possible Faults: Line-to-Line Fault, Three-Phase Fault
│
├─ Level 2 Impact: Circuit Breaker
│  Cascade Risk: HIGH
│  Possible Faults: Contact Wear, Spring Failure
│
└─ Level 3 Impact: Protection Relay
   Cascade Risk: CRITICAL
   Possible Faults: Relay Misoperation, Setting Drift
```

#### Alert
```
Alert ID: ALERT-20260507154628
Alert Level: 🔴 CRITICAL
Priority: P1

Recommended Action:
→ Manual disconnection required. Service switchgear.

Confidence: 95%
Risk Level: CRITICAL - Maximum system risk
```

---

## API Response Examples

### 1. Get Machinery for Generation Industry
```bash
$ curl "http://localhost:5000/api/power-system/machinery?industry=Generation"

["Generator", "Transformer", "Switchgear", "Capacitor Bank", "Protection Relay"]
```

### 2. Get Faults for Transformer
```bash
$ curl "http://localhost:5000/api/power-system/faults?machinery=Transformer"

{
  "faults": [
    {
      "type": "Core Loss",
      "code": "CL",
      "severity": "medium"
    },
    {
      "type": "Copper Loss",
      "code": "CPL",
      "severity": "medium"
    },
    {
      "type": "Oil Breakdown",
      "code": "OB",
      "severity": "critical"
    },
    {
      "type": "Winding Short Circuit",
      "code": "WSC",
      "severity": "critical"
    },
    {
      "type": "Phase-to-Phase Fault",
      "code": "PPF",
      "severity": "high"
    }
  ],
  "cascading_risk": "critical"
}
```

### 3. Get Cascading Effects
```bash
$ curl "http://localhost:5000/api/power-system/cascading?industry=Transmission&machinery=Transmission+Line&fault=Three-Phase+Fault"

{
  "root_cause": {
    "industry": "Transmission",
    "machinery": "Transmission Line",
    "fault": "Three-Phase Fault (LLL)",
    "severity": "critical"
  },
  "cascading_effects": [
    {
      "level": 1,
      "affected_machinery": "Switchgear",
      "possible_faults": ["Trip Failure", "Insulation Breakdown"],
      "cascade_risk": "high"
    },
    {
      "level": 2,
      "affected_machinery": "Circuit Breaker",
      "possible_faults": ["Arc Extinguishing Failure", "Spring Failure"],
      "cascade_risk": "high"
    }
  ],
  "total_affected_systems": 3
}
```

### 4. Generate Alert
```bash
$ curl -X POST "http://localhost:5000/api/power-system/alert" \
  -H "Content-Type: application/json" \
  -d '{
    "industry": "Transmission",
    "machinery": "Transmission Line",
    "fault_type": "Three-Phase Fault (LLL)",
    "fault_code": "LLL",
    "confidence": 95
  }'

{
  "alert_id": "ALERT-20260507160000",
  "timestamp": "2026-05-07T16:00:00.000000",
  "alert_level": "CRITICAL",
  "priority": 1,
  "industry": "Transmission",
  "machinery": "Transmission Line",
  "fault_type": "Three-Phase Fault (LLL)",
  "fault_code": "LLL",
  "confidence": 95,
  "message": "CRITICAL ALERT: Three-Phase Fault (LLL) detected in Transmission Line (Transmission sector)",
  "recommended_action": "Immediate circuit isolation required. Maximum cascading risk.",
  "estimated_impact": "System may experience cascading failures if not addressed immediately"
}
```

### 5. Generate Compliance Report
```bash
$ curl -X POST "http://localhost:5000/api/power-system/compliance-report" \
  -H "Content-Type: application/json" \
  -d '{
    "industry": "Transmission",
    "machinery": "Transmission Line",
    "fault_type": "Three-Phase Fault (LLL)",
    "alert_id": "ALERT-20260507160000"
  }'

{
  "report_id": "ISO-RPT-20260507160000",
  "report_date": "2026-05-07T16:00:00.000000",
  "compliance_standard": "ISO 55001:2024 (Asset Management)",
  "audit_trail": {
    "alert_id": "ALERT-20260507160000",
    "industry_segment": "Transmission",
    "asset_type": "Transmission Line",
    "fault_classification": "Three-Phase Fault (LLL)"
  },
  "asset_management_lifecycle": {
    "plan": "Predictive maintenance scheduled quarterly",
    "acquire": "Equipment sourced from certified vendors",
    "use": "Operating within design parameters",
    "maintain": "Preventive maintenance per schedule",
    "dispose": "End-of-life recycling per regulations"
  },
  "risk_assessment": {
    "risk_level": "HIGH",
    "mitigation_required": true,
    "mitigation_steps": [
      "Immediate equipment isolation",
      "Diagnostic testing within 24 hours",
      "Root cause analysis within 48 hours",
      "Corrective action implementation",
      "Verification testing before re-commissioning"
    ]
  },
  "documentation": {
    "incident_logged": true,
    "maintenance_record_updated": true,
    "compliance_status": "UNDER_INVESTIGATION",
    "next_review_date": "7 days"
  },
  "legal_and_regulatory": {
    "regulatory_body": "National Grid Authority / Local Authority",
    "compliance_requirement": "Mandatory incident reporting within 24 hours",
    "penalties_for_non_compliance": "Significant fines and operational restrictions"
  }
}
```

---

## Downloadable Report Example

When user clicks "Download Report", a text file is generated:

**Filename**: `ISO-55001-Report-ISO-RPT-20260507160000.txt`

```
ISO 55001 COMPLIANCE INCIDENT REPORT
=====================================

Report ID: ISO-RPT-20260507160000
Date: 2026-05-07T16:00:00.000000
Compliance Standard: ISO 55001:2024 (Asset Management)

--- INCIDENT DETAILS ---
Alert ID: ALERT-20260507160000
Industry: Transmission
Equipment: Transmission Line
Fault Type: Three-Phase Fault (LLL)
Confidence: 95%

--- ASSET MANAGEMENT LIFECYCLE ---
Plan: Predictive maintenance scheduled quarterly
Acquire: Equipment sourced from certified vendors
Use: Operating within design parameters
Maintain: Preventive maintenance per schedule
Dispose: End-of-life recycling per regulations

--- RISK ASSESSMENT ---
Risk Level: HIGH
Mitigation Required: True

Mitigation Steps:
1. Immediate equipment isolation
2. Diagnostic testing within 24 hours
3. Root cause analysis within 48 hours
4. Corrective action implementation
5. Verification testing before re-commissioning

--- COMPLIANCE STATUS ---
Incident Logged: True
Records Updated: True
Status: UNDER_INVESTIGATION
Next Review: 7 days

--- LEGAL & REGULATORY ---
Regulatory Body: National Grid Authority / Local Authority
Requirement: Mandatory incident reporting within 24 hours
Penalties: Significant fines and operational restrictions

=====================================
Generated: 2026-05-07 16:00:00
```

---

## UI Screenshots Description

### Portal Step-by-Step:

1. **Industry Selection Screen**
   - Three large cards with icons (⚡🔌📡)
   - Labels: Generation, Transmission, Distribution
   - Hover effects on cards

2. **Machinery Selection Screen**
   - Grid of equipment cards for selected industry
   - Each card shows equipment name and type
   - Hover effects and selection states

3. **Fault Analysis Screen**
   - List of faults color-coded by severity
   - Severity badges (CRITICAL, HIGH, MEDIUM, LOW)
   - Fault codes displayed
   - Each fault clickable

4. **Cascading Effects Screen**
   - Red box showing root cause with severity
   - Animated cascade cards showing impacted systems
   - Level indicators (Level 1, Level 2, etc.)
   - Risk assessment for each level

5. **Compliance Report Screen**
   - Large alert box at top (red for critical)
   - Report ID and timestamp
   - Lifecycle stages in boxes
   - Mitigation steps as numbered list
   - Download and New Analysis buttons

---

## Key Output Characteristics

✅ **All outputs follow ISO 55001:2024 standards**  
✅ **Alerts always include recommended actions**  
✅ **Reports are downloadable and compliance-ready**  
✅ **Cascading effects show industry-specific chains**  
✅ **All timestamps are ISO 8601 formatted**  
✅ **Confidence levels always shown (typically 95%)**  
✅ **Risk assessments include specific mitigation steps**  

---

This document shows what users will experience when using the Power System Intelligence Portal. All outputs are real examples of the system's capabilities.
