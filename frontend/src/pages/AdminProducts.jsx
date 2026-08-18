import { useEffect, useState } from "react";
import api from "../api/axios";

const emptyForm = {
  name: "",
  description: "",
  category_id: "",
  price: "",
  sku: "",
  stock_quantity: "",
  image: "",
  status: "active",
};

function AdminProducts() {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);

  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const fetchData = async () => {
    try {
      setLoading(true);
      setError("");

      const [productsResponse, categoriesResponse] =
        await Promise.all([
          api.get("/products/"),
          api.get("/categories/"),
        ]);

      setProducts(productsResponse.data);
      setCategories(categoriesResponse.data);
    } catch (error) {
      setError(
        error.response?.data?.detail ||
          "Unable to load products or categories."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleChange = (event) => {
    const { name, value } = event.target;

    setForm((currentForm) => ({
      ...currentForm,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");
    setSuccess("");
    setSaving(true);

    try {
      const productData = {
        name: form.name,
        description: form.description || null,
        category_id: Number(form.category_id),
        price: form.price,
        sku: form.sku,
        stock_quantity: Number(form.stock_quantity),
        image: form.image || null,
        status: form.status,
      };

      if (editingId) {
        await api.put(
          `/products/${editingId}`,
          productData
        );

        setSuccess("Product updated successfully.");
      } else {
        await api.post(
          "/products/",
          productData
        );

        setSuccess("Product created successfully.");
      }

      setForm(emptyForm);
      setEditingId(null);

      await fetchData();
    } catch (error) {
      setError(
        error.response?.data?.detail ||
          (editingId
            ? "Unable to update product."
            : "Unable to create product.")
      );
    } finally {
      setSaving(false);
    }
  };

  const handleEdit = (product) => {
    setError("");
    setSuccess("");

    setEditingId(product.id);

    setForm({
      name: product.name || "",
      description: product.description || "",
      category_id: product.category_id
        ? String(product.category_id)
        : "",
      price: product.price || "",
      sku: product.sku || "",
      stock_quantity:
        product.stock_quantity ?? "",
      image: product.image || "",
      status: product.status || "active",
    });

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setForm(emptyForm);
    setError("");
    setSuccess("");
  };

  const handleDelete = async (productId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this product?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setError("");
      setSuccess("");

      await api.delete(
        `/products/${productId}`
      );

      setSuccess("Product deleted successfully.");

      if (editingId === productId) {
        setEditingId(null);
        setForm(emptyForm);
      }

      await fetchData();
    } catch (error) {
      setError(
        error.response?.data?.detail ||
          "Unable to delete product."
      );
    }
  };

  if (loading) {
    return (
      <div className="admin-page">
        <header className="admin-header">
          <h1>Product Management</h1>
          <p>Manage products, prices and stock.</p>
        </header>

        <main className="admin-content">
          <p>Loading products...</p>
        </main>
      </div>
    );
  }

  return (
    <div className="admin-page">
      <header className="admin-header">
        <div>
          <h1>Product Management</h1>
          <p>Manage products, prices and stock.</p>
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
          <h2>
            {editingId
              ? "Edit Product"
              : "Add Product"}
          </h2>

          <form onSubmit={handleSubmit}>
            <label>Product Name</label>

            <input
              type="text"
              name="name"
              value={form.name}
              onChange={handleChange}
              placeholder="Enter product name"
              required
            />

            <label>Description</label>

            <textarea
              name="description"
              value={form.description}
              onChange={handleChange}
              placeholder="Enter product description"
            />

            <label>Category</label>

            <select
              name="category_id"
              value={form.category_id}
              onChange={handleChange}
              required
            >
              <option value="">
                Select category
              </option>

              {categories.map((category) => (
                <option
                  key={category.id}
                  value={category.id}
                >
                  {category.name}
                </option>
              ))}
            </select>

            <label>Price</label>

            <input
              type="number"
              name="price"
              value={form.price}
              onChange={handleChange}
              placeholder="Enter price"
              min="0"
              step="0.01"
              required
            />

            <label>SKU</label>

            <input
              type="text"
              name="sku"
              value={form.sku}
              onChange={handleChange}
              placeholder="Example: KB-001"
              required
            />

            <label>Stock Quantity</label>

            <input
              type="number"
              name="stock_quantity"
              value={form.stock_quantity}
              onChange={handleChange}
              placeholder="Enter stock quantity"
              min="0"
              required
            />

            <label>Image URL</label>

            <input
              type="url"
              name="image"
              value={form.image}
              onChange={handleChange}
              placeholder="https://example.com/product-image.jpg"
            />

            <label>Status</label>

            <select
              name="status"
              value={form.status}
              onChange={handleChange}
            >
              <option value="active">
                Active
              </option>

              <option value="inactive">
                Inactive
              </option>
            </select>

            <button
              type="submit"
              disabled={saving}
            >
              {saving
                ? editingId
                  ? "Updating..."
                  : "Creating..."
                : editingId
                ? "Update Product"
                : "Create Product"}
            </button>

            {editingId && (
              <button
                type="button"
                className="cancel-button"
                onClick={handleCancelEdit}
                disabled={saving}
              >
                Cancel Edit
              </button>
            )}
          </form>
        </section>

        <section className="admin-section">
          <h2>Products</h2>

          {products.length === 0 ? (
            <p>No products found.</p>
          ) : (
            <div className="product-list">
              {products.map((product) => (
                <div
                  className="product-card"
                  key={product.id}
                >
                  {product.image ? (
                    <img
                      className="admin-product-image"
                      src={product.image}
                      alt={product.name}
                    />
                  ) : (
                    <div className="product-image-placeholder">
                      No Image
                    </div>
                  )}

                  <h3>{product.name}</h3>

                  <p>
                    {product.description ||
                      "No description available."}
                  </p>

                  <p>
                    <strong>SKU:</strong>{" "}
                    {product.sku}
                  </p>

                  <p>
                    <strong>Price:</strong>{" "}
                    ₹{product.price}
                  </p>

                  <p>
                    <strong>Stock:</strong>{" "}
                    {product.stock_quantity}
                  </p>

                  <p>
                    <strong>Status:</strong>{" "}
                    {product.status}
                  </p>

                  <div className="product-actions">
                    <button
                      type="button"
                      className="edit-button"
                      onClick={() =>
                        handleEdit(product)
                      }
                    >
                      Edit
                    </button>

                    <button
                      type="button"
                      className="delete-button"
                      onClick={() =>
                        handleDelete(product.id)
                      }
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default AdminProducts;