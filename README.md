# Signature Detection Service

This project provides a web service for detecting signatures in scanned documents. The service uses Flask, SQLAlchemy, Flask-Login for user authentication, and OpenCV for image processing.

## Features

- User registration and login
- Signature detection in uploaded images
- Logging of requests and responses in the database
- Cropped signature images returned in the response

## Requirements

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Bcrypt
- Flask-Migrate
- OpenCV
- NumPy

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/almakhanova/signature_detection_service.git
    cd signature_detection_service
    ```

2. Create and activate a virtual environment:

    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Initialize the database:

    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

5. Run the application:

    ```bash
    python main.py
    ```

The application will be available at `http://127.0.0.1:5009`.

## Usage

### Register a new user

1. Open a web browser and go to `http://127.0.0.1:5009/register`.
2. Fill out the registration form and submit.

### Login

1. Go to `http://127.0.0.1:5009/login`.
2. Enter your credentials and submit.

### Detect Signature

1. After logging in, go to `http://127.0.0.1:5009/detect_signature`.
2. Upload an image and click "Detect".
3. The response will contain the coordinates of the detected signatures and URLs of the cropped signature images.


## Task 5: Standalone Signature Detection Script

A standalone script for signature detection is provided in the `task_5` directory. This script can be run independently of the web service.

### Running the Standalone Script

1. Navigate to the `task_5` directory:

    ```bash
    cd task_5
    ```

2. Run the script:

    ```bash
    python detect_signature.py
    ```

3. Enter the path to the image when prompted. If no path is provided, the script will use the default image `signature_example.png` located in the `task_5` directory. The script will process the image and output the coordinates of the detected signatures.


