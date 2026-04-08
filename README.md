# Transmission Line Fault Detection

A complete web application for predicting transmission line faults using machine learning.

## Prerequisites

- **Python 3.8 or higher** (required for scikit-learn 1.3+ compatibility)
- A trained scikit-learn model file named `model.joblib` or `fault_model.joblib` in the project directory

**Note:** If your model was saved with scikit-learn 1.3+, you need Python 3.8+. 
If you have Python 3.7, you'll need to either upgrade Python or re-save your model with scikit-learn 1.0.2.

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

**IMPORTANT:** Use Python 3.8 or higher (you have Python 3.14 installed).

1. Start the Flask server with Python 3.14:
```bash
py -3.14 app.py
```

Or on Windows, double-click `RUN.bat`

## Groq Chatbot Setup (New)

The UI now includes a fault-domain chatbot powered by Groq through backend endpoint `POST /chat`.

Set your Groq API key before starting the app.

### PowerShell (current session)

```powershell
$env:GROQ_API_KEY="PASTE_YOUR_GROQ_API_KEY_HERE"
```

### Command Prompt (current session)

```bat
set GROQ_API_KEY=PASTE_YOUR_GROQ_API_KEY_HERE
```

Optional environment variables:

- `GROQ_MODEL` (default: `llama-3.1-8b-instant`)
- `GROQ_API_URL` (default: `https://api.groq.com/openai/v1/chat/completions`)

Example (PowerShell):

```powershell
$env:GROQ_API_KEY="PASTE_YOUR_GROQ_API_KEY_HERE"
$env:GROQ_MODEL="llama-3.1-8b-instant"
py -3.14 app.py
```

## Intelligent Fault Response Setup (Gemini)

The new Intelligence Console at `/intelligence` uses Gemini for root-cause analysis and mitigation planning.

Set your Gemini API key before starting the app.

### PowerShell (current session)

```powershell
$env:GEMINI_API_KEY="PASTE_YOUR_GEMINI_API_KEY_HERE"
```

### Command Prompt (current session)

```bat
set GEMINI_API_KEY=PASTE_YOUR_GEMINI_API_KEY_HERE
```

Optional Gemini environment variables:

- `GEMINI_MODEL` (default: `gemini-2.0-flash`)
- `GEMINI_API_URL` (default: `https://generativelanguage.googleapis.com`)
- `GEMINI_MAX_RETRIES` (default: `3`)
- `GEMINI_FALLBACK_MODELS` (default: `gemini-2.0-flash,gemini-1.5-flash-latest,gemini-1.5-pro-latest`)

Intelligence routes added:

- `GET /intelligence` - separate UI for intelligent response workflow
- `POST /api/decision-intelligence` - graph-based impact + cascade analysis
- `POST /api/fault-analysis` - Gemini fault interpretation service
- `POST /api/governance/evaluate` - policy-driven governance actions
- `POST /api/intelligent-response` - end-to-end orchestrated pipeline

2. Open your web browser and navigate to:
```
http://localhost:5000
```

**Note:** If `py` defaults to Python 3.7, always use `py -3.14` to run the app.

## Project Structure

```
ML/
├── app.py                 # Flask backend application
├── templates/
│   └── index.html        # Frontend HTML template
├── static/              # Static assets (CSS, JS, icons)
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── model.joblib         # Your trained model (or fault_model.joblib)
└── predictions.db       # SQLite database (created automatically)
```

## API Endpoints

- `GET /` - Serves the main HTML page
- `POST /predict` - Accepts prediction request with Ia, Ib, Ic, Va, Vb, Vc
- `GET /history` - Returns all prediction history
- `GET /export` - Downloads history as CSV
- `POST /clear_history` - Clears all prediction history

## Usage

1. Enter the six input parameters (Ia, Ib, Ic, Va, Vb, Vc) in the form
2. Click "Predict Fault" to get predictions
3. View prediction history in the table below
4. Use search to filter predictions
5. Click "Export CSV" to download history
6. Click "Clear" to delete all history (with confirmation)

## Troubleshooting

**Model Not Loaded Error:**
- Ensure your model file is named `model.joblib` or `fault_model.joblib`
- Place it in the same directory as `app.py`
- Check the console output for loading errors

**Port Already in Use:**
- Modify the port in `app.py` to an available port if needed (default is `5000`)
