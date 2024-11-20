# Base image with Python and Spark
FROM apache/spark-py:latest

# Set the working directory in the container
WORKDIR /app
USER root

RUN pip install --upgrade pip --user

# Copy project files to the container
COPY app/ /app
COPY requirements.txt /app
COPY config/ /app/config

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt --user

# Set environment variables (optional)
ENV SPARK_HOME=/opt/spark
ENV PYTHONPATH=/app

# Expose any necessary ports (e.g., Spark UI)
EXPOSE 4040

# Command to run the pipeline
CMD ["python3", "tvp_pipeline.py"]
