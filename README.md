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

### Backend
- Python 3.9+
- Flask 2.0+
- MySQL 8.0
- JWT Authentication
- Flask Extensions:
  - Flask-SQLAlchemy 3.0
  - Flask-Migrate 4.0
  - Flask-CORS 4.0
  - Flask-RESTx

### Frontend
- React 18
- TypeScript 4.9+
- Material UI 5.0
- Redux Toolkit
- React Router 6
- Axios

## Project Structure
```
campusKorner/
├── backend/          # Flask application
│   ├── api/         # API endpoints
│   ├── models/      # Database models
│   └── services/    # Business logic
└── frontend/        # React application
    ├── src/
    ├── components/  # Reusable UI components
    └── features/    # Feature-specific code
```

## Setup

### Backend Setup

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
CORS_ORIGINS=http://localhost:3000
```

5. Initialize database:
```bash
flask create-db
```

6. Run the application:
```bash
flask run
```

### Frontend Setup
1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables in `.env`:
```
REACT_APP_API_URL=http://localhost:5000/api
```

4. Start development server:
```bash
npm start
```

## Development Workflow

1. Backend Development:
```bash
# Start Flask development server
flask run --debug

# Run tests
pytest

# Run linting
flake8
```

2. Frontend Development:
```bash
# Start React development server
npm start

# Run tests
npm test

# Build for production
npm run build
```

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

### Search
- GET /api/search - Search across products
- GET /api/search/filters - Get available search filters

### Notifications
- GET /api/notifications - Get user notifications
- PUT /api/notifications/<id>/read - Mark notification as read

## Database Models

- User: User accounts and profiles
- Product: Product listings
- ProductImage: Product images
- Order: Order management
- Review: User reviews
- Category: Product categories

## Environment Variables

### Backend
```
DATABASE_URL=mysql+pymysql://user:password@localhost/dbname
SECRET_KEY=your-secret-key
JWT_EXPIRATION_HOURS=24
CORS_ORIGINS=http://localhost:3000
```

### Frontend
```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_GOOGLE_MAPS_KEY=your-google-maps-key
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

[Add your license here]
