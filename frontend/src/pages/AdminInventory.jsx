
import { useEffect, useState } from "react";
import api from "../api/axios";

function AdminInventory() {
  const [inventory, setInventory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [form, setForm] = useState({
    product_id: "",
    current_stock: "",
    minimum_stock_level: "",
    maximum_stock_level: "",
  });

  const fetchInventory = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("/inventory/");
      setInventory(response.data);
    } catch (error) {
      setError(
        error.response?.data?.detail ||
          "Unable to load inventory."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInventory();
  }, []);

  const handleChange = (event) => {
    setForm({
      ...form,
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");
    setSuccess("");

    if (
      Number(form.maximum_stock_level) <=
      Number(form.minimum_stock_level)
    ) {
      setError(
        "Maximum stock level must be greater than minimum stock level."
      );
      return;
    }

    setSaving(true);

    try {
      await api.post("/inventory/", {
        product_id: Number(form.product_id),
        current_stock: Number(form.current_stock),
        minimum_stock_level: Number(form.minimum_stock_level),
        maximum_stock_level: Number(form.maximum_stock_level),
      });

      setSuccess("Inventory created successfully.");

      setForm({
        product_id: "",
        current_stock: "",
        minimum_stock_level: "",
        maximum_stock_level: "",
      });

      await fetchInventory();
    } catch (error) {
      setError(
        error.response?.data?.detail ||
          "Unable to create inventory."
      );
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="admin-page">
        <header className="admin-header">
          <div>
            <h1>Inventory Management</h1>
            <p>Track product stock and inventory.</p>
          </div>
        </header>

        <main className="admin-content">
          <section className="admin-section">
            <p>Loading inventory...</p>
          </section>
        </main>
      </div>
    );
  }

  return (
    <div className="admin-page">
      <header className="admin-header">
        <div>
          <h1>Inventory Management</h1>
          <p>Track product stock and inventory.</p>
        </div>
      </header>

      <main className="admin-content">
        {error && (
          <p className="error-message">
            {error}
          </p>
        )}

        {success && (
          <p className="success-message">
            {success}
          </p>
        )}

        <section className="admin-section">
          <h2>Add Inventory</h2>

          <form onSubmit={handleSubmit}>
            <label>Product ID</label>

            <input
              type="number"
              name="product_id"
              value={form.product_id}
              onChange={handleChange}
              placeholder="Enter product ID"
              min="1"
              required
            />

            <label>Current Stock</label>

            <input
              type="number"
              name="current_stock"
              value={form.current_stock}
              onChange={handleChange}
              placeholder="Enter current stock"
              min="0"
              required
            />

            <label>Minimum Stock Level</label>

            <input
              type="number"
              name="minimum_stock_level"
              value={form.minimum_stock_level}
              onChange={handleChange}
              placeholder="Enter minimum stock level"
              min="0"
              required
            />

            <label>Maximum Stock Level</label>

            <input
              type="number"
              name="maximum_stock_level"
              value={form.maximum_stock_level}
              onChange={handleChange}
              placeholder="Enter maximum stock level"
              min="1"
              required
            />

            <button
              type="submit"
              disabled={saving}
            >
              {saving
                ? "Creating..."
                : "Create Inventory"}
            </button>
          </form>
        </section>

        <section className="admin-section">
          <h2>Inventory Records</h2>

          {inventory.length === 0 ? (
            <p>No inventory records found.</p>
          ) : (
            <div className="product-list">
              {inventory.map((item) => (
                <div
                  className="product-card"
                  key={item.id}
                >
                  <h3>
                    Inventory #{item.id}
                  </h3>

                  <p>
                    <strong>Product ID:</strong>{" "}
                    {item.product_id}
                  </p>

                  <p>
                    <strong>Current Stock:</strong>{" "}
                    {item.current_stock}
                  </p>

                  <p>
                    <strong>Minimum Stock:</strong>{" "}
                    {item.minimum_stock_level}
                  </p>

                  <p>
                    <strong>Maximum Stock:</strong>{" "}
                    {item.maximum_stock_level}
                  </p>

                  <p>
                    <strong>Last Updated:</strong>{" "}
                    {new Date(
                      item.last_updated_at
                    ).toLocaleString()}
                  </p>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default AdminInventory;

