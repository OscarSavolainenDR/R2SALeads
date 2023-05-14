import React from 'react';
// import { useNavigate } from 'react-router-dom'
import useThemeClass from 'utils/hooks/useThemeClass'
import { Link } from "react-router-dom";

function LandingPage() {


    // Styling
    const { textTheme } = useThemeClass()
    const boldText = {
        fontWeight: 'bold',
        // marginLeft: '5px'
    }


  return (
    <div className="landing-page">
      <header>
        <h1>Welcome to the Future of Airbnb Arbitrage</h1>
      </header>
      <main style={{ fontSize: '15px'}}> 
        <br/>
        <p>Are you tired of spending countless hours sifting through rental listings, trying to determine which ones would be profitable as Airbnbs? Look no further!</p>
        <br/>
        <p>Our cutting-edge website scans the entire rental market and uses advanced algorithms to determine which properties would make the perfect Airbnb investment.</p>
        <br/>
        <p>With our subscription service, R2SA investors and sourcers can access all of the market research on each potential Airbnb, saving them time and effort in their search for profitable listings. Our platform is designed to provide you with all the information you need to make informed decisions, giving you the competitive edge you need to succeed in the fast-paced world of Airbnb Arbitrage.</p>
        <br/>
        <p>Our team of experts has years of experience in real estate, technology, and data analysis, ensuring that our platform is accurate, reliable, and user-friendly. We are dedicated to helping you achieve your financial goals and make the most of your Airbnb investments.</p>
        <br/>
        <p>Join our growing community of successful real estate professionals and start making profitable Airbnb investments today!
        </p>

        <p> 
            <Link to={{pathname: `/app/subscribe/product-list`}} style={boldText} className={`cursor-pointer hover:${textTheme}`}>
                Subscribe to a city now
            </Link>
            &nbsp;to gain access to our comprehensive market research and take your Airbnb Arbitrage, R2SA business to the next level!
        </p>
        <br/>
        <p> 
            As a special offer, we're currently providing a free sample of our market research in Oxford, England to give you a taste of what our platform can do. 
            <Link to={{pathname: `/app/project/table-view`}} style={boldText} className={`cursor-pointer hover:${textTheme}`}>
            &nbsp;Check out our leads in Oxford
            </Link>
            &nbsp;and see for yourself how our platform can help you find profitable Airbnb listings with ease.
        </p>
        <br/>



      </main>
    </div>
  );
}

export default LandingPage;
