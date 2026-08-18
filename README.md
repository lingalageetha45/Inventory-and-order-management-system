\# Inventory \& Order Management System



A full-stack Inventory \& Order Management System built using \*\*FastAPI, PostgreSQL, SQLAlchemy, Alembic, and React\*\*.



\## Project Overview



This system allows customers to browse products, add products to a shopping cart, place orders, select a payment method, and view their order history.



Administrators and staff can manage products, categories, inventory, and customer orders.



\## User Roles



\* \*\*Admin\*\* – Manage products, categories, inventory, and orders.

\* \*\*Staff\*\* – Manage operational product, inventory, and order activities.

\* \*\*Customer\*\* – Browse products, add items to cart, place orders, make payments, and view orders.



\## Features



\### Authentication \& Authorization



\* User registration and login

\* JWT-based authentication

\* Role-based authorization

\* Admin, Staff, and Customer roles

\* Active/inactive user account handling

\* Protected API endpoints



\### Product Management



\* Create products

\* Update products

\* View products

\* Product name and description

\* Category assignment

\* Price

\* SKU

\* Stock quantity

\* Active/inactive status

\* Product image URL



\### Category Management



\* Create categories

\* View categories

\* Update categories

\* Organize products by category



\### Inventory Management



\* Inventory record for products

\* Current stock tracking

\* Minimum stock level

\* Maximum stock level

\* Stock synchronization with products

\* Automatic stock deduction when an order is placed

\* Low-stock tracking



\### Shopping Cart



\* Browse available products

\* Add products to cart

\* Increase/decrease quantity

\* Remove products from cart

\* Stock quantity validation

\* Automatic cart total calculation



\### Order Management



\* Customer checkout

\* Order creation

\* Order items

\* Quantity tracking

\* Unit price and subtotal

\* Total order amount

\* Customer order history

\* Admin/staff order management

\* Order cancellation

\* Order status management



\### Order Status Flow



```text

Pending

&#x20;  ↓

Confirmed

&#x20;  ↓

Shipped

&#x20;  ↓

Delivered

```



Orders can also be cancelled according to the application's authorization and business rules.



\### Payment Management



Supported payment methods:



\* UPI

\* Card

\* Cash

\* Bank Transfer



\### Reviews



\* Product reviews

\* Product ratings

\* Customer-based review functionality



\### Notifications



\* Notification functionality for application events



\### Image/File Support



\* Product image URL support

\* Profile/upload directories

\* Frontend product image display



\## Technology Stack



\### Backend



\* Python

\* FastAPI

\* SQLAlchemy

\* PostgreSQL

\* Pydantic

\* Alembic

\* JWT Authentication

\* Uvicorn



\### Frontend



\* React

\* React Router

\* Axios

\* JavaScript

\* CSS



\## Backend Setup



\### 1. Open the backend folder



```powershell

cd backend

```



\### 2. Create a virtual environment



```powershell

python -m venv venv

```



\### 3. Activate the virtual environment



Windows PowerShell:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



\### 4. Install dependencies



```powershell

pip install -r requirements.txt

```



\## PostgreSQL Setup



Create a PostgreSQL database named:



```text

inventory\_order\_db

```



The application uses PostgreSQL as its database.



Configure the database connection in `.env`.



Example:



```text

DATABASE\_URL=postgresql+psycopg2://postgres:YOUR\_PASSWORD@localhost:5432/inventory\_order\_db

```



\*\*Do not commit or submit the real `.env` file. Use `.env.example` for configuration reference.\*\*



\## Database Migrations



Alembic is used for database migrations.



From the `backend` directory:



```powershell

alembic upgrade head

```



To check migration status:



```powershell

alembic check

```



To create a new migration:



```powershell

alembic revision --autogenerate -m "migration message"

```



\## Run the Backend



From the `backend` directory:



```powershell

uvicorn app.main:app --reload

```



Backend URL:



```text

http://127.0.0.1:8000

```



\## Swagger API Documentation



FastAPI provides interactive API documentation.



Open:



```text

http://127.0.0.1:8000/docs

```



ReDoc:



```text

http://127.0.0.1:8000/redoc

```



Swagger can be used to test the available authentication, product, category, inventory, order, payment, review, and notification APIs.



\## Run the Frontend



Open a second terminal and run:



```powershell

cd frontend

npm install

npm run dev

```



Then open the URL displayed by the frontend development server.



Usually:



```text

http://localhost:5173

```



\## Database Entities



The main database entities include:



\* Users

\* Categories

\* Products

\* Inventory

\* Orders

\* Order Items

\* Payments

\* Reviews

\* Notifications



\## Inventory \& Order Verification



Product stock and inventory stock are synchronized.



Example:



```text

Gaming Headset



Before order:

Stock = 14



Quantity ordered:

1



After order:

Stock = 13



Inventory current\_stock:

13

```



The application also maintains inventory records for all available products.



\## Security



\* JWT authentication is used for protected APIs.

\* Role-based authorization controls access to operations.

\* Customers can access their own orders.

\* Admin and Staff users can manage operational order activities.

\* Database credentials should remain in `.env`.

\* Real passwords and secrets should not be included in the submitted project.



\## Docker



Docker is \*\*not required\*\* for this project.



The application is configured to run using:



\* PostgreSQL

\* FastAPI

\* Python

\* React



\## Submission Notes



Before submitting the project, do not include:



\* `.env` containing real credentials

\* `venv`

\* `node\_modules`

\* `\_\_pycache\_\_`

\* `.pyc` files

\* Other machine-specific development files



The submission should contain the source code, migrations, configuration example, requirements, documentation, and project screenshots.



\## Application Status



The core Inventory \& Order Management System functionality has been implemented and tested, including:



\* Authentication

\* Role-based authorization

\* Category management

\* Product management

\* Product images

\* Inventory management

\* Shopping cart

\* Checkout

\* Payment method selection

\* Order creation

\* Inventory stock deduction

\* Customer order history

\* Admin/staff order management

\* Order status workflow

\* Reviews

\* Notifications

\* PostgreSQL database

\* Alembic migrations

\* FastAPI Swagger documentation



