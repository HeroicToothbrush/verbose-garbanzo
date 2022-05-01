# Overview
- Kept logic and design very simple according to the requirements, rather than making too many additional assumptions. Created 1 app (`products`) and implemented 2 models for `Product` and `Order` + 2 custom exceptions (defined in `models.py`)
  - The business logic for ordering is defined on the `Order` model and implemented by overriding the save method. 
  - It checks order details are valid, that there is enough stock to fulfill the order and then decrements the stock quantity for the related product.
- Created the API layer using Django Rest Framework
  - Exchange the username and password for an auth token e.g. :
    `http POST http://localhost:8000/api-token-auth/ username='[username]' password="[password]"`
  - Use the token in subsequent requests to protected endpoints (`/products` and `/orders`) e.g.:
    `http GET http://localhost:8000/api/orders/ "Authorization: Token 03e7e0c1a8fa5142778edd0d45c78e984f0c0ba7"`
  - `/api/products` supports GET requests to retrieve the product details and includes pagination of the output
  - `/api/orders` supports GET requests to retrieve the order history details (limited to only those belonging to the authenticated user) and POST requests to create an order (for a specified product)
  
# Deployment
- Deployment to AWS/GCP is fairly straightforward. Here are some example steps for GCP:
  - Configure production webserver (nginx, gunicorn/uvicorn)
  - Change the default SQLlite db to a production RDBMS such as Postgres (e.g. Postgres on Cloud SQL on GCP)
  - Ideally set up CI/CD to continuously automate the build, test and deployment steps (e.g. using circleCI/github actions)
  - Select deployment target - for example, on GCP, Cloud Run is a serverless option that's easy to deploy and scale. If requirements are more complex, could use Kubernetes (GKE)
  - Provision infrastructure - e.g. postgresSQL instance on CloudSQL as the db, with correct IAM permissions and
  ideally some kind of secrets manager to store configuration data like db passwords
  - Build a docker image
  - Push to a Docker image repository - e.g. GCP container registry 
  - Deploy container onto target (e.g. using `gcloud`)
- Other considerations - load balancing, caching, monitoring/observability, provisioning infrastructure using infrastructure as code tool such as terraform

# Enhancements with more time and information
- It'd be great to understand the domain further and add additional logic - kept this very simple for now as described above. An order can contain only 1 type of product at present. There is no concept of order processing, fulfillment, a 'cart' or a session where a user can add products and then checkout. 
  - Example further questions - How does a user interact with the application? Should users be able to view products without being authenticated? Should we display out of stock products to the user? 
- Add more tests including the endpoints (included tests for the domain logic but ran of time for automated testing of the endpoints - these were tested manually using Postman)
- Set up docker and postgres, configure CI & CD, logging, etc (described above for deployment)
- Security improvements - token expiry, HTTPS basic for exchanging username and password for token
- Add more functionality to the APIs - e.g. querying, additional endpoints as required, graceful handling of invalid input etc
