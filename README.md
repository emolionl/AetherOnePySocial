# AetherOnePySocial

### Group Analysis with AetherOnePy Integration
This API serves as a backend for extending the functionality of AetherOnePy, a powerful program for conducting individual analyses and broadcasts. While AetherOnePy excels in individual work, this project is designed to enable collaborative group analysis and broadcasting efforts by:

### Combining Analysis Results: 
When multiple users perform analyses on the same subject, this API collects and consolidates their results.
### Group Broadcasting: 
Facilitates group collaboration by merging intentions and ensuring coordinated broadcasts.
### Team Collaboration: 
The API is built to support distributed teams working together on shared projects, enhancing the efficiency of group efforts.


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
# To build frontend you could use openAPI
```
python ./generateOpenAPI.py
```
## you will generate 
```openapi.json``` file


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
cd AetherOnePySocial
```

### 2. **Set Up the Environment**
Create a virtual environment and install dependencies:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -e .
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

## Entity Relationship Diagram (ERD)

```
[User] 1---* [SessionKey] *---1 [Session] *---1 [Analysis] *---1 [RateAnalysis]
   |                |                |                |
   |                |                |                |
   |                |                |                |
   *                *                *                *
[Case]           [Catalog]        [Rate]           [Machine]
```

- **User**: Has many SessionKeys, Sessions, and Cases.
- **SessionKey**: Belongs to a User, referenced by Sessions.
- **Session**: Belongs to a User, Case, and SessionKey. Has many Analyses.
- **Analysis**: Belongs to a Session and Catalog. Has many RateAnalyses.
- **RateAnalysis**: Belongs to an Analysis and Catalog.
- **Case**: Belongs to a User. Has many Sessions.
- **Catalog**: Has many Analyses, Rates, and RateAnalyses.
- **Rate**: Belongs to a Catalog.
- **Machine**: Can be referenced by Sessions, Cases, etc.

## Endpoint Data Requirements

### Register a User
`POST /api/auth/register`
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

### Login
`POST /api/auth/login`
- Content-Type: application/x-www-form-urlencoded
- Body:
  - username: your email (e.g., test@example.com)
  - password: your password

### Create a Machine
`POST /api/machines/`
```json
{
  "machine_name": "Machine1",
  "description": "Test machine",
  "api_key": "1234"
}
```

### Create a Session Key
`POST /api/keys/`
```json
{
  "user_id": 1,
  "local_session_id": 123
}
```

### Share Analysis
`POST /api/analysis/share`
```json
{
  "data": {
    "user_id": 1,
    "machine_id": "machine_id_1",
    "key": "session-key-uuid",
    "session_id": 7,
    "analyses": {
      "analyses": [
        {
          "analysis": {
            "catalog_id": 2,
            "created": "2025-01-27T14:11:40",
            "id": 9,
            "name": null,
            "session_id": 7,
            "target_gv": 699
          },
          "catalog": {
            "description": "radionics-rates",
            "id": 2,
            "name": "emotions"
          },
          "rate_analysis": [
            {
              "analysis_id": 9,
              "catalog_id": 2,
              "description": null,
              "energetic_value": 1002,
              "gv": 962,
              "id": 1,
              "level": 0,
              "note": "",
              "potency": 0,
              "potencyType": "8989",
              "signature": "wary"
            }
            // ... more rate_analysis objects ...
          ]
        }
        // ... more analyses ...
      ],
      "case": {
        "color": "#303de8",
        "created": "2025-01-27T14:10:50",
        "description": "test6",
        "email": "test6@test.com",
        "id": 6,
        "last_change": "Mon, 27 Jan 2025 14:10:50 GMT",
        "name": "test6"
      },
      "session": {
        "case_id": 6,
        "created": "2025-01-27T14:11:18",
        "description": "test6",
        "id": 7,
        "intention": "test6"
      }
    }
  },
  "message": "Found 3 analyses with their related data",
  "status": "success"
}
```

### Get Analysis by Key
`GET /api/analysis/key/{key}`
- Requires Authorization header with Bearer token.

### Other Endpoints
See the OpenAPI docs at `/docs` for full details on all endpoints and their required/requested data.

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