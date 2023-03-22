# Django REST framework and Vue.js recipe app

The app is built with the **Django REST framework** on the backend and **Vue.js** on the frontend.
DRF backend uses:

- Docker
- Postgres
- drf-spectacular for documentation

Vue frontend uses:

- Vue 3
    + TypeScript
    + Composition API
- Vuetify

## Getting started

1. Clone the repository.
2. To run the backend app:
    1) In the main project directory, run in the terminal `cd drf_backend`
    2) Rename `.env.sample` to `.env` and replace the values
    3) Then run `docker-compose up --build`
    4) Now everything should be set up and app's documentation available on http://localhost:8000/api/docs/

3. To run the frontend app:
    1) In the main project directory, run in the terminal `cd vue_frontend`
    2) Rename `.env.sample` to `.env` and replace the values
    3) Run in the terminal `yarn` or `npm install`
    4) Then run: `yarn dev` or `npm run dev`
    5) Now, app should be running at http://localhost:3000/

## Testing

To run DRF tests:
1. If containers are not running, run in your terminal (in `drf_backend` directory) `docker-compose up`
2. In the second terminal tab, run `docker ps` and get the ID of the app container
3. Run `docker exec -itu 0 <container ID> sh` to get access to the container's shell as a root user
4. Run `python manage.py test` to run all tests or `python manage.py test <app-name>.tests` to run tests for a specific
   app.

## API Endpoints

**User app**

- Use `/api/user/create/` to create a new user
- Then use `/api/user/token/` to create a token for the created user
- Use `/api/user/me/` to retrieve and update user details

**Recipe app**

- Use `/api/recipe/recipes/` to create a new recipe and retrieve all recipes
- Use `/api/recipe/recipes/{id}/` to see recipe details, update and delete a recipe
- Use `/api/recipe/recipes/{id}/upload-image/` to upload recipe image


- Use `/api/recipe/tags/` to retrieve all tags
- Use `/api/recipe/tags/{id}/` to update and delete a tag


- Use `/api/recipe/ingredients/` to retrieve all ingredients
- Use `/api/recipe/ingredients/{id}/` to update and delete an ingredient


More information about API endpoints, with examples of data that needs to be sent with a request, can be found
on http://localhost:8000/api/docs/ 


### More Information
This DRF app uses djangorestframework-camel-case to enable the server to send and receive data in a format that is compatible with TypeScript. This package provides support for camel-case style serialization and deserialization, which is appropriate for the conventions used in Vue.js.
