FROM python:3.12-slim

WORKDIR /app

# Install agent dependencies
COPY link_agent/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared code and agent code
COPY shared/ ./shared/
COPY link_agent/ ./link_agent/

# Expose the A2A agent port
EXPOSE 8001

CMD ["uvicorn", "link_agent.app:a2a_app", "--host", "0.0.0.0", "--port", "8001"]
