class FaultAnalysisService {
    constructor(baseUrl = "") {
        this.baseUrl = baseUrl;
    }

    async interpretFault(payload) {
        const response = await fetch(`${this.baseUrl}/api/fault-analysis`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Fault analysis request failed");
        }
        return data;
    }

    async runDecisionEngine(payload) {
        const response = await fetch(`${this.baseUrl}/api/decision-intelligence`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Decision intelligence request failed");
        }
        return data;
    }

    async runGovernance(payload) {
        const response = await fetch(`${this.baseUrl}/api/governance/evaluate`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Governance evaluation failed");
        }
        return data;
    }

    async runIntelligentResponse(payload) {
        const response = await fetch(`${this.baseUrl}/api/intelligent-response`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Intelligent response pipeline failed");
        }
        return data;
    }
}

window.FaultAnalysisService = FaultAnalysisService;
