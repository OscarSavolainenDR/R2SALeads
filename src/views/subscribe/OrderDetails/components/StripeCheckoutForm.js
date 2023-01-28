import React, {useState, useEffect} from 'react'
// import CheckoutForm from "./components/CheckoutForm";
import {stripeCheckout} from '../store/dataSlice'
// import { useSelector } from 'react-redux'
import { toast, Notification, Checkbox, Button } from 'components/ui'
// import Loading from 'components/shared/Loading' 
import { useNavigate } from 'react-router-dom'
import { Loading, Container } from 'components/shared'
import { Card } from 'components/ui'
import useThemeClass from 'utils/hooks/useThemeClass'



import {CardElement, useElements, useStripe} from "@stripe/react-stripe-js";

// const checkingOut = async () => {
    // const loading = useSelector((state) => state.salesOrderDetails.data.loading)
    // const response = await stripeCheckout({email: email, payment_method_id: paymentMethod.id, product: product})
// }


const StripeCheckoutForm = (product) => {
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const { textTheme } = useThemeClass()
    const navigate = useNavigate()
    const stripe = useStripe();
    const elements = useElements();
    const [agree, setAgree] = useState(false);

    const TermsClick = () => {
        navigate(`/app/legals/terms-and-conditions`)
    }

    const PrivacyClick = () => {
        navigate(`/app/legals/privacy-policy`)
    }

    // Checkbox (read T&Cs)
    const canBeSubmitted = () => {
        const isValid =
          agree; // checkbox for terms
    
        if (isValid) {
          document.getElementById("stripeSubmitButton").removeAttribute("disabled");
        } else {
          document.getElementById("stripeSubmitButton").setAttribute("disabled", true);
        }
    };
    useEffect(() => canBeSubmitted());

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

        if (!error) {
            
            setLoading(true)
            // console.log('Error', error)
            // console.log('Loading')

            //    console.log(paymentMethod, error)

            const response = await stripeCheckout({payment_method_id: paymentMethod.id, product: product})
            setLoading(false)
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
                    navigate(`/app/subscribe/product-list`)
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
        }
    };

    return (
        <div>
        <Container className="h-full">
            <Loading loading={loading } type="cover">
            <form onSubmit={handleSubmit} className="stripe-form">
                {/* <div className="form-row">
                    <label htmlFor="email" className="font-semibold">Email Address (NOTE: THIS SHOULD BE AUTOFILLED BY ME)</label>
                    <input className="form-input" id="email" name="name"    type="email" placeholder="jenny.rosen@example.com" required 
                    value={email} onChange={ (event) => { setEmail(event.target.value) } } />
                </div> */}
                <Card className="mb-4"> 
                <div className="form-row">
                    <h5 className="mb-4">Credit or debit card</h5>
                    {/* <label htmlFor="card-element" className="mb-4">Credit or debit card</label>  */}
                    <CardElement id="card-element" className="font-semibold" onChange={handleChange}/>
                    <div className="card-errors" role="alert">{error}</div>
                </div> 
                </Card> 
                <Card className="mb-4">
                <div className="mb-4 flex justify-between">
                    <p className="mb-4" >
                        I have read and agree to Rent2SA Leads &nbsp;
                        <button className={`hover:${textTheme}`} style={{ fontWeight: 'bold'}} onClick={TermsClick}> Terms and Conditons </button> 
                        &nbsp;and&nbsp;
                        <button className={`hover:${textTheme}`} style={{ fontWeight: 'bold'}} onClick={PrivacyClick}>Privacy Policy</button>
                        .
                    </p>
                    <Checkbox id="agree"  onClick={(e) => setAgree(e.target.checked)} />
                    {/* <input
                        type="checkbox"
                        name="agree"
                        id="agree"
                        onClick={(e) => setAgree(e.target.checked)}
                    /> */}
                </div>
                </Card>

                <Button variant="solid" className={`submit-btn font-semibold hover:${textTheme}`} id='stripeSubmitButton' type="submit">
                    Submit Payment
                </Button>
            </form>
            </Loading>
        </Container>
        </div>
    );
};

// const StripeCheckoutForm = () => (
//   <Elements stripe={stripePromise}>
//     <CheckoutForm />
//   </Elements>
// );

export default StripeCheckoutForm