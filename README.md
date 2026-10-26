# WODS
Weather Observations Databse in SQLite (WODS) is a python application that reads GeoJSON data from weather station sites across the CONUS
and converts them into SQLite databases. This was created in the Spring of 2026 as the final project for my computer science course.

## How to Install
Create a venv that contains matplotlib, scipy, tkintermapview, numpy, and pandas:
```python
python -m venv .venv
```

Activate the venv and install with:
```python
python -m pip install -e .
```

And run:
```python
python -m wods
```