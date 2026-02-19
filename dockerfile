# ---------------------------------------------------
# I used a minimal official Python base image to keep
# the container compatible with arm64 systems
# ---------------------------------------------------
FROM python:3.11-slim

# ---------------------------------------------------
# I have set a dedicated working directory inside the
# container so that all commands run from a known,
# predictable location.
# ---------------------------------------------------
WORKDIR /app

# ---------------------------------------------------
# I have copied the entire project (source code + data)
# into the container.
# ---------------------------------------------------
COPY . .

# ---------------------------------------------------
# I have installed only the Python libraries needed to run
# the forecasting pipeline.
# ---------------------------------------------------
RUN pip install --no-cache-dir pandas numpy transformers torch

# ---------------------------------------------------
# When the container is started, it automatically runs
# the full forecasting pipeline end-to-end. 
# ---------------------------------------------------
CMD ["python", "main.py"]
