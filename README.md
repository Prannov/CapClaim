# 📟 CapClaim – Insurance Claim Submission System

**CapClaim** is a mini full-stack project simulating a real-world insurance claim workflow. It allows users to submit claims via a web form, securely uploads documents to AWS S3, stores metadata in a MySQL database, and sends real-time logs.

> ⚙️ Built with technologies aligned to CapSpecialty's internship description.

---

## 🚀 Tech Stack

- **Flask** – REST API backend
- **HTML** – Web-based claim submission form
- **MySQL** – Local database for storing claim records
- **Amazon S3** – Secure file/document storage
- **boto3** – AWS SDK for Python
- **python-dotenv** – For environment configuration
- **Logging** – Tracks submissions and errors

---

## ✨ Features

- ✅ Clean HTML form for user input
- ✅ Input validation on both frontend and backend
- ✅ File upload to **Amazon S3**
- ✅ Claim data inserted into **MySQL**
- ✅ Centralized logging to `logs/app.log`

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/CapClaim.git
cd CapClaim
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create Your `.env` File

```env
# AWS
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1

# MySQL
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=capclaim

# Email (Gmail SMTP with App Password)
EMAIL_USER=yourname@gmail.com
EMAIL_PASSWORD=your_app_password
```

> ❗ Make sure to enable 2-Step Verification on your Gmail and use an **App Password**.

---

### 4. Start the Flask Server

```bash
python app.py
```

Open in your browser:
```
http://127.0.0.1:5000/
```

---

## 🧪 Sample Flow

1. User submits claim via form  
2. Flask receives data and handles validation  
3. File uploaded to **S3**  
4. Claim metadata saved in **MySQL**   
5. Logs recorded in `logs/app.log`

---

## 📁 Project Structure

```
CapClaim/
├── app.py
├── lambda_handler.py
├── templates/
│   └── form.html
├── logs/
│   └── app.log
├── .env           # NOT COMMITTED
├── .gitignore
├── requirements.txt
└── README.md
```


