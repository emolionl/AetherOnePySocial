# AetherOnePySocial

### Group Analysis with AetherOnePy Integration
This API serves as a backend for extending the functionality of AetherOnePy, a powerful program for conducting individual analyses and broadcasts. While AetherOnePy excels in individual work, this project is designed to enable collaborative group analysis and broadcasting efforts by:

### Combining Analysis Results: When multiple users perform analyses on the same subject, this API collects and consolidates their results.
### Group Broadcasting: Facilitates group collaboration by merging intentions and ensuring coordinated broadcasts.
### Team Collaboration: The API is built to support distributed teams working together on shared projects, enhancing the efficiency of group efforts.


# Getting started

## install all packages

go to tha map AetherOnePySocial/py and run

```
pip install -e .
```

then in command line in the same map run
```
 uvicorn app.main:app --reload
```

## If you want to run tests on PostMan
```
AetherOnePySocial_Postman_Collection.json
```

## To run tests
```
pytest
```

# Introduction to the AetherOnePySocial Project

## Overview
This project is a modular and scalable web application built using **FastAPI**, designed with a clear Model-View-Controller (MVC) architecture. It serves as a foundation for developing APIs with features like authentication, data management, and analysis. The application includes:

- **User authentication** (register and login).
- Management of **machines**, **catalogs**, **rates**, **cases**, **sessions**, **analyses**, and **comparisons**.
- Unit tests to ensure application reliability.
- Integration with an SQLite database (or any other database of your choice).

## Key Components

### 1. **Application Structure**
The project follows an MVC structure:
- `models/`: Database models for each entity.
- `schemas/`: Pydantic schemas for request and response validation.
- `routers/`: FastAPI routers that define the API endpoints.
- `tests/`: Unit tests for all endpoints to validate functionality.

### 2. **Database**
The project uses **SQLAlchemy** for ORM and database management. It also includes an `alembic` integration for database migrations (not implemented here but can be added).

### 3. **Endpoints**
The application has endpoints for:
- Authentication (`/api/auth/`)
- Machines (`/api/machines/`)
- Catalogs (`/api/catalog/`)
- Rates (`/api/rates/`)
- Cases (`/api/cases/`)
- Sessions (`/api/sessions/`)
- Analyses (`/api/analysis/`)
- Merged Analyses (`/api/merged-analysis/`)
- Comparisons (`/api/comparison/`)

### 4. **Unit Testing**
All endpoints are tested using **pytest**. The `tests/` directory includes test cases for creating, retrieving, and validating data for all entities.

## How to Use

### 1. **Clone the Repository**
```bash
git clone <repository-url>
cd fastapi_mvc_project
```

### 2. **Set Up the Environment**
Create a virtual environment and install dependencies:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
```

### 3. **Run the Application**
Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
Access the API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 4. **Run Unit Tests**
Run the unit tests to verify functionality:
```bash
pytest
```

## Features
- **Automatic documentation**: Interactive API documentation is available with Swagger UI.
- **Validation**: Input and output validation using Pydantic.
- **Extensibility**: Easily add new models, endpoints, and features.
- **Testing**: Comprehensive unit tests for all entities.

## Example Usage
### Register a User
Endpoint: `POST /api/auth/register`
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```
Response:
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com"
}
```

### Create a Machine
Endpoint: `POST /api/machines/`
```json
{
  "machine_name": "Machine1",
  "description": "Test machine",
  "api_key": "1234"
}
```
Response:
```json
{
  "id": 1,
  "machine_name": "Machine1",
  "description": "Test machine",
  "api_key": "1234"
}
```

## Contribution
Feel free to fork the repository and submit pull requests. For major changes, open an issue to discuss what you would like to change.

## License
This project is licensed under the MIT License.


files schema
# Directory Structure:
```
 project/
 ├── app/
 │   ├── __init__.py
 │   ├── main.py
 │   ├── config.py
 │   ├── database.py
 │   ├── models/
 │   │   ├── __init__.py
 │   │   ├── user.py
 │   │   ├── machine.py
 │   │   ├── catalog.py
 │   │   ├── rate.py
 │   │   ├── case.py
 │   │   ├── session.py
 │   │   ├── analysis.py
 │   │   ├── merged_analysis.py
 │   │   ├── comparison.py
 │   ├── routers/
 │   │   ├── __init__.py
 │   │   ├── auth.py
 │   │   ├── machines.py
 │   │   ├── catalog.py
 │   │   ├── rates.py
 │   │   ├── cases.py
 │   │   ├── sessions.py
 │   │   ├── analysis.py
 │   │   ├── merged_analysis.py
 │   │   ├── comparison.py
 │   ├── schemas/
 │   │   ├── __init__.py
 │   │   ├── user.py
 │   │   ├── machine.py
 │   │   ├── catalog.py
 │   │   ├── rate.py
 │   │   ├── case.py
 │   │   ├── session.py
 │   │   ├── analysis.py
 │   │   ├── merged_analysis.py
 │   │   ├── comparison.py
 ├── setup.py
 ├── tests/
 │   ├── __init__.py
 │   ├── test_auth.py
 │   ├── test_machines.py
 │   ├── test_catalog.py
 │   ├── test_rates.py
 │   ├── test_cases.py
 │   ├── test_sessions.py
 │   ├── test_analysis.py
 │   ├── test_merged_analysis.py
 │   ├── test_comparison.py
 ├── .gitignore

```