
import { useEffect, useState } from "react";
import api from "../api/axios";

const PAYMENT_STATUSES = [
  "pending",
  "paid",
  "failed",
  "refunded",
];

function AdminPayments() {
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [updatingId, setUpdatingId] = useState(null);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const fetchPayments = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("/payments/");
      setPayments(response.data);
    } catch (error) {
      setError(
        error.response?.data?.detail ||
          "Unable to load payments."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPayments();
  }, []);

  const handleStatusChange = async (
    paymentId,
    payment_status
  ) => {
    setError("");
    setSuccess("");
    setUpdatingId(paymentId);

    try {
      await api.patch(
        `/payments/${paymentId}/status`,
        {
          payment_status,
        }
      );

      setSuccess(
        `Payment #${paymentId} status updated successfully.`
      );

      await fetchPayments();
    } catch (error) {
      setError(
        error.response?.data?.detail ||
          "Unable to update payment status."
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
            <h1>Payment Management</h1>
            <p>
              View and manage customer payments.
            </p>
          </div>
        </header>

        <main className="admin-content">
          <section className="admin-section">
            <p>Loading payments...</p>
          </section>
        </main>
      </div>
    );
  }

  return (
    <div className="admin-page">
      <header className="admin-header">
        <div>
          <h1>Payment Management</h1>
          <p>
            View and manage customer payments.
          </p>
        </div>

        <button
          type="button"
          onClick={fetchPayments}
        >
          Refresh Payments
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
          <h2>Payments</h2>

          {payments.length === 0 ? (
            <p>No payments found.</p>
          ) : (
            <div className="payments-list">
              {payments.map((payment) => (
                <article
                  className="payment-card"
                  key={payment.id}
                >
                  <div className="payment-card-header">
                    <div>
                      <h3>
                        Payment #{payment.id}
                      </h3>

                      <p>
                        Order ID:{" "}
                        <strong>
                          #{payment.order_id}
                        </strong>
                      </p>
                    </div>

                    <span
                      className={`payment-status payment-status-${payment.payment_status}`}
                    >
                      {payment.payment_status}
                    </span>
                  </div>

                  <div className="payment-details">
                    <p>
                      <strong>Amount:</strong>{" "}
                      ₹{payment.amount}
                    </p>

                    <p>
                      <strong>Method:</strong>{" "}
                      {payment.payment_method}
                    </p>

                    <p>
                      <strong>Payment Date:</strong>{" "}
                      {new Date(
                        payment.payment_date
                      ).toLocaleString()}
                    </p>

                    <p>
                      <strong>Last Updated:</strong>{" "}
                      {new Date(
                        payment.updated_at
                      ).toLocaleString()}
                    </p>
                  </div>

                  <div className="payment-actions">
                    <label
                      htmlFor={`payment-status-${payment.id}`}
                    >
                      Update Payment Status
                    </label>

                    <select
                      id={`payment-status-${payment.id}`}
                      value={payment.payment_status}
                      disabled={
                        updatingId === payment.id
                      }
                      onChange={(event) =>
                        handleStatusChange(
                          payment.id,
                          event.target.value
                        )
                      }
                    >
                      {PAYMENT_STATUSES.map(
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

                    {updatingId === payment.id && (
                      <span>Updating...</span>
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

export default AdminPayments;
