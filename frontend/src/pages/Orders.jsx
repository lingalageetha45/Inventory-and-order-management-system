
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

function Orders() {
  const navigate = useNavigate();

  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await api.get("/orders/");
        setOrders(response.data);
      } catch (error) {
        setError(
          error.response?.data?.detail ||
            "Unable to load your orders."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, []);

  if (loading) {
    return (
      <div className="customer-page">
        <h1>My Orders</h1>
        <p>Loading your orders...</p>
      </div>
    );
  }

  return (
    <div className="customer-page">
      <header className="customer-header">
        <div>
          <h1>My Orders</h1>
          <p>View your order history and status.</p>
        </div>

        <button
          type="button"
          onClick={() => navigate("/products")}
        >
          Continue Shopping
        </button>
      </header>

      <main className="customer-content">
        {error && (
          <p className="error-message">
            {error}
          </p>
        )}

        {orders.length === 0 ? (
          <section className="empty-state">
            <h2>No Orders Yet</h2>

            <p>
              You haven't placed any orders yet.
            </p>

            <button
              type="button"
              onClick={() => navigate("/products")}
            >
              Start Shopping
            </button>
          </section>
        ) : (
          <section className="orders-section">
            {orders.map((order) => (
              <article
                className="order-card"
                key={order.id}
              >
                <div className="order-header">
                  <div>
                    <h2>
                      Order #{order.id}
                    </h2>

                    <p>
                      Placed on{" "}
                      {new Date(
                        order.created_at
                      ).toLocaleString()}
                    </p>
                  </div>

                  <span
                    className={`order-status status-${order.status}`}
                  >
                    {order.status}
                  </span>
                </div>

                <div className="order-items">
                  {order.items?.map((item) => (
                    <div
                      className="order-item"
                      key={item.id}
                    >
                      <div>
                        <strong>
                          Product #{item.product_id}
                        </strong>

                        <p>
                          Quantity: {item.quantity}
                        </p>
                      </div>

                      <div>
                        <p>
                          Unit Price: ₹
                          {Number(
                            item.unit_price
                          ).toFixed(2)}
                        </p>

                        <strong>
                          Subtotal: ₹
                          {Number(
                            item.subtotal
                          ).toFixed(2)}
                        </strong>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="order-footer">
                  <span>Total Amount</span>

                  <strong>
                    ₹
                    {Number(
                      order.total_amount
                    ).toFixed(2)}
                  </strong>
                </div>
              </article>
            ))}
          </section>
        )}
      </main>
    </div>
  );
}

export default Orders;
