# 📚 QUICK REFERENCE & RUNNING GUIDE

---

# 🚀 HOW TO RUN YOUR WEBSITE RIGHT NOW

## Option 1: Run Existing Project

```bash
# Navigate to project
cd /workspaces/NavaNirman

# Activate virtual environment
source .venv/bin/activate

# Navigate to backend
cd backend

# Install dependencies (if not already done)
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Open browser and visit:
# http://localhost:8000
```

**What `--reload` does:**
- Automatically restarts server when you change code
- Perfect for development
- Don't use in production!

---

## Option 2: Build from Scratch

```bash
# Follow steps in IMPLEMENTATION_STEPS.md
# Create all files from scratch
# Then run as above
```

---

# 🧠 UNDERSTANDING THE FLOW

## Request Flow (What Happens When Customer Visits Website)

```
Customer types URL: http://localhost:8000/
                    ↓
Browser sends HTTP GET request to server
                    ↓
FastAPI receives request at app.py
                    ↓
@app.get("/") function runs
                    ↓
Function queries database for products/categories
                    ↓
Function renders index.html template with data
                    ↓
HTML response sent back to browser
                    ↓
Browser displays website
```

---

## Form Submission Flow

```
Customer fills form (name, email, password)
                    ↓
Clicks Submit button
                    ↓
Browser sends HTTP POST request with form data
                    ↓
FastAPI receives at @app.post("/signup") endpoint
                    ↓
Validate inputs (passwords match? strong?)
                    ↓
Hash password using bcrypt
                    ↓
Create user in database
                    ↓
Set session cookie (store user_id)
                    ↓
Redirect to homepage
                    ↓
Subsequent requests include user_id in cookies
```

---

## Shopping Cart Flow

```
Customer clicks "Add to Cart"
                    ↓
JavaScript calls addToCart(productId, quantity)
                    ↓
AJAX request sent to /api/cart/add
                    ↓
IF user logged in:
    - Save to database (CartItem table)
ELSE:
    - Save to session cookies (temporary)
                    ↓
Response: "Added to cart!"
                    ↓
Customer clicks "View Cart"
                    ↓
Website shows cart items (from DB or cookies)
                    ↓
Customer clicks "Checkout"
                    ↓
IF logged in: Show checkout form
ELSE: Redirect to login
                    ↓
Customer enters address, payment method
                    ↓
Clicks "Place Order"
                    ↓
create_order() function:
  - Creates Order record
  - Creates OrderItem for each cart item
  - Clears cart
  - Sends SMS notification
                    ↓
Show order confirmation page
```

---

# 💾 DATABASE STRUCTURE AT A GLANCE

```
┌─────────────────────────────────────┐
│             TABLES                  │
├─────────────────────────────────────┤
│                                     │
│  USER ──┐                           │
│  ├─ id  │                           │
│  ├─ email                           │
│  ├─ password_hash                   │
│  └─ address                         │
│         │                           │
│         ├──→ CARTITEM ──→ PRODUCT  │
│         │    ├─ user_id            │
│         │    ├─ product_id         │
│         │    └─ quantity           │
│         │                           │
│         └──→ ORDER ──→ ORDERITEM   │
│              ├─ id                  │
│              ├─ total               │
│              └─ status              │
│                                     │
│  CATEGORY ──→ PRODUCT               │
│   ├─ id       ├─ id                │
│   ├─ name     ├─ name              │
│   └─ desc     ├─ price             │
│               ├─ stock             │
│               └─ category_id       │
│                                     │
│  CONTACT                            │
│   ├─ id                             │
│   ├─ email                          │
│   └─ message                        │
└─────────────────────────────────────┘
```

---

# 🔑 KEY CONCEPTS EXPLAINED

## 1. MVC Pattern (Model-View-Controller)

```
MODEL = Database (crud.py, models.py)
        - What data do we have?
        - How is it related?

CONTROLLER = Business Logic (main.py routes)
        - What happens when user clicks?
        - Validate inputs
        - Update data
        - Decide what to show

VIEW = Frontend (templates, CSS, JS)
        - What user sees
        - HTML structure
        - Styling
        - Interactivity
```

---

## 2. REST API

```
REST = Representational State Transfer

HTTP Methods:
GET     = Read data (safe, doesn't change anything)
POST    = Create/Update data (changes something)
PUT     = Replace data
DELETE  = Remove data

Our API endpoints:
GET  /                 → Show homepage
GET  /product/5        → Show product 5
POST /login            → Process login
POST /checkout         → Process order
POST /api/cart/add     → Add to cart (AJAX)
```

---

## 3. Session vs Database

```
SESSION (Cookies)
├─ Temporary storage (on user's browser)
├─ For non-logged-in users
├─ Store: Shopping cart items
├─ Expires when browser closes
└─ Limited storage (4-8KB)

DATABASE
├─ Permanent storage (on server)
├─ For logged-in users
├─ Store: Users, products, orders, cart
├─ Persists forever
└─ Unlimited storage
```

---

## 4. Password Security

```
Plain password (NEVER store this!):
"MyPassword123!"

Hashed password (what we store):
"$2b$12$R9h/cIPz0gi.URNNX3kha2OPST9/PgBkqquzi.Ss..."

Login process:
1. User enters: "MyPassword123!"
2. We hash it
3. Compare with stored hash
4. If match → Login successful

Why?
- If someone steals database, they don't get passwords
- Even admin can't see passwords
- One-way process (can't reverse hash)
```

---

## 5. Form Validation

```
FRONTEND (JavaScript)
├─ Check password entered twice matches
├─ Check at least 8 characters
├─ Check has numbers
└─ UX improvement (instant feedback)

BACKEND (Python)
├─ Check again (never trust frontend!)
├─ Check email not already used
├─ Hash password
├─ Save to database
└─ Security (prevent hacking)
```

---

# 📝 FILE STRUCTURE EXPLAINED

```
NavaNirman/                          ← Project root
│
├── backend/                          ← Server code
│   ├── app/
│   │   ├── __init__.py              ← Makes app a Python package
│   │   ├── main.py                  ← All routes/endpoints
│   │   ├── models.py                ← Database table definitions
│   │   ├── database.py              ← Database connection
│   │   ├── crud.py                  ← Database operations
│   │   │
│   │   ├── static/                  ← Static files (not changing)
│   │   │   ├── styles.css           ← Styling
│   │   │   ├── script.js            ← JavaScript
│   │   │   └── images/              ← Product images
│   │   │
│   │   └── templates/               ← HTML templates
│   │       ├── base.html            ← Master template
│   │       ├── index.html           ← Homepage
│   │       ├── product.html         ← Product page
│   │       ├── cart.html            ← Shopping cart
│   │       ├── login.html           ← Login page
│   │       ├── signup.html          ← Signup page
│   │       ├── checkout.html        ← Checkout page
│   │       ├── profile.html         ← User profile
│   │       ├── order_confirmation.html
│   │       ├── contact.html         ← Contact page
│   │       ├── about.html           ← About page
│   │       └── categories.html      ← Categories page
│   │
│   ├── requirements.txt             ← Python packages
│   ├── Dockerfile                   ← Docker setup
│   └── Procfile                     ← Deploy instructions
│
├── .venv/                           ← Virtual environment (hidden)
├── .env                             ← Secret settings (hidden)
├── .gitignore                       ← What to ignore in Git
├── README.md                        ← Project description
├── COMPLETE_BUILD_GUIDE.md          ← Detailed explanation
└── IMPLEMENTATION_STEPS.md          ← Step-by-step code
```

---

# 🔍 DEBUGGING GUIDE

## Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Cause:** Virtual environment not activated or dependencies not installed

**Fix:**
```bash
# Activate venv
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

---

## Issue: "Port 8000 already in use"

**Cause:** Another process using port 8000

**Fix:**
```bash
# Use different port
uvicorn app.main:app --port 8001

# OR kill process using 8000
lsof -i :8000
kill -9 <PID>
```

---

## Issue: "No such file or directory: 'nawa_nirman.db'"

**Cause:** Database not created yet

**Fix:** This is normal! First time run creates it automatically.
If not:
```bash
# In Python terminal
from app.database import init_db
init_db()
```

---

## Issue: "Template not found"

**Cause:** Templates in wrong location

**Fix:** Make sure templates are in: `backend/app/templates/`

---

## Issue: CSS/JavaScript not loading

**Cause:** Static files not serving

**Fix:** Check static files in browser (F12 > Network tab)
Should be: `/static/styles.css` and `/static/script.js`

---

# 📊 COMMON QUERIES

## SQL Queries Behind the Scenes

```python
# Get all categories
SELECT * FROM category;

# Get products by category
SELECT * FROM product WHERE category_id = 1;

# Get user by email
SELECT * FROM user WHERE email = 'user@example.com';

# Get cart items
SELECT * FROM cartitem WHERE user_id = 5;

# Get orders
SELECT * FROM order WHERE user_id = 5;
```

(SQLModel converts these automatically - you don't write SQL directly!)

---

# 🚢 DEPLOYMENT CHECKLIST

- [ ] Change SESSION_SECRET in .env to random string
- [ ] Set DATABASE_URL to production database
- [ ] Set SECRET_KEY for password hashing
- [ ] Remove `--reload` from uvicorn command
- [ ] Use environment variables for all secrets
- [ ] Add HTTPS/SSL certificate
- [ ] Set up logging
- [ ] Test login/cart/checkout on production
- [ ] Set up email for order notifications
- [ ] Configure payment gateway (Stripe/Razorpay)

---

# 💡 NEXT FEATURES TO ADD

## Easy:
- Product search
- Product filtering by price
- Sort products
- Product reviews

## Medium:
- Admin panel
- Product wishlist
- Email confirmations
- Order tracking

## Advanced:
- Payment gateway (Stripe/Razorpay)
- SMS notifications (Twilio)
- AI recommendations
- Mobile app

---

# 📚 LEARNING RESOURCES

**Python:**
- docs.python.org

**FastAPI:**
- fastapi.tiangolo.com

**SQLModel:**
- sqlmodel.tiangolo.com

**Jinja2:**
- jinja.palletsprojects.com

**HTML/CSS/JavaScript:**
- developer.mozilla.org

---

# 🎓 WHAT YOU'VE LEARNED

✅ How to structure a web project
✅ How to design databases
✅ How to build a REST API
✅ How to authenticate users (login/signup)
✅ How to build a shopping cart
✅ How to process orders
✅ How to create responsive frontend
✅ How to handle forms
✅ How to validate data
✅ How to secure passwords
✅ How to store data in databases
✅ How the web works end-to-end

**You can now build ANY web application!** 🚀

---

# 🤝 QUESTIONS TO ASK YOURSELF

1. "What database table stores this data?"
2. "What route handles this request?"
3. "What function processes this?"
4. "Is this user logged in?"
5. "What could go wrong here? How do I validate?"
6. "Should this be on frontend or backend?"
7. "Is this secure?"
8. "Is this fast enough?"

---

# 💪 FINAL THOUGHTS

Building this website from scratch taught you:
- **Architecture** - How systems are organized
- **Security** - How to protect data
- **Database design** - How to structure information
- **Frontend-Backend communication** - How parts talk to each other
- **User experience** - How to make things easy
- **Problem solving** - How to debug and fix

These skills apply to ANY technology stack!

---

**Now go build something amazing!** 🚀✨

