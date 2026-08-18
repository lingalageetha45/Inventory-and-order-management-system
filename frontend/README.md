# Inventory & Order Management System — Frontend

Professional React + Vite frontend for the Inventory & Order Management System.

## Features

- JWT login and customer registration
- Customer product browsing
- Product image support with local fallback for the Wireless Mouse
- Shopping cart with quantity controls
- Checkout with UPI, Card, Cash and Bank Transfer options
- Customer order history
- Admin dashboard
- Product management
- Category management
- Inventory management
- Order management
- Payment management
- Responsive layout for desktop and mobile

## Requirements

- Node.js 18+
- Running FastAPI backend on `http://127.0.0.1:8000`

## Setup

```powershell
cd "C:\Inventory and order management system\frontend"
npm install
npm run dev
```

Open the Vite URL shown in the terminal, normally:

`http://localhost:5173`

## Backend URL

The frontend uses:

`http://127.0.0.1:8000/api/v1`

You can override it by creating `.env` from `.env.example`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

## Production build

```powershell
npm run build
```

## Product Images

The Wireless Mouse image is included at:

`public/images/wireless-mouse.png`

The customer Products page automatically uses this image when Product #1 has no image URL in the database. If the backend returns an `image` value, that backend image takes priority.

## Important

This frontend is designed to work with the existing FastAPI API routes in the project. No backend database changes are required for the included local product image fallback.
