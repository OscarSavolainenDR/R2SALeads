import json


city = 'London'
all_listings = []
for i in range(5):
    listing = { 'city': city,
                'country': 'England',
                'rent': i * 100,
                'bedrooms': i+1,
                'expected_occupancy': 70,
                'median_income': 1000,
                'url': f'{i+10}.co.uk',
                'website': 'Zoopla',
                'agency_or_host': 'Snack',
                'address': 'fvnnvdf',
                'postcode': 's-ZHSYSU',
                'excel_sheet': f'dd_{i+10}.xlsx'}
    all_listings.append(listing)

with open("json_data_London.json", "w") as final:
   json.dump(all_listings, final)