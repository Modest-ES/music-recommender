# Build stage (Node.js)
FROM node:18 AS builder

WORKDIR /app

# Copy package files first (caching optimization)
COPY package*.json ./
RUN npm install

# Copy the rest and build
COPY . .
RUN npm run build

# Production stage (Nginx)
FROM nginx:alpine

# Copy built files to Nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom Nginx config (if needed)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]