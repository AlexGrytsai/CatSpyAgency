# Spy Cat Agency Management System

This is a management system designed for Spy Cat Agency (SCA), built using *
*Django REST Framework (DRF)**, **SimpleJWT** for authentication, **Argon2**
for password hashing, **Docker** and **Docker Compose** for containerization,
and **PostgreSQL** as the database. The system allows SCA to manage spy cats,
missions, and targets with a RESTful API. It includes validation,
authentication, and API documentation.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Authentication](#authentication)
- [Testing](#testing)
- [License](#license)

## Overview

This application allows Spy Cat Agency to manage their spy cats, missions, and
targets. The core features of the system include:

- **Spy Cats**: Ability to create, update, list, and remove spy cats from the
  system.
- **Missions and Targets**: Ability to create, update, delete, and list
  missions along with their associated targets.
- **Notes and Complete State**: Cats can add and update notes for their
  assigned targets, with restrictions once a target is marked as complete.

## Installation

To get started with this project, follow these steps:

1. Clone this repository:

```sh  
git clone https://github.com/AlexGrytsai/CatSpyAgency.git  
cd https://github.com/AlexGrytsai/CatSpyAgency.git  
```

2. Build and run the Docker containers:

```sh  
docker-compose up  
```

This will set up the following services:

- **PostgreSQL** database (with initialization scripts)
- **Django application** running on port 8000


3. Create a superuser:

```
docker-compose exec app-1 python manage.py createsuperuser 
```

After created Super User, exit from container using the following command:

```sh  
exit  
```

## Configuration

1. **Database**:

    - PostgreSQL is used as the database.
    - The database connection settings are defined in the `.env` file.
2. **JWT Authentication**:

    - SimpleJWT is used for authentication.
    - Secure login is required to interact with most endpoints.
3. **API Documentation**:

    - DRF Spectacular is used to generate interactive API documentation.
4. **Cat Breed Validation**:

    - Breed validation for spy cats is done using
      the [TheCatAPI](https://api.thecatapi.com/v1/breeds) service.

## Usage

Once the application is running, the API can be accessed at:

arduino

Копировать код

`http://localhost:8000`

### Endpoints

Use swagger doc - [SWAGGER](127.0.0.1:8000/api/v1/doc/swagger/)

#### **Authentication**

- **Login**: `POST /api/token/`
    - Request body: `{ "username": "username", "password": "password" }`
    - Returns JWT tokens for authentication.
- **Refresh token**: `POST /api/token/refresh/`
    - Request body: `{ "refresh": "refresh_token" }`

## Authentication

Authentication is handled via **JWT tokens** using the SimpleJWT package. To
access most endpoints, you need to first authenticate using the login endpoint,
which will return access and refresh tokens. Use the access token as a Bearer
token in the Authorization header for subsequent requests.

For use an access token, you can
use [ModHeader - Modify HTTP headers](https://chromewebstore.google.com/detail/modheader-modify-http-hea/idgpnmonknjnojddfkpgkljpfnnfcklj?pli=1)
for Chrome. After installing it, you need added Authorization with "Bearer <
your_access_token>".  
Now, you can use all application's feathers.

## Testing

To run tests for this application, use the following command:

```sh
docker-compose exec app-1 python manage.py test
```

This will run all the tests defined in the `tests` directory.

## License

This project is licensed under the MIT License. See the LICENSE file for more
details.

----------

This README provides an overview of the system's functionality, setup, and
usage. The application allows the Spy Cat Agency to manage spy cats, missions,
and targets efficiently through a simple, RESTful API.