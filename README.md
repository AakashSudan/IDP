# AI-Powered Document OCR & Verification API

## 📌 Overview
This project is an **AI-powered OCR-based document verification system** that extracts and validates key details from identity documents such as **Aadhaar Card, PAN Card, Driving License, and University Certificates**. It uses **PaddleOCR, OpenCV, and FastAPI** to provide an efficient, scalable, and accurate document verification solution.

## 🚀 Features
- **Automatic text extraction** from Aadhaar, PAN, and other identity documents
- **Advanced preprocessing** to enhance OCR accuracy
- **Regex-based data validation** for name, date of birth, ID numbers, etc.
- **Fuzzy matching for better field identification**
- **FastAPI-based API** for easy integration into applications
- **Multi-language support** (English + Indian regional languages)
- **High-speed and scalable solution** using AI-driven techniques

---

## 🔧 Tech Stack
- **Programming Language:** Python
- **OCR Engine:** PaddleOCR
- **Preprocessing:** OpenCV
- **Backend Framework:** FastAPI
- **Data Processing:** NumPy, Pandas, re (Regex)
- **Version Control:** Git & GitHub

---

## 📂 Installation & Setup
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/yourusername/document-ocr-api.git
cd document-ocr-api
```

### 2️⃣ Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
```

### 3️⃣ Install Dependencies
```sh
<<<<<<< HEAD
pip install fastapi uvicorn paddleocr opencv-python numpy pandas fuzzywuzzy python-Levenshtein
```

### 4️⃣ Run the API
```sh
uvicorn main:app --reload
=======
pip install fastapi[all] pdf2image paddlepaddle paddleocr opencv-python numpy pandas fuzzywuzzy python-Levenshtein
```

### 4️⃣ Run the API [inside the virtual environment]
```sh
fastapi dev main.py
>>>>>>> 5ac6fcd2fbe65644606a167793e198717fb801ea
```
API will be accessible at: **http://127.0.0.1:8000**

---

## 📜 API Usage
### **1️⃣ Upload an Image for OCR Processing**
#### **Endpoint:** `POST /extract`
#### **Request Example (cURL):**
```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/extract' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@path/to/your/document.jpg'
```
#### **Response Example:**
```json
{
  "Name": "John Doe",
  "Date of Birth": "01/01/1990",
  "Aadhaar Number": "1234 5678 9012",
  "PAN": "ABCDE1234F"
}
```

### **2️⃣ Health Check**
#### **Endpoint:** `GET /`
#### **Response:**
```json
{"status": "API is running successfully!"}
```

---

## 🛠 Future Enhancements
- ✅ Support for additional regional languages
- ✅ Improve deep learning models for better OCR accuracy
- ✅ Add biometric verification as a secondary check
- ✅ Create a SaaS platform for real-time document validation

---



