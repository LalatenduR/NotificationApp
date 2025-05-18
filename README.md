# Notification Service

This is a Notification Service built using FastAPI and Celery, designed to send notifications to users via Email, SMS, and in-app channels. This project fulfills the requirements outlined in the intern assignment.

## Requirements

1.  **API Endpoints:**
    * `GET /api/v1/`: Test the base URL.
    * `POST /api/v1/notifications`: Send a notification to a user.
    * `GET /api/v1/users/{id}/notifications`: Get all notifications for a specific user.
2.  **Notification Types:**
    * Email notifications (sending via SMTP and also stored in a MongoDB database).
    * SMS notifications (simulated due to free service limitations, designed for integration with an SMS gateway and so stored in a MongoDB database).
    * In-app notifications (stored in a MongoDB database).
3.  **Bonus Points:**
    * **Queue:** Uses Celery with RabbitMQ for asynchronous processing of notifications.
    * **Retries:** Celery tasks for sending notifications are configured with automatic retries for failed attempts.

## Deliverables

This repository contains the source code for the Notification Service.

## Setup Instructions

Follow these steps to set up and run the project locally:

1.  **Clone the Repository:**
    Open your terminal and navigate to the directory where you want to clone the project. Then run:
    ```bash
    git clone [<YOUR_GIT_REPOSITORY_LINK>](https://github.com/LalatenduR/PepsalesAssignment)
    cd PepsalesAssignment
    ```

2.  **Install Python Virtual Environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    ```bash
    # On Windows
    venv\Scripts\activate

    # On macOS and Linux
    source venv/bin/activate
    ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up RabbitMQ using Docker:**
    * Ensure you have Docker installed. If not, you can download it from [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/).
    * Run the following command to start RabbitMQ with the management interface:
        ```bash
        # Latest RabbitMQ 4.x
        docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4-management
        ```
    * The RabbitMQ management interface will be accessible at `http://localhost:15672/`. The default username/password is `guest`/`guest`.

6.  **Set up MongoDB:**
    * Ensure you have MongoDB installed and running. You might need to configure the connection URL in your `.env` file.

7.  **Configure Environment Variables:**
    * Copy the `.env.example` file to a new file named `.env`:
        ```bash
        cp .env.example .env
        ```
    * Open the `.env` file and replace the placeholder values with your actual configuration details. For example, update the MongoDB connection URL, SMTP settings, etc.
    * **Important:** Ensure that your `.env` file is **not** committed to your Git repository. It should be listed in your `.gitignore` file to protect sensitive information.

    The `.env.example` file provides a template for the required environment variables:

    ```
    # MongoDB Connection URL (Replace with your actual connection details)
    # If your MongoDB has authentication:
    MONGODB_URL=mongodb://your_mongodb_username:your_mongodb_password@your_mongodb_host:your_mongodb_port/


    # MongoDB Collection Name
    COLLECTION_NAME=notifications

    # Email Sending Configuration (SMTP)
    SMTP_HOST=smtp.example.com  # e.g., smtp.gmail.com
    SMTP_PORT=587             # e.g., 587 (TLS) 
    SMTP_USERNAME=your_email_username
    SMTP_PASSWORD=your_email_password 
    FROM_EMAIL=your_sending_email@example.com

    # Celery/RabbitMQ Configuration 
    # Default RabbitMQ setup for local development (NOT for production):
    # CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//
    ```

## Running the Project

Follow these steps to run the Notification Service:

1.  **Run the FastAPI Application:**
    Open a terminal in the project directory and run:
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be accessible at `http://127.0.0.1:8000/api/v1`.

2.  **Run the Celery Worker:**
    Open another terminal in the project directory and run:
    ```bash
    celery -A app.celery_worker worker --loglevel=info --pool=solo
    ```
    Ensure RabbitMQ is running before starting the Celery worker.

    **Important:** Make sure to run the FastAPI application first, then RabbitMQ (if you don't have it running already via Docker), and finally the Celery worker.

## API Documentation

This project uses FastAPI, which automatically generates interactive API documentation using OpenAPI. You can access it at:

* **Swagger UI:** `http://127.0.0.1:8000/docs`
* **Redoc:** `http://127.0.0.1:8000/redoc`

These documentation interfaces provide details about the available API endpoints, request and response schemas, and allow you to interact with the API directly.

### API Endpoints

* **`GET /api/v1/`**:
    * **Summary:** Test the base URL.
    * **Description:** Returns a simple message to verify that the API is running.

* **`POST /api/v1/notifications`**:
    * **Summary:** Send a new notification.
    * **Description:** Sends a notification to a specified user via email, SMS, or in-app. The request body should be a JSON object with the user ID, notification type, message, and relevant contact details (email or phone number) based on the notification type.

* **`GET /api/v1/users/{user_id}/notifications`**:
    * **Summary:** Get notifications for a specific user.
    * **Description:** Retrieves a list of all notification records associated with the user ID provided in the path. The `user_id` must be a positive integer.

## Assumptions Made

* It is assumed that a running instance of MongoDB is accessible at the configured `MONGODB_URL`.
* It is assumed that there can be many users and any user can be sent as many types of notification.
* Email sending relies on a correctly configured SMTP server and credentials provided in the environment variables.
* SMS sending is currently simulated. To implement real SMS sending, integration with a third-party SMS gateway (e.g., Twilio, Nexmo) would be required. The code is structured to facilitate such integration.
* The Celery worker and RabbitMQ broker are running and accessible to the FastAPI application.
