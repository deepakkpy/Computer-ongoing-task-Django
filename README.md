# 🖥️ Process Monitor - Django Project

A lightweight **process and system monitoring tool** built with **Django**, **JavaScript**, and a clean UI.  
It allows you to:
- List connected computers
- View running processes in a tree structure
- Switch between **Process Details** and **System Details** tabs
- Auto-refresh data to see real-time changes

---

## 🚀 Features
- **Computer List Panel**  
  Displays all registered hosts with the last seen timestamp.
- **Process Details Tab**  
  - Expand/collapse process trees
  - View columns for **Name**, **Memory (MB)**, **CPU (%)**, **PPID**
- **System Details Tab**  
  - OS, CPU, RAM, and Disk information
- **Auto-Refresh**  
  Enable/disable auto-refresh for the process list.
- **Responsive Design**  
  Works on most screen sizes with a clean, modern UI.

---

## 🛠️ Tech Stack
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Vanilla JS
- **API:** Django REST Framework (for computer & process data)
- **Database:** SQLite/PostgreSQL/MySQL (your choice)
- **Version Control:** Git + GitHub

---

## 📂 Project Structure

```
project-root/
│
├── static/
│   ├── styles.css       # Custom CSS for UI styling
│   ├── ui.js            # Frontend logic (tabs, API calls, rendering)
│
├── templates/
│   └── index.html       # Main UI layout
│
├── api/
│   ├── views.py         # API endpoints for computers and processes
│   ├── serializers.py   # Serialization of data for frontend
│
├── manage.py
└── README.md
```

---

## ⚙️ Setup & Installation

### **1. Clone the repository**
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### **2. Create and activate a virtual environment**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### **3. Install dependencies**
```bash
pip install -r requirements.txt
```

### **4. Run migrations**
```bash
python manage.py migrate
```

### **5. Start the development server**
```bash
python manage.py runserver
```

Visit:
```
http://127.0.0.1:8000
```

---

## 🔄 API Endpoints

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/api/computers/` | GET | List all computers |
| `/api/computers/<hostname>/latest/` | GET | Get system details and process list for the host |

---

## 🧪 Development Notes
- Customize refresh intervals in `ui.js` (default: 5 seconds).
- Update CSS in `static/styles.css` to tweak theme colors or layout.

---

## 🤝 Contributing
1. Fork the repository  
2. Create a feature branch  
3. Commit your changes  
4. Open a pull request

---

## 📜 License
This project is licensed under the **MIT License**.  
You’re free to use, modify, and distribute with attribution.

---

## 👨‍💻 Author
- **Your Name**  
  GitHub: [@your-username](https://github.com/your-username)
