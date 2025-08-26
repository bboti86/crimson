# Crimson Cycle

Crimson Cycle is a self-hosted web application designed to help users track their menstrual cycles. It provides a simple and intuitive interface to record period data, view it on a calendar, and get an estimation for the next cycle.

The entire application is containerized using Docker, making it easy to deploy and manage.

## Features

-   **Record Periods:** Easily add new period entries with a start and end date.
-   **View History:** See a list of all your past period entries.
-   **Delete Entries:** Remove any entry with a single click.
-   **Calendar View:** Visualize your past periods on a monthly calendar.
-   **Future Period Estimation:** Get an automatic calculation of your estimated periods for the next three years based on your cycle history.
-   **Status Notifications:** Receive feedback for your actions (e.g., "Period added successfully").
-   **Persistent Storage:** Your data is safely stored in a JSON file on a Docker volume, so it persists even if the container is restarted.
-   **Self-Hosted:** You have full control over your data.

## Tech Stack

-   **Backend:** Python with Flask, a lightweight web framework.
-   **Frontend:** Vue.js, a progressive JavaScript framework.
-   **Web Server:** Nginx, used to serve the frontend and proxy API requests.
-   **Containerization:** Docker and Docker Compose.

## How it Works

The application is composed of two main services: a backend and a frontend.

### Backend

The backend is a simple Flask application that exposes a REST API for managing period data. The data is stored in a `database.json` file, which is located in a Docker volume to ensure data persistence.

The API has the following endpoints:

-   `GET /api/periods`: Retrieves all period entries. The response is a JSON object with two keys: `historical` (an array of user-recorded periods) and `estimated` (an array of future periods calculated by the backend).
-   `POST /api/periods`: Adds a new period entry. When a new period is added, the backend recalculates the future estimated periods.
-   `DELETE /api/periods/<start_date>`: Deletes a specific period entry. When a period is deleted, the backend recalculates the future estimated periods.

### Frontend

The frontend is a single-page application (SPA) built with Vue.js. It provides a user-friendly interface for interacting with the backend API.

The key components of the frontend are:

-   **Period Form:** A form to submit the start and end dates of a new period.
-   **Periods List:** A list that displays all recorded periods.
-   **Calendar:** A calendar view that highlights past and estimated future periods.
-   **API Integration:** The frontend uses `axios` to make HTTP requests to the backend API.

The frontend is served by an Nginx container, which is also configured to act as a reverse proxy. This means that any requests to `/api` are forwarded to the backend container, which is running the Flask application. This setup avoids cross-origin (CORS) issues and simplifies the overall architecture.

## Getting Started

To run Crimson Cycle, you need to have Docker and Docker Compose installed on your system.

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd crimson-cycle
    ```

2.  **Build and run the application:**
    ```bash
    docker-compose up --build
    ```
    This command will build the Docker images for the backend and frontend services and then start the containers.

3.  **Access the application:**
    Once the containers are running, you can access the Crimson Cycle web interface by navigating to `http://localhost:8080` in your web browser.

## Codebase Overview

The repository is structured as follows:

-   `backend/`: Contains the Flask backend application.
    -   `app.py`: The main Flask application file with all the API logic.
    -   `Dockerfile`: Defines the Docker image for the backend.
    -   `requirements.txt`: Lists the Python dependencies.
    -   `data/`: This directory is mounted as a volume and stores the `database.json` file.
-   `frontend/`: Contains the. Vue.js frontend application.
    -   `src/`: The main source code for the Vue app.
        -   `App.vue`: The main component that contains the entire UI and application logic.
        -   `main.js`: The entry point of the Vue application.
    -   `Dockerfile`: A multi-stage Dockerfile that builds the Vue app and sets up the Nginx server.
    -   `nginx.conf`: Nginx configuration file.
    -   `package.json`: Lists the Node.js dependencies and scripts.
-   `docker-compose.yaml`: The Docker Compose file that orchestrates the entire application.
-   `README.md`: This file.

All code is extensively commented to provide a clear understanding of how the different parts of the application work and interact with each other.
