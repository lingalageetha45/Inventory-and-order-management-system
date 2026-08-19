import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Login from "../pages/Login";
import Register from "../pages/Register";

import Products from "../pages/Products";
import Checkout from "../pages/Checkout";
import Orders from "../pages/Orders";

import AdminDashboard from "../pages/AdminDashboard";
import AdminProducts from "../pages/AdminProducts";
import AdminCategories from "../pages/AdminCategories";
import AdminInventory from "../pages/AdminInventory";
import AdminOrders from "../pages/AdminOrders";
import AdminPayments from "../pages/AdminPayments";

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>

        {/* =====================================================
            DEFAULT
        ===================================================== */}

        <Route
          path="/"
          element={<Navigate to="/login" replace />}
        />

        {/* =====================================================
            AUTHENTICATION
        ===================================================== */}

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />

        {/* =====================================================
            CUSTOMER
        ===================================================== */}

        <Route
          path="/products"
          element={<Products />}
        />

        <Route
          path="/checkout"
          element={<Checkout />}
        />

        <Route
          path="/orders"
          element={<Orders />}
        />

        {/* =====================================================
            ADMIN
        ===================================================== */}

        <Route
          path="/admin"
          element={<AdminDashboard />}
        />

        <Route
          path="/admin/products"
          element={<AdminProducts />}
        />

        <Route
          path="/admin/categories"
          element={<AdminCategories />}
        />

        <Route
          path="/admin/inventory"
          element={<AdminInventory />}
        />

        <Route
          path="/admin/orders"
          element={<AdminOrders />}
        />

        <Route
          path="/admin/payments"
          element={<AdminPayments />}
        />

        {/* =====================================================
            STAFF
        ===================================================== */}

        <Route
          path="/staff"
          element={<AdminDashboard />}
        />

        <Route
          path="/staff/products"
          element={<AdminProducts />}
        />

        <Route
          path="/staff/categories"
          element={<AdminCategories />}
        />

        <Route
          path="/staff/inventory"
          element={<AdminInventory />}
        />

        <Route
          path="/staff/orders"
          element={<AdminOrders />}
        />

        <Route
          path="/staff/payments"
          element={<AdminPayments />}
        />

        {/* =====================================================
            UNKNOWN ROUTES
        ===================================================== */}

        <Route
          path="*"
          element={<Navigate to="/login" replace />}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;