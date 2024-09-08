import os
from mathmatize.api import MathMatizeAPI

api = MathMatizeAPI(
    '/Users/reyaan/Projects/common/web_drivers/chromedriver-mac-arm64/chromedriver',
    os.getenv('EMAIL'),
    os.getenv('PASSWORD')
)

rows = api.scrape_classroom(1269)
for r in rows:
    print (r.title)
    for t in r.tasks:
        print (t.title)
        print (t.activity)