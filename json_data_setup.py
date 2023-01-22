import json

city = 'London'
all_listings = []
for i in range(5):
    listing = { 'city': city,
                'rent': i * 100,
                'expected_occupancy': 70,
                'expected_profit': 1000,
                'expected_ADR': 100,
                'break_even_o': 50,
                'url': f'{i+10}.co.uk',
                'website': 'Zoopla',
                'agency_or_host': 'Snack',
                'address': 'fvnnvdf',
                'postcode': 's-ZHSYSU',
                'excel_file': f'dd_{i}.xlsx'}
    all_listings.append(listing)

with open("json_data.json", "w") as final:
   json.dump(all_listings, final)