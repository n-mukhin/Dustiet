# Dustiet

**Dustiet** is a web application designed for anime enthusiasts to register, share, and review their favorite anime series. Users can create accounts, post detailed reviews, rate anime, and explore random anime quotes to enrich their experience. The application leverages modern technologies to ensure scalability, security, and a seamless user experience.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring and Observability](#monitoring-and-observability)

## Features

- **User Authentication**
  - Register with a unique username and email.
  - Secure login with hashed passwords.

- **Anime Reviews**
  - Create, view, and manage anime reviews.
  - Rate anime series on a scale.
  - View all reviews by a specific user.

- **Random Anime Quotes**
  - Fetch and display random quotes from various anime series via an external API.

- **Containerized Deployment**
  - Easy setup and deployment using Docker and Docker Compose.

## Tech Stack

- **Backend:** Python, Flask
- **Database:** PostgreSQL
- **Containerization:** Docker, Docker Compose
- **Authentication:** Werkzeug Security
- **External APIs:** [AnimeChan](https://animechan.vercel.app/)

## Getting Started

Follow these instructions to set up and run the Dustiet application on your local machine.

### Prerequisites

Ensure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/n-mukhin/Dustiet.git
   cd Dustiet
   ```

2. **Directory Structure**

   ```
   Dustiet
   ├── app.py
   ├── Dockerfile
   ├── docker-compose.yml
   ├── requirements.txt
   ├── .gitlab-ci.yml
   └── tests
       └── test_app.py
   ```

### Running the Application

1. **Build the Docker Images**

   Navigate to the project directory and build the Docker images using Docker Compose:

   ```bash
   docker-compose build
   ```

2. **Start the Containers**

   Launch the application and the PostgreSQL database:

   ```bash
   docker-compose up -d
   ```

3. **Access the Application**

   The application will be accessible at [http://localhost:5000](http://localhost:5000).

4. **Stopping the Application**

   To stop the containers, run:

   ```bash
   docker-compose down
   ```

## API Endpoints

### Authentication

#### Register User

- **Endpoint:** `POST /register`
- **Description:** Creates a new user account.
- **Request Body:**

  ```json
  {
    "username": "johndoe",
    "email": "johndoe@example.com",
    "password": "securepassword"
  }
  ```

- **Response:**

  ```json
  {
    "user_id": 1
  }
  ```

#### Login User

- **Endpoint:** `POST /login`
- **Description:** Authenticates a user.
- **Request Body:**

  ```json
  {
    "email": "johndoe@example.com",
    "password": "securepassword"
  }
  ```

- **Response:**

  ```json
  {
    "user_id": 1,
    "status": "authorized"
  }
  ```

  Or, in case of failure:

  ```json
  {
    "status": "unauthorized"
  }
  ```

### Anime Reviews

#### Create Review

- **Endpoint:** `POST /reviews`
- **Description:** Adds a new anime review.
- **Request Body:**

  ```json
  {
    "user_id": 1,
    "anime_title": "Attack on Titan",
    "review_text": "An intense and gripping series with deep character development.",
    "rating": 5
  }
  ```

- **Response:**

  ```json
  {
    "review_id": 10
  }
  ```

#### Get User Reviews

- **Endpoint:** `GET /reviews/<int:user_id>`
- **Description:** Retrieves all reviews by a specific user.
- **Response:**

  ```json
  [
    {
      "review_id": 10,
      "anime_title": "Attack on Titan",
      "review_text": "An intense and gripping series with deep character development.",
      "rating": 5,
      "created_at": "2024-04-27T12:34:56.789Z"
    },
    {
      "review_id": 12,
      "anime_title": "Naruto",
      "review_text": "A classic tale of perseverance and friendship.",
      "rating": 4,
      "created_at": "2024-05-01T08:22:33.456Z"
    }
  ]
  ```

### External API

#### Get Random Anime Quote

- **Endpoint:** `GET /random-anime-quote`
- **Description:** Fetches a random quote from an anime series.
- **Response:**

  ```json
  {
    "anime": "Fullmetal Alchemist: Brotherhood",
    "character": "Edward Elric",
    "quote": "A lesson without pain is meaningless."
  }
  ```

## Database Schema

The application uses PostgreSQL with the following schema:

### Users Table

| Column   | Type    | Constraints          |
|----------|---------|----------------------|
| id       | SERIAL  | PRIMARY KEY          |
| username | VARCHAR | NOT NULL             |
| email    | VARCHAR | NOT NULL, UNIQUE     |
| password | VARCHAR | NOT NULL             |

### Reviews Table

| Column      | Type     | Constraints                          |
|-------------|----------|--------------------------------------|
| id          | SERIAL   | PRIMARY KEY                          |
| user_id     | INTEGER  | REFERENCES users(id) ON DELETE CASCADE |
| anime_title | VARCHAR  | NOT NULL                             |
| review_text | TEXT     | NOT NULL                             |
| rating      | INTEGER  | NOT NULL                             |
| created_at  | TIMESTAMP| NOT NULL (defaults to current timestamp) |

#### Initialization Script (`db/init.sql`):

```sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    anime_title VARCHAR(255) NOT NULL,
    review_text TEXT NOT NULL,
    rating INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## CI/CD Pipeline

The project uses GitLab CI/CD to automate the testing, building, and deployment processes.

### Pipeline Stages:

- **Test:** Runs automated tests using `pytest`.
- **Build:** Builds the Docker image and pushes it to GitLab Container Registry.
- **Deploy:** Deploys the Docker image to Heroku.

### Continuous Deployment:

Every push to the `main` branch triggers the CI/CD pipeline, ensuring that the latest changes are tested and deployed automatically.

## Monitoring and Observability

To ensure the reliability and performance of Dustiet, we’ve integrated Prometheus and Grafana for real-time monitoring and visualization.

### Monitoring Features

#### Flask Application Metrics:

- Total HTTP requests by endpoint and method.
- Average response times.
- HTTP status code distribution.

#### Nginx Metrics:

- Requests per second.
- Active connections.
- HTTP status code breakdown.

#### System Health Checks:

- CPU and memory usage of the application containers.
- Container uptime.

### How to Set Up Monitoring

#### Prometheus Configuration:

The Prometheus server is configured to scrape metrics from:

- **Flask application:** Exposes metrics at `/metrics` using `prometheus_flask_exporter`.
- **Nginx:** Exposes metrics using `nginx-prometheus-exporter`.

Prometheus Configuration File (`prometheus/prometheus.yml`):

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'flask_app'
    static_configs:
      - targets: ['web:5000']

  - job_name: 'nginx_exporter'
    static_configs:
      - targets: ['nginx_exporter:9113']
```

#### Grafana Setup:

Grafana is used to visualize the data collected by Prometheus. It provides a customizable dashboard for monitoring metrics.

- Access Grafana at [http://localhost:3000](http://localhost:3000).
- Default login credentials:
  - **Username:** admin
  - **Password:** admin
- Add Prometheus as a data source with the URL [http://prometheus:9090](http://prometheus:9090).

#### Pre-built Dashboards:

You can import pre-built dashboards from Grafana.com or create custom dashboards to suit your needs.
