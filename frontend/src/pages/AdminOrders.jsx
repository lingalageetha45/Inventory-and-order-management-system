import { useEffect, useState } from "react";
import api from "../api/axios";

const ORDER_STATUSES = [
  "pending",
  "confirmed",
  "shipped",
  "delivered",
  "cancelled",
];

function AdminOrders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [updatingId, setUpdatingId] = useState(null);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const fetchOrders = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("/orders/");
      setOrders(response.data);
    } catch (error) {
      setError(
        error.response?.data?.detail ||
          "Unable to load orders."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const handleStatusChange = async (orderId, status) => {
    setError("");
    setSuccess("");
    setUpdatingId(orderId);

    try {
      let endpoint = null;

      if (status === "confirmed") {
        endpoint = `/orders/${orderId}/confirm`;
      } else if (status === "shipped") {
        endpoint = `/orders/${orderId}/ship`;
      } else if (status === "delivered") {
        endpoint = `/orders/${orderId}/deliver`;
      } else if (status === "cancelled") {
        endpoint = `/orders/${orderId}/cancel`;
      }

      if (!endpoint) {
        setUpdatingId(null);
        return;
      }

      await api.put(endpoint);

      setSuccess(
        `Order #${orderId} status updated successfully.`
      );

      await fetchOrders();
    } catch (error) {
      setError(
        error.response?.data?.detail ||
          "Unable to update order status."
      );
    } finally {
      setUpdatingId(null);
    }
  };

  if (loading) {
    return (
      <div className="admin-page">
        <header className="admin-header">
          <div>
            <h1>Order Management</h1>
            <p>View and manage customer orders.</p>
          </div>
        </header>

        <main className="admin-content">
          <section className="admin-section">
            <p>Loading orders...</p>
          </section>
        </main>
      </div>
    );
  }

  return (
    <div className="admin-page">
      <header className="admin-header">
        <div>
          <h1>Order Management</h1>
          <p>View and manage customer orders.</p>
        </div>

        <button
          type="button"
          onClick={fetchOrders}
        >
          Refresh Orders
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
          <h2>Orders</h2>

          {orders.length === 0 ? (
            <p>No orders found.</p>
          ) : (
            <div className="orders-list">
              {orders.map((order) => (
                <article
                  className="order-card"
                  key={order.id}
                >
                  <div className="order-card-header">
                    <div>
                      <h3>
                        Order #{order.id}
                      </h3>

                      <p>
                        Customer ID:{" "}
                        <strong>
                          {order.customer_id}
                        </strong>
                      </p>
                    </div>

                    <span
                      className={`order-status status-${order.status}`}
                    >
                      {order.status}
                    </span>
                  </div>

                  <div className="order-details">
                    <p>
                      <strong>Total:</strong>{" "}
                      ₹{order.total_amount}
                    </p>

                    <p>
                      <strong>Created:</strong>{" "}
                      {new Date(
                        order.created_at
                      ).toLocaleString()}
                    </p>

                    <p>
                      <strong>Updated:</strong>{" "}
                      {new Date(
                        order.updated_at
                      ).toLocaleString()}
                    </p>
                  </div>

                  <div className="order-items">
                    <h4>Order Items</h4>

                    {order.items?.length ? (
                      <div className="order-item-list">
                        {order.items.map((item) => (
                          <div
                            className="order-item"
                            key={item.id}
                          >
                            <div>
                              <strong>
                                Product #{item.product_id}
                              </strong>

                              <p>
                                Quantity:{" "}
                                {item.quantity}
                              </p>
                            </div>

                            <div>
                              <p>
                                Unit Price: ₹
                                {item.unit_price}
                              </p>

                              <p>
                                Subtotal: ₹
                                {item.subtotal}
                              </p>
                            </div>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p>No items found.</p>
                    )}
                  </div>

                  <div className="order-actions">
                    <label
                      htmlFor={`status-${order.id}`}
                    >
                      Update Status
                    </label>

                    <select
                      id={`status-${order.id}`}
                      value={order.status}
                      disabled={
                        updatingId === order.id
                      }
                      onChange={(event) =>
                        handleStatusChange(
                          order.id,
                          event.target.value
                        )
                      }
                    >
                      {ORDER_STATUSES.map(
                        (status) => (
                          <option
                            key={status}
                            value={status}
                          >
                            {status
                              .charAt(0)
                              .toUpperCase() +
                              status.slice(1)}
                          </option>
                        )
                      )}
                    </select>

                    {updatingId === order.id && (
                      <span>
                        Updating...
                      </span>
                    )}
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

export default AdminOrders;