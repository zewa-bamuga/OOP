FROM node:18-alpine AS build
ENV NODE_ENV=development

WORKDIR /app

COPY ./frontend/package-lock.json ./frontend/package.json ./
RUN npm install

COPY ./frontend/tsconfig.json ./frontend/tailwind.config.ts ./frontend/next-env.d.ts ./frontend/next.config.mjs ./frontend/.prettierrc ./
ADD ./frontend/public ./public
ADD ./frontend/src ./src

COPY .env .env

RUN npm run dev

FROM node:16-alpine AS production
WORKDIR /app
COPY --from=build /app ./
ENV NODE_ENV=production

RUN npm ci --only=production --legacy-peer-deps

EXPOSE 3000
CMD ["npm", "start"]
