# Imagen base para Nginx
FROM nginx:alpine

# Copiar la configuración de Nginx al directorio de configuración predeterminado de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar los archivos estáticos (HTML/CSS/JS) al directorio de servicio de Nginx
COPY . /usr/share/nginx/html

# Puerto por defecto de Nginx
EXPOSE 80