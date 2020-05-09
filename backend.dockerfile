FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
COPY ./backend /app
RUN pip3 install -r requirements.txt