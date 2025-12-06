FROM node:18 AS build

WORKDIR /app

# Copy package files from THIS directory (no frontend/ prefix)
COPY package.json package-lock.json ./
RUN npm install

# Copy all frontend source code
COPY . .
RUN npm run build

# -----------------------------
# Production stage
# -----------------------------
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80 for NGINX
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
