#Backend test assignment
<hr>

##How to run test assignment

Any of these variants:

- With docker compose by running `docker compose up --build`
- With venv (or any environment with python) after installing packages from `requirements.txt` (`python manage.py runserver 0.0.0.0:8000`)

Database with pre-created test is included in db.sqlite3, if it needed.
<hr>

##Api documentation

All endpoint are using `application/json` content-type.
### Authorization
**Endpoint:** `POST /api/auth`

**Body:** 
- _username_ - user login
- _password_ - user password

**Response:**<br>
Status: 200<br>
Body: 
- _access_ - JWT access token
- _refresh_ - JWT refresh token

### Token refresh
**Endpoint** `POST /api/refresh`

**Body:**
- _refresh_ - JWT refresh token

**Response:**<br>
Status: 200<br>
Body: 
- _access_ - refreshed token

###Products list
**Endpoint** `GET /api/products`

**Parameters:**
- _page_ - # of page
- _limit_ - # of displayed products (default 50)

**Response:**<br>
Status: 200<br>
Body: 
- _count_ - quantity of products in DB
- _next_ and _previous_ - links to next and previous pages
- _results_ - list of products

###Place an order
Authorization required

**Endpoint** `POST /api/order`

**Body:**
- _parts_ - list of ordered products and their quantity (_product_ - product id, _quantity_in_order_ - quantity)

**Response:**<br>
Status: 
- 201 - order created
- 400 - validation error (wrong data, product id, insufficient amount of products in stock)<br>
Body: 
- _id_ - order id
- _parts_ - list of order parts 
- _created_ - date and time of order creation
- _user_ - user id

###User orders
Authorization required
**Endpoint** `GET /api/my-orders`

**Response**:<br>
Status: 200 (always)<br>
Body: List of orders (can be empty)
<hr>

##Data schemas

###Order
- _id_ - order id
- _parts_ - list of order parts
- _created_ - date and time of order creation
- _user_ - user id

###Order part
- _product_ - product id
- _quantity_in_order_ - quantity of products
- _product_name_ - product's name, fallback in case the product is removed from DB
<hr>

##Extras

###Deploying 
App can be deployed on cloud providers supporting docker (Heroku, AWS, etc). 
In case of Heroku - you need to replace coping of `requirements.txt` only to copying whole project in Dockerfile, build this image and push it to Heroku container registry, or use automatic deploy from github repository.
Also, heroku.yml can be used.

###What to add 
Outside the specified timeframe I would like to add:
- order cost calculation
- filter for products (based of price or quantity in stock)
- endpoint to searching through the products
- ability for the user to edit their data (first name, last name, email, etc)
- more fields for products, like photos, descriptions
- models and logic to apply special offers to user's orders (something like 'buy one - get one') 
