# Use an official lightweight Python image
FROM python:3.10
SHELL ["/bin/bash", "-c"]

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy project files to the container
COPY pyproject.toml poetry.lock ./
COPY . .

# Create a virtual environment and install dependencies using Poetry
RUN python -m venv .venv \
    && source .venv/bin/activate \
    && poetry install --no-interaction --no-ansi

# Set the environment path to use the virtual environment
ENV PATH="/root/.local/share/pypoetry/venv/bin:$PATH"

# Expose the port Flask runs on
EXPOSE 5000

# Define the command to run the application
CMD ["poetry", "run", "python", "app.py"]
