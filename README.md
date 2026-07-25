
# 🏫 Smart Classroom Attentiveness Monitoring System

An automated computer vision and deep learning solution designed to monitor, analyze, and report student attentiveness during classroom sessions using facial analysis and engagement tracking.

---

## ✨ Features

* 👤 **Face Detection & Recognition:** Identifies enrolled students from video input.
* 👁️ **Attentiveness Tracking:** Real-time engagement and posture analysis.
* 📊 **Automated Reports:** Generates detailed attendance and attentiveness summary reports.
* 🗄️ **Database Integration:** Stores session history, student profiles, and class logs seamlessly.
* 💻 **Web Dashboard:** Intuitive UI built for easy navigation, reporting, and management.

---

## 🛠️ Tech Stack

* **Language:** Python
* **Backend:** Flask
* **Computer Vision & ML:** OpenCV, InsightFace
* **Frontend:** HTML5, CSS3, JavaScript
* **Database:** SQLite

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1. Prerequisites

Ensure you have Python 3.8+ installed on your system.

### 2. Clone the Repository

```bash
git clone [https://github.com/Aspirant5/Nothing_.git](https://github.com/Aspirant5/Nothing_.git)
cd Nothing_

```

### 3. Install Dependencies

Install all the required Python packages using `requirements.txt`:

```bash
pip install -r requirements.txt

```

### 4. Initialize the Database

Run the database setup script to prepare the database tables:

```bash
python init_db.py

```

### 5. Run the Application

Start the Flask development server:

```bash
python app.py

```

Open your browser and navigate to `http://127.0.0.1:5000/`.

---

## 📁 Project Structure

```text
├── dataset/             # Sample facial images and enrollment data
├── static/              # CSS styles, JS scripts, and static media
│   ├── css/
│   ├── recordings/      # Local video recordings (ignored in git)
│   └── uploads/         # Uploaded video files (ignored in git)
├── templates/           # HTML templates (Dashboard, Login, Reports)
├── app.py               # Flask application entry point
├── main.py              # Main core execution script
├── init_db.py           # Database initialization script
├── recognizer.py        # Face recognition logic
├── attentiveness.py     # Attentiveness detection pipeline
├── requirements.txt     # Python dependency requirements
└── README.md            # Project documentation

```

---

## 📝 Usage Instructions

1. **Login:** Access the dashboard using system credentials.
2. **Upload Video / Feed:** Upload classroom recordings (`.mp4`) or stream input for processing.
3. **View Dashboard:** Inspect live processing metrics, engagement ratings, and roll-wise logs.
4. **Generate Reports:** Download or view historical attendance and attentiveness reports.

---

## 📄 License

This project is developed for academic and educational purposes.

```

---

### How to add this to your GitHub Repository:
1. Go to your repository on GitHub: [`Aspirant5/Nothing_`](https://github.com/Aspirant5/Nothing_).
2. Click on the `README.md` file in the file list.
3. Click the **pencil icon (Edit this file)** at the top right.
4. Paste the content above, replacing what's currently in `README.md`.
5. Scroll down and click **Commit changes...**.

```
