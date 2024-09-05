FROM python:3.12.4

# Expose port for Streamlit
EXPOSE 8501

# Create an app directory
CMD mkdir -p /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy everything else except the files in .dockerignore
COPY . .

# Run the Streamlit app
ENTRYPOINT [ "streamlit", "run" ]
CMD ["translator.py"]
