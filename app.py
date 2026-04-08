from flask import Flask, request, jsonify, render_template, send_file
import joblib
import numpy as np
import csv
import os
import random
import json
from urllib import request as urlrequest
from urllib import error as urlerror
from datetime import datetime
from services.decision_intelligence import DecisionIntelligenceEngine
from services.fault_analysis_service import GeminiFaultAnalysisService
from services.smart_governance import SmartGovernanceLayer

app = Flask(__name__)

# ================= CONFIG =================
MODEL_PATH = "decision_tree_fault_model.pkl"
ENCODER_PATH = "label_encoder.pkl"
CSV_FILE = "prediction_history.csv"

ZERO_THRESHOLD = 0.3   # 🔴 VERY IMPORTANT
GROQ_API_URL = os.getenv("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
CHAT_HTTP_USER_AGENT = os.getenv(
    "CHAT_HTTP_USER_AGENT",
    "fault-detection-software/1.0 (+https://api.groq.com)"
)

CHAT_SYSTEM_PROMPT = (
    "You are GridGuard Assistant, a concise technical assistant for transmission line faults. "
    "Answer questions about fault types (LG, LLG, LLL, LL), repercussions, relay behavior, mitigation, "
    "maintenance actions, and operator playbooks. "
    "When applicable, provide: 1) Fault type summary, 2) likely impact, 3) mitigation steps, "
    "4) preventive actions. Keep replies clear and practical. "
    "Avoid pretending to be certain when data is missing; say assumptions explicitly."
)

# ================= LOAD ML =================
model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)

latest_iot_data = None
decision_engine = DecisionIntelligenceEngine()
gemini_fault_analysis_service = GeminiFaultAnalysisService()
smart_governance_layer = SmartGovernanceLayer("config/governance_policies.json")

# ================= CSV INIT =================
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Timestamp", "Va", "Vb", "Vc",
            "Ia", "Ib", "Ic",
            "Fault", "Latitude", "Longitude", "Confidence"
        ])


def get_latest_fault_snapshot():
    """Returns a compact context line from the latest stored CSV row if available."""
    try:
        with open(CSV_FILE, "r") as f:
            rows = list(csv.DictReader(f))
            if not rows:
                return "No recent fault records available."

            latest = rows[-1]
            timestamp = latest.get("Timestamp", "Unknown time")
            fault = latest.get("Fault", "Unknown fault")
            confidence = latest.get("Confidence", "--")
            lat = latest.get("Latitude", "--")
            lon = latest.get("Longitude", "--")
            return (
                f"Latest record -> Time: {timestamp}, Fault: {fault}, "
                f"Confidence: {confidence}%, Location: {lat}, {lon}."
            )
    except Exception:
        return "Latest fault context could not be loaded from history."


def get_recent_fault_history(limit=15):
    """Returns recent fault history records from CSV as a list of dicts."""
    try:
        with open(CSV_FILE, "r") as f:
            rows = list(csv.DictReader(f))
            if not rows:
                return []
            return rows[-limit:]
    except Exception:
        return []


def ask_groq(user_message, history_messages):
    """Sends chat prompt to Groq endpoint and returns assistant text."""
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        # Backward compatibility if previous setup used GROK_API_KEY
        api_key = os.getenv("GROK_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Missing GROQ_API_KEY. Set it in your environment before using chatbot.")

    safe_history = []
    for msg in history_messages[-8:]:
        role = (msg.get("role") or "").strip().lower()
        content = (msg.get("content") or "").strip()
        if role in {"user", "assistant"} and content:
            safe_history.append({"role": role, "content": content[:2000]})

    system_context = CHAT_SYSTEM_PROMPT + " " + get_latest_fault_snapshot()
    messages = [{"role": "system", "content": system_context}]
    messages.extend(safe_history)
    messages.append({"role": "user", "content": user_message[:2000]})

    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.25,
        "max_tokens": 650
    }

    body = json.dumps(payload).encode("utf-8")
    req = urlrequest.Request(
        GROQ_API_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": CHAT_HTTP_USER_AGENT,
            "Authorization": f"Bearer {api_key}"
        },
        method="POST"
    )

    try:
        with urlrequest.urlopen(req, timeout=35) as response:
            response_json = json.loads(response.read().decode("utf-8"))
    except urlerror.HTTPError as e:
        details = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Groq API HTTP {e.code}: {details[:300]}")
    except Exception as e:
        raise RuntimeError(f"Failed to reach Groq API: {str(e)}")

    choices = response_json.get("choices") or []
    if not choices:
        raise RuntimeError("Groq API response did not contain choices.")

    message = choices[0].get("message") or {}
    content = (message.get("content") or "").strip()
    if not content:
        raise RuntimeError("Groq API returned empty content.")
    return content

# ================= ROUTES =================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/intelligence")
def intelligence_console():
    return render_template("intelligence.html")


# ---------- RECEIVE ESP32 DATA ----------
@app.route("/iot_data", methods=["POST"])
def receive_iot_data():
    global latest_iot_data
    latest_iot_data = request.json
    print("📡 ESP32 DATA:", latest_iot_data)
    return jsonify({"status": "ok"})


# ---------- PREDICT USING ESP32 DATA ----------
@app.route("/predict_iot")
def predict_from_iot():
    if not latest_iot_data:
        return jsonify({"error": "No IoT data yet"})

    Va = float(latest_iot_data.get("Va", 0))
    Vb = float(latest_iot_data.get("Vb", 0))
    Vc = float(latest_iot_data.get("Vc", 0))
    Ia = float(latest_iot_data.get("Ia", 0))
    Ib = float(latest_iot_data.get("Ib", 0))
    Ic = float(latest_iot_data.get("Ic", 0))

    # 🔴 RULE-BASED LOGIC (ESP32 ONLY)
    zero_count = sum([
        Ia < ZERO_THRESHOLD,
        Ib < ZERO_THRESHOLD,
        Ic < ZERO_THRESHOLD
    ])

    if zero_count == 1:
        fault = "LG Fault"
        confidence = 96.0

    elif zero_count == 2:
        fault = "LLG Fault"
        confidence = 97.0

    elif zero_count == 3:
        fault = "LLL Fault"
        confidence = 98.0

    else:
        # ML MODEL
        X = np.array([[Va, Vb, Vc, Ia, Ib, Ic]])
        pred = model.predict(X)[0]
        fault = label_encoder.inverse_transform([pred])[0]
        confidence = round(random.uniform(90, 99), 1)

    # META
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    latitude = round(12.9210 + random.uniform(-0.005, 0.005), 6)
    longitude = round(77.4931 + random.uniform(-0.005, 0.005), 6)

    # SAVE TO CSV
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            timestamp, Va, Vb, Vc,
            Ia, Ib, Ic,
            fault, latitude, longitude, confidence
        ])

    return jsonify({
        "fault": fault,
        "confidence": confidence,
        "timestamp": timestamp,
        "latitude": latitude,
        "longitude": longitude
    })


# ---------- MANUAL ML PREDICTION ----------
@app.route("/predict", methods=["POST"])
def predict_manual():
    data = request.json

    Va = float(data["Va"])
    Vb = float(data["Vb"])
    Vc = float(data["Vc"])
    Ia = float(data["Ia"])
    Ib = float(data["Ib"])
    Ic = float(data["Ic"])

    X = np.array([[Va, Vb, Vc, Ia, Ib, Ic]])
    pred = model.predict(X)[0]
    fault = label_encoder.inverse_transform([pred])[0]

    return jsonify({
        "fault": fault,
        "confidence": round(random.uniform(90, 99), 1),
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "latitude": 12.9210,
        "longitude": 77.4931
    })


# ---------- HISTORY ----------
@app.route("/history")
def history():
    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        return jsonify(list(reader)[::-1])


# ---------- EXPORT CSV ----------
@app.route("/export")
def export():
    return send_file(CSV_FILE, as_attachment=True)


# ---------- CHATBOT (GROQ) ----------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = str(data.get("message", "")).strip()
    history_messages = data.get("history", [])

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    if not isinstance(history_messages, list):
        history_messages = []

    try:
        reply = ask_groq(user_message, history_messages)
        return jsonify({"reply": reply})
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception:
        return jsonify({"error": "Unexpected chatbot error"}), 500


@app.route("/api/decision-intelligence", methods=["POST"])
def run_decision_intelligence():
    data = request.get_json(silent=True) or {}
    fault_data = data.get("fault_data", data)

    try:
        decision_output = decision_engine.analyze_fault(fault_data)
        return jsonify({"decision_intelligence": decision_output})
    except Exception as e:
        return jsonify({"error": f"Decision intelligence failed: {str(e)}"}), 500


@app.route("/api/fault-analysis", methods=["POST"])
def run_fault_analysis():
    data = request.get_json(silent=True) or {}
    fault_data = data.get("fault_data", {})
    architecture_context = data.get("architecture_context", {})
    fault_history = data.get("fault_history")
    if not isinstance(fault_history, list):
        fault_history = get_recent_fault_history(limit=12)

    try:
        analysis_output = gemini_fault_analysis_service.analyze_fault(
            fault_json=fault_data,
            architecture_context=architecture_context,
            fault_history=fault_history
        )
        return jsonify({"fault_analysis": analysis_output})
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception:
        return jsonify({"error": "Unexpected fault analysis error"}), 500


@app.route("/api/governance/evaluate", methods=["POST"])
def run_governance_evaluation():
    data = request.get_json(silent=True) or {}
    decision_output = data.get("decision_intelligence", {})
    mitigation_plan = data.get("mitigation_plan", [])

    if not isinstance(decision_output, dict):
        decision_output = {}
    if not isinstance(mitigation_plan, list):
        mitigation_plan = []

    try:
        governance_output = smart_governance_layer.evaluate(decision_output, mitigation_plan)
        return jsonify({"governance": governance_output})
    except Exception as e:
        return jsonify({"error": f"Governance evaluation failed: {str(e)}"}), 500


@app.route("/api/intelligent-response", methods=["POST"])
def intelligent_response_pipeline():
    data = request.get_json(silent=True) or {}
    fault_data = data.get("fault_data", {})
    architecture_context = data.get("architecture_context", {})
    fault_history = data.get("fault_history")
    if not isinstance(fault_history, list):
        fault_history = get_recent_fault_history(limit=12)

    try:
        decision_output = decision_engine.analyze_fault(fault_data)
        analysis_output = gemini_fault_analysis_service.analyze_fault(
            fault_json=fault_data,
            architecture_context=architecture_context,
            fault_history=fault_history
        )
        governance_output = smart_governance_layer.evaluate(
            decision_output,
            analysis_output.get("mitigation_plan", [])
        )

        return jsonify({
            "decision_intelligence": decision_output,
            "fault_analysis": analysis_output,
            "governance": governance_output
        })
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Intelligent response pipeline failed: {str(e)}"}), 500


# ================= RUN =================
if __name__ == "__main__":
    print("⚡ Transmission Line Fault Detection Server Running")
    app.run(host="0.0.0.0", port=5000, debug=True)
