# AetherOnePySocial
We have a great program AetherOnePy and there you can do the analysis, but when you work in groups on analysis or broadcasting, then you could use this API to serve as combining all results


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

files schema
# Directory Structure:
# project/
# ├── app/
# │   ├── __init__.py
# │   ├── main.py
# │   ├── config.py
# │   ├── database.py
# │   ├── models/
# │   │   ├── __init__.py
# │   │   ├── user.py
# │   │   ├── machine.py
# │   │   ├── catalog.py
# │   │   ├── rate.py
# │   │   ├── case.py
# │   │   ├── session.py
# │   │   ├── analysis.py
# │   │   ├── merged_analysis.py
# │   │   ├── comparison.py
# │   ├── routers/
# │   │   ├── __init__.py
# │   │   ├── auth.py
# │   │   ├── machines.py
# │   │   ├── catalog.py
# │   │   ├── rates.py
# │   │   ├── cases.py
# │   │   ├── sessions.py
# │   │   ├── analysis.py
# │   │   ├── merged_analysis.py
# │   │   ├── comparison.py
# │   ├── schemas/
# │   │   ├── __init__.py
# │   │   ├── user.py
# │   │   ├── machine.py
# │   │   ├── catalog.py
# │   │   ├── rate.py
# │   │   ├── case.py
# │   │   ├── session.py
# │   │   ├── analysis.py
# │   │   ├── merged_analysis.py
# │   │   ├── comparison.py
# ├── setup.py
# ├── tests/
# │   ├── __init__.py
# │   ├── test_auth.py
# │   ├── test_machines.py
# │   ├── test_catalog.py
# │   ├── test_rates.py
# │   ├── test_cases.py
# │   ├── test_sessions.py
# │   ├── test_analysis.py
# │   ├── test_merged_analysis.py
# │   ├── test_comparison.py
# ├── .gitignore