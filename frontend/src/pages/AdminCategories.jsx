
import { useEffect, useState } from "react";
import api from "../api/axios";

const CATEGORY_STATUSES = ["active", "inactive"];

function AdminCategories() {
  const [categories, setCategories] = useState([]);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [deletingId, setDeletingId] = useState(null);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [editingId, setEditingId] = useState(null);

  const [form, setForm] = useState({
    name: "",
    description: "",
    status: "active",
  });

  const fetchCategories = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("/categories/");
      setCategories(response.data);
    } catch (error) {
      setError(
        error.response?.data?.detail ||
          "Unable to load categories."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  const handleChange = (event) => {
    setForm({
      ...form,
      [event.target.name]: event.target.value,
    });
  };

  const resetForm = () => {
    setForm({
      name: "",
      description: "",
      status: "active",
    });

    setEditingId(null);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");
    setSuccess("");
    setSaving(true);

    try {
      const data = {
        name: form.name.trim(),
        description: form.description.trim() || null,
        status: form.status,
      };

      if (editingId) {
        await api.put(
          `/categories/${editingId}`,
          data
        );

        setSuccess(
          "Category updated successfully."
        );
      } else {
        await api.post("/categories/", data);

        setSuccess(
          "Category created successfully."
        );
      }

      resetForm();
      await fetchCategories();
    } catch (error) {
      setError(
        error.response?.data?.detail ||
          "Unable to save category."
      );
    } finally {
      setSaving(false);
    }
  };

  const handleEdit = (category) => {
    setError("");
    setSuccess("");

    setEditingId(category.id);

    setForm({
      name: category.name,
      description: category.description || "",
      status: category.status,
    });

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  const handleDelete = async (categoryId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this category?"
    );

    if (!confirmed) {
      return;
    }

    setError("");
    setSuccess("");
    setDeletingId(categoryId);

    try {
      await api.delete(
        `/categories/${categoryId}`
      );

      setSuccess(
        "Category deleted successfully."
      );

      await fetchCategories();
    } catch (error) {
      setError(
        error.response?.data?.detail ||
          "Unable to delete category."
      );
    } finally {
      setDeletingId(null);
    }
  };

  if (loading) {
    return (
      <div className="admin-page">
        <header className="admin-header">
          <div>
            <h1>Category Management</h1>
            <p>
              Manage product categories.
            </p>
          </div>
        </header>

        <main className="admin-content">
          <section className="admin-section">
            <p>Loading categories...</p>
          </section>
        </main>
      </div>
    );
  }

  return (
    <div className="admin-page">
      <header className="admin-header">
        <div>
          <h1>Category Management</h1>
          <p>
            Create, update and manage product
            categories.
          </p>
        </div>

        <button
          type="button"
          onClick={fetchCategories}
        >
          Refresh
        </button>
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
              ? "Edit Category"
              : "Add Category"}
          </h2>

          <form onSubmit={handleSubmit}>
            <label htmlFor="category-name">
              Category Name
            </label>

            <input
              id="category-name"
              type="text"
              name="name"
              value={form.name}
              onChange={handleChange}
              placeholder="Enter category name"
              required
            />

            <label htmlFor="category-description">
              Description
            </label>

            <textarea
              id="category-description"
              name="description"
              value={form.description}
              onChange={handleChange}
              placeholder="Enter category description"
              rows="4"
            />

            <label htmlFor="category-status">
              Status
            </label>

            <select
              id="category-status"
              name="status"
              value={form.status}
              onChange={handleChange}
            >
              {CATEGORY_STATUSES.map(
                (status) => (
                  <option
                    key={status}
                    value={status}
                  >
                    {status === "active"
                      ? "Active"
                      : "Inactive"}
                  </option>
                )
              )}
            </select>

            <div className="form-actions">
              <button
                type="submit"
                disabled={saving}
              >
                {saving
                  ? "Saving..."
                  : editingId
                    ? "Update Category"
                    : "Create Category"}
              </button>

              {editingId && (
                <button
                  type="button"
                  onClick={resetForm}
                  disabled={saving}
                >
                  Cancel
                </button>
              )}
            </div>
          </form>
        </section>

        <section className="admin-section">
          <h2>Categories</h2>

          {categories.length === 0 ? (
            <p>No categories found.</p>
          ) : (
            <div className="category-list">
              {categories.map((category) => (
                <article
                  className="category-card"
                  key={category.id}
                >
                  <div>
                    <h3>{category.name}</h3>

                    <p>
                      {category.description ||
                        "No description available."}
                    </p>

                    <p>
                      <strong>ID:</strong>{" "}
                      {category.id}
                    </p>

                    <p>
                      <strong>Status:</strong>{" "}
                      {category.status}
                    </p>
                  </div>

                  <div className="category-actions">
                    <button
                      type="button"
                      onClick={() =>
                        handleEdit(category)
                      }
                    >
                      Edit
                    </button>

                    <button
                      type="button"
                      onClick={() =>
                        handleDelete(
                          category.id
                        )
                      }
                      disabled={
                        deletingId ===
                        category.id
                      }
                    >
                      {deletingId === category.id
                        ? "Deleting..."
                        : "Delete"}
                    </button>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default AdminCategories;

