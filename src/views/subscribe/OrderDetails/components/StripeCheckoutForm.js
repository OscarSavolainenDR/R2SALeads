import React, {useState} from 'react'
// import CheckoutForm from "./components/CheckoutForm";
import {stripeCheckout} from '../store/dataSlice'
// import { useSelector } from 'react-redux'
import { toast, Notification } from 'components/ui'
// import Loading from 'components/shared/Loading' 
import { useNavigate } from 'react-router-dom'


import {CardElement, useElements, useStripe} from "@stripe/react-stripe-js";

// const checkingOut = async () => {
    // const loading = useSelector((state) => state.salesOrderDetails.data.loading)
    // const response = await stripeCheckout({email: email, payment_method_id: paymentMethod.id, product: product})
// }

const StripeCheckoutForm = (product) => {
    const [error, setError] = useState(null);
    const [email, setEmail] = useState('');
    // const loading = useSelector((state) => state.salesOrderDetails.data.loading)
    // console.log(loading)

    const navigate = useNavigate()


    const stripe = useStripe();
    const elements = useElements();

    // Handle real-time validation errors from the CardElement.
    const handleChange = (event) => {
        if (event.error) {
            setError(event.error.message);
        } else {
            setError(null);
        }
    }

    // Handle form submission.
    const handleSubmit = async (event) => {
        event.preventDefault();
        const card = elements.getElement(CardElement);

        const {paymentMethod, error} = await stripe.createPaymentMethod({
            type: 'card',
            card: card
       });
    //    console.log(paymentMethod, error)

       const response = await stripeCheckout({email: email, payment_method_id: paymentMethod.id, product: product})

       // Some waiting here, loading circle.

       if (response.status) {
            toast.push(
                <Notification title={"Payment successful"} type="success" duration={2500}>
                    Payment successful.
                </Notification>
                ,{
                    placement: 'bottom-end'
                }
            )
            // Redirect to 
            navigate(`/app/project/scrum-board`)
       } else {
        toast.push(
            <Notification title={"Payment unsuccessful"} type="warning" duration={2500}>
                Payment not successful. Error: {response.data.message}.
            </Notification>
            ,{
                placement: 'bottom-end'
            }
        )
       }
    };

    return (
        // <Loading loading={loading } type="cover">
            <form onSubmit={handleSubmit} className="stripe-form">
                <div className="form-row">
                    <label htmlFor="email">Email Address (NOTE: THIS SHOULD BE AUTOFILLED BY ME)</label>
                    <input className="form-input" id="email" name="name"    type="email" placeholder="jenny.rosen@example.com" required 
                    value={email} onChange={ (event) => { setEmail(event.target.value) } } />
                </div>
                <div className="form-row">
                    <label for="card-element">Credit or debit card</label> 
                    <CardElement id="card-element" onChange={handleChange}/>
                    <div className="card-errors" role="alert">{error}</div>
                </div>
                <button type="submit" className="submit-btn">
                    Submit Payment
                </button>
            </form>
        // </Loading>
    );
};

// const StripeCheckoutForm = () => (
//   <Elements stripe={stripePromise}>
//     <CheckoutForm />
//   </Elements>
// );

export default StripeCheckoutForm