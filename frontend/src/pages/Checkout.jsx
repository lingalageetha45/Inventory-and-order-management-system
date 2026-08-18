
import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import api from "../api/axios";

const PAYMENT_METHODS = [
  {
    value: "upi",
    label: "UPI",
  },
  {
    value: "card",
    label: "Card",
  },
  {
    value: "cash",
    label: "Cash",
  },
  {
    value: "bank_transfer",
    label: "Bank Transfer",
  },
];

function Checkout() {
  const location = useLocation();
  const navigate = useNavigate();

  const cart = location.state?.cart || [];
  const totalAmount =
    location.state?.totalAmount || 0;

  const [paymentMethod, setPaymentMethod] =
    useState("upi");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleCheckout = async (event) => {
    event.preventDefault();

    if (cart.length === 0) {
      setError("Your cart is empty.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      const orderResponse = await api.post(
        "/orders/",
        {
          items: cart.map((item) => ({
            product_id: item.id,
            quantity: item.quantity,
          })),
        }
      );

      const order = orderResponse.data;

      await api.post("/payments/", {
        order_id: order.id,
        payment_method: paymentMethod,
      });

      navigate("/orders");
    } catch (error) {
      setError(
        error.response?.data?.detail ||
          "Unable to complete checkout."
      );
    } finally {
      setLoading(false);
    }
  };

  if (cart.length === 0) {
    return (
      <div className="checkout-page">
        <h1>Checkout</h1>

        <p>Your cart is empty.</p>

        <button
          type="button"
          onClick={() => navigate("/products")}
        >
          Back to Products
        </button>
      </div>
    );
  }

  return (
    <div className="checkout-page">
      <header className="checkout-header">
        <div>
          <h1>Checkout</h1>
          <p>
            Review your order and select a
            payment method.
          </p>
        </div>
      </header>

      <main className="checkout-content">
        {error && (
          <p className="error-message">
            {error}
          </p>
        )}

        <section className="checkout-card">
          <h2>Order Summary</h2>

          {cart.map((item) => (
            <div
              className="checkout-item"
              key={item.id}
            >
              <div>
                <strong>{item.name}</strong>

                <p>
                  Quantity: {item.quantity}
                </p>
              </div>

              <strong>
                ₹
                {(
                  Number(item.price) *
                  item.quantity
                ).toFixed(2)}
              </strong>
            </div>
          ))}

          <div className="checkout-total">
            <span>Total Amount</span>

            <strong>
              ₹{Number(totalAmount).toFixed(2)}
            </strong>
          </div>
        </section>

        <section className="checkout-card">
          <h2>Payment Method</h2>

          <form onSubmit={handleCheckout}>
            <div className="payment-methods">
              {PAYMENT_METHODS.map(
                (method) => (
                  <label
                    className="payment-option"
                    key={method.value}
                  >
                    <input
                      type="radio"
                      name="payment_method"
                      value={method.value}
                      checked={
                        paymentMethod ===
                        method.value
                      }
                      onChange={(event) =>
                        setPaymentMethod(
                          event.target.value
                        )
                      }
                    />

                    <span>
                      {method.label}
                    </span>
                  </label>
                )
              )}
            </div>

            <button
              type="submit"
              disabled={loading}
            >
              {loading
                ? "Processing..."
                : "Place Order & Pay"}
            </button>
          </form>
        </section>
      </main>
    </div>
  );
}

export default Checkout;

