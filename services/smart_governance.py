import json
import os
import queue
import threading
from datetime import datetime


class EventBus:
    """Simple event bus with a background dispatcher thread."""

    def __init__(self):
        self.subscribers = {}
        self.event_queue = queue.Queue()
        self.worker = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker.start()

    def subscribe(self, event_name, callback):
        self.subscribers.setdefault(event_name, []).append(callback)

    def publish(self, event_name, payload):
        self.event_queue.put((event_name, payload))

    def _worker_loop(self):
        while True:
            event_name, payload = self.event_queue.get()
            callbacks = self.subscribers.get(event_name, [])
            for callback in callbacks:
                try:
                    callback(payload)
                except Exception:
                    # Keep dispatcher alive even if one subscriber fails.
                    pass
            self.event_queue.task_done()


class SmartGovernanceLayer:
    """Policy-driven escalation workflow with notifications and audit logs."""

    def __init__(self, policy_file_path):
        self.policy_file_path = policy_file_path
        self.audit_log_path = os.getenv("AUDIT_LOG_PATH", "audit/governance_audit.log")
        self.policies = self._load_policies()
        self.event_bus = EventBus()
        self._ensure_audit_dir()
        self._register_default_subscribers()

    def evaluate(self, decision_output, mitigation_plan):
        risk_score = int(decision_output.get("risk_score", 0))
        severity = str(decision_output.get("severity_escalation", "low")).lower()

        workflow = self._resolve_workflow(risk_score, severity)
        notifications = []
        actions = []

        if workflow == "log_only":
            actions.append("log_event")
        elif workflow == "notify_admin":
            actions.extend(["log_event", "notify_admin"])
            notifications.append(self._mock_notify_admin(decision_output))
        elif workflow == "notify_admin_and_trigger_mitigation":
            actions.extend(["log_event", "notify_admin", "trigger_mitigation"])
            notifications.append(self._mock_notify_admin(decision_output))
            notifications.append(self._mock_trigger_mitigation(mitigation_plan))

        governance_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "workflow": workflow,
            "actions": actions,
            "notifications": notifications,
            "risk_score": risk_score,
            "severity": severity,
            "priority": decision_output.get("priority_level", "unknown")
        }

        self._audit_log(governance_record)
        self.event_bus.publish("governance.action.completed", governance_record)

        return governance_record

    def _resolve_workflow(self, risk_score, severity):
        thresholds = self.policies.get("thresholds", {})
        high_threshold = int(thresholds.get("high_risk_score", 80))
        medium_threshold = int(thresholds.get("medium_risk_score", 45))

        if severity == "critical" or risk_score >= high_threshold:
            return "notify_admin_and_trigger_mitigation"
        if severity == "high" or risk_score >= medium_threshold:
            return "notify_admin"
        return "log_only"

    def _load_policies(self):
        if not os.path.exists(self.policy_file_path):
            return {
                "thresholds": {
                    "medium_risk_score": 45,
                    "high_risk_score": 80
                }
            }

        with open(self.policy_file_path, "r", encoding="utf-8") as policy_file:
            return json.load(policy_file)

    def _ensure_audit_dir(self):
        directory = os.path.dirname(self.audit_log_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

    def _register_default_subscribers(self):
        self.event_bus.subscribe("governance.action.completed", self._console_event_listener)

    def _console_event_listener(self, payload):
        print("[Governance Event]", json.dumps(payload))

    def _mock_notify_admin(self, decision_output):
        summary = (
            f"Admin notified: priority={decision_output.get('priority_level')} "
            f"risk={decision_output.get('risk_score')}"
        )
        print(summary)
        return summary

    def _mock_trigger_mitigation(self, mitigation_plan):
        step_count = len(mitigation_plan) if isinstance(mitigation_plan, list) else 0
        summary = f"Mitigation trigger invoked with {step_count} steps."
        print(summary)
        return summary

    def _audit_log(self, governance_record):
        with open(self.audit_log_path, "a", encoding="utf-8") as audit_file:
            audit_file.write(json.dumps(governance_record) + "\\n")
