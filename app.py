from flask import Flask, request, jsonify, render_template
from lambda_handler import lambda_handler
import logging
from logging.handlers import RotatingFileHandler
import os
from email_utils import send_claim_email

# Create logs directory if not exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Setup logging
log_file = 'logs/app.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        RotatingFileHandler(log_file, maxBytes=100000, backupCount=3),
        logging.StreamHandler()  # also print to console
    ]
)


app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("form.html")

@app.route("/submit-claim", methods=["POST"])
def submit_claim():
    try:
        # validation
        required = ["name", "email", "claim_type", "description"]
        for field in required:
            if field not in request.form or not request.form[field].strip():
                return jsonify({"error": f"Missing or empty field: {field}"}), 400

        # extract fields
        data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "claim_type": request.form["claim_type"],
            "description": request.form["description"]
        }

        if "file" not in request.files or request.files["file"].filename == "":
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        file_path = f"temp_{file.filename}"
        file.save(file_path)
        data["file_path"] = file_path

        result = lambda_handler(data)
        logging.info(f"Received claim from {data['name']} ({data['email']})")

        send_claim_email(data["email"], data["name"], data["claim_type"])

        return jsonify(result), 200
        
    except Exception as e:
        logging.error("Error in /submit-claim", exc_info=True)
        return jsonify({"error": str(e)}), 500

        


if __name__ == "__main__":
    app.run(debug=True)

    
