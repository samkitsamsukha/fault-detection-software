const service = new window.FaultAnalysisService();

const ids = {
    faultJson: document.getElementById("faultJson"),
    archJson: document.getElementById("archJson"),
    historyJson: document.getElementById("historyJson"),
    runBtn: document.getElementById("runBtn"),
    status: document.getElementById("status"),
    output: document.getElementById("output"),
    kpiRisk: document.getElementById("kpiRisk"),
    kpiPriority: document.getElementById("kpiPriority"),
    kpiWorkflow: document.getElementById("kpiWorkflow"),
    decisionSeed: document.getElementById("decisionSeed"),
    decisionSeverity: document.getElementById("decisionSeverity"),
    decisionImpacted: document.getElementById("decisionImpacted"),
    aiRootCause: document.getElementById("aiRootCause"),
    aiMitigation: document.getElementById("aiMitigation"),
    aiPrevention: document.getElementById("aiPrevention"),
    govWorkflow: document.getElementById("govWorkflow"),
    govActions: document.getElementById("govActions"),
    govNotifications: document.getElementById("govNotifications")
};

function setStatus(text, isError = false) {
    ids.status.textContent = text;
    ids.status.className = isError
        ? "text-sm font-semibold text-red-700"
        : "text-sm font-semibold text-slate-700";
}

function parseJson(text, fallback) {
    if (!text || !text.trim()) {
        return fallback;
    }
    return JSON.parse(text);
}

function prettyPrint(obj) {
    ids.output.textContent = JSON.stringify(obj, null, 2);
}

function fillList(target, values, ordered = false) {
    if (!target) {
        return;
    }
    target.innerHTML = "";

    const safeValues = Array.isArray(values) ? values : [];
    if (!safeValues.length) {
        const li = document.createElement("li");
        li.textContent = "No data";
        target.appendChild(li);
        return;
    }

    safeValues.forEach((value) => {
        const item = document.createElement("li");
        item.textContent = String(value);
        target.appendChild(item);
    });

    if (ordered && target.tagName.toLowerCase() !== "ol") {
        target.style.listStyleType = "decimal";
    }
}

function renderImpactedComponents(components) {
    ids.decisionImpacted.innerHTML = "";
    const safeValues = Array.isArray(components) ? components : [];

    if (!safeValues.length) {
        const empty = document.createElement("span");
        empty.className = "rounded-full border border-white/20 px-3 py-1 text-xs text-slate-200";
        empty.textContent = "No impacted components";
        ids.decisionImpacted.appendChild(empty);
        return;
    }

    safeValues.forEach((component) => {
        const chip = document.createElement("span");
        chip.className = "rounded-full border border-emerald-300/35 bg-emerald-300/10 px-3 py-1 text-xs font-semibold text-emerald-100";
        chip.textContent = component;
        ids.decisionImpacted.appendChild(chip);
    });
}

function renderModules(result) {
    const decision = result.decision_intelligence || {};
    const analysis = result.fault_analysis || {};
    const governance = result.governance || {};

    ids.kpiRisk.textContent = decision.risk_score != null ? String(decision.risk_score) : "--";
    ids.kpiPriority.textContent = decision.priority_level || "--";
    ids.kpiWorkflow.textContent = governance.workflow || "--";

    ids.decisionSeed.textContent = decision.seed_component || "--";
    ids.decisionSeverity.textContent = decision.severity_escalation || "--";
    renderImpactedComponents(decision.impacted_components);

    ids.aiRootCause.textContent = analysis.root_cause_explanation || "No explanation available.";
    fillList(ids.aiMitigation, analysis.mitigation_plan, true);
    fillList(ids.aiPrevention, analysis.preventive_recommendations, false);

    ids.govWorkflow.textContent = governance.workflow || "--";
    ids.govActions.textContent = Array.isArray(governance.actions) && governance.actions.length
        ? governance.actions.join(", ")
        : "--";
    fillList(ids.govNotifications, governance.notifications, false);
}

async function runPipeline() {
    ids.runBtn.disabled = true;
    setStatus("Running decision intelligence + Gemini analysis + smart governance...");

    try {
        const payload = {
            fault_data: parseJson(ids.faultJson.value, {}),
            architecture_context: parseJson(ids.archJson.value, {}),
            fault_history: parseJson(ids.historyJson.value, [])
        };

        const result = await service.runIntelligentResponse(payload);
        renderModules(result);
        prettyPrint(result);
        setStatus("Pipeline completed successfully.");
    } catch (error) {
        setStatus(error.message || "Request failed", true);
    } finally {
        ids.runBtn.disabled = false;
    }
}

ids.runBtn.addEventListener("click", runPipeline);
