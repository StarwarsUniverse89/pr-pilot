# Use the official Nginx image as the parent image
FROM nginx:alpine

# Remove the default Nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy the collected static files into the Nginx image
COPY ./static /usr/share/nginx/html/static

# Copy a custom Nginx configuration file into the image
COPY nginx.conf /etc/nginx/conf.d

# Expose port 80 to the Docker host, so we can access it
# from the outside.
EXPOSE 80
