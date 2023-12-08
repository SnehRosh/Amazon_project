from dputils.scrape import Scraper, Tag
from sqlalchemy.orm import sessionmaker
from orm import Product, create_engine

page = 1
query = 'oppo'
limit = 5
all_results=[]
for i in range(1,limit+1):
    url = f'https://www.amazon.in/s?k={query}&ref={page}'
    #create a scraper object
    scr = Scraper(webpage_url=url)
    # content to
    t = Tag('span',cls='a-color-base') # Title
    p = Tag('span',cls='a-price-whole')
    l = Tag('a',cls='puisg-col-inner',output='href')
    i = Tag('img',cls='s-image',output='src')
    ra=Tag('span',cls='a-declarative')

    #extract data
    results = scr.get_repeating_page_data(
        target = Tag(cls='s-result-list'),
        items = Tag(cls='s-card-container'),
        title = t, price = p, link=l, imgurl=i,rating=ra
    )
    print(results)
    page += 1

    if len(results)==0:
        print('No more results')
        break
    all_results += results


if len(all_results) > 0:
    engine = create_engine('sqlite:///extracted.db', echo=True)
    Session = sessionmaker(bind=engine)
    db = Session() # will create a session object
    for record in all_results:
        p = Product(title = record['title'],
                    price = record['price'],
                    url = record['link'],
                    imgurl = record['imgurl'],
                    rating=record['rating'])
        
        db.add(p)
        print("🌀 Record added")
    db.commit() # save all the records
    db.close() # close the connection