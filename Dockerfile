FROM python:3.14.7    

WORKDIR /app

COPY inventory_manager.py .
COPY inventory.json .   

CMD ["python", "inventory_manager.py"]