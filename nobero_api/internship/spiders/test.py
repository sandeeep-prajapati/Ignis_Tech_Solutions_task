import scrapy
import sqlite3
from scrapy.linkextractors import LinkExtractor
from scrapy.spidermiddlewares.httperror import HttpError

class NoberoSpider(scrapy.Spider):
    name = 'nobero'
    start_urls = ['https://nobero.com/pages/men']

    def __init__(self, *args, **kwargs):
        super(NoberoSpider, self).__init__(*args, **kwargs)
        # Initialize SQLite connection and create table
        self.conn = sqlite3.connect('nobero_products.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                url TEXT,
                title TEXT,
                img_url TEXT,
                bought TEXT,
                description TEXT,
                price TEXT,
                MPR TEXT,
                color TEXT,
                size TEXT
            )
        ''')
        self.conn.commit()

    def parse(self, response):
        # Extract category links
        base_url = 'https://nobero.com'
        category_links = response.css('div.icartShopifyCartContent > div > section > div > div > div > div > a::attr(href)').getall()
        category_links = [base_url + link.replace(' /', '/') for link in category_links]
        for link in category_links:
            print(link)
            yield response.follow(link, self.parse_link, errback=self.handle_http_error)

    def handle_http_error(self, failure):
        if failure.check(HttpError):
            response = failure.value.response
            if response.status == 404:
                print(f"Ignoring 404 error for {response.url}")

    def parse_link(self, response):
        # Visiting each link
        card_link = response.css('article > section > div > a::attr(href)').getall()
        for link in card_link:
            data_id = response.css('article > section > div > a::attr(data-id)').get()
            product_link = response.urljoin(link) + f'?variant={data_id}'
            product = {}
            product['category'] = response.css('main > div > section > section > h1::text').get()
            yield response.follow(product_link, self.parse_product, cb_kwargs={'product': product})

    def parse_product(self, response, product):
        # Extract product data
        product['url'] = response.url
        product['title'] = response.css('main > div > div > div > div > h1::text').get().strip()
        product['img_url'] = response.css('figure#image-container  img::attr(src)').get().strip()
        bought_text = response.css('div.product_bought_count > span::text').get()
        product['bought'] = bought_text.strip() if bought_text else None
        product['description'] = ' '.join(response.css('div#description_content p::text').getall()).strip()
        
        # Extract and clean the price
        price_text = response.css('h2#variant-price *::text').get()
        product['price'] = price_text.replace('₹', '').strip() if price_text else None
        product['product_url'] = response.url

        # Extract and clean the MPR
        mrp_text = response.css('span#variant-compare-at-price *::text').get()
        product['MPR'] = mrp_text.replace('₹', '').strip() if mrp_text else None

        # Clean and extract color
        color_text = response.css('div.capitalize > span > span::text').get()
        product['color'] = color_text.strip() if color_text else None

        # Clean and extract sizes
        sizes = response.css('div.flex.overflow-x-scroll > fieldset > label::text').getall()
        product['size'] = ', '.join(sorted(set(size.strip() for size in sizes if size.strip())))

        # Store the product in the database
        self.store_in_db(product)

    def store_in_db(self, product):
        self.cursor.execute('''
            INSERT INTO products (category, url, title, img_url, bought, description, price, MPR, color, size)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            product['category'], product['url'], product['title'], product['img_url'], 
            product['bought'], product['description'], product['price'], product['MPR'], 
            product['color'], product['size']
        ))
        self.conn.commit()

    def close(self, reason):
        # Close the SQLite connection
        self.conn.close()
