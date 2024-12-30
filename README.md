# CampusKorner

A marketplace platform for university students to buy and sell items within their campus community.

## Features

- User Authentication
  - Registration and Login
  - JWT-based authentication
  - Role-based access (buyers, sellers, admins)

- Product Management
  - Create, read, update, delete products
  - Search and filter products
  - Product categories
  - Product status tracking (available, pending, sold)
  - Image support for products

- Order System
  - Place orders
  - Track order status
  - Order history for buyers and sellers

- Review System
  - Rate and review sellers
  - View seller ratings and reviews

- Profile Management
  - User profiles
  - Seller verification
  - University-specific marketplace

## Tech Stack

- Backend: Python/Flask
- Database: MySQL
- Authentication: JWT
- Extensions:
  - Flask-SQLAlchemy
  - Flask-Migrate
  - Flask-CORS

## API Endpoints

### Authentication
- POST /api/register - Register new user
- POST /api/login - User login
- POST /api/logout - User logout

### Products
- GET /api/products - List products with filters
- POST /api/products - Create new product
- GET /api/products/<id> - Get product details
- PUT /api/products/<id> - Update product
- DELETE /api/products/<id> - Delete product

### Orders
- POST /api/orders - Create new order
- GET /api/orders/<id> - Get order details
- PUT /api/orders/<id>/status - Update order status
- GET /api/user/orders - Get user's orders

### Reviews
- POST /api/reviews - Create review
- GET /api/reviews/user/<id> - Get user reviews

### Categories
- GET /api/categories - List categories
- POST /api/categories - Create category (admin only)
- PUT /api/categories/<id> - Update category
- DELETE /api/categories/<id> - Delete category

### Profile
- GET /api/profile - Get user profile
- PUT /api/profile/update - Update profile
- POST /api/profile/seller - Become seller

## Setup

1. Clone the repository
2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables in `.env`:
```
DATABASE_URL=mysql+pymysql://user:password@localhost/dbname
SECRET_KEY=your-secret-key
JWT_EXPIRATION_HOURS=24
```

5. Initialize database:
```bash
flask create-db
```

6. Run the application:
```bash
flask run
```

## Database Models

- User: User accounts and profiles
- Product: Product listings
- ProductImage: Product images
- Order: Order management
- Review: User reviews
- Category: Product categories

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

[Add your license here]
