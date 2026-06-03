# 🏗️ NavaNirman Hardware Store - Complete Build Guide
## Building an E-Commerce Website from Scratch

---

# TABLE OF CONTENTS
1. [The Big Picture - What Are We Building?](#big-picture)
2. [Phase 1: Project Setup](#phase-1)
3. [Phase 2: Database Design](#phase-2)
4. [Phase 3: Backend API](#phase-3)
5. [Phase 4: Frontend Templates](#phase-4)
6. [Phase 5: Frontend Styling](#phase-5)
7. [Phase 6: Frontend Interactivity](#phase-6)

---

# <a id="big-picture"></a>🎯 THE BIG PICTURE - WHAT ARE WE BUILDING?

## Imagine a Real Store

Think of a **physical hardware store**. Let's say you own **NavaNirman Hardware** and want to go online.

**Real Store has:**
- A storefront (what customers see) ➜ This is our **HTML/CSS/JavaScript** (Frontend)
- Storage/Inventory system (where products are kept) ➜ This is our **Database**
- Employees managing inventory (finding products, processing orders) ➜ This is our **Backend API**
- A cash register (where purchases happen) ➜ This is our **Server**

**NavaNirman Website will have:**
```
┌─────────────────────────────────────────────────────────────┐
│                      BROWSER (Customer)                      │
│  What the customer sees: HTML, CSS, JavaScript              │
│  - Homepage with categories                                 │
│  - Product pages                                            │
│  - Shopping cart                                            │
│  - Login/Signup                                             │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP Requests (Customer asks for something)
                         │ 
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND SERVER (FastAPI)                 │
│  The "brain" - Logic & Decisions                            │
│  - Process customer requests                                │
│  - Check if user is authenticated                          │
│  - Retrieve products from database                          │
│  - Calculate prices, add to cart                            │
│  - Process orders                                           │
└────────────────────────┬────────────────────────────────────┘
                         │ SQL Queries (Store data)
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATABASE (SQLite)                        │
│  The "memory" - Stores all data                            │
│  - Users (email, password, address)                         │
│  - Products (name, price, description)                     │
│  - Orders (what customers bought)                           │
│  - Categories (Drills, Hammers, etc.)                      │
└─────────────────────────────────────────────────────────────┘
```

---

# <a id="phase-1"></a>📦 PHASE 1: PROJECT SETUP

## Step 1.1: Create Project Directory Structure

**What we're doing:** Think of this like drawing a blueprint before building a house. We're creating folders for different parts of our website.

```
NavaNirman/                      ← Main project folder
├── backend/                     ← Server code (Python)
│   ├── app/                     ← Application code
│   │   ├── __init__.py          ← Marks folder as Python package
│   │   ├── main.py              ← Main server file (like receptionist)
│   │   ├── models.py            ← Database structure
│   │   ├── database.py          ← Database connection
│   │   ├── crud.py              ← Database operations
│   │   ├── static/              ← CSS, JavaScript, Images
│   │   │   ├── styles.css       ← Styling
│   │   │   ├── script.js        ← Interactivity
│   │   │   └── images/          ← Product images
│   │   └── templates/           ← HTML pages
│   │       ├── base.html        ← Master template
│   │       ├── index.html       ← Homepage
│   │       ├── product.html     ← Product page
│   │       ├── cart.html        ← Shopping cart
│   │       └── ... (other pages)
│   ├── requirements.txt         ← List of tools we need
│   ├── Dockerfile              ← Instructions to package for deployment
│   └── Procfile                ← How to run on hosting service
├── .venv/                       ← Python virtual environment (isolated workspace)
├── .env                         ← Secret settings (passwords, API keys)
├── .gitignore                   ← Files to ignore in version control
└── README.md                    ← Documentation
```

**Why?** Organized structure makes code easier to maintain and find things.

---

## Step 1.2: Python Virtual Environment

**What:** A virtual environment is like having your own isolated Python workspace, so your project's dependencies don't conflict with other projects.

**Real-world analogy:** It's like having a separate toolbox for each project - you don't mix tools from different jobs.

### Commands:
```bash
# Create virtual environment
python3 -m venv .venv

# Activate it (enter this isolated workspace)
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate     # On Windows

# You'll see: (.venv) $ (shows you're inside)
```

**Why `python3 -m venv .venv`?**
- `python3` = We're using Python 3 (latest version)
- `-m venv` = Run the virtual environment module
- `.venv` = Create a folder named ".venv" (hidden folder with all tools)

---

## Step 1.3: Install Dependencies

**What:** Download and install all the tools/libraries we need (like getting your toolbox).

### The `requirements.txt` file:
```
fastapi                    # Web framework - handles HTTP requests
uvicorn[standard]          # Server to run FastAPI
jinja2                     # Template engine - inject data into HTML
sqlmodel                   # ORM - Convert Python to database queries
python-dotenv              # Read environment variables from .env
itsdangerous               # Create secure tokens for authentication
```

**What each does (in simple terms):**

1. **FastAPI** - The framework that catches customer requests and decides what to do
   - Like the receptionist at a store who directs customers

2. **Uvicorn** - The server that actually runs our website
   - Like the building that houses the store

3. **Jinja2** - Template engine that combines data with HTML
   - Like a mail-merge: template + data = personalized HTML

4. **SQLModel** - Converts our Python code to database language
   - Translator between Python and database (SQLite)

5. **python-dotenv** - Reads settings from `.env` file
   - Like keeping secret recipes in a private notebook

6. **itsdangerous** - Creates secure tokens for login sessions
   - Like a tamper-proof ID card you give customers

### Installation:
```bash
pip install -r requirements.txt
```

**What happens:** `pip` (Package Installer for Python) downloads all these tools into your `.venv` folder.

---

# <a id="phase-2"></a>🗄️ PHASE 2: DATABASE DESIGN - THE BLUEPRINT

## Understanding Databases

**Real-world analogy:** A database is like a library.

- **Library** = Database
- **Shelves** = Tables (different topics)
- **Books** = Records (individual entries)
- **Book information** = Columns (ISBN, Title, Author)

For NavaNirman, we need these "shelves" (tables):

```
┌──────────────────────────────────────┐
│           USER TABLE                 │
├──────────────────────────────────────┤
│ id (unique ID)                       │
│ email (login email)                  │
│ full_name (customer's name)          │
│ password_hash (encrypted password)   │
│ phone (contact number)               │
│ address (delivery address)           │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│         PRODUCT TABLE                │
├──────────────────────────────────────┤
│ id (unique product ID)               │
│ name (product name)                  │
│ description (details)                │
│ price (cost)                         │
│ category_id (which category)         │
│ image_url (product image link)       │
│ stock (quantity available)           │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│        CATEGORY TABLE                │
├──────────────────────────────────────┤
│ id (unique category ID)              │
│ name (category name)                 │
│ description (what it is)             │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│         CART TABLE                   │
├──────────────────────────────────────┤
│ id (unique cart item ID)             │
│ user_id (whose cart)                 │
│ product_id (which product)           │
│ quantity (how many)                  │
│ added_at (when added)                │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│         ORDER TABLE                  │
├──────────────────────────────────────┤
│ id (order number)                    │
│ user_id (who ordered)                │
│ total (final price)                  │
│ status (pending/completed)           │
│ created_at (order date)              │
│ shipping_address (where to send)     │
│ payment_method (COD/Online)          │
│ phone (contact for delivery)         │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│       ORDER ITEM TABLE               │
├──────────────────────────────────────┤
│ id (unique)                          │
│ order_id (which order)               │
│ product_id (which product)           │
│ quantity (how many)                  │
│ price (price at time of order)       │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│        CONTACT TABLE                 │
├──────────────────────────────────────┤
│ id (message ID)                      │
│ name (who contacted)                 │
│ email (reply-to email)               │
│ message (what they said)             │
│ created_at (when sent)               │
└──────────────────────────────────────┘
```

---

## Step 2.1: `models.py` - Defining Database Structure

**What:** This file defines what our tables look like. It's like drawing a template for how to store information.

**File: `backend/app/models.py`**

```python
"""
MODEL DEFINITIONS - Think of this as the blueprint for our database tables
Each class below becomes a table in our database
"""

from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String, Integer, Float, DateTime, Text


# ============================================================================
# 1. CATEGORY MODEL - Types of products (Drills, Hammers, etc.)
# ============================================================================

class CategoryBase(SQLModel):
    """
    Base category info - shared between creating and reading
    
    Why separate Base/Create/Read?
    - Base: Common fields
    - Create: What data you need TO CREATE a category
    - Read: What data you GET BACK when reading a category
    """
    name: str = Field(index=True)  # Make name searchable (indexed)
    description: Optional[str] = None


class Category(CategoryBase, table=True):
    """
    The actual Category table in database
    table=True means this becomes a real database table
    """
    id: Optional[int] = Field(default=None, primary_key=True)  # Unique identifier
    products: List["Product"] = Relationship(back_populates="category")
    # ^ One category can have many products


# ============================================================================
# 2. PRODUCT MODEL - The items we're selling
# ============================================================================

class ProductBase(SQLModel):
    """All product info needed for creation"""
    name: str = Field(index=True)
    description: str
    price: float = Field(gt=0)  # gt=0 means "greater than 0" (validation)
    category_id: int = Field(foreign_key="category.id")  # Link to category
    image_url: Optional[str] = None
    stock: int = Field(default=0, ge=0)  # ge=0 means "greater or equal to 0"


class Product(ProductBase, table=True):
    """The actual Product table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    category: Optional[Category] = Relationship(back_populates="products")
    cart_items: List["CartItem"] = Relationship(back_populates="product")
    order_items: List["OrderItem"] = Relationship(back_populates="product")


# ============================================================================
# 3. USER MODEL - Customers
# ============================================================================

class UserBase(SQLModel):
    """All user info needed"""
    email: str = Field(unique=True, index=True)  # Unique login
    full_name: str
    phone: Optional[str] = None  # Contact number
    address: Optional[str] = None  # Delivery address


class User(UserBase, table=True):
    """The actual User table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str  # Never store plain passwords! Only encrypted hashes
    cart_items: List["CartItem"] = Relationship(back_populates="user")
    orders: List["Order"] = Relationship(back_populates="user")
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# 4. CART ITEM MODEL - Items in shopping cart
# ============================================================================

class CartItemBase(SQLModel):
    """Cart item info"""
    user_id: int = Field(foreign_key="user.id")  # Whose cart?
    product_id: int = Field(foreign_key="product.id")  # Which product?
    quantity: int = Field(gt=0)  # Must be more than 0


class CartItem(CartItemBase, table=True):
    """The actual CartItem table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user: Optional[User] = Relationship(back_populates="cart_items")
    product: Optional[Product] = Relationship(back_populates="cart_items")
    added_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# 5. ORDER MODEL - Customer orders
# ============================================================================

class OrderBase(SQLModel):
    """Order info"""
    user_id: int = Field(foreign_key="user.id")
    total: float
    payment_method: str = "Cash on delivery"  # Default payment method
    shipping_address: str
    phone: str
    receipt_method: str = "email"  # How to send receipt


class Order(OrderBase, table=True):
    """The actual Order table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user: Optional[User] = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")
    status: str = "pending"  # pending, confirmed, shipped, delivered
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# 6. ORDER ITEM MODEL - Individual products in an order
# ============================================================================

class OrderItemBase(SQLModel):
    """Order item info"""
    order_id: int = Field(foreign_key="order.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int = Field(gt=0)
    price: float  # Price at time of order (in case price changed later)


class OrderItem(OrderItemBase, table=True):
    """The actual OrderItem table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    order: Optional[Order] = Relationship(back_populates="items")
    product: Optional[Product] = Relationship(back_populates="order_items")


# ============================================================================
# 7. CONTACT MODEL - Messages from contact form
# ============================================================================

class ContactBase(SQLModel):
    """Contact message info"""
    name: str
    email: str = Field(index=True)
    message: str = Field(min_length=10)  # At least 10 characters


class Contact(ContactBase, table=True):
    """The actual Contact table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Key Concepts Explained:**

1. **`SQLModel`** - Base class for all models. Tells SQLModel "this is a database thing"

2. **`Field()`** - Describes constraints and properties
   - `primary_key=True` = This column uniquely identifies each row
   - `foreign_key="table.column"` = Links to another table
   - `unique=True` = No duplicates allowed
   - `index=True` = Make searches faster
   - `default=...` = Use this if no value provided
   - `gt=0` = Greater than 0 (validation)

3. **`Relationship()`** - Links between tables
   - One User can have many CartItems
   - One Product can be in many Orders

4. **`table=True`** - This means "create an actual database table for this"

---

## Step 2.2: `database.py` - Connecting to Database

**File: `backend/app/database.py`**

```python
"""
DATABASE CONNECTION - Sets up the connection to SQLite database
"""

import os
from sqlmodel import create_engine, SQLModel
from sqlalchemy.pool import StaticPool

# ============================================================================
# DATABASE SETUP
# ============================================================================

# Check if we're in testing mode or production
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///nawa_nirman.db")
# If no DATABASE_URL set, use local SQLite file called "nawa_nirman.db"

# Why different settings for SQLite vs other databases?
if DATABASE_URL.startswith("sqlite"):
    # SQLite: Keep connection open (StaticPool)
    # SQLite is file-based, not server-based
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    # Other databases: Connection pooling (safer for multiple connections)
    engine = create_engine(
        DATABASE_URL,
        echo=False  # Set to True to see SQL queries in console
    )

# ============================================================================
# CREATE TABLES
# ============================================================================

def init_db():
    """
    Create all database tables based on our models
    Only creates if they don't exist
    """
    SQLModel.metadata.create_all(engine)
```

**What's happening:**

- **`create_engine()`** = Opens connection to database
- **`sqlite:///nawa_nirman.db`** = Creates/uses local SQLite file
- **`connect_args={"check_same_thread": False}`** = Allow multiple connections (needed for web)
- **`SQLModel.metadata.create_all(engine)`** = Create all tables

---

# <a id="phase-3"></a>⚙️ PHASE 3: BACKEND API - THE BRAIN

## What is an API?

**API** = Application Programming Interface

**Real-world analogy:** An API is like a restaurant menu.

- You don't see the kitchen (database)
- You tell the waiter what you want (make request)
- The waiter goes to kitchen (backend processes)
- Waiter brings back your food (response)

Our API will have endpoints like:
- `/` - Show homepage
- `/products` - Get all products
- `/product/{id}` - Get specific product
- `/login` - User login
- `/cart` - View shopping cart
- `/checkout` - Place order

---

## Step 3.1: `crud.py` - Database Operations

**CRUD = Create, Read, Update, Delete**

This file contains all the database operations. Think of it as the database instructions manual.

**File: `backend/app/crud.py`** (This will be LONG - this is where all logic happens)

```python
"""
CRUD OPERATIONS - All database interactions
C = Create (add new data)
R = Read (fetch data)
U = Update (modify existing data)
D = Delete (remove data)
"""

from datetime import datetime
from typing import Optional, List
from sqlmodel import Session, select, or_
from passlib.context import CryptContext
from .models import (
    User, Product, Category, CartItem, Order, OrderItem, Contact
)


# ============================================================================
# PASSWORD HASHING SETUP
# ============================================================================

"""
Why hash passwords?
Never store passwords as plain text. If hackers get database, they get all passwords!
Hashing = one-way encryption. Can't reverse it.

passlib = Library for secure password hashing
CryptContext = Tool to hash and verify passwords
"""

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Convert plain password to hash
    
    Example:
    - Input: "MyPassword123!"
    - Output: "$2b$12$R9h/cIPz0gi.URNNX3kha2OPST9/PgBkqquzi.Ss..."
    
    Always different even for same password (due to random salt)
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Check if plain password matches the hash
    
    Example:
    - User enters: "MyPassword123!"
    - We have stored: "$2b$12$R9h/cIPz0gi.URNNX3kha2OPST9/PgBkqquzi.Ss..."
    - verify_password returns: True or False
    """
    return pwd_context.verify(plain_password, hashed_password)


# ============================================================================
# USER OPERATIONS
# ============================================================================

def create_user(session: Session, email: str, full_name: str, password: str, 
                phone: Optional[str] = None, address: Optional[str] = None) -> User:
    """
    Create a new user account
    
    Flow:
    1. Check if email already exists
    2. Hash the password (never store plain password!)
    3. Create User object
    4. Save to database
    5. Return the created user
    """
    # Check if email already taken
    existing_user = get_user_by_email(session, email)
    if existing_user:
        raise ValueError(f"Email {email} already registered")
    
    # Create password hash
    hashed_pwd = hash_password(password)
    
    # Create new user
    user = User(
        email=email,
        full_name=full_name,
        password_hash=hashed_pwd,
        phone=phone,
        address=address
    )
    
    # Add to database
    session.add(user)
    session.commit()
    session.refresh(user)  # Reload to get the ID
    
    return user


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """
    Find user by email
    
    Why? Users login with email, so we need to look them up
    """
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()  # .first() = get first result or None


def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
    """
    Find user by ID
    
    Why? After login, we store user ID in session, need to get user details
    """
    return session.get(User, user_id)


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """
    Verify email and password match
    
    Login flow:
    1. Find user by email
    2. Check if password matches stored hash
    3. Return user if match, None if not
    """
    user = get_user_by_email(session, email)
    
    # No user found
    if not user:
        return None
    
    # Password doesn't match
    if not verify_password(password, user.password_hash):
        return None
    
    # Both match!
    return user


def update_user_profile(session: Session, user_id: int, full_name: Optional[str] = None,
                       phone: Optional[str] = None, address: Optional[str] = None) -> User:
    """
    Update user's profile information
    
    Example: After user adds their address during checkout
    """
    user = get_user_by_id(session, user_id)
    if not user:
        raise ValueError(f"User {user_id} not found")
    
    # Update only provided fields
    if full_name:
        user.full_name = full_name
    if phone:
        user.phone = phone
    if address:
        user.address = address
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user


# ============================================================================
# CATEGORY OPERATIONS
# ============================================================================

def get_categories(session: Session) -> List[Category]:
    """
    Get all product categories
    
    Used to show: Drills, Hammers, Screwdrivers, etc.
    """
    statement = select(Category)
    return session.exec(statement).all()  # .all() = get all results


def get_category_by_id(session: Session, category_id: int) -> Optional[Category]:
    """Get specific category by ID"""
    return session.get(Category, category_id)


def create_category(session: Session, name: str, description: Optional[str] = None) -> Category:
    """Create a new category"""
    category = Category(name=name, description=description)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


# ============================================================================
# PRODUCT OPERATIONS
# ============================================================================

def get_products(session: Session, category_id: Optional[int] = None) -> List[Product]:
    """
    Get all products (or filtered by category)
    
    Example usage:
    - get_products(session) = Get ALL products
    - get_products(session, category_id=2) = Get only category 2
    """
    statement = select(Product)
    
    # Filter by category if provided
    if category_id:
        statement = statement.where(Product.category_id == category_id)
    
    return session.exec(statement).all()


def get_product_by_id(session: Session, product_id: int) -> Optional[Product]:
    """
    Get specific product by ID
    
    Used when showing product details page
    """
    return session.get(Product, product_id)


def create_product(session: Session, name: str, description: str, price: float,
                  category_id: int, image_url: Optional[str] = None,
                  stock: int = 0) -> Product:
    """Create a new product"""
    product = Product(
        name=name,
        description=description,
        price=price,
        category_id=category_id,
        image_url=image_url,
        stock=stock
    )
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


# ============================================================================
# CART OPERATIONS
# ============================================================================

def add_or_update_cart_item(session: Session, user_id: int, product_id: int,
                           quantity: int) -> CartItem:
    """
    Add item to cart, or update quantity if already there
    
    Flow:
    1. Check if this product already in this user's cart
    2. If yes, update quantity
    3. If no, create new cart item
    """
    # Look for existing cart item
    statement = select(CartItem).where(
        (CartItem.user_id == user_id) & (CartItem.product_id == product_id)
    )
    existing_item = session.exec(statement).first()
    
    if existing_item:
        # Update quantity
        existing_item.quantity = quantity
        session.add(existing_item)
    else:
        # Create new
        existing_item = CartItem(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )
        session.add(existing_item)
    
    session.commit()
    session.refresh(existing_item)
    return existing_item


def get_cart_items(session: Session, user_id: int) -> List[CartItem]:
    """
    Get all items in user's cart from database
    """
    statement = select(CartItem).where(CartItem.user_id == user_id)
    return session.exec(statement).all()


def remove_cart_item(session: Session, user_id: int, product_id: int) -> bool:
    """
    Remove item from cart
    """
    statement = select(CartItem).where(
        (CartItem.user_id == user_id) & (CartItem.product_id == product_id)
    )
    item = session.exec(statement).first()
    
    if item:
        session.delete(item)
        session.commit()
        return True
    return False


def clear_cart(session: Session, user_id: int) -> None:
    """
    Remove ALL items from user's cart (after checkout)
    """
    statement = select(CartItem).where(CartItem.user_id == user_id)
    items = session.exec(statement).all()
    
    for item in items:
        session.delete(item)
    
    session.commit()


# ============================================================================
# ORDER OPERATIONS
# ============================================================================

def create_order(session: Session, user_id: int, cart_items: List[CartItem],
                total: float, payment_method: str, shipping_address: str,
                phone: str) -> Order:
    """
    Create order from cart items
    
    Complex flow:
    1. Create Order record
    2. Loop through cart items
    3. Create OrderItem for each (copy product info)
    4. Clear user's cart
    5. Return order
    """
    # Create order
    order = Order(
        user_id=user_id,
        total=total,
        payment_method=payment_method,
        shipping_address=shipping_address,
        phone=phone,
        status="pending"
    )
    session.add(order)
    session.flush()  # Save but don't commit yet (need order ID for items)
    
    # Create order items from cart
    for cart_item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
        session.add(order_item)
    
    # Clear cart
    clear_cart(session, user_id)
    
    session.commit()
    session.refresh(order)
    
    return order


def get_order_by_id(session: Session, order_id: int) -> Optional[Order]:
    """Get order details"""
    return session.get(Order, order_id)


def get_user_orders(session: Session, user_id: int) -> List[Order]:
    """Get all orders by a user"""
    statement = select(Order).where(Order.user_id == user_id)
    return session.exec(statement).all()


# ============================================================================
# CONTACT OPERATIONS
# ============================================================================

def create_contact(session: Session, name: str, email: str, message: str) -> Contact:
    """Save contact form submission"""
    contact = Contact(
        name=name,
        email=email,
        message=message
    )
    session.add(contact)
    session.commit()
    session.refresh(contact)
    return contact


# ============================================================================
# CART SESSION MANAGEMENT
# ============================================================================

def get_cart_items_from_session(session_data: dict) -> dict:
    """
    Parse cart data stored in session cookies
    
    Session is for non-logged-in users (temporary)
    Format: {product_id: quantity}
    """
    return session_data.get("cart", {})


def merge_session_cart(db_session: Session, user_id: int, session_cart: dict) -> None:
    """
    When user logs in, merge their temporary session cart with database cart
    
    Why? If they browsed without logging in, don't lose their cart!
    """
    for product_id_str, quantity in session_cart.items():
        product_id = int(product_id_str)
        add_or_update_cart_item(db_session, user_id, product_id, quantity)


# ============================================================================
# SEED DATABASE WITH DEMO DATA
# ============================================================================

def seed_database(session: Session):
    """
    Populate database with sample data on startup
    
    This helps us test without manually adding products
    """
    # Check if already seeded
    statement = select(Category)
    if session.exec(statement).first():
        return  # Already has data
    
    # Create categories
    cat_drills = create_category(session, "Drills", "Power drills and drilling tools")
    cat_hammers = create_category(session, "Hammers", "Various types of hammers")
    cat_safety = create_category(session, "Safety Gear", "Protective equipment")
    
    # Create products
    create_product(
        session,
        name="Cordless Drill Kit",
        description="20V lithium-ion cordless drill with accessories",
        price=3499.00,
        category_id=cat_drills.id,
        image_url="/static/images/drill.jpg",
        stock=15
    )
    
    create_product(
        session,
        name="Claw Hammer",
        description="16 oz claw hammer with comfortable grip",
        price=499.00,
        category_id=cat_hammers.id,
        image_url="/static/images/hammer.jpg",
        stock=25
    )
    
    create_product(
        session,
        name="Safety Helmet",
        description="Hard plastic safety helmet with adjustable strap",
        price=349.00,
        category_id=cat_safety.id,
        image_url="/static/images/helmet.jpg",
        stock=30
    )
```

**Key Concepts:**

1. **`Session`** - Database connection session (like a conversation with database)
2. **`select()`** - SQL SELECT query builder
3. **`.where()`** - Filter conditions (SQL WHERE)
4. **`.first()`** - Get first result or None
5. **`.all()`** - Get all results
6. **`session.add()`** - Mark object for saving
7. **`session.commit()`** - Actually save to database
8. **`session.flush()`** - Save but don't commit yet (need to get IDs first)

---

## Step 3.2: `main.py` - The Server Application

This is the CORE of the backend. This file handles every request from the browser.

**File: `backend/app/main.py`** (This is VERY long - take time to read)

```python
"""
MAIN APPLICATION - FastAPI server
Every HTTP request comes through here
"""

import os
import re
import smtplib
import ssl
from email.message import EmailMessage
from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy import text
from starlette.middleware.sessions import SessionMiddleware
from sqlmodel import SQLModel, Session
from .database import engine
from .crud import (
    add_or_update_cart_item,
    authenticate_user,
    clear_cart,
    create_contact,
    create_order,
    create_user,
    get_cart_items,
    get_cart_items_from_session,
    get_categories,
    get_order_by_id,
    get_product_by_id,
    get_products,
    get_user_by_id,
    get_user_by_email,
    update_user_profile,
    merge_session_cart,
    remove_cart_item,
    seed_database,
)


# ============================================================================
# INITIALIZE FASTAPI APP
# ============================================================================

"""
FastAPI app object - This is the central server
When browser makes request, it comes to this 'app'
"""

app = FastAPI(title="Nawa Nirman Backend")

# Mount static files - Serve CSS, JavaScript, Images
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),
    name="static"
)

# Add session middleware - Store user info in cookies
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "change-this-secret")
)

"""
Middleware = Software that processes every request before it reaches endpoints
SessionMiddleware = Allows us to store data in cookies (like "user is logged in")
"""


# ============================================================================
# TEMPLATE SETUP
# ============================================================================

"""
Jinja2 = Template engine
Takes HTML template + data → Produces final HTML

Example:
Template: <p>Hello {{ name }}</p>
Data: {name: "Ali"}
Result: <p>Hello Ali</p>
"""

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),  # Where to find templates
    autoescape=select_autoescape(["html", "xml"]),  # Protect against injection
    cache_size=0,  # Don't cache (useful during development)
)

templates = Jinja2Templates(env=jinja_env)


# ============================================================================
# APP STARTUP - Runs once when server starts
# ============================================================================

@app.on_event("startup")
def on_startup():
    """
    Setup database on server startup
    
    Flow:
    1. Create all tables if they don't exist
    2. Check schema and add missing columns
    3. Add demo data if database is empty
    """
    # Create tables based on models
    SQLModel.metadata.create_all(engine)
    
    # Ensure all columns exist (migration)
    ensure_database_schema()
    
    # Add demo data if empty
    with Session(engine) as session:
        seed_database(session)


def ensure_database_schema():
    """
    Check if all required columns exist
    Add any missing columns (for migrations)
    """
    with engine.begin() as conn:
        def has_column(table_name: str, column_name: str) -> bool:
            """Check if column exists in table"""
            result = conn.execute(text(f"PRAGMA table_info('{table_name}')")).all()
            return any(row[1] == column_name for row in result)

        # Check each required column
        if not has_column("user", "address"):
            conn.execute(text('ALTER TABLE "user" ADD COLUMN address TEXT'))
        if not has_column("user", "phone"):
            conn.execute(text('ALTER TABLE "user" ADD COLUMN phone TEXT'))
        if not has_column("order", "payment_method"):
            conn.execute(text('ALTER TABLE "order" ADD COLUMN payment_method TEXT DEFAULT "Cash on delivery"'))
        if not has_column("order", "shipping_address"):
            conn.execute(text('ALTER TABLE "order" ADD COLUMN shipping_address TEXT'))
        if not has_column("order", "phone"):
            conn.execute(text('ALTER TABLE "order" ADD COLUMN phone TEXT'))
        if not has_column("order", "receipt_method"):
            conn.execute(text('ALTER TABLE "order" ADD COLUMN receipt_method TEXT DEFAULT "email"'))


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_current_user(request: Request):
    """
    Get the currently logged-in user from session
    
    How session works:
    1. When user logs in, we store their user_id in cookies
    2. Browser sends cookies with every request
    3. We read user_id from cookies
    4. Look up user from database
    """
    user_id = request.session.get("user_id")
    if user_id is None:
        return None
    
    with Session(engine) as session:
        return get_user_by_id(session, user_id)


def is_password_strong(password: str) -> bool:
    """
    Validate password strength
    
    Rules:
    - At least 8 characters
    - At least 1 digit (0-9)
    - At least 1 special character (!@#$%)
    """
    return (
        len(password) >= 8
        and re.search(r"\d", password)  # Has digit
        and re.search(r"[^A-Za-z0-9]", password)  # Has special char
    )


# ============================================================================
# ROUTES - Endpoints that handle requests
# ============================================================================

"""
Routes = URLs that browser can visit

@app.get("/page") = When browser asks for GET /page
@app.post("/data") = When browser sends POST to /data

GET = Asking for data
POST = Sending data
"""


# ============================================================================
# ROUTE 1: Homepage
# ============================================================================

@app.get("/")
def homepage(request: Request):
    """
    Show homepage
    
    What happens:
    1. Get current user (if logged in)
    2. Get all categories
    3. Get all products
    4. Render index.html with this data
    """
    with Session(engine) as session:
        categories = get_categories(session)
        products = get_products(session)
        current_user = get_current_user(request)
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "categories": categories,
            "products": products,
            "user": current_user
        })


# ============================================================================
# ROUTE 2: About page
# ============================================================================

@app.get("/about")
def about_page(request: Request):
    """Show about page"""
    current_user = get_current_user(request)
    
    return templates.TemplateResponse("about.html", {
        "request": request,
        "user": current_user
    })


# ============================================================================
# ROUTE 3: Categories page
# ============================================================================

@app.get("/categories")
def categories_page(request: Request):
    """Show all categories"""
    with Session(engine) as session:
        categories = get_categories(session)
        current_user = get_current_user(request)
        
        return templates.TemplateResponse("categories.html", {
            "request": request,
            "categories": categories,
            "user": current_user
        })


# ============================================================================
# ROUTE 4: Product details
# ============================================================================

@app.get("/product/{product_id}")
def product_page(request: Request, product_id: int):
    """
    Show single product details
    
    URL: /product/5 → Shows product with ID 5
    """
    with Session(engine) as session:
        product = get_product_by_id(session, product_id)
        current_user = get_current_user(request)
        
        if not product:
            return {"error": "Product not found"}
        
        return templates.TemplateResponse("product.html", {
            "request": request,
            "product": product,
            "user": current_user
        })


# ============================================================================
# ROUTE 5: Shopping Cart
# ============================================================================

@app.get("/cart")
def cart_page(request: Request):
    """
    Show shopping cart
    
    Cart can be:
    1. Database cart (logged-in users)
    2. Session cart (non-logged-in users)
    """
    current_user = get_current_user(request)
    
    if current_user:
        # Logged in - get cart from database
        with Session(engine) as session:
            cart_items = get_cart_items(session, current_user.id)
            total = sum(item.quantity * item.product.price for item in cart_items)
    else:
        # Not logged in - get cart from session cookies
        cart_items = get_cart_items_from_session(request.session)
        total = 0
        for product_id_str, quantity in cart_items.items():
            # Note: Can't get price without database lookup
            total += quantity * 0  # Placeholder
    
    return templates.TemplateResponse("cart.html", {
        "request": request,
        "cart_items": cart_items,
        "total": total,
        "user": current_user
    })


# ============================================================================
# ROUTE 6: Add to cart (API)
# ============================================================================

@app.post("/api/cart/add")
def add_to_cart(request: Request, product_id: int = Form(...), quantity: int = Form(...)):
    """
    Add item to cart
    
    This is an API endpoint (returns JSON, not HTML)
    
    Flow:
    1. Get product to verify it exists
    2. If logged in, add to database cart
    3. If not logged in, add to session cart
    """
    with Session(engine) as session:
        product = get_product_by_id(session, product_id)
        
        if not product:
            return JSONResponse({"error": "Product not found"}, status_code=404)
        
        current_user = get_current_user(request)
        
        if current_user:
            # Add to database
            add_or_update_cart_item(session, current_user.id, product_id, quantity)
            return JSONResponse({"message": "Added to cart"})
        else:
            # Add to session (cookies)
            if "cart" not in request.session:
                request.session["cart"] = {}
            
            product_id_str = str(product_id)
            if product_id_str in request.session["cart"]:
                request.session["cart"][product_id_str] += quantity
            else:
                request.session["cart"][product_id_str] = quantity
            
            return JSONResponse({"message": "Added to cart"})


# ============================================================================
# ROUTE 7: Remove from cart
# ============================================================================

@app.post("/api/cart/remove")
def remove_from_cart(request: Request, product_id: int = Form(...)):
    """Remove item from cart"""
    current_user = get_current_user(request)
    
    if current_user:
        # Remove from database
        with Session(engine) as session:
            remove_cart_item(session, current_user.id, product_id)
    else:
        # Remove from session
        if "cart" in request.session and str(product_id) in request.session["cart"]:
            del request.session["cart"][str(product_id)]
    
    return JSONResponse({"message": "Removed from cart"})


# ============================================================================
# ROUTE 8: Signup page
# ============================================================================

@app.get("/signup")
def signup_page(request: Request):
    """Show signup form"""
    return templates.TemplateResponse("signup.html", {
        "request": request,
        "user": None
    })


# ============================================================================
# ROUTE 9: Create account (POST from signup form)
# ============================================================================

@app.post("/signup")
def do_signup(request: Request, email: str = Form(...), full_name: str = Form(...),
              password: str = Form(...), confirm_password: str = Form(...)):
    """
    Process account creation
    
    Flow:
    1. Validate inputs
    2. Check if passwords match
    3. Check if password is strong
    4. Check if email already exists
    5. Create user
    6. Log them in (store user_id in session)
    7. Redirect to home
    """
    # Validate passwords match
    if password != confirm_password:
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error": "Passwords don't match"
        })
    
    # Validate password strength
    if not is_password_strong(password):
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error": "Password must be 8+ chars with numbers and special characters"
        })
    
    try:
        with Session(engine) as session:
            # Create user in database
            user = create_user(session, email, full_name, password)
            
            # Log them in (set session cookie)
            request.session["user_id"] = user.id
            
            # Merge any session cart into database cart
            session_cart = get_cart_items_from_session(request.session)
            if session_cart:
                merge_session_cart(session, user.id, session_cart)
                request.session.clear()
            
            # Redirect to home
            return RedirectResponse(url="/", status_code=302)
    
    except ValueError as e:
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error": str(e)
        })


# ============================================================================
# ROUTE 10: Login page
# ============================================================================

@app.get("/login")
def login_page(request: Request):
    """Show login form"""
    return templates.TemplateResponse("login.html", {
        "request": request,
        "user": None
    })


# ============================================================================
# ROUTE 11: Process login
# ============================================================================

@app.post("/login")
def do_login(request: Request, email: str = Form(...), password: str = Form(...)):
    """
    Process login
    
    Flow:
    1. Find user by email
    2. Verify password
    3. If correct, set session cookie
    4. Redirect to home
    5. If wrong, show error
    """
    with Session(engine) as session:
        user = authenticate_user(session, email, password)
        
        if user:
            # Login successful
            request.session["user_id"] = user.id
            
            # Merge session cart into database cart
            session_cart = get_cart_items_from_session(request.session)
            if session_cart:
                merge_session_cart(session, user.id, session_cart)
            
            request.session.clear()
            request.session["user_id"] = user.id
            
            return RedirectResponse(url="/", status_code=302)
        else:
            # Login failed
            return templates.TemplateResponse("login.html", {
                "request": request,
                "error": "Invalid email or password"
            })


# ============================================================================
# ROUTE 12: Logout
# ============================================================================

@app.get("/logout")
def logout(request: Request):
    """
    Logout - Clear session and redirect to home
    """
    request.session.clear()
    return RedirectResponse(url="/", status_code=302)


# ============================================================================
# ROUTE 13: User profile page
# ============================================================================

@app.get("/profile")
def profile_page(request: Request):
    """
    Show user profile
    
    Only accessible if logged in
    """
    current_user = get_current_user(request)
    
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": current_user
    })


# ============================================================================
# ROUTE 14: Update profile
# ============================================================================

@app.post("/profile/update")
def update_profile(request: Request, full_name: str = Form(...),
                  phone: str = Form(...), address: str = Form(...)):
    """Update user profile information"""
    current_user = get_current_user(request)
    
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    
    with Session(engine) as session:
        update_user_profile(session, current_user.id, full_name, phone, address)
    
    return RedirectResponse(url="/profile", status_code=302)


# ============================================================================
# ROUTE 15: Checkout page
# ============================================================================

@app.get("/checkout")
def checkout_page(request: Request):
    """
    Show checkout page
    
    Only if user is logged in and has cart items
    """
    current_user = get_current_user(request)
    
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    
    with Session(engine) as session:
        cart_items = get_cart_items(session, current_user.id)
        total = sum(item.quantity * item.product.price for item in cart_items)
        
        if not cart_items:
            return RedirectResponse(url="/cart", status_code=302)
        
        return templates.TemplateResponse("checkout.html", {
            "request": request,
            "user": current_user,
            "cart_items": cart_items,
            "total": total
        })


# ============================================================================
# ROUTE 16: Process order (POST from checkout)
# ============================================================================

@app.post("/checkout")
def process_order(request: Request, payment_method: str = Form(...),
                 shipping_address: str = Form(...), phone: str = Form(...)):
    """
    Process order creation
    
    Flow:
    1. Get current user
    2. Get their cart items
    3. Calculate total
    4. Create order
    5. Send confirmation SMS/Email
    6. Clear cart
    7. Show confirmation page
    """
    current_user = get_current_user(request)
    
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    
    with Session(engine) as session:
        cart_items = get_cart_items(session, current_user.id)
        
        if not cart_items:
            return RedirectResponse(url="/cart", status_code=302)
        
        # Calculate total
        total = sum(item.quantity * item.product.price for item in cart_items)
        
        # Create order
        order = create_order(
            session,
            current_user.id,
            cart_items,
            total,
            payment_method,
            shipping_address,
            phone
        )
        
        # Send confirmation SMS
        send_order_confirmation_sms(order)
        
        # Redirect to confirmation page
        return RedirectResponse(url=f"/order-confirmation/{order.id}", status_code=302)


# ============================================================================
# ROUTE 17: Order confirmation page
# ============================================================================

@app.get("/order-confirmation/{order_id}")
def order_confirmation(request: Request, order_id: int):
    """Show order confirmation"""
    with Session(engine) as session:
        order = get_order_by_id(session, order_id)
        
        if not order:
            return {"error": "Order not found"}
        
        current_user = get_current_user(request)
        
        return templates.TemplateResponse("order_confirmation.html", {
            "request": request,
            "order": order,
            "user": current_user
        })


# ============================================================================
# ROUTE 18: Contact page
# ============================================================================

@app.get("/contact")
def contact_page(request: Request):
    """Show contact form"""
    return templates.TemplateResponse("contact.html", {
        "request": request,
        "user": get_current_user(request)
    })


# ============================================================================
# ROUTE 19: Submit contact form
# ============================================================================

@app.post("/contact")
def submit_contact(request: Request, name: str = Form(...), 
                  email: str = Form(...), message: str = Form(...)):
    """
    Process contact form submission
    
    Flow:
    1. Validate inputs
    2. Save to database
    3. Optionally: send email to admin
    4. Thank user
    """
    if len(message) < 10:
        return templates.TemplateResponse("contact.html", {
            "request": request,
            "error": "Message must be at least 10 characters"
        })
    
    try:
        with Session(engine) as session:
            create_contact(session, name, email, message)
        
        return templates.TemplateResponse("contact.html", {
            "request": request,
            "success": "Thank you! We'll get back to you soon."
        })
    except Exception as e:
        return templates.TemplateResponse("contact.html", {
            "request": request,
            "error": f"Error: {str(e)}"
        })


# ============================================================================
# SMS NOTIFICATION FUNCTION
# ============================================================================

def send_order_confirmation_sms(order):
    """
    Send SMS confirmation to customer
    
    This is a placeholder - in production, use Twilio or similar
    
    Why SMS?
    - Fast notification
    - Works even if email is spam folder
    - Customers can track order
    """
    phone = order.phone
    if not phone:
        print("SMS skipped: No phone number provided.")
        return False
    
    message_text = f"Order #{order.id} confirmed! Total: Rs. {order.total}. Thank you for shopping at Nawa Nirman Hardware!"
    
    # Placeholder - In production:
    # 1. Install Twilio SDK
    # 2. Set up Twilio account with API key
    # 3. Use Twilio client to send SMS
    print(f"SMS would be sent to {phone}: {message_text}")
    return True


# ============================================================================
# EMAIL NOTIFICATION FUNCTION
# ============================================================================

def send_order_confirmation_email(order):
    """
    Send confirmation email
    
    Not implemented in current version, but here's how:
    
    1. Create email with order details
    2. Use SMTP to send via email server
    3. Catch errors (invalid email, server down)
    """
    # TODO: Implement
    pass
```

This is the MASSIVE file that handles everything! Let me continue with Phase 4...

---

# <a id="phase-4"></a>🎨 PHASE 4: FRONTEND TEMPLATES (HTML)

## What are Templates?

Templates are HTML files with "holes" you can fill with data.

**Without template:**
```html
<p>Hello John</p>
```
(Works for only John)

**With template:**
```html
<p>Hello {{ name }}</p>
```
(Works for anyone - Jinja2 fills in the name)

---

## Step 4.1: `base.html` - Master Template

**File: `backend/app/templates/base.html`**

This is the FOUNDATION. All other pages extend this.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>
        {# {% block title %} - Show different title on each page #}
        {% block title %}Nawa Nirman Hardware{% endblock %}
    </title>
    
    {# {% block extra_css %} - Allow child templates to add extra CSS #}
    {% block extra_css %}{% endblock %}
    
    {# Link to main CSS file #}
    <link rel="stylesheet" href="{{ url_for('static', path='/styles.css') }}">
</head>
<body>
    {# ======================================================================
       NAVIGATION BAR - Shows on every page
       ====================================================================== #}
    <nav class="navbar">
        <div class="navbar-container">
            {# Logo/Brand #}
            <a href="/" class="navbar-logo">
                <i class="fas fa-tools"></i> Nawa Nirman
            </a>
            
            {# Mobile menu toggle button #}
            <div class="hamburger" id="hamburger">
                <span></span>
                <span></span>
                <span></span>
            </div>
            
            {# Navigation links #}
            <ul class="nav-menu" id="nav-menu">
                <li class="nav-item">
                    <a href="/" class="nav-link">Home</a>
                </li>
                <li class="nav-item">
                    <a href="/categories" class="nav-link">Categories</a>
                </li>
                <li class="nav-item">
                    <a href="/about" class="nav-link">About</a>
                </li>
                <li class="nav-item">
                    <a href="/contact" class="nav-link">Contact</a>
                </li>
                
                {# Show different links based on login status #}
                {% if user %}
                    {# User IS logged in #}
                    <li class="nav-item">
                        <a href="/cart" class="nav-link">Cart</a>
                    </li>
                    <li class="nav-item">
                        <a href="/profile" class="nav-link">{{ user.full_name }}</a>
                    </li>
                    <li class="nav-item">
                        <a href="/logout" class="nav-link">Logout</a>
                    </li>
                {% else %}
                    {# User is NOT logged in #}
                    <li class="nav-item">
                        <a href="/login" class="nav-link">Login</a>
                    </li>
                    <li class="nav-item">
                        <a href="/signup" class="nav-link">Sign Up</a>
                    </li>
                {% endif %}
            </ul>
        </div>
    </nav>
    
    {# ======================================================================
       MAIN CONTENT - This changes on each page
       ====================================================================== #}
    <main>
        {% block content %}
        {# This is where each child template puts its HTML #}
        {% endblock %}
    </main>
    
    {# ======================================================================
       FOOTER - Shows on every page
       ====================================================================== #}
    <footer class="footer">
        <div class="footer-container">
            <div class="footer-section">
                <h3>About Us</h3>
                <p>Nawa Nirman Hardware - Your trusted source for quality tools.</p>
            </div>
            
            <div class="footer-section">
                <h3>Quick Links</h3>
                <ul>
                    <li><a href="/about">About</a></li>
                    <li><a href="/categories">Categories</a></li>
                    <li><a href="/contact">Contact</a></li>
                </ul>
            </div>
            
            <div class="footer-section">
                <h3>Contact Info</h3>
                <p>Email: info@navanirman.com</p>
                <p>Phone: +1-555-0123</p>
            </div>
        </div>
        
        <div class="footer-bottom">
            <p>&copy; 2024 Nawa Nirman Hardware. All rights reserved.</p>
        </div>
    </footer>
    
    {# ======================================================================
       SCRIPTS - JavaScript files
       ====================================================================== #}
    <script src="{{ url_for('static', path='/script.js') }}"></script>
    
    {# Allow child templates to add extra scripts #}
    {% block extra_js %}{% endblock %}
</body>
</html>
```

**Key template concepts:**

1. **`{% %}` = Control flow** - if statements, loops
2. **`{{ }}` = Output variable** - Show data on page
3. **`{# #}` = Comment** - Notes (not shown on page)
4. **`{% block %}` = Placeholder** - Child templates fill this
5. **`{% if user %}` = Conditional** - Show different content based on condition
6. **`url_for()` = Generate URL** - Makes links to static files

---

## Step 4.2: `index.html` - Homepage

**File: `backend/app/templates/index.html`**

```html
{# EXTEND base.html means this page inherits navbar, footer, everything #}
{% extends "base.html" %}

{# Change the title on this page #}
{% block title %}Home - Nawa Nirman Hardware{% endblock %}

{# Main content for this page #}
{% block content %}

{# ======================================================================
   HERO SECTION - Big banner at top
   ====================================================================== #}
<section class="hero">
    <div class="hero-content">
        <h1>Welcome to Nawa Nirman Hardware</h1>
        <p>Your one-stop shop for quality tools and hardware supplies</p>
        <a href="/categories" class="cta-button">Shop Now</a>
    </div>
</section>

{# ======================================================================
   FEATURED PRODUCTS SECTION
   ====================================================================== #}
<section class="featured-products">
    <div class="container">
        <h2>Featured Products</h2>
        
        {# Loop through each product #}
        <div class="products-grid">
            {% for product in products %}
                <div class="product-card">
                    {# Show product image #}
                    <img src="{{ product.image_url }}" alt="{{ product.name }}">
                    
                    {# Show product name #}
                    <h3>{{ product.name }}</h3>
                    
                    {# Show product price #}
                    <p class="price">Rs. {{ product.price }}</p>
                    
                    {# Show product description #}
                    <p class="description">{{ product.description[:50] }}...</p>
                    
                    {# Links to view and add to cart #}
                    <a href="/product/{{ product.id }}" class="btn-primary">View Details</a>
                    <button class="btn-secondary" onclick="addToCart({{ product.id }}, 1)">Add to Cart</button>
                </div>
            {% endfor %}
        </div>
    </div>
</section>

{# ======================================================================
   CATEGORIES SECTION
   ====================================================================== #}
<section class="categories">
    <div class="container">
        <h2>Shop by Category</h2>
        
        <div class="categories-grid">
            {% for category in categories %}
                <div class="category-card">
                    <h3>{{ category.name }}</h3>
                    <p>{{ category.description }}</p>
                    <a href="/categories">Explore</a>
                </div>
            {% endfor %}
        </div>
    </div>
</section>

{% endblock %}
```

**Template Syntax Explained:**

- `{% for product in products %}` = Loop through each product
- `{{ product.name }}` = Show the product name
- `{{ product.price }}` = Show the price
- `{{ product.id }}` = Show the product ID (needed for linking)
- `product.description[:50]` = Show first 50 characters

---

## Step 4.3: `product.html` - Single Product Page

**File: `backend/app/templates/product.html`**

```html
{% extends "base.html" %}

{% block title %}{{ product.name }} - Nawa Nirman Hardware{% endblock %}

{% block content %}

<section class="product-detail">
    <div class="container">
        <div class="product-row">
            {# LEFT: Product image #}
            <div class="product-image">
                <img src="{{ product.image_url }}" alt="{{ product.name }}">
            </div>
            
            {# RIGHT: Product information #}
            <div class="product-info">
                <h1>{{ product.name }}</h1>
                
                {# Price #}
                <div class="price-section">
                    <span class="price">Rs. {{ product.price }}</span>
                    
                    {# Show if in stock #}
                    {% if product.stock > 0 %}
                        <span class="in-stock">In Stock ({{ product.stock }} available)</span>
                    {% else %}
                        <span class="out-of-stock">Out of Stock</span>
                    {% endif %}
                </div>
                
                {# Description #}
                <div class="description-section">
                    <h3>Description</h3>
                    <p>{{ product.description }}</p>
                </div>
                
                {# Add to cart section #}
                <div class="add-to-cart-section">
                    <label for="quantity">Quantity:</label>
                    <input type="number" id="quantity" value="1" min="1" max="{{ product.stock }}">
                    
                    {% if product.stock > 0 %}
                        <button onclick="addToCart({{ product.id }}, document.getElementById('quantity').value)" 
                                class="btn-primary btn-large">
                            Add to Cart
                        </button>
                    {% else %}
                        <button disabled class="btn-disabled">
                            Out of Stock
                        </button>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</section>

{% endblock %}
```

---

## Step 4.4: `cart.html` - Shopping Cart

**File: `backend/app/templates/cart.html`**

```html
{% extends "base.html" %}

{% block title %}Shopping Cart - Nawa Nirman Hardware{% endblock %}

{% block content %}

<section class="cart-section">
    <div class="container">
        <h1>Shopping Cart</h1>
        
        {% if cart_items %}
            {# Cart has items #}
            <table class="cart-table">
                <thead>
                    <tr>
                        <th>Product</th>
                        <th>Price</th>
                        <th>Quantity</th>
                        <th>Total</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in cart_items %}
                        <tr>
                            <td>{{ item.product.name }}</td>
                            <td>Rs. {{ item.product.price }}</td>
                            <td>{{ item.quantity }}</td>
                            <td>Rs. {{ item.product.price * item.quantity }}</td>
                            <td>
                                <button onclick="removeFromCart({{ item.product.id }})">Remove</button>
                            </td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
            
            {# Cart summary #}
            <div class="cart-summary">
                <h2>Cart Total: Rs. {{ total }}</h2>
                
                {% if user %}
                    <a href="/checkout" class="btn-primary btn-large">Proceed to Checkout</a>
                {% else %}
                    <p>Please <a href="/login">login</a> to checkout</p>
                {% endif %}
            </div>
        {% else %}
            {# Cart is empty #}
            <p class="empty-cart">Your cart is empty</p>
            <a href="/" class="btn-primary">Continue Shopping</a>
        {% endif %}
    </div>
</section>

{% endblock %}
```

---

## Step 4.5: `checkout.html` - Checkout Page

**File: `backend/app/templates/checkout.html`**

```html
{% extends "base.html" %}

{% block title %}Checkout - Nawa Nirman Hardware{% endblock %}

{% block content %}

<section class="checkout-section">
    <div class="container">
        <h1>Checkout</h1>
        
        {# Order summary #}
        <div class="checkout-summary">
            <h2>Order Summary</h2>
            <table>
                {% for item in cart_items %}
                    <tr>
                        <td>{{ item.product.name }} x {{ item.quantity }}</td>
                        <td>Rs. {{ item.product.price * item.quantity }}</td>
                    </tr>
                {% endfor %}
                <tr class="total">
                    <td>Total:</td>
                    <td>Rs. {{ total }}</td>
                </tr>
            </table>
        </div>
        
        {# Checkout form #}
        <form method="POST" class="checkout-form">
            <h2>Shipping Information</h2>
            
            <label>
                Full Name:
                <input type="text" name="full_name" value="{{ user.full_name }}" required>
            </label>
            
            <label>
                Phone:
                <input type="tel" name="phone" value="{{ user.phone }}" required>
            </label>
            
            <label>
                Shipping Address:
                <textarea name="shipping_address" required>{{ user.address }}</textarea>
            </label>
            
            <h2>Payment Method</h2>
            <label>
                <input type="radio" name="payment_method" value="Cash on delivery" checked>
                Cash on Delivery
            </label>
            <label>
                <input type="radio" name="payment_method" value="Online">
                Online Payment
            </label>
            
            <button type="submit" class="btn-primary btn-large">Place Order</button>
        </form>
    </div>
</section>

{% endblock %}
```

---

## Step 4.6: `login.html` & `signup.html`

**File: `backend/app/templates/login.html`**

```html
{% extends "base.html" %}

{% block title %}Login - Nawa Nirman Hardware{% endblock %}

{% block content %}

<section class="auth-section">
    <div class="auth-container">
        <h1>Login</h1>
        
        {% if error %}
            <div class="error-message">{{ error }}</div>
        {% endif %}
        
        <form method="POST" class="auth-form">
            <label>
                Email:
                <input type="email" name="email" required>
            </label>
            
            <label>
                Password:
                <input type="password" name="password" required>
            </label>
            
            <button type="submit" class="btn-primary">Login</button>
        </form>
        
        <p>Don't have an account? <a href="/signup">Sign up here</a></p>
    </div>
</section>

{% endblock %}
```

**File: `backend/app/templates/signup.html`**

```html
{% extends "base.html" %}

{% block title %}Sign Up - Nawa Nirman Hardware{% endblock %}

{% block content %}

<section class="auth-section">
    <div class="auth-container">
        <h1>Create Account</h1>
        
        {% if error %}
            <div class="error-message">{{ error }}</div>
        {% endif %}
        
        <form method="POST" class="auth-form">
            <label>
                Full Name:
                <input type="text" name="full_name" required>
            </label>
            
            <label>
                Email:
                <input type="email" name="email" required>
            </label>
            
            <label>
                Password:
                <input type="password" name="password" required>
                <small>Must be 8+ chars with numbers and special characters</small>
            </label>
            
            <label>
                Confirm Password:
                <input type="password" name="confirm_password" required>
            </label>
            
            <button type="submit" class="btn-primary">Sign Up</button>
        </form>
        
        <p>Already have an account? <a href="/login">Login here</a></p>
    </div>
</section>

{% endblock %}
```

---

# <a id="phase-5"></a>🎨 PHASE 5: FRONTEND STYLING (CSS)

**File: `backend/app/static/styles.css`**

CSS is like makeup for HTML - it makes everything look beautiful!

```css
/* ========================================================================
   GLOBAL STYLES - Applies to whole website
   ======================================================================== */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    /* box-sizing: border-box means padding doesn't add to width
       Normal: width + padding = total width
       border-box: width INCLUDES padding */
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    /* Font stack: Try first font, if not available try next, etc. */
    
    line-height: 1.6;
    /* Space between lines - makes text easier to read */
    
    color: #333;
    /* Text color: dark gray */
    
    background-color: #f4f4f4;
    /* Page background */
}

/* ========================================================================
   CONTAINER - Used throughout for centering content
   ======================================================================== */

.container {
    max-width: 1200px;
    /* Content never wider than 1200px */
    
    margin: 0 auto;
    /* Center the container */
    
    padding: 0 20px;
    /* Space on sides */
}

/* ========================================================================
   NAVIGATION BAR
   ======================================================================== */

.navbar {
    background-color: #2c3e50;
    /* Dark blue-gray background */
    
    padding: 1rem 0;
    /* 1rem = 16px usually */
    
    position: sticky;
    /* Stays at top when scrolling */
    
    top: 0;
    z-index: 100;
    /* 100 = always on top */
}

.navbar-container {
    display: flex;
    /* Flexbox = easy alignment */
    
    justify-content: space-between;
    /* Space items apart */
    
    align-items: center;
    /* Vertically center */
    
    max-width: 1200px;
    margin: 0 auto;
}

.navbar-logo {
    color: white;
    font-size: 1.5rem;
    font-weight: bold;
    text-decoration: none;
}

.nav-menu {
    display: flex;
    list-style: none;
    /* Remove bullet points */
}

.nav-item {
    margin-left: 2rem;
    /* Space between menu items */
}

.nav-link {
    color: white;
    text-decoration: none;
    transition: color 0.3s;
    /* Smooth color change over 0.3 seconds */
}

.nav-link:hover {
    /* When mouse hovers over link */
    color: #3498db;
    /* Light blue */
}

/* ========================================================================
   HAMBURGER MENU (Mobile)
   ======================================================================== */

.hamburger {
    display: none;
    /* Hidden on desktop */
    
    flex-direction: column;
    cursor: pointer;
    /* Show pointer icon */
}

.hamburger span {
    width: 25px;
    height: 3px;
    background-color: white;
    margin: 5px 0;
    transition: 0.3s;
}

/* When hamburger is active (mobile menu open) */
.hamburger.active span:nth-child(1) {
    transform: rotate(45deg) translate(10px, 10px);
    /* Rotate and move first line */
}

.hamburger.active span:nth-child(2) {
    opacity: 0;
    /* Hide middle line */
}

.hamburger.active span:nth-child(3) {
    transform: rotate(-45deg) translate(7px, -7px);
    /* Rotate bottom line opposite direction */
}

/* ========================================================================
   RESPONSIVE: Mobile phones (less than 768px wide)
   ======================================================================== */

@media screen and (max-width: 768px) {
    /* Show hamburger on mobile */
    .hamburger {
        display: flex;
    }
    
    /* Hide menu by default on mobile */
    .nav-menu {
        position: fixed;
        left: -100%;
        /* Off-screen */
        
        top: 70px;
        flex-direction: column;
        background-color: #2c3e50;
        width: 100%;
        text-align: center;
        transition: 0.3s;
        /* Smooth slide in/out */
    }
    
    /* When menu is active */
    .nav-menu.active {
        left: 0;
        /* Slide in */
    }
    
    .nav-item {
        margin: 1rem 0;
    }
}

/* ========================================================================
   HERO SECTION - Big banner
   ======================================================================== */

.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    /* Diagonal gradient: purple to pink */
    
    color: white;
    padding: 150px 20px;
    /* Big top/bottom padding for space */
    
    text-align: center;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

.cta-button {
    /* CTA = Call To Action */
    background-color: #3498db;
    color: white;
    padding: 12px 30px;
    text-decoration: none;
    border-radius: 5px;
    /* Rounded corners */
    
    font-weight: bold;
    display: inline-block;
    /* So padding works */
    
    transition: background-color 0.3s;
}

.cta-button:hover {
    background-color: #2980b9;
    /* Darker blue on hover */
}

/* ========================================================================
   PRODUCTS GRID
   ======================================================================== */

.products-grid {
    display: grid;
    /* CSS Grid = awesome for layouts */
    
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    /* On desktop: 4-5 products per row
       On tablet: 2-3 products per row
       On mobile: 1 product per row
       auto-fit = automatically adjust number of columns
       minmax(250px, 1fr) = min 250px wide, flexible up to 1 fraction of space */
    
    gap: 2rem;
    /* Space between products */
    
    margin: 2rem 0;
}

.product-card {
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    /* Subtle shadow = depth effect */
    
    transition: transform 0.3s, box-shadow 0.3s;
}

.product-card:hover {
    transform: translateY(-5px);
    /* Lift up slightly on hover */
    
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    /* Bigger shadow when lifted */
}

.product-card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    /* Cover the space, crop if needed */
}

.product-card h3 {
    padding: 1rem;
    font-size: 1.1rem;
}

.product-card .price {
    padding: 0 1rem;
    font-size: 1.3rem;
    color: #e74c3c;
    /* Red color */
    
    font-weight: bold;
}

.product-card .description {
    padding: 0 1rem;
    color: #666;
    font-size: 0.9rem;
}

.product-card .btn-primary,
.product-card .btn-secondary {
    margin: 1rem;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: 0.3s;
}

.btn-primary {
    background-color: #3498db;
    color: white;
    text-decoration: none;
    display: inline-block;
}

.btn-primary:hover {
    background-color: #2980b9;
}

.btn-secondary {
    background-color: #27ae60;
    /* Green */
    
    color: white;
}

.btn-secondary:hover {
    background-color: #229954;
    /* Darker green */
}

/* ========================================================================
   FEATURED PRODUCTS SECTION
   ======================================================================== */

.featured-products {
    background-color: white;
    padding: 3rem 0;
    /* Top/bottom padding */
}

.featured-products h2 {
    text-align: center;
    font-size: 2rem;
    margin-bottom: 2rem;
    color: #2c3e50;
}

/* ========================================================================
   CATEGORIES SECTION
   ======================================================================== */

.categories {
    background-color: #ecf0f1;
    /* Light gray */
    
    padding: 3rem 0;
}

.categories h2 {
    text-align: center;
    font-size: 2rem;
    margin-bottom: 2rem;
    color: #2c3e50;
}

.categories-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
}

.category-card {
    background-color: white;
    padding: 2rem;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.category-card h3 {
    margin-bottom: 1rem;
    color: #2c3e50;
}

.category-card a {
    color: #3498db;
    text-decoration: none;
    font-weight: bold;
}

/* ========================================================================
   FOOTER
   ======================================================================== */

.footer {
    background-color: #2c3e50;
    color: white;
    padding: 3rem 0 1rem;
    margin-top: 3rem;
}

.footer-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

.footer-section h3 {
    margin-bottom: 1rem;
}

.footer-section a {
    color: #ecf0f1;
    text-decoration: none;
}

.footer-section a:hover {
    color: #3498db;
}

.footer-bottom {
    text-align: center;
    padding: 2rem;
    border-top: 1px solid #34495e;
    margin-top: 2rem;
}

/* ========================================================================
   FORMS
   ======================================================================== */

.auth-section {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 80vh;
    /* Vertical centering */
}

.auth-container {
    background-color: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    width: 100%;
    max-width: 400px;
}

.auth-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

label {
    display: flex;
    flex-direction: column;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

input[type="text"],
input[type="email"],
input[type="password"],
textarea {
    padding: 10px;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    font-size: 1rem;
}

input[type="text"]:focus,
input[type="email"]:focus,
input[type="password"]:focus,
textarea:focus {
    outline: none;
    border-color: #3498db;
    box-shadow: 0 0 5px rgba(52, 152, 219, 0.5);
}

button {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    font-weight: bold;
}

/* ========================================================================
   CART TABLE
   ======================================================================== */

.cart-table {
    width: 100%;
    border-collapse: collapse;
    background-color: white;
    margin-bottom: 2rem;
}

.cart-table th,
.cart-table td {
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid #ecf0f1;
}

.cart-table th {
    background-color: #2c3e50;
    color: white;
}

.cart-table tr:hover {
    background-color: #f9f9f9;
}
```

---

# <a id="phase-6"></a>⚡ PHASE 6: FRONTEND INTERACTIVITY (JavaScript)

**File: `backend/app/static/script.js`**

JavaScript makes the website interactive - buttons that work, responsive menus, etc.

```javascript
// ========================================================================
// MOBILE MENU TOGGLE
// ========================================================================

/*
 * When user clicks hamburger menu on mobile:
 * 1. Show/hide the navigation menu
 * 2. Animate hamburger icon (lines rotate into X)
 */

// Get the hamburger button and menu
const hamburger = document.getElementById('hamburger');
// ^ Finds HTML element with id="hamburger"

const navMenu = document.getElementById('nav-menu');
// ^ Finds HTML element with id="nav-menu"

// When hamburger is clicked
hamburger.addEventListener('click', function() {
    // addEventListener = "Listen for click events on this element"
    // function() { } = "When clicked, run this code"
    
    // Toggle (add if not there, remove if there) the 'active' class
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
    // CSS says when .active, show menu and rotate hamburger
});

// Close menu when link is clicked
navMenu.addEventListener('click', function(e) {
    // If clicked element is a link
    if (e.target.tagName === 'A') {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    }
});


// ========================================================================
// ADD TO CART
// ========================================================================

function addToCart(productId, quantity) {
    /*
     * Send product to cart
     * productId = which product (e.g., 5)
     * quantity = how many (e.g., 2)
     */
    
    // Create FormData (like a form submission)
    const formData = new FormData();
    formData.append('product_id', productId);
    formData.append('quantity', quantity);
    
    // Send to server
    fetch('/api/cart/add', {
        method: 'POST',  // Type of request
        body: formData   // Data to send
    })
    .then(response => response.json())
    // ^ Convert server response to JSON
    
    .then(data => {
        // Show success message
        alert('Added to cart!');
    })
    
    .catch(error => {
        console.error('Error:', error);
        alert('Error adding to cart');
    });
}


// ========================================================================
// REMOVE FROM CART
// ========================================================================

function removeFromCart(productId) {
    /*
     * Remove product from cart
     */
    
    const formData = new FormData();
    formData.append('product_id', productId);
    
    fetch('/api/cart/remove', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert('Removed from cart!');
        // Reload page to show updated cart
        location.reload();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error removing from cart');
    });
}


// ========================================================================
// FORM VALIDATION
// ========================================================================

// Validate signup form before submitting
function validateSignupForm() {
    const password = document.querySelector('input[name="password"]').value;
    const confirmPassword = document.querySelector('input[name="confirm_password"]').value;
    
    // Check if passwords match
    if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return false;
    }
    
    // Check if password is strong
    if (password.length < 8) {
        alert('Password must be at least 8 characters');
        return false;
    }
    
    // Has number?
    if (!/\d/.test(password)) {
        alert('Password must contain at least one number');
        return false;
    }
    
    // Has special character?
    if (!/[^A-Za-z0-9]/.test(password)) {
        alert('Password must contain at least one special character (!@#$%)');
        return false;
    }
    
    return true;
}
```

---

# 🎉 CONGRATULATIONS!

You've just learned how to build a complete e-commerce website!

## Summary:

### Frontend (What customers see):
- **HTML** (`base.html`, `index.html`, etc.) = Structure (skeleton)
- **CSS** (`styles.css`) = Styling (makeup)
- **JavaScript** (`script.js`) = Interactivity (nervous system)

### Backend (The engine):
- **FastAPI** (`main.py`) = Handles requests, manages logic
- **SQLModel/Database** (`models.py`, `database.py`) = Stores data
- **CRUD operations** (`crud.py`) = Manipulates data

### Flow:
```
Customer clicks "Add to Cart"
    ↓
JavaScript sends request
    ↓
FastAPI receives at /api/cart/add
    ↓
Database is updated
    ↓
JavaScript shows confirmation
```

This is how EVERY website works! 🚀

---

## Next Steps:

1. **Deploy** - Put online (Heroku, Vercel, AWS)
2. **Add features** - Reviews, wishlist, search
3. **Improve design** - Better CSS, animations
4. **Payment integration** - Stripe, Razorpay
5. **Admin panel** - Manage products, orders

**You now understand the complete architecture of a professional e-commerce website!**

