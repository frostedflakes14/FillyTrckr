# Frontend Dockerfile - Multi-stage build for React app
# Stage 1: Build the React application
FROM node:20-alpine as build

WORKDIR /app

# Copy package files and install dependencies
# We copy package*.json first for better Docker layer caching
COPY package*.json ./
RUN npm install

# Copy source code and build
COPY . .
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine

# Copy built files from build stage to nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx configuration (we'll create this file)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
