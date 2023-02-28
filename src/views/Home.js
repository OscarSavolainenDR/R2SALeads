import React from 'react'

const Home = () => {
    const liStyle = {
        listStyleType: 'disc',
        marginLeft: '30px',
    }


	return (
		<div>
			<h3>Welcome to R2SA Leads!</h3>
			<span style={{ fontSize: '18px'}}>
				<br/>
				<h5>
					DO NOT USE, IN TEST MODE.
				</h5>
				<h5>
					Here at R2SA Leads, we believe in helping you scale your Rent to Serviced Accommodation business.
				</h5>
				
				<br />
				Spend less time searching for properties on OpenRent, Gumtree, Zoopla, etc., and more time growing your business!
				<br />
				<br />
				R2SA Leads works by scanning all of the top rental websites, and comparing their listings to nearby SAs.
				<br />
				For each listing, we do all of the due diligence. We then upload all of the properties that will work well as SAs to your dashboard!
				<br />
				From there, you can move forward and contact them, knowing that all of the due diligence has been done.
				<br />
				You can even download the due diligence for each listing, and check how many Airbnbs are in the area, how much they earn, what their occupancy rates are, and take a look at their profiles on Airbnb!
				<br />
				<br />
				Our profit calculations are very conservative: 60% of (mean turnover - listing rent), where the mean turnover is that of Airbnbs within 500m and with the same number of bedrooms.
				<br />
				<br />
				We make finding R2SA Leads easy. Get started by going to Manage Lead Subscriptions, and signing up for your city of choice! 
				<br />
				If you want to check out what the leads look like, go to Leads and see what's looking good in Oxford &#40;we give Leads there for free so you can see what the service is like&#41;.
				<br />
				<br />
				<h5>Points worth highlighting:</h5>
				<br />
				<ul>
					<li style={liStyle}>We think the best way to use the table is a combination of the filter and query tools, and clicking on the listing status will toggle it (that you can use in conjunction with filtering).
					</li>
					<li style={liStyle}>The leads are updated once a week, every Sunday.</li>
					<li style={liStyle}>Unfortunately, some listings are incorrectly marketed, e.g. some people will market a room as if it's a 1 bed flat. There's nothing we can do about that. Where possible, we do our best to filter out listings that describe themselves as house shares, flat shares, etc. If a listing is not appropriate for R2SA Leads for whatever reason, and you feel like helping us improve our service, then please include the listing link in a feedback note you send us.</li>
				</ul>

				<br />
				<br />
				If you have any queries, you can either use the feedback tab or email us at contact@r2sa-leads.co.uk . 

			</span>
		</div>
	)
}

export default Home