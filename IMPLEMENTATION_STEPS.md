# 🛠️ HANDS-ON IMPLEMENTATION GUIDE
## Build NavaNirman Step-by-Step

This guide takes you through EXACTLY what to type, in what order, with complete explanations.

---

# STEP 0: Pre-requisites

Make sure you have:
- Python 3.8+ installed (`python3 --version`)
- pip installed (`pip --version`)
- A text editor or VS Code
- Terminal access

---

# STEP 1: Create Project from Scratch

## 1.1 Create Main Directory

```bash
# Create the main project folder
mkdir NavaNirman
cd NavaNirman

# Initialize Git (version control)
git init

# Create a README to explain project
echo "# NavaNirman Hardware E-commerce Store" > README.md
```

**What we're doing:**
- `mkdir` = Make directory (folder)
- `cd` = Change directory (enter folder)
- `git init` = Initialize Git to track changes
- `echo` = Create a README file

---

## 1.2 Create Virtual Environment

```bash
# Create isolated Python workspace
python3 -m venv .venv

# Activate it (enter the workspace)
source .venv/bin/activate  # On Mac/Linux
# OR on Windows:
# .venv\Scripts\activate

# You should see: (.venv) $ in terminal now
```

**What this does:**
- Creates a `.venv` folder with isolated Python
- `source` = Load the activation script
- Now any `pip install` only affects THIS project

---

## 1.3 Create .gitignore

Create file: `.gitignore`

```
# Ignore virtual environment
.venv/
venv/
ENV/

# Python cache
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/

# Environment variables
.env

# Database
*.db
*.sqlite

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

**Why?**
- Tells Git what NOT to track
- .venv is huge and changes often - no need to track
- .env has passwords - definitely keep secret!
- We'll recreate `__pycache__` automatically

---

## 1.4 Create Backend Directory Structure

```bash
# Create backend folder with subfolders
mkdir -p backend/app/static/images
mkdir -p backend/app/templates

# Create __init__.py files (marks as Python packages)
touch backend/__init__.py
touch backend/app/__init__.py

# Create main Python files (we'll fill these in next)
touch backend/app/main.py
touch backend/app/models.py
touch backend/app/database.py
touch backend/app/crud.py

# Create static files
touch backend/app/static/styles.css
touch backend/app/static/script.js

# Create config files
touch backend/requirements.txt
touch backend/Dockerfile
touch backend/Procfile
```

**Directory structure now:**
```
NavaNirman/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   ├── crud.py
│   │   ├── static/
│   │   │   ├── styles.css
│   │   │   ├── script.js
│   │   │   └── images/
│   │   └── templates/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── Procfile
├── .venv/ (hidden)
├── .gitignore
└── README.md
```

---

## 1.5 Create requirements.txt

**File: `backend/requirements.txt`**

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
jinja2==3.1.2
sqlmodel==0.0.14
python-dotenv==1.0.0
itsdangerous==2.1.2
passlib[bcrypt]==1.7.4
sqlalchemy==2.0.23
```

**What each does:**
- `fastapi` = Web framework
- `uvicorn` = Server
- `jinja2` = Template engine
- `sqlmodel` = Database ORM
- `python-dotenv` = Read .env files
- `itsdangerous` = Secure tokens
- `passlib` = Password hashing
- `sqlalchemy` = Database toolkit

**Version numbers:**
- `==` = Exact version
- Using specific versions = reproducible (same code for everyone)

---

## 1.6 Install Dependencies

```bash
# Install all packages from requirements.txt
pip install -r backend/requirements.txt

# Wait... this installs everything into your .venv
# You should see lots of "Successfully installed" messages

# Verify installation
pip list
# Should show all installed packages
```

**What's happening:**
- `pip install -r` = Install all packages listed in file
- `-r` = read from file
- All packages go into `.venv` (isolated)
- Other projects won't be affected

---

## 1.7 Create .env File

**File: `.env`**

```
# Secret key for sessions (keep this SECRET in production!)
SESSION_SECRET=your-super-secret-key-change-me-in-production

# Database URL
DATABASE_URL=sqlite:///./nawa_nirman.db

# Email settings (for future use)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
```

**WHY separate .env file?**
- Passwords should NEVER be in code
- Different servers have different passwords
- .gitignore prevents accidental upload

---

# STEP 2: Database Layer

## 2.1 Create models.py

**File: `backend/app/models.py`**

```python
"""
DATABASE MODELS - Defines what data we store and its structure
Each class = one database table
"""

from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


# ============================================================================
# 1. CATEGORY TABLE - Product categories
# ============================================================================

class CategoryBase(SQLModel):
    """Shared category fields"""
    name: str = Field(index=True)
    description: Optional[str] = None


class Category(CategoryBase, table=True):
    """Actual Category table in database"""
    id: Optional[int] = Field(default=None, primary_key=True)
    # Relationships
    products: List["Product"] = Relationship(back_populates="category")


# ============================================================================
# 2. PRODUCT TABLE
# ============================================================================

class ProductBase(SQLModel):
    """Product fields"""
    name: str = Field(index=True)
    description: str
    price: float = Field(gt=0)  # Must be greater than 0
    category_id: int = Field(foreign_key="category.id")
    image_url: Optional[str] = None
    stock: int = Field(default=0, ge=0)  # Greater or equal to 0


class Product(ProductBase, table=True):
    """Actual Product table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    # Relationships
    category: Optional[Category] = Relationship(back_populates="products")
    cart_items: List["CartItem"] = Relationship(back_populates="product")
    order_items: List["OrderItem"] = Relationship(back_populates="product")


# ============================================================================
# 3. USER TABLE
# ============================================================================

class UserBase(SQLModel):
    """User fields"""
    email: str = Field(unique=True, index=True)
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None


class User(UserBase, table=True):
    """Actual User table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str
    # Relationships
    cart_items: List["CartItem"] = Relationship(back_populates="user")
    orders: List["Order"] = Relationship(back_populates="user")
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# 4. CART ITEM TABLE
# ============================================================================

class CartItemBase(SQLModel):
    """Cart item fields"""
    user_id: int = Field(foreign_key="user.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int = Field(gt=0)


class CartItem(CartItemBase, table=True):
    """Actual CartItem table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    # Relationships
    user: Optional[User] = Relationship(back_populates="cart_items")
    product: Optional[Product] = Relationship(back_populates="cart_items")
    added_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# 5. ORDER TABLE
# ============================================================================

class OrderBase(SQLModel):
    """Order fields"""
    user_id: int = Field(foreign_key="user.id")
    total: float
    payment_method: str = "Cash on delivery"
    shipping_address: str
    phone: str
    receipt_method: str = "email"


class Order(OrderBase, table=True):
    """Actual Order table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    status: str = "pending"
    # Relationships
    user: Optional[User] = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# 6. ORDER ITEM TABLE - Individual items in an order
# ============================================================================

class OrderItemBase(SQLModel):
    """Order item fields"""
    order_id: int = Field(foreign_key="order.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int = Field(gt=0)
    price: float  # Price at time of purchase


class OrderItem(OrderItemBase, table=True):
    """Actual OrderItem table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    # Relationships
    order: Optional[Order] = Relationship(back_populates="items")
    product: Optional[Product] = Relationship(back_populates="order_items")


# ============================================================================
# 7. CONTACT TABLE - Contact form submissions
# ============================================================================

class ContactBase(SQLModel):
    """Contact fields"""
    name: str
    email: str = Field(index=True)
    message: str = Field(min_length=10)


class Contact(ContactBase, table=True):
    """Actual Contact table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Key concepts:**

1. **`SQLModel`** - Base class for database models
2. **`Field()`** - Describe column properties
   - `primary_key=True` = Unique identifier
   - `foreign_key="table.id"` = Link to other table
   - `unique=True` = No duplicates
   - `index=True` = Make searches fast
   - `gt=0` = Greater than 0 (validation)
3. **`Relationship()`** - Link tables together
4. **`table=True`** = Create actual database table

---

## 2.2 Create database.py

**File: `backend/app/database.py`**

```python
"""
DATABASE CONNECTION - Sets up SQLite database
"""

import os
from sqlmodel import create_engine, SQLModel
from sqlalchemy.pool import StaticPool

# Get database URL from environment or use default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./nawa_nirman.db")

# Create database engine
if DATABASE_URL.startswith("sqlite"):
    # SQLite settings
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # Allow multiple connections
        poolclass=StaticPool,  # Keep connections open
        echo=False  # Set to True to see SQL in console
    )
else:
    # Other databases (PostgreSQL, MySQL, etc.)
    engine = create_engine(DATABASE_URL, echo=False)


def init_db():
    """Create all database tables"""
    SQLModel.metadata.create_all(engine)
```

**Explanation:**

- **`create_engine()`** - Opens connection to database
- **`sqlite:///./nawa_nirman.db`** - Creates/uses local SQLite file
- **`connect_args={"check_same_thread": False}`** - Allow web server to use multiple threads
- **`StaticPool`** - Keep SQLite connections alive
- **`echo=False`** - Don't print SQL queries (set True for debugging)

---

# STEP 3: CRUD Operations

## 3.1 Create crud.py (Part 1 - User Operations)

**File: `backend/app/crud.py`** (This is LARGE - we'll break it into parts)

```python
"""
CRUD OPERATIONS - All database interactions
C = Create, R = Read, U = Update, D = Delete
"""

from datetime import datetime
from typing import Optional, List
from sqlmodel import Session, select
from passlib.context import CryptContext

from .models import (
    User, Product, Category, CartItem, Order, OrderItem, Contact
)

# ============================================================================
# PASSWORD HASHING
# ============================================================================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Convert plain password to secure hash"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if plain password matches hash"""
    return pwd_context.verify(plain_password, hashed_password)


# ============================================================================
# USER OPERATIONS
# ============================================================================

def create_user(session: Session, email: str, full_name: str, password: str,
                phone: Optional[str] = None, address: Optional[str] = None) -> User:
    """
    Create new user account
    
    Args:
        session: Database session
        email: User email (unique)
        full_name: User's name
        password: Plain password (will be hashed)
        phone: Phone number (optional)
        address: Address (optional)
    
    Returns:
        Created User object
    
    Raises:
        ValueError: If email already exists
    """
    # Check if email exists
    existing = get_user_by_email(session, email)
    if existing:
        raise ValueError(f"Email {email} already registered")
    
    # Hash password
    hashed = hash_password(password)
    
    # Create user
    user = User(
        email=email,
        full_name=full_name,
        password_hash=hashed,
        phone=phone,
        address=address
    )
    
    # Save to database
    session.add(user)
    session.commit()
    session.refresh(user)  # Reload to get ID
    
    return user


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """Find user by email"""
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
    """Find user by ID"""
    return session.get(User, user_id)


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """
    Verify email and password
    
    Returns:
        User if authenticated, None if not
    """
    user = get_user_by_email(session, email)
    if not user:
        return None
    
    if not verify_password(password, user.password_hash):
        return None
    
    return user


def update_user_profile(session: Session, user_id: int,
                       full_name: Optional[str] = None,
                       phone: Optional[str] = None,
                       address: Optional[str] = None) -> User:
    """Update user profile"""
    user = session.get(User, user_id)
    if not user:
        raise ValueError(f"User {user_id} not found")
    
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
    """Get all categories"""
    statement = select(Category)
    return session.exec(statement).all()


def get_category_by_id(session: Session, category_id: int) -> Optional[Category]:
    """Get specific category"""
    return session.get(Category, category_id)


def create_category(session: Session, name: str, description: Optional[str] = None) -> Category:
    """Create new category"""
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
    Get all products, optionally filtered by category
    
    Example:
        get_products(session) # All products
        get_products(session, category_id=2) # Only category 2
    """
    statement = select(Product)
    if category_id:
        statement = statement.where(Product.category_id == category_id)
    return session.exec(statement).all()


def get_product_by_id(session: Session, product_id: int) -> Optional[Product]:
    """Get specific product"""
    return session.get(Product, product_id)


def create_product(session: Session, name: str, description: str, price: float,
                  category_id: int, image_url: Optional[str] = None,
                  stock: int = 0) -> Product:
    """Create new product"""
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
    """Add item to cart or update quantity if exists"""
    
    # Check if already in cart
    statement = select(CartItem).where(
        (CartItem.user_id == user_id) & (CartItem.product_id == product_id)
    )
    existing = session.exec(statement).first()
    
    if existing:
        # Update quantity
        existing.quantity = quantity
        item = existing
    else:
        # Create new
        item = CartItem(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )
    
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def get_cart_items(session: Session, user_id: int) -> List[CartItem]:
    """Get all cart items for user"""
    statement = select(CartItem).where(CartItem.user_id == user_id)
    return session.exec(statement).all()


def remove_cart_item(session: Session, user_id: int, product_id: int) -> bool:
    """Remove item from cart"""
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
    """Remove all items from cart"""
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
    Create order from cart
    
    Process:
    1. Create Order record
    2. Create OrderItem for each cart item
    3. Clear cart
    4. Return order
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
    session.flush()  # Save but don't commit (need order ID)
    
    # Create order items
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
    """Get order by ID"""
    return session.get(Order, order_id)


def get_user_orders(session: Session, user_id: int) -> List[Order]:
    """Get all orders by user"""
    statement = select(Order).where(Order.user_id == user_id)
    return session.exec(statement).all()


# ============================================================================
# CONTACT OPERATIONS
# ============================================================================

def create_contact(session: Session, name: str, email: str, message: str) -> Contact:
    """Save contact form submission"""
    contact = Contact(name=name, email=email, message=message)
    session.add(contact)
    session.commit()
    session.refresh(contact)
    return contact


# ============================================================================
# SESSION CART (for non-logged-in users)
# ============================================================================

def get_cart_items_from_session(session_data: dict) -> dict:
    """Get cart from session cookies"""
    return session_data.get("cart", {})


def merge_session_cart(session: Session, user_id: int, session_cart: dict) -> None:
    """Merge temporary session cart into database cart when user logs in"""
    for product_id_str, quantity in session_cart.items():
        product_id = int(product_id_str)
        add_or_update_cart_item(session, user_id, product_id, quantity)


# ============================================================================
# SEED DATABASE
# ============================================================================

def seed_database(session: Session):
    """Populate database with demo data"""
    
    # Check if already seeded
    existing = session.exec(select(Category)).first()
    if existing:
        return  # Already has data
    
    # Create categories
    drills = create_category(session, "Drills", "Power drills and drilling tools")
    hammers = create_category(session, "Hammers", "Various types of hammers")
    safety = create_category(session, "Safety Gear", "Protective equipment")
    
    # Create products
    create_product(
        session,
        name="Cordless Drill Kit",
        description="20V lithium-ion cordless drill with accessories",
        price=3499.00,
        category_id=drills.id,
        image_url="/static/images/drill.jpg",
        stock=15
    )
    
    create_product(
        session,
        name="Claw Hammer",
        description="16 oz claw hammer with comfortable grip",
        price=499.00,
        category_id=hammers.id,
        image_url="/static/images/hammer.jpg",
        stock=25
    )
    
    create_product(
        session,
        name="Safety Helmet",
        description="Hard plastic safety helmet with adjustable strap",
        price=349.00,
        category_id=safety.id,
        image_url="/static/images/helmet.jpg",
        stock=30
    )
```

**Key CRUD operations:**

- **Create** = `create_user()`, `create_product()`, etc.
- **Read** = `get_user_by_id()`, `get_products()`, etc.
- **Update** = `update_user_profile()`, `add_or_update_cart_item()`, etc.
- **Delete** = `remove_cart_item()`, `clear_cart()`, etc.

---

# STEP 4: Main Server Application

## 4.1 Create main.py (Part 1 - Setup)

**File: `backend/app/main.py`** (This is MASSIVE - break into parts)

```python
"""
MAIN APPLICATION - FastAPI server
All HTTP requests come through here
"""

import os
import re
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
# INITIALIZE APP
# ============================================================================

app = FastAPI(title="Nawa Nirman Hardware Store")

# Mount static files (CSS, JS, images)
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Add session middleware (store user in cookies)
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "change-this-secret")
)

# ============================================================================
# TEMPLATE SETUP
# ============================================================================

template_dir = os.path.join(os.path.dirname(__file__), "templates")

jinja_env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=select_autoescape(["html", "xml"]),
    cache_size=0,  # No caching during development
)

templates = Jinja2Templates(env=jinja_env)

# ============================================================================
# STARTUP EVENT
# ============================================================================

@app.on_event("startup")
def on_startup():
    """Run when server starts"""
    # Create database tables
    SQLModel.metadata.create_all(engine)
    
    # Check schema and add missing columns
    ensure_database_schema()
    
    # Populate with demo data
    with Session(engine) as session:
        seed_database(session)


def ensure_database_schema():
    """Ensure all required columns exist"""
    with engine.begin() as conn:
        def has_column(table_name: str, column_name: str) -> bool:
            result = conn.execute(text(f"PRAGMA table_info('{table_name}')")).all()
            return any(row[1] == column_name for row in result)

        # Check and add missing columns
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
    """Get logged-in user from session"""
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    
    with Session(engine) as session:
        return get_user_by_id(session, user_id)


def is_password_strong(password: str) -> bool:
    """Validate password strength"""
    return (
        len(password) >= 8
        and re.search(r"\d", password)  # Has digit
        and re.search(r"[^A-Za-z0-9]", password)  # Has special char
    )


# ============================================================================
# ROUTES
# ============================================================================

@app.get("/")
def homepage(request: Request):
    """Show homepage"""
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


@app.get("/about")
def about_page(request: Request):
    """Show about page"""
    return templates.TemplateResponse("about.html", {
        "request": request,
        "user": get_current_user(request)
    })


@app.get("/categories")
def categories_page(request: Request):
    """Show categories"""
    with Session(engine) as session:
        categories = get_categories(session)
        return templates.TemplateResponse("categories.html", {
            "request": request,
            "categories": categories,
            "user": get_current_user(request)
        })


@app.get("/product/{product_id}")
def product_page(request: Request, product_id: int):
    """Show product details"""
    with Session(engine) as session:
        product = get_product_by_id(session, product_id)
        
        if not product:
            return {"error": "Product not found"}
        
        return templates.TemplateResponse("product.html", {
            "request": request,
            "product": product,
            "user": get_current_user(request)
        })


@app.get("/cart")
def cart_page(request: Request):
    """Show shopping cart"""
    current_user = get_current_user(request)
    
    if current_user:
        with Session(engine) as session:
            cart_items = get_cart_items(session, current_user.id)
            total = sum(item.quantity * item.product.price for item in cart_items)
    else:
        cart_items = []
        total = 0
    
    return templates.TemplateResponse("cart.html", {
        "request": request,
        "cart_items": cart_items,
        "total": total,
        "user": current_user
    })


@app.post("/api/cart/add")
def add_to_cart(request: Request, product_id: int = Form(...), quantity: int = Form(...)):
    """Add item to cart"""
    with Session(engine) as session:
        product = get_product_by_id(session, product_id)
        
        if not product:
            return JSONResponse({"error": "Product not found"}, status_code=404)
        
        current_user = get_current_user(request)
        
        if current_user:
            # Add to database
            add_or_update_cart_item(session, current_user.id, product_id, quantity)
        else:
            # Add to session
            if "cart" not in request.session:
                request.session["cart"] = {}
            
            product_id_str = str(product_id)
            if product_id_str in request.session["cart"]:
                request.session["cart"][product_id_str] += quantity
            else:
                request.session["cart"][product_id_str] = quantity
        
        return JSONResponse({"message": "Added to cart"})


@app.post("/api/cart/remove")
def remove_from_cart(request: Request, product_id: int = Form(...)):
    """Remove from cart"""
    current_user = get_current_user(request)
    
    if current_user:
        with Session(engine) as session:
            remove_cart_item(session, current_user.id, product_id)
    else:
        if "cart" in request.session and str(product_id) in request.session["cart"]:
            del request.session["cart"][str(product_id)]
    
    return JSONResponse({"message": "Removed from cart"})


@app.get("/signup")
def signup_page(request: Request):
    """Show signup form"""
    return templates.TemplateResponse("signup.html", {
        "request": request,
        "user": None
    })


@app.post("/signup")
def do_signup(request: Request, email: str = Form(...), full_name: str = Form(...),
              password: str = Form(...), confirm_password: str = Form(...)):
    """Process signup"""
    # Passwords match?
    if password != confirm_password:
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error": "Passwords don't match"
        })
    
    # Password strong?
    if not is_password_strong(password):
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error": "Password must be 8+ chars with numbers and special characters"
        })
    
    try:
        with Session(engine) as session:
            # Create user
            user = create_user(session, email, full_name, password)
            
            # Log them in
            request.session["user_id"] = user.id
            
            # Merge session cart
            session_cart = get_cart_items_from_session(request.session)
            if session_cart:
                merge_session_cart(session, user.id, session_cart)
                request.session.clear()
                request.session["user_id"] = user.id
            
            return RedirectResponse(url="/", status_code=302)
    
    except ValueError as e:
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error": str(e)
        })


@app.get("/login")
def login_page(request: Request):
    """Show login form"""
    return templates.TemplateResponse("login.html", {
        "request": request,
        "user": None
    })


@app.post("/login")
def do_login(request: Request, email: str = Form(...), password: str = Form(...)):
    """Process login"""
    with Session(engine) as session:
        user = authenticate_user(session, email, password)
        
        if user:
            # Login successful
            request.session["user_id"] = user.id
            
            # Merge session cart
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


@app.get("/logout")
def logout(request: Request):
    """Logout"""
    request.session.clear()
    return RedirectResponse(url="/", status_code=302)


@app.get("/profile")
def profile_page(request: Request):
    """Show profile"""
    current_user = get_current_user(request)
    
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": current_user
    })


@app.post("/profile/update")
def update_profile(request: Request, full_name: str = Form(...),
                  phone: str = Form(...), address: str = Form(...)):
    """Update profile"""
    current_user = get_current_user(request)
    
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    
    with Session(engine) as session:
        update_user_profile(session, current_user.id, full_name, phone, address)
    
    return RedirectResponse(url="/profile", status_code=302)


@app.get("/checkout")
def checkout_page(request: Request):
    """Show checkout"""
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


@app.post("/checkout")
def process_order(request: Request, payment_method: str = Form(...),
                 shipping_address: str = Form(...), phone: str = Form(...)):
    """Process order"""
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
        
        # Send SMS notification
        send_order_confirmation_sms(order)
        
        return RedirectResponse(url=f"/order-confirmation/{order.id}", status_code=302)


@app.get("/order-confirmation/{order_id}")
def order_confirmation(request: Request, order_id: int):
    """Show order confirmation"""
    with Session(engine) as session:
        order = get_order_by_id(session, order_id)
        
        if not order:
            return {"error": "Order not found"}
        
        return templates.TemplateResponse("order_confirmation.html", {
            "request": request,
            "order": order,
            "user": get_current_user(request)
        })


@app.get("/contact")
def contact_page(request: Request):
    """Show contact page"""
    return templates.TemplateResponse("contact.html", {
        "request": request,
        "user": get_current_user(request)
    })


@app.post("/contact")
def submit_contact(request: Request, name: str = Form(...), 
                  email: str = Form(...), message: str = Form(...)):
    """Process contact form"""
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
# SMS NOTIFICATION
# ============================================================================

def send_order_confirmation_sms(order):
    """Send SMS notification"""
    if not order.phone:
        print("SMS skipped: No phone provided")
        return False
    
    message = f"Order #{order.id} confirmed! Total: Rs. {order.total}. Thank you for shopping at Nawa Nirman Hardware!"
    print(f"SMS would be sent to {order.phone}: {message}")
    return True
```

That's the complete Step-by-Step Implementation Guide! Continue with templates and CSS in the next file...

---

# STEP 5: Frontend Templates

See the COMPLETE_BUILD_GUIDE.md for all HTML templates - they're fully documented there!

---

# RUNNING YOUR APP

```bash
# From backend directory
cd backend

# Activate virtual environment
source ../.venv/bin/activate

# Run the server
uvicorn app.main:app --reload

# Visit in browser: http://localhost:8000
```

**That's it! Your website is running!** 🚀

