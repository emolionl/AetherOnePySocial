from setuptools import setup, find_packages

# to run this setup pip install -e ".[test]"
# pip install -e .

setup(
    name="AetherOnePySocial",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "psycopg2-binary",
        "pydantic",
        "pydantic-settings",
        "email-validator",
        "passlib[bcrypt]",
        "alembic",
        "pytest",
        "psycopg2-binary",
        "alembic",
        "sqlalchemy-to-pydantic",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "python-multipart"
    ],
    entry_points={
        "console_scripts": [
            "runserver=app.main:run_server",
        ]
    },
    python_requires=">=3.8",
    extras_require={
        'test': [
            'pytest',
            'httpx',  # Required for FastAPI TestClient
            'pytest-cov',  # If you want coverage reports
            'pytest-order',
        ],
    }
)
