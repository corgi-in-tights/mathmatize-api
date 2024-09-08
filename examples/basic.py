import os
from mathmatize.api import MathMatizeAPI

api = MathMatizeAPI(
    None, # silently install new chromedriver, best practice is to provide path to a local chromedriver if avaliable
    os.getenv('MATHMATIZE_EMAIL'),
    os.getenv('MATHMATIZE_PASSWORD')
)

rows = api.scrape_classroom(1269)
for r in rows:
    print (r.title)
    for t in r.tasks:
        print (t.title)
        print (t.activity)