from setuptools import setup, find_packages

setup(
    name="AetherOnePySocial",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "pydantic-settings",
        "email-validator",
        "passlib[bcrypt]",
        "alembic",
        "pytest",
    ],
    entry_points={
        "console_scripts": [
            "runserver=app.main:run_server",
        ]
    },
    python_requires=">=3.8",
)
