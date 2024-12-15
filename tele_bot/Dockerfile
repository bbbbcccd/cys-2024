# Use a base image with Python
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot script
COPY . .

# Run the bot script
CMD ["python", "phishzilla_bot.py"]
