# Grocery_BFF
This is Grocery BFF Microservice.

# 1. Activate virtual environment (if using)
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux

# 2. Run Flask BFF
python bff.py

# 3. Open Swagger UI
Visit http://127.0.0.1:5001/swagger in your browser

# 4. Update the related microservice endpoint and port accordingly in config/appsettings.development.config
"UserMicroserviceUrl": "http://127.0.0.1:5002",
"OrderMicroserviceUrl": "http://127.0.0.1:5003",
"ProductMicroserviceUrl": "http://127.0.0.1:5000",

# required package installation
pip install quart
pip install flask_smorest
