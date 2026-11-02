# Student Management System

A beginner-friendly Flask project with SQLite and a responsive HTML/CSS interface.

## Features
- Add student records
- View all student records
- Edit student details
- Delete student records
- Prevent duplicate email addresses
- Store data in a local SQLite database (`students.db`)

## Run on Windows PowerShell

1. Open this folder in VS Code.
2. Open the terminal in this folder.
3. Create a virtual environment (only once):

   ```powershell
   python -m venv venv
   ```

4. Activate it:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use this for the current terminal session:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\venv\Scripts\Activate.ps1
   ```

   Or skip activation and run commands using `.\venv\Scripts\python.exe`.

5. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

6. Start the app:

   ```powershell
   python app.py
   ```

7. Open http://127.0.0.1:5000 in your browser.

The SQLite database is created automatically the first time the app starts.

## Project structure

```text
student_management_system/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   ├── index.html
│   └── edit.html
└── static/
    └── style.css
```

This is a learning project. Flask's debug server is for local development only.
