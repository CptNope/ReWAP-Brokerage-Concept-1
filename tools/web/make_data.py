"""Sample listing data for the Concept 1 website pages. Every record is fictional:
invented street names, SAMPLE- MLS numbers, round illustrative figures. Towns and their
coordinates are real so the map plate can place them."""
import json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
REGIONS = [
  ('berkshires', 'The Berkshires'), ('pioneer-valley', 'Pioneer Valley'), ('central', 'Central Massachusetts'),
  ('metrowest', 'MetroWest'), ('greater-boston', 'Greater Boston'), ('north-shore', 'North Shore & Merrimack Valley'),
  ('south-shore', 'South Shore'), ('south-coast', 'South Coast'), ('cape-islands', 'Cape & Islands')]
T = {  # town: (region, lat, lng)
 'Pittsfield': ('berkshires', 42.4501, -73.2454), 'Lenox': ('berkshires', 42.3565, -73.2848), 'Great Barrington': ('berkshires', 42.1959, -73.3620),
 'Northampton': ('pioneer-valley', 42.3251, -72.6412), 'Springfield': ('pioneer-valley', 42.1015, -72.5898), 'Greenfield': ('pioneer-valley', 42.5876, -72.5995),
 'Worcester': ('central', 42.2626, -71.8023), 'Shrewsbury': ('central', 42.2959, -71.7128), 'Sturbridge': ('central', 42.1084, -72.0787),
 'Fitchburg': ('central', 42.5834, -71.8023), 'Grafton': ('central', 42.2070, -71.6856),
 'Framingham': ('metrowest', 42.2793, -71.4162), 'Natick': ('metrowest', 42.2834, -71.3495),
 'Somerville': ('greater-boston', 42.3876, -71.0995), 'Quincy': ('greater-boston', 42.2529, -71.0023), 'Lowell': ('north-shore', 42.6334, -71.3162),
 'Salem': ('north-shore', 42.5195, -70.8967), 'Newburyport': ('north-shore', 42.8126, -70.8773),
 'Plymouth': ('south-shore', 41.9584, -70.6673), 'Hingham': ('south-shore', 42.2418, -70.8898),
 'New Bedford': ('south-coast', 41.6362, -70.9342), 'Fall River': ('south-coast', 41.7015, -71.1550),
 'Falmouth': ('cape-islands', 41.5515, -70.6148), 'Chatham': ('cape-islands', 41.6821, -69.9597),
}
# (num, street, town, type, price, beds, baths, sqft, lot_ac, year, units, elevation, status, office)
L = [
 (14, 'Larkspur Row', 'Worcester', 'Multi-family', 689000, 9, 3, 3960, 0.14, 1912, 3, 'triple-decker', 'For sale', 'rewap'),
 (3, 'Quarry Bend', 'Shrewsbury', 'Single-family', 559000, 4, 2, 2040, 0.42, 1958, 1, 'cape', 'For sale', 'oberdorfer'),
 (88, 'Hollis Mill Way, Unit 304', 'Worcester', 'Condo', 349000, 2, 2, 1210, 0, 1890, 1, 'mill', 'Open house', 'coop'),
 (27, 'Tenterden Hill', 'Grafton', 'Single-family', 624500, 4, 2.5, 2380, 0.9, 1798, 1, 'colonial', 'For sale', 'oberdorfer'),
 (6, 'Weybridge Court', 'Sturbridge', 'Single-family', 489000, 3, 2, 1760, 1.1, 1972, 1, 'cape', 'Under agreement', 'coop'),
 (41, 'Coldbrook Terrace', 'Fitchburg', 'Multi-family', 459000, 6, 2, 2610, 0.12, 1905, 2, 'triple-decker', 'For sale', 'coop'),
 (12, 'Ashgrove Lane', 'Lenox', 'Single-family', 824500, 4, 2.5, 2610, 1.2, 1840, 1, 'colonial', 'Open house', 'rewap'),
 (205, 'Marchmont Street', 'Pittsfield', 'Multi-family', 389000, 6, 2, 2480, 0.16, 1915, 2, 'rowhouse', 'For sale', 'coop'),
 (9, 'Tamarack Rise', 'Great Barrington', 'Single-family', 935000, 3, 2.5, 2150, 3.4, 1820, 1, 'colonial', 'For sale', 'coop'),
 (51, 'Wexcombe Avenue', 'Northampton', 'Single-family', 615000, 3, 2, 1880, 0.22, 1895, 1, 'rowhouse', 'For sale', 'coop'),
 (130, 'Dunmore Place', 'Springfield', 'Multi-family', 429000, 8, 3, 3420, 0.15, 1910, 3, 'triple-decker', 'Open house', 'rewap'),
 (18, 'Fennimore Road', 'Greenfield', 'Single-family', 339000, 3, 1.5, 1540, 0.3, 1926, 1, 'cape', 'For sale', 'coop'),
 (60, 'Holloway Mill Road, Unit 2B', 'Framingham', 'Condo', 419000, 2, 2, 1180, 0, 1886, 1, 'mill', 'For sale', 'coop'),
 (7, 'Kestrel Way', 'Natick', 'Single-family', 989000, 4, 3, 2860, 0.5, 1964, 1, 'colonial', 'For sale', 'coop'),
 (44, 'Abernathy Street', 'Somerville', 'Multi-family', 1495000, 7, 3, 3180, 0.09, 1900, 3, 'triple-decker', 'For sale', 'coop'),
 (310, 'Calloway Wharf, Unit 5', 'Quincy', 'Condo', 529000, 2, 2, 1050, 0, 2004, 1, 'rowhouse', 'Under agreement', 'coop'),
 (22, 'Penmarric Mill Way, Unit 410', 'Lowell', 'Condo', 379000, 2, 2, 1240, 0, 1882, 1, 'mill', 'For sale', 'rewap'),
 (11, 'Saltonstall Lane', 'Salem', 'Single-family', 749000, 3, 2.5, 1980, 0.11, 1790, 1, 'colonial', 'Open house', 'coop'),
 (5, 'Halyard Street', 'Newburyport', 'Single-family', 1125000, 4, 3, 2520, 0.14, 1810, 1, 'colonial', 'For sale', 'coop'),
 (19, 'Brantwood Road', 'Plymouth', 'Single-family', 574000, 3, 2, 1820, 0.6, 1984, 1, 'cape', 'For sale', 'coop'),
 (36, 'Oldfield Bend', 'Hingham', 'Single-family', 1290000, 4, 3.5, 3150, 0.7, 1760, 1, 'colonial', 'For sale', 'coop'),
 (102, 'Mariner Row', 'New Bedford', 'Multi-family', 469000, 6, 2, 2700, 0.1, 1906, 3, 'triple-decker', 'For sale', 'rewap'),
 (2, 'Riverbank Mill Way, Unit 12', 'Fall River', 'Condo', 289000, 1, 1, 890, 0, 1876, 1, 'mill', 'For sale', 'coop'),
 (15, 'Shoal Point Lane', 'Chatham', 'Single-family', 1675000, 3, 2.5, 1940, 0.4, 1932, 1, 'cape', 'For sale', 'coop'),
 (8, 'Sippewissett Path', 'Falmouth', 'Single-family', 879000, 3, 2, 1690, 0.5, 1948, 1, 'cape', 'Open house', 'coop'),
]
OFFICE = {'rewap': 'REWAP Brokerage', 'oberdorfer': 'The Oberdorfer Group at REWAP Brokerage', 'coop': 'Sample Realty Co. (cooperating brokerage)'}
out = []
for i, r in enumerate(L, 1):
    num, street, town, typ, price, beds, baths, sqft, lot, year, units, elev, status, office = r
    reg, lat, lng = T[town]
    slug = f"{num}-{street.split(',')[0].lower().replace(' ', '-')}-{town.lower().replace(' ', '-')}"
    out.append({'id': f'SAMPLE-{i:04d}', 'slug': slug, 'address': f'{num} {street}', 'town': town, 'region': reg,
                'lat': lat, 'lng': lng, 'type': typ, 'price': price, 'beds': beds, 'baths': baths, 'sqft': sqft,
                'lotAcres': lot, 'yearBuilt': year, 'units': units, 'elevation': elev, 'status': status,
                'office': OFFICE[office], 'own': office != 'coop', 'team': 'oberdorfer' if office == 'oberdorfer' else None,
                'openHouse': 'Sat 11:00–1:00' if status == 'Open house' else None})
json.dump({'notice': 'All listings are fictional sample data for the Concept 1 website. Towns and coordinates are real; streets, figures and MLS numbers are invented.',
           'regions': [{'slug': s, 'name': n} for s, n in REGIONS], 'towns': {k: {'region': v[0], 'lat': v[1], 'lng': v[2]} for k, v in T.items()},
           'listings': out}, open(os.path.join(ROOT, 'assets/data/listings.json'), 'w'), indent=1, ensure_ascii=False)
print(len(out), 'listings')
