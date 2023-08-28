FROM nginx:latest

# Remove the default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy your custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d

# Create a user named "appuser"
RUN useradd -ms /bin/bash appuser

# Set the working directory to /var/www (adjust as needed)
WORKDIR /app/static

# Change ownership of the working directory to "appuser"
RUN chown -R appuser:appuser /app/static
RUN chmod -R 755 /app/static
