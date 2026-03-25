# Ecommerce API

A REST API for an ecommerce platform built with FastAPI and PostgreSQL. Provides user management, product catalog, shopping cart, and an admin dashboard with role-based access control.

---

## Tech Stack

- **Framework**: FastAPI
- **Server**: Uvicorn
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **Authentication**: JWT (python-jose, HS256)
- **Password Hashing**: passlib (bcrypt)
- **Validation**: Pydantic v2
- **Python**: >= 3.12

---

## Project Structure

```
app/
├── core/
│   ├── database.py        # DB connection and session
│   └── security.py        # JWT, password hashing, auth dependencies
├── models/
│   ├── user_model.py
│   ├── product_model.py
│   ├── cart_model.py
│   └── cart_items.py
├── routers/
│   ├── users_router.py
│   ├── admin_router.py
│   ├── products_router.py
│   └── cart_router.py
├── schemas/
│   ├── user/
│   ├── product/
│   └── cart/
└── services/
    ├── user/
    ├── admin/
    └── product/
```

---

## Setup

1. **Clone the repository and create a virtual environment:**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. **Configure environment variables:**

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/ecommerce
```

3. **Run the server:**

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.  
Interactive docs at `http://localhost:8000/docs`.

---

## Authentication

The API uses OAuth2 with JWT Bearer tokens.

- Obtain a token via `POST /users/login`.
- Include the token in the `Authorization` header: `Bearer <token>`.
- Tokens expire after 30 minutes.
- Admin endpoints require a user with `role = "admin"`.

---

## Endpoints

### Users

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/users/register` | No | Register a new user |
| POST | `/users/login` | No | Login and obtain access token |
| GET | `/users/me` | Yes | Get current user info |
| POST | `/users/logout` | Yes | Invalidate current token |
| PUT | `/users/me/modify` | Yes | Update username and email |
| PUT | `/users/me/password` | Yes | Change password |
| DELETE | `/users/me/delete` | Yes | Delete own account |

#### POST `/users/register`
```json
{
  "username": "frandev",
  "email": "fran@gmail.com",
  "password": "test123"
}
```
Response:
```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "username": "frandev",
    "email": "fran@gmail.com",
    "role": "customer"
  }
}
```

#### POST `/users/login`
Form data: `username`, `password`

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### PUT `/users/me/modify`
```json
{
  "username": "frandev2",
  "email": "fran2@gmail.com"
}
```

#### PUT `/users/me/password`
```json
{
  "old_password": "test123",
  "new_password": "newpass456"
}
```

---

### Cart

All cart endpoints require authentication.

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/cart` | Yes | Get current user's active cart |
| POST | `/cart/add` | Yes | Add a product to the cart |
| POST | `/cart/remove` | Yes | Remove a product from the cart |
| POST | `/cart/clear` | Yes | Clear all items from the cart |
| PUT | `/cart/update` | Yes | Update item quantity |

#### GET `/cart`
Response:
```json
[
  {
    "id": 1,
    "name": "Laptop",
    "description": "High performance laptop",
    "price": 999.99
  }
]
```

#### POST `/cart/add`
```json
{
  "product_id": 1,
  "quantity": 2
}
```

---

### Admin Dashboard

All admin endpoints require authentication and `role = "admin"`.

#### Users

| Method | Path | Description |
|--------|------|-------------|
| GET | `/admin/dashboard` | Welcome message with admin username |
| POST | `/admin/dashboard/users/create` | Create a user with any role |
| GET | `/admin/dashboard/users` | List all users |
| GET | `/admin/dashboard/users/{user_id}` | Get user by ID |
| DELETE | `/admin/dashboard/users/delete/{user_id}` | Delete user by ID |
| PUT | `/admin/dashboard/users/{user_id}/role` | Update user role |

#### POST `/admin/dashboard/users/create`
```json
{
  "username": "newadmin",
  "email": "admin@example.com",
  "password": "securepass",
  "role": "admin"
}
```

#### Products

| Method | Path | Description |
|--------|------|-------------|
| POST | `/admin/dashboard/products/add` | Add a new product |
| GET | `/admin/dashboard/products` | List all products |
| GET | `/admin/dashboard/products/{product_id}` | Get product by ID |

#### POST `/admin/dashboard/products/add`
```json
{
  "name": "Laptop",
  "description": "High performance laptop for professionals",
  "price": 999.99
}
```

Response:
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "High performance laptop for professionals",
  "price": 999.99
}
```

---

## Database Models

### User
| Field | Type | Description |
|-------|------|-------------|
| id | Integer (PK) | Auto-incremented ID |
| username | String(50) | Unique username |
| email | String(120) | Unique email |
| password_hash | String(128) | Bcrypt hashed password |
| role | String(20) | `customer` (default) or `admin` |

### Product
| Field | Type | Description |
|-------|------|-------------|
| id | Integer (PK) | Auto-incremented ID |
| name | String(100) | Product name |
| description | String(255) | Product description |
| price | Float | Product price |

### Cart
| Field | Type | Description |
|-------|------|-------------|
| id | Integer (PK) | Auto-incremented ID |
| user_id | FK → users.id | Owner of the cart |
| is_active | Boolean | Whether the cart is active |

### CartItems
| Field | Type | Description |
|-------|------|-------------|
| id | Integer (PK) | Auto-incremented ID |
| cart_id | FK → carts.id | Associated cart |
| product_id | FK → products.id | Associated product |
