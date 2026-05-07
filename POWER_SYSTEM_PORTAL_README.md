# Power System Intelligence Portal - Complete Guide

## Overview

You now have a **comprehensive Power System Intelligence Portal** that replaces the previous intelligence model. This new system is specifically designed for the power system industry and follows your exact requirements.

## Key Features

### 1. **Multi-Step Industry & Machinery Selection**
- **Step 1**: Select your power system industry:
  - ⚡ **Generation** - Power generation facilities (generators, transformers, etc.)
  - 🔌 **Transmission** - High-voltage transmission networks
  - 📡 **Distribution** - Local distribution networks

- **Step 2**: Select machinery type based on selected industry
  - Different equipment types appear based on industry context
  - Each equipment has industry-specific fault profiles

### 2. **Comprehensive Fault Detection**
- **Step 3**: View all possible faults for selected machinery
- Each fault displays:
  - Fault type (e.g., "Stator Winding Fault")
  - Fault code (e.g., "SWF")
  - Severity level (Critical, High, Medium, Low)
- Select a fault to trigger detailed analysis

### 3. **Visual Cascading Effect Analysis**
- **Step 4**: See how faults cascade through the system
- Displays:
  - Root cause fault and its severity
  - All affected systems (Level 1, Level 2, etc. impacts)
  - Cascade risk for each affected system
  - Possible faults in downstream equipment
- Visual animation shows the propagation chain

### 4. **Alert Notifications**
- Real-time alert generation with:
  - Alert ID (unique timestamp-based identifier)
  - Alert level (CRITICAL, HIGH, MEDIUM, LOW)
  - Priority ranking
  - Recommended immediate actions
  - Confidence percentage
  - Estimated system impact

### 5. **ISO 55001 Compliance Reporting**
- Generates compliance reports following **ISO 55001:2024 (Asset Management)**
- Includes:
  - Incident audit trail
  - Asset management lifecycle status (Plan, Acquire, Use, Maintain, Dispose)
  - Risk assessment and mitigation steps
  - Legal & regulatory requirements
  - Compliance documentation status
  - Report downloadable as text file

## How to Use

### Starting the Application

1. **Install Dependencies** (if not already installed):
   ```bash
   python -m pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```
   The server will start at `http://localhost:5000`

3. **Access the Portal**:
   - Navigate to `http://localhost:5000/intelligence`

### Workflow

1. **Select Industry** → Choose Generation, Transmission, or Distribution
2. **Select Machinery** → Pick equipment type for that industry
3. **View Faults** → See all possible faults for that equipment
4. **Analyze Fault** → Select a fault to trigger analysis
5. **View Cascading Effects** → See how the fault propagates
6. **Review Compliance Report** → View ISO 55001 report with alert
7. **Download Report** → Save as text file for compliance documentation

## Supported Equipment & Faults

### Generation Industry
- **Generator**: Stator Winding Fault, Rotor Winding Fault, Air Gap Eccentricity, Phase-to-Ground Fault
- **Transformer**: Core Loss, Copper Loss, Oil Breakdown, Winding Short Circuit, Phase-to-Phase Fault
- **Switchgear**: Contact Erosion, Arc Tracking, Insulation Breakdown, Trip Failure
- **Capacitor Bank**: Capacitor Rupture, Dielectric Breakdown, Fuse Failure
- **Protection Relay**: Relay Misoperation, Setting Drift, Communication Failure

### Transmission Industry
- **Transmission Line**: Line-to-Ground (LG), Line-to-Line (LL), Line-to-Line-to-Ground (LLG), Three-Phase Fault (LLL)
- **Transformer**: Same as Generation
- **Switchgear**: Same as Generation
- **Circuit Breaker**: Contact Wear, Spring Failure, Trip Unit Failure, Arc Extinguishing Failure
- **Protection Relay**: Same as Generation
- **Capacitor Bank**: Same as Generation

### Distribution Industry
- **Transformer**: Same as Generation
- **Switchgear**: Same as Generation
- **Circuit Breaker**: Same as Transmission
- **Motor**: Stator Winding Fault, Rotor Bar Breakage, Bearing Fault, Phase Loss
- **Capacitor Bank**: Same as Generation

## API Endpoints

All endpoints are available for programmatic access:

```
GET  /api/power-system/machinery?industry=Generation
GET  /api/power-system/faults?machinery=Generator
GET  /api/power-system/cascading?industry=Generation&machinery=Generator&fault=Stator Winding Fault
POST /api/power-system/alert
POST /api/power-system/compliance-report
```

## Data Structure

### Alert Notification Response
```json
{
  "alert_id": "ALERT-20260507143022",
  "timestamp": "2026-05-07T14:30:22.123456",
  "alert_level": "CRITICAL",
  "priority": 1,
  "industry": "Generation",
  "machinery": "Generator",
  "fault_type": "Stator Winding Fault",
  "fault_code": "SWF",
  "confidence": 95,
  "message": "CRITICAL ALERT: Stator Winding Fault detected in Generator (Generation sector)",
  "recommended_action": "Isolate affected equipment immediately. Check winding insulation.",
  "estimated_impact": "System may experience cascading failures if not addressed immediately"
}
```

### ISO 55001 Compliance Report Response
```json
{
  "report_id": "ISO-RPT-20260507143022",
  "report_date": "2026-05-07T14:30:22.123456",
  "compliance_standard": "ISO 55001:2024 (Asset Management)",
  "audit_trail": { ... },
  "asset_management_lifecycle": { ... },
  "risk_assessment": { ... },
  "documentation": { ... },
  "legal_and_regulatory": { ... }
}
```

## Key Differences from Previous Model

| Aspect | Old Model | New Model |
|--------|-----------|-----------|
| **Focus** | Generic fault analysis pipeline | Power system industry-specific |
| **Workflow** | JSON input-based | Interactive step-by-step portal |
| **Industry Context** | Single-size-fits-all | Industry & equipment-specific |
| **Cascading Effects** | Graph-based generic | Power system specific cascade chains |
| **Compliance** | Generic governance | ISO 55001 asset management standard |
| **UI** | Technical input/output | User-friendly wizard interface |
| **Reports** | System architecture focused | Compliance & regulatory focused |

## Cascading Effect Logic

The portal uses industry and equipment-specific cascading maps to show how faults spread:

1. **Root Cause Identification**: Primary fault in selected equipment
2. **Impact Analysis**: Identifies all systems that depend on the failed equipment
3. **Risk Propagation**: Shows severity escalation through cascade levels
4. **Mitigation Recommendations**: Provides specific actions for each affected system

## Compliance Features

- ✅ **ISO 55001:2024 Compliant** - Follows asset management best practices
- ✅ **Audit Trail** - Complete incident logging with timestamps
- ✅ **Risk Assessment** - Documented risk levels and mitigation steps
- ✅ **Regulatory Alignment** - References national grid authority requirements
- ✅ **Incident Tracking** - All alerts logged with compliance status
- ✅ **Downloadable Reports** - Export for compliance documentation

## System Architecture

```
┌─────────────────────────────────────────────┐
│   Power System Intelligence Portal UI       │
│   (intelligence.html with Tailwind CSS)     │
└────────────┬────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────┐
│   Flask REST API Routes                     │
│   (/api/power-system/*)                     │
└────────────┬────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────┐
│   PowerSystemIntelligenceEngine             │
│   (services/power_system_intelligence.py)   │
├─────────────────────────────────────────────┤
│ • Industry/Machinery Mapping                │
│ • Fault Database                            │
│ • Cascading Effect Analysis                 │
│ • Alert Generation                          │
│ • ISO 55001 Report Generation               │
└─────────────────────────────────────────────┘
```

## Troubleshooting

### Portal Not Loading
- Ensure Flask is running: `python app.py`
- Check browser console (F12) for errors
- Verify port 5000 is not in use

### API Errors
- Check that industry, machinery, and fault names match exactly
- View API responses in browser Network tab
- Ensure all required parameters are provided

### Report Generation Issues
- Verify alert was generated first
- Check that fault_type matches exactly from the fault list
- Ensure alert_id is properly returned from alert endpoint

## Future Enhancements

Possible additions to the system:
- Historical fault data analytics
- Predictive maintenance scheduling
- Real-time grid monitoring integration
- Advanced cascading effect simulation with physics models
- Mobile app version
- Database persistence for audit trails
- Integration with SCADA systems
- Automated alert escalation workflows

## Support

For issues or feature requests related to the power system intelligence portal, check:
1. This README
2. API endpoint responses for error messages
3. Browser console for JavaScript errors
4. Application server logs

---

**Version**: 1.0  
**Last Updated**: May 7, 2026  
**Compliance**: ISO 55001:2024  
**Industry**: Power Systems (Generation, Transmission, Distribution)
