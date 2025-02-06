# 🚀 HRManager - Human Resource Management System

HRManager is a **FastAPI + React** based **Human Resource Management System** that provides a seamless way to manage employee data. It supports **CRUD operations, bulk Excel uploads**, and **Docker containerization for easy deployment**.

---

## 📌 Table of Contents
- [🚀 HRManager - Human Resource Management System](#-hrmanager---human-resource-management-system)
  - [📌 Table of Contents](#-table-of-contents)
  - [📌 Project Overview](#-project-overview)
  - [📌 Technology Stack](#-technology-stack)
  - [📌 Prerequisites](#-prerequisites)
  - [📌 Installation \& Execution](#-installation--execution)
    - [**1️⃣ Running Locally (Development Mode)**](#1️⃣-running-locally-development-mode)
      - [**📌 Start Backend**](#-start-backend)

---

## 📌 Project Overview
**HRManager** offers the following features:

✅ **View all employees on the website**  
✅ **Add, edit, and delete employees via a web interface**  
✅ **Bulk upload employee data via Excel**  
✅ **Fully containerized using Docker Compose for easy deployment**  

---

## 📌 Technology Stack
| Category          | Technology Used         |
|------------------|------------------------|
| **Frontend**     | React, Axios, Bootstrap |
| **Backend**      | FastAPI, SQLAlchemy, Pandas |
| **Database**     | PostgreSQL |
| **Containerization** | Docker, Docker Compose |
| **File Processing** | OpenPyXL (Excel Upload) |

---

## 📌 Prerequisites
- **Python 3.9+**
- **Node.js 14+**
- **Docker & Docker Compose**

---

## 📌 Installation & Execution
### **1️⃣ Running Locally (Development Mode)**

#### **📌 Start Backend**
```bash
cd backend
python -m venv venv  # Create a virtual environment
source venv/bin/activate  # For Windows: use `venv\Scripts\activate`
pip install -r requirements.txt
uvicorn app.main:app --reload
