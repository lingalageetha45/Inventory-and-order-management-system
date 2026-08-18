
import { useNavigate } from "react-router-dom";

function AdminDashboard() {
  const navigate = useNavigate();

  return (
    <div className="admin-page">
      <header className="admin-header">
        <div>
          <h1>Inventory & Order Management</h1>
          <p>Admin Dashboard</p>
        </div>
      </header>

      <main className="admin-content">
        <div className="dashboard-grid">
          <div className="dashboard-card">
            <h2>Products</h2>
            <p>Manage products and pricing.</p>

            <button
              type="button"
              onClick={() => navigate("/admin/products")}
            >
              Manage Products
            </button>
          </div>

          <div className="dashboard-card">
            <h2>Categories</h2>
            <p>Manage product categories.</p>

            <button
              type="button"
              onClick={() => navigate("/admin/categories")}
            >
              Manage Categories
            </button>
          </div>

          <div className="dashboard-card">
            <h2>Inventory</h2>
            <p>Track stock and inventory.</p>

            <button
              type="button"
              onClick={() => navigate("/admin/inventory")}
            >
              Manage Inventory
            </button>
          </div>

          <div className="dashboard-card">
              <h2>Payments</h2>
              <p>View and manage customer payments.</p>

              <button
                type="button"
                onClick={() => navigate("/admin/payments")}
                >
                Manage Payments
              </button>
          </div>

          <div className="dashboard-card">
            <h2>Orders</h2>
            <p>View and manage customer orders.</p>

            <button
              type="button"
              onClick={() => navigate("/admin/orders")}
            >
              Manage Orders
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

export default AdminDashboard;

