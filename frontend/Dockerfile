# Dockerfile para frontend com Node.js + Vite
FROM node:20

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

# Instalar Tailwind e dependências via npm
RUN npx tailwindcss init -p

COPY . .

# Rodar dev server
CMD ["npm", "run", "dev"]
