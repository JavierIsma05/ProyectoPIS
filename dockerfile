# Imagen nos va a servir para basar nuestra nueva imagen en una imagen ya existente
FROM python:3.10
#nos va a servir para crear variables de ambiente dentro
# de nuestra imagen(Ambiente testing o productivo)
ENV PYTHONUNBUFFERED 1

# Directorio que se crea en el contenedor y 
# en donde se ejecutarán otras instrucciones como CMD, 
# COPY o RUN
WORKDIR /app
# Copiar archivo con las dependencias del backend
COPY requirements.txt /app/requirements.txt

# Instalar dependencias
RUN pip install -r requirements.txt

# Copiar todos los demas archivos
COPY . /app/

#CMD [ "python", "manage.py", "runserver", "0.0.0.0:80" ]
CMD python manage.py runserver 0.0.0.0:80