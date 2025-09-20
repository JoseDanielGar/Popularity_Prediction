FROM node:20-alpine
WORKDIR /app
ARG PORT
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE $PORT
CMD ["sh", "-c", "npm run dev -- --host --port $PORT"]
