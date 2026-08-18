
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

function Products() {
  const navigate = useNavigate();

  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await api.get("/products/");
        setProducts(response.data);
      } catch (error) {
        setError(
          error.response?.data?.detail ||
            "Unable to load products."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  const addToCart = (product) => {
    setCart((currentCart) => {
      const existingItem = currentCart.find(
        (item) => item.id === product.id
      );

      if (existingItem) {
        if (
          existingItem.quantity >=
          product.stock_quantity
        ) {
          return currentCart;
        }

        return currentCart.map((item) =>
          item.id === product.id
            ? {
                ...item,
                quantity: item.quantity + 1,
              }
            : item
        );
      }

      return [
        ...currentCart,
        {
          ...product,
          quantity: 1,
        },
      ];
    });
  };

  const increaseQuantity = (productId) => {
    setCart((currentCart) =>
      currentCart.map((item) => {
        if (item.id !== productId) {
          return item;
        }

        if (item.quantity >= item.stock_quantity) {
          return item;
        }

        return {
          ...item,
          quantity: item.quantity + 1,
        };
      })
    );
  };

  const decreaseQuantity = (productId) => {
    setCart((currentCart) =>
      currentCart
        .map((item) =>
          item.id === productId
            ? {
                ...item,
                quantity: item.quantity - 1,
              }
            : item
        )
        .filter((item) => item.quantity > 0)
    );
  };

  const removeFromCart = (productId) => {
    setCart((currentCart) =>
      currentCart.filter(
        (item) => item.id !== productId
      )
    );
  };

  const getProductImage = (product) => {
    if (product.image) {
      return product.image;
    }

    if (
      product.id === 1 ||
      product.name?.toLowerCase().includes("wireless mouse")
    ) {
      return "/images/wireless-mouse.png";
    }

    return null;
  };

  const totalAmount = cart.reduce(
    (total, item) =>
      total +
      Number(item.price) * item.quantity,
    0
  );

  const checkout = () => {
    if (cart.length === 0) {
      return;
    }

    navigate("/checkout", {
      state: {
        cart,
        totalAmount,
      },
    });
  };

  if (loading) {
    return (
      <div className="customer-page">
        <h1>Inventory & Order Management</h1>
        <p>Loading products...</p>
      </div>
    );
  }

  return (
    <div className="customer-page">
      <header className="customer-header">
        <div>
          <h1>Inventory & Order Management</h1>
          <p>Browse our available products</p>
        </div>

        <button
          type="button"
          onClick={() => navigate("/orders")}
        >
          My Orders
        </button>
      </header>

      {error && (
        <p className="error-message">
          {error}
        </p>
      )}

      <main className="customer-content">
        <section className="products-section">
          <h2>Products</h2>

          {products.length === 0 ? (
            <p>No products available.</p>
          ) : (
            <div className="products-grid">
              {products.map((product) => (
                <article
                  className="product-card"
                  key={product.id}
                >
                  {getProductImage(product) ? (
                    <img
                      className="product-image"
                      src={getProductImage(product)}
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

                  <strong>
                    ₹{product.price}
                  </strong>

                  <p>
                    Stock: {product.stock_quantity}
                  </p>

                  <button
                    type="button"
                    onClick={() =>
                      addToCart(product)
                    }
                    disabled={
                      product.stock_quantity <= 0
                    }
                  >
                    {product.stock_quantity <= 0
                      ? "Out of Stock"
                      : "Add to Cart"}
                  </button>
                </article>
              ))}
            </div>
          )}
        </section>

        <aside className="cart-section">
          <div className="cart-header">
            <h2>Shopping Cart</h2>

            <span>
              {cart.reduce(
                (total, item) =>
                  total + item.quantity,
                0
              )}{" "}
              item(s)
            </span>
          </div>

          {cart.length === 0 ? (
            <p>Your cart is empty.</p>
          ) : (
            <>
              <div className="cart-items">
                {cart.map((item) => (
                  <div
                    className="cart-item"
                    key={item.id}
                  >
                    <div>
                      <h3>{item.name}</h3>

                      <p>
                        ₹{item.price} each
                      </p>
                    </div>

                    <div className="cart-controls">
                      <button
                        type="button"
                        onClick={() =>
                          decreaseQuantity(
                            item.id
                          )
                        }
                      >
                        −
                      </button>

                      <span>
                        {item.quantity}
                      </span>

                      <button
                        type="button"
                        onClick={() =>
                          increaseQuantity(
                            item.id
                          )
                        }
                      >
                        +
                      </button>
                    </div>

                    <strong>
                      ₹
                      {(
                        Number(item.price) *
                        item.quantity
                      ).toFixed(2)}
                    </strong>

                    <button
                      type="button"
                      onClick={() =>
                        removeFromCart(item.id)
                      }
                    >
                      Remove
                    </button>
                  </div>
                ))}
              </div>

              <div className="cart-total">
                <strong>Total</strong>

                <strong>
                  ₹{totalAmount.toFixed(2)}
                </strong>
              </div>

              <button
                type="button"
                className="checkout-button"
                onClick={checkout}
              >
                Proceed to Checkout
              </button>
            </>
          )}
        </aside>
      </main>
    </div>
  );
}

export default Products;

