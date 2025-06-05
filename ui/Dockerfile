FROM node:22-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm build build

FROM nginx:alpine

COPY nginx/ssl/selfsigned.crt /etc/nginx/ssl/selfsigned.crt
COPY nginx/ssl/selfsigned.key /etc/nginx/ssl/selfsigned.key
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
