FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

# This AI component is a CLI runtime used by the ASP.NET API, not a public HTTP service.
# Example: echo '{"age":30,"weight":75,"height":175,"goal":"maintain"}' | python eatopia_ai_cli.py diet-plan
ENTRYPOINT ["python", "eatopia_ai_cli.py"]
