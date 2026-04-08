import math
from collections import deque


class DecisionIntelligenceEngine:
    """Graph-based impact and cascade analyzer for detected faults."""

    SEVERITY_ORDER = ["low", "medium", "high", "critical"]
    SEVERITY_TO_INDEX = {label: index for index, label in enumerate(SEVERITY_ORDER)}

    def __init__(self, dependency_graph=None):
        self.dependency_graph = dependency_graph or self._default_dependency_graph()

    def _default_dependency_graph(self):
        # Directed graph: key component failure can affect each downstream component.
        return {
            "grid_sensor_network": ["fault_detection_service", "telemetry_api"],
            "telemetry_api": ["fault_detection_service", "historian_db"],
            "fault_detection_service": ["decision_engine", "alert_dispatcher"],
            "decision_engine": ["governance_layer", "mitigation_orchestrator"],
            "governance_layer": ["alert_dispatcher", "audit_service"],
            "mitigation_orchestrator": ["switch_controller", "workorder_service"],
            "switch_controller": ["substation_relay_cluster"],
            "substation_relay_cluster": ["power_distribution_core"],
            "historian_db": ["reporting_service", "ai_analysis_service"],
            "ai_analysis_service": ["decision_engine"],
            "alert_dispatcher": ["notification_gateway"],
            "notification_gateway": ["admin_console"],
            "admin_console": [],
            "audit_service": [],
            "workorder_service": [],
            "reporting_service": [],
            "power_distribution_core": []
        }

    def analyze_fault(self, fault_data):
        fault_data = fault_data or {}

        seed_component = str(fault_data.get("component", "fault_detection_service")).strip()
        if not seed_component:
            seed_component = "fault_detection_service"

        base_severity = str(fault_data.get("severity", "medium")).strip().lower()
        if base_severity not in self.SEVERITY_TO_INDEX:
            base_severity = "medium"

        confidence = self._safe_float(fault_data.get("confidence", 75.0), 75.0)

        impacted_components, max_depth = self._simulate_cascade(seed_component)
        cascade_detected = len(impacted_components) > 1 and max_depth > 0

        escalated_severity = self._escalate_severity(base_severity, max_depth)
        risk_score = self._compute_risk_score(
            base_severity=base_severity,
            escalated_severity=escalated_severity,
            impacted_count=len(impacted_components),
            max_depth=max_depth,
            confidence=confidence,
            cascade_detected=cascade_detected
        )
        priority = self._priority_from_risk(risk_score)

        return {
            "fault_id": fault_data.get("fault_id"),
            "fault_type": fault_data.get("fault_type", "unknown"),
            "seed_component": seed_component,
            "impacted_components": impacted_components,
            "cascade_detected": cascade_detected,
            "severity_input": base_severity,
            "severity_escalation": escalated_severity,
            "risk_score": risk_score,
            "priority_level": priority,
            "analysis_factors": {
                "max_cascade_depth": max_depth,
                "impacted_count": len(impacted_components),
                "confidence": round(confidence, 2)
            }
        }

    def _simulate_cascade(self, seed_component):
        visited = set()
        queue = deque([(seed_component, 0)])
        impacted = []
        max_depth = 0

        while queue:
            component, depth = queue.popleft()
            if component in visited:
                continue

            visited.add(component)
            impacted.append(component)
            max_depth = max(max_depth, depth)

            for downstream in self.dependency_graph.get(component, []):
                if downstream not in visited:
                    queue.append((downstream, depth + 1))

        return impacted, max_depth

    def _escalate_severity(self, base_severity, depth):
        index = self.SEVERITY_TO_INDEX[base_severity]

        if depth >= 4:
            index = min(index + 2, len(self.SEVERITY_ORDER) - 1)
        elif depth >= 2:
            index = min(index + 1, len(self.SEVERITY_ORDER) - 1)

        return self.SEVERITY_ORDER[index]

    def _compute_risk_score(self, base_severity, escalated_severity, impacted_count, max_depth, confidence, cascade_detected):
        base = (self.SEVERITY_TO_INDEX[base_severity] + 1) * 15
        escalated = (self.SEVERITY_TO_INDEX[escalated_severity] + 1) * 8

        impact_term = min(impacted_count * 3.5, 25)
        depth_term = min(max_depth * 7, 21)
        confidence_term = min(max(confidence, 0), 100) * 0.12
        cascade_term = 10 if cascade_detected else 0

        raw_score = base + escalated + impact_term + depth_term + confidence_term + cascade_term
        return int(max(0, min(100, math.floor(raw_score))))

    def _priority_from_risk(self, risk_score):
        if risk_score >= 85:
            return "P1 - Critical"
        if risk_score >= 65:
            return "P2 - High"
        if risk_score >= 40:
            return "P3 - Medium"
        return "P4 - Low"

    def _safe_float(self, value, default):
        try:
            return float(value)
        except (TypeError, ValueError):
            return float(default)
