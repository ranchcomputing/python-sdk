
# Use an official Sphinx image as a base
FROM sphinxdoc/sphinx:latest

# Set the working directory
WORKDIR /sdk

# Copy the Sphinx project files to the container
COPY . .

# # Build the Sphinx documentation
# RUN make html
RUN pip install furo
RUN pip install myst-parser
RUN python3 -m pip install nox
RUN nox

# Use an official Nginx image as the final base image
FROM nginx:latest

# Copy the built documentation from the Sphinx image to the Nginx image
COPY --from=0 sdk/docs/_build/html /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
