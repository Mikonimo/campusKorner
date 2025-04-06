# CampusKorner 🎓🛒

![CampusKorner Banner](https://via.placeholder.com/800x200?text=CampusKorner)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://semver.org)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> A modern marketplace for university students to buy and sell items within their campus community. This platform simplifies product listings, ordering, reviews, and more, all tailored to university life.

## 📋 Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Screenshots](#screenshots)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [API Documentation](#api-documentation)
- [Database Models](#database-models)
- [Environment Variables](#environment-variables)
- [Testing](#testing)
- [Deployment](#deployment)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [FAQ](#faq)
- [License](#license)
- [Contact](#contact)

## 🚀 Introduction

CampusKorner was born from a simple observation: university students often struggle to find safe, convenient ways to buy and sell items within their campus community. Traditional marketplaces like KiliMall or Jiji lack the campus-specific focus and verification that students need.

Our platform connects students within their campus by providing an easy-to-use interface for product management, orders, reviews, and profiles. The goal is to foster a trusted and convenient environment to exchange goods or services exclusively for university students.

**Why CampusKorner?**
- **Campus-focused**: All listings are from verified students at your university
- **Convenient**: No need to coordinate with strangers from across town
- **Community-driven**: Build trust through our review system
- **Cost-effective**: Save on shipping with local exchanges

[View Demo](https://campuskorner-demo.example.com) | [Report Bug](https://github.com/yourusername/campuskorner/issues) | [Request Feature](https://github.com/yourusername/campuskorner/issues)

## ✨ Features

### User Authentication
- **Registration and Login**: Secure account creation and authentication
- **JWT-based authentication**: Modern token-based security
- **Role-based access**: Differentiated permissions for buyers, sellers, and admins
- **University Email Verification**: Ensures users are part of the campus community

### Product Management
- **CRUD Operations**: Create, read, update, delete products with ease
- **Advanced Search**: Find products by keyword, category, price range, and more
- **Categorization**: Organized product categories for easy browsing
- **Status Tracking**: Monitor products as available, pending, or sold
- **Rich Media Support**: Upload multiple images for each product

### Order System
- **Streamlined Checkout**: Simple process to place orders
- **Status Updates**: Real-time tracking of order status
- **History Tracking**: Comprehensive order history for both buyers and sellers
- **In-app Messaging**: Coordinate pickup or delivery details

### Review System
- **Seller Ratings**: Rate and review sellers after transactions
- **Transparency**: View seller ratings and reviews before purchasing
- **Trust Building**: Build community trust through honest feedback

### Profile Management
- **Customizable Profiles**: Personalize your presence on the platform
- **Seller Verification**: Additional verification for sellers
- **University-specific Marketplace**: Connect only with students from your campus
- **Dashboard**: Track your buying and selling activity

## 📸 Screenshots

Here's a glimpse of CampusKorner in action:

| Home Page | Product Details | User Profile |
|:---:|:---:|:---:|
| ![Home Page](./screenshots/home_page.png) | ![Product Details](./screenshots/product_listing.png) | ![User Profile](./screenshots/buyers_profile.png) |

## 💻 Tech Stack

### Backend
- **Python 3.9+**: Modern, readable, and powerful programming language
- **Flask 2.0+**: Lightweight and flexible web framework
- **MySQL 8.0**: Robust and scalable database solution
- **JWT Authentication**: Secure user authentication and authorization
- **Flask Extensions**:
  - Flask-SQLAlchemy 3.0: ORM for database operations
  - Flask-Migrate 4.0: Database migration management
  - Flask-CORS 4.0: Cross-Origin Resource Sharing
  - Flask-RESTx: API documentation and validation

### Frontend
- **React 18**: Modern UI library for building interactive interfaces
- **TypeScript 4.9+**: Type-safe JavaScript for better developer experience
- **Material UI 5.0**: Comprehensive component library for consistent design
- **Redux Toolkit**: State management with simplified Redux
- **React Router 6**: Client-side routing
- **Axios**: Promise-based HTTP client for API requests

## 📁 Project Structure

Our codebase is organized with a clear separation between frontend and backend:

```
campusKorner/
├── backend/                # Flask application
│   ├── routes/             # API endpoints
│   │   ├── auth.py         # Authentication routes
│   │   ├── products.py     # Product management routes
│   │   ├── orders.py       # Order management routes
│   │   └── profiles.py     # Profile management routes
│   ├── models/             # Database models
│   │   ├── user.py         # User model
│   │   ├── product.py      # Product model
│   │   ├── order.py        # Order model
│   │   └── review.py       # Review model
│   ├── services/           # Business logic
│   │   ├── auth_service.py # Authentication logic
│   │   ├── product_service.py # Product business logic
│   │   └── order_service.py # Order processing logic
│   ├── migrations/         # Database migrations
│   └── tests/              # Test files
│       ├── unit/           # Unit tests
│       └── integration/    # Integration tests
└── frontend/               # React application
    ├── public/             # Public files
    ├── src/                # Source code
    │   ├── components/     # Reusable UI components
    │   │   ├── common/     # Shared components
    │   │   ├── product/    # Product-related components
    │   │   └── user/       # User-related components
    │   ├── pages/          # Application pages
    │   ├── services/       # API interaction
    │   ├── store/          # Redux store configuration
    │   └── utils/          # Helper functions
    └── tests/              # Frontend tests
        ├── unit/           # Unit tests
        └── e2e/            # End-to-end tests
```

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+**: [Download Python](https://www.python.org/downloads/)
- **Node.js 14+**: [Download Node.js](https://nodejs.org/)
- **MySQL 8.0**: [Download MySQL](https://dev.mysql.com/downloads/)
- **(Optional)** Virtual environment tools for Python: `pip install virtualenv`

## 🔧 Setup Instructions

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/campuskorner.git
   cd campuskorner
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On Unix or MacOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the backend directory with the following variables:
   ```
   DATABASE_URL=mysql+pymysql://user:password@localhost/dbname
   SECRET_KEY=your-secret-key
   JWT_EXPIRATION_HOURS=24
   CORS_ORIGINS=http://localhost:3000
   ```

5. **Initialize database**
   ```bash
   flask create-db
   ```

6. **Run migrations**
   ```bash
   flask db upgrade
   ```

7. **Run the application**
   ```bash
   flask run
   ```
   The API will be available at `http://localhost:5000`.

#### Troubleshooting Backend Setup

- **Database Connection Issues**: Verify MySQL is running and credentials are correct
- **Module Import Errors**: Ensure virtual environment is activated
- **Port Conflicts**: If port 5000 is in use, specify a different port with `flask run --port=5001`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment variables**

   Create a `.env` file in the frontend directory:
   ```
   REACT_APP_API_URL=http://localhost:5000/api
   ```

4. **Start development server**
   ```bash
   npm start
   ```
   The application will be available at `http://localhost:3000`.

#### Troubleshooting Frontend Setup

- **Node Version Conflicts**: Use nvm to switch to a compatible Node version
- **Package Installation Errors**: Try clearing npm cache with `npm cache clean --force`
- **API Connection Issues**: Verify backend is running and CORS is properly configured

## 📡 API Documentation

Our REST API is organized around resources. All requests should be made to endpoints beginning with `/api/`.

### Authentication

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|-------------|----------|
| `/api/register` | POST | Register new user | `{email, password, name, university}` | User object with token |
| `/api/login` | POST | User login | `{email, password}` | User object with token |
| `/api/logout` | POST | User logout | None | Success message |

**Example Login Request:**
```javascript
const response = await axios.post('/api/login', {
  email: 'student@university.edu',
  password: 'securepassword'
});
// Store token from response.data.token
```

### Products

| Endpoint | Method | Description | Request Body/Params | Response |
|----------|--------|-------------|-------------|----------|
| `/api/products` | GET | List products | Query params: `category`, `search`, `min_price`, `max_price`, `status` | Array of products |
| `/api/products` | POST | Create new product | `{title, description, price, category_id, images[]}` | Created product |
| `/api/products/<id>` | GET | Get product details | Product ID in URL | Product details |
| `/api/products/<id>` | PUT | Update product | `{title, description, price, category_id, status}` | Updated product |
| `/api/products/<id>` | DELETE | Delete product | Product ID in URL | Success message |

### Orders

| Endpoint | Method | Description | Request Body/Params | Response |
|----------|--------|-------------|-------------|----------|
| `/api/orders` | POST | Create new order | `{product_id, quantity, payment_method}` | Order details |
| `/api/orders/<id>` | GET | Get order details | Order ID in URL | Order details |
| `/api/orders/<id>/status` | PUT | Update order status | `{status}` | Updated order |
| `/api/user/orders` | GET | Get user's orders | Query param: `role` (buyer/seller) | Array of orders |

### Additional Endpoints (Not Yet Implemented)

```
# Future API endpoints planned for upcoming releases:

### Reviews
- POST /api/reviews - Create review
- GET /api/reviews/user/<id> - Get user reviews

### Categories
- GET /api/categories - List categories
- POST /api/categories - Create category (admin only)
- PUT /api/categories/<id> - Update category
- DELETE /api/categories/<id> - Delete category

### Search
- GET /api/search - Search across products
- GET /api/search/filters - Get available search filters

### Notifications
- GET /api/notifications - Get user notifications
- PUT /api/notifications/<id>/read - Mark notification as read
```

## 📊 Database Models

Our database design focuses on clarity and efficient relationships:

### Core Models

- **User**: User accounts and profiles
  - Fields: id, name, email, password_hash, university, role, created_at, updated_at

- **Product**: Product listings
  - Fields: id, title, description, price, status, seller_id, category_id, created_at, updated_at

- **ProductImage**: Product images
  - Fields: id, product_id, image_url, is_primary, created_at

- **Order**: Order management
  - Fields: id, buyer_id, seller_id, status, total_price, created_at, updated_at

- **OrderItem**: Specific order items
  - Fields: id, order_id, product_id, quantity, price

### Additional Models (Planned)

- **Review**: User reviews
  - Fields: id, reviewer_id, reviewed_id, rating, comment, created_at

- **Category**: Product categories
  - Fields: id, name, description, icon

### Database Relationship Diagram

```
User 1 --- * Product
User 1 --- * Order (as buyer)
User 1 --- * Order (as seller)
Product 1 --- * ProductImage
Product 1 --- * OrderItem
Order 1 --- * OrderItem
Category 1 --- * Product
```

## 🔐 Environment Variables

### Backend Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | MySQL connection string | `mysql+pymysql://user:password@localhost/dbname` |
| `SECRET_KEY` | JWT signing key | `a-secure-random-string` |
| `JWT_EXPIRATION_HOURS` | Token expiration time | `24` |
| `CORS_ORIGINS` | Allowed origins for CORS | `http://localhost:3000` |

### Frontend Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `REACT_APP_API_URL` | Backend API URL | `http://localhost:5000/api` |
| `REACT_APP_GOOGLE_MAPS_KEY` | Google Maps API key (future) | `your-google-maps-key` |

## 🧪 Testing

### Running Backend Tests

```bash
# From the backend directory
pytest
```

### Running Frontend Tests

```bash
# From the frontend directory
npm test
```

### Test Coverage

To generate test coverage reports:

```bash
# Backend coverage
pytest --cov=app

# Frontend coverage
npm test -- --coverage
```

## 🚀 Deployment

### Deployment Options

- **Development**: Local development environment
- **Staging**: Test environment with production-like settings
- **Production**: Live environment for real users

### Deployment Instructions

#### Backend Deployment (Example for Ubuntu/Nginx)

1. Set up a production server with Python, Nginx, and Gunicorn
2. Clone the repository and install dependencies
3. Configure environment variables for production
4. Set up Gunicorn service
5. Configure Nginx as reverse proxy

#### Frontend Deployment

1. Build the production bundle:
   ```bash
   npm run build
   ```
2. Deploy the contents of the `build` directory to a static site host or CDN

## 🗺️ Roadmap

We're continuously improving CampusKorner. Here's what's coming next:

### Short-term (1-3 months)
- In-app messaging between buyers and sellers
- Mobile app development (React Native)
- Payment integration (PayPal, Stripe)

### Mid-term (3-6 months)
- AI-powered product recommendations
- Advanced analytics dashboard for sellers
- Multi-university expansion

### Long-term (6+ months)
- Service listings (tutoring, skill sharing)
- Community events section
- Sustainable marketplace features (carbon footprint tracking)

## 👥 Contributing

We welcome contributions to CampusKorner! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**:
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to your branch**:
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on code style, review process, and more.

### Development Workflow

1. Pick an issue from our issue tracker
2. Discuss approach in the issue comments
3. Implement solution in a feature branch
4. Ensure tests pass and add new tests as needed
5. Submit PR and address review comments

## ❓ FAQ

### Technical Questions

**Q: What browsers are supported?**
A: CampusKorner supports recent versions of Chrome, Firefox, Safari, and Edge.

**Q: Is there a mobile app available?**
A: Not yet, but our website is fully responsive. A dedicated mobile app is on our roadmap!

**Q: How secure is my data?**
A: We take security seriously. All passwords are hashed, communications are encrypted, and we follow industry best practices for data protection.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📬 Contact

Project Link: [https://github.com/Mikonimo/campuskorner](https://github.com/Mikonimo/campuskorner)

Email: markmanani19@gmail.com

---

⭐ Star this repo if you find it useful! ⭐

[Back to top](#campuskorner-)