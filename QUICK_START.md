# Quick Start Guide

## ✅ Your Setup is Ready!

You have Python 3.14 installed. The app is configured to work with it.

## 🚀 To Run the Application:

### Method 1: Using Command Line (Recommended)
1. Open PowerShell or Command Prompt
2. Navigate to the project folder:
   ```powershell
   cd C:\Users\shree\OneDrive\Desktop\5TH_SEM_EL\ML
   ```
3. Run with Python 3.14:
   ```powershell
   py -3.14 app.py
   ```

### Method 2: Using the Batch File
1. Double-click `RUN.bat` in the project folder
2. The server will start automatically

## 🌐 Access the Application:

Once the server starts, open your browser and go to:
```
http://localhost:5000
```

## ✅ What's Fixed:

1. ✅ Model loading - Now works with Python 3.14
2. ✅ Feature engineering - Automatically expands 6 inputs to 27 features
3. ✅ All dependencies installed for Python 3.14
4. ✅ Database and endpoints ready

## 📝 Using the App:

1. Enter values for Ia, Ib, Ic, Va, Vb, Vc
2. Click "Predict Fault"
3. View results and history
4. Export data or clear history as needed

## ⚠️ If You See Errors:

- **"Model not loaded"**: Make sure you're using `py -3.14 app.py` (not just `py app.py`)
- **Port already in use**: Another instance might be running. Close it first.
- **Import errors**: Run `py -3.14 -m pip install -r requirements.txt` again

## 🎯 The model expects 27 features, but you only enter 6. The app automatically:
- Takes your 6 inputs (Ia, Ib, Ic, Va, Vb, Vc)
- Expands them to 27 features using feature engineering
- Makes predictions correctly

Everything is set up and ready to go!

