import CardIcon from "../images/credit-card.svg";
import ProductImage from "../images/product-image.jpg";
import { loadStripe } from "@stripe/stripe-js" // need
import "../styles.css";

let stripePromise
const getStripe = () => {
    if (!stripePromise) {
        stripePromise = loadStripe(process.env.REACT_APP_STRIPE_KEY) // need
    }
    return stripePromise
}

const Checkout = () => {
    const item = {
        "price": "price_1MaMAQJeYWzBWqCqEFyHkScq",
        quantity: 1,
    }

    const checkoutOptions = {
        lineItems: [item],
        mode: "payment",
        successUrl: '${window.location.origin}/success',
        cancelUrl: '${window.location.origin}/cancel',

    }
    // Called from OnClick
    const redirectToCheckout = async () => {
        console.log('redirect to checkout')

        const stripe = await getStripe()
        const { error } = await stripe.redirectToCheckout(checkoutOptions)
        console.log("Stripe checkout error", error)
    }
  return (
    <div className="checkout">
      <h1>Stripe Checkout</h1>
      <p className="checkout-title">Design+Code React Hooks Course</p>
      <p className="checkout-description">
        Learn how to build a website with React Hooks
      </p>
      <h1 className="checkout-price">$19</h1>
      <img
        className="checkout-product-image"
        src={ProductImage}
        alt="Product"
      />
      <button className="checkout-button">
        <div className="grey-circle">
          <div className="purple-circle">
            <img className="icon" src={CardIcon} alt="credit-card-icon" />
          </div>
        </div>
        <div className="text-container">
          <p className="text">Buy</p>
        </div>
      </button>
    </div>
  );
};

export default Checkout;
