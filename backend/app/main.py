import os
from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader, select_autoescape
from starlette.middleware.sessions import SessionMiddleware
from sqlmodel import SQLModel
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
    merge_session_cart,
    remove_cart_item,
    seed_database,
)

app = FastAPI(title="Nawa Nirman Backend")
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "change-this-secret"))

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml"]),
    cache_size=0,
)
templates = Jinja2Templates(env=jinja_env)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    seed_database()

def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    if user_id is None:
        return None
    return get_user_by_id(user_id)

def get_request_cart_items(request: Request):
    user = get_current_user(request)
    if user:
        return get_cart_items(user.id)
    return get_cart_items_from_session(request.session.get("cart", {}))

def get_cart_count(request: Request) -> int:
    items = get_request_cart_items(request)
    return sum(item["quantity"] for item in items)

def common_context(request: Request, extra: dict = None):
    context = {
        "request": request,
        "user": get_current_user(request),
        "cart_count": get_cart_count(request),
    }
    if extra:
        context.update(extra)
    return context

@app.get("/")
def homepage(request: Request):
    return templates.TemplateResponse("index.html", common_context(request))

@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse("about.html", common_context(request))

@app.get("/categories")
def categories(request: Request):
    items = get_categories()
    return templates.TemplateResponse("categories.html", common_context(request, {"categories": items}))

@app.get("/product")
def product_list(request: Request):
    products = get_products()
    return templates.TemplateResponse("product.html", common_context(request, {"products": products}))

@app.get("/product/{product_id}")
def product_detail(request: Request, product_id: int):
    product = get_product_by_id(product_id)
    if product is None:
        return templates.TemplateResponse(
            "product.html",
            common_context(request, {"products": get_products(), "error": "Product not found."}),
        )
    return templates.TemplateResponse("product.html", common_context(request, {"product": product}))

@app.post("/cart/add/{product_id}")
def cart_add(request: Request, product_id: int, quantity: int = Form(1)):
    user = get_current_user(request)
    if get_product_by_id(product_id) is None:
        return RedirectResponse(url="/product", status_code=303)
    if user:
        add_or_update_cart_item(user.id, product_id, quantity)
    else:
        cart = request.session.get("cart", {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
        if cart[str(product_id)] <= 0:
            cart.pop(str(product_id), None)
        request.session["cart"] = cart
    return RedirectResponse(url="/cart", status_code=303)

@app.post("/cart/remove/{product_id}")
def cart_remove(request: Request, product_id: int):
    user = get_current_user(request)
    if user:
        remove_cart_item(user.id, product_id)
    else:
        cart = request.session.get("cart", {})
        cart.pop(str(product_id), None)
        request.session["cart"] = cart
    return RedirectResponse(url="/cart", status_code=303)

@app.get("/cart")
def cart_page(request: Request):
    items = get_request_cart_items(request)
    total = sum(item["subtotal"] for item in items)
    return templates.TemplateResponse("cart.html", common_context(request, {"cart_items": items, "total": total}))

@app.get("/checkout")
def checkout_page(request: Request):
    items = get_request_cart_items(request)
    if not items:
        return RedirectResponse(url="/cart", status_code=303)
    total = sum(item["subtotal"] for item in items)
    return templates.TemplateResponse("checkout.html", common_context(request, {"cart_items": items, "total": total}))

@app.post("/checkout")
def checkout_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
):
    items = get_request_cart_items(request)
    if not items:
        return RedirectResponse(url="/cart", status_code=303)
    user = get_current_user(request)
    order = create_order(user.id if user else None, name, email, items)
    if user:
        clear_cart(user.id)
    else:
        request.session["cart"] = {}
    return RedirectResponse(url=f"/order/confirmation/{order.id}", status_code=303)

@app.get("/order/confirmation/{order_id}")
def order_confirmation(request: Request, order_id: int):
    order = get_order_by_id(order_id)
    if order is None:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("order_confirmation.html", common_context(request, {"order": order}))

@app.get("/signup")
def signup_form(request: Request):
    return templates.TemplateResponse("signup.html", common_context(request))

@app.post("/signup")
def signup_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    if get_user_by_email(email):
        return templates.TemplateResponse(
            "signup.html",
            common_context(request, {"error": "Email is already registered.", "name": name, "email": email}),
        )
    user = create_user(name=name, email=email, password=password)
    merge_session_cart(user.id, request.session.get("cart", {}))
    request.session["user_id"] = user.id
    request.session["cart"] = {}
    return RedirectResponse(url="/cart", status_code=303)

@app.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", common_context(request))

@app.post("/login")
def login_submit(request: Request, email: str = Form(...), password: str = Form(...)):
    user = authenticate_user(email, password)
    if user is None:
        return templates.TemplateResponse(
            "login.html",
            common_context(request, {"error": "Invalid email or password.", "email": email}),
        )
    merge_session_cart(user.id, request.session.get("cart", {}))
    request.session["user_id"] = user.id
    request.session["cart"] = {}
    return RedirectResponse(url="/cart", status_code=303)

@app.get("/logout")
def logout(request: Request):
    request.session.pop("user_id", None)
    return RedirectResponse(url="/", status_code=303)

@app.get("/contact")
def contact_form(request: Request, submitted: int = 0):
    return templates.TemplateResponse(
        "contact.html",
        common_context(request, {"success": bool(submitted)}),
    )

@app.post("/contact")
def submit_contact(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    create_contact(name=name, email=email, message=message)
    return RedirectResponse(url="/contact?submitted=1", status_code=303)

@app.get("/api/products")
def api_products():
    return get_products()

@app.get("/api/products/{product_id}")
def api_product(product_id: int):
    item = get_product_by_id(product_id)
    if item is None:
        return JSONResponse(status_code=404, content={"detail": "Product not found"})
    return item

@app.get("/api/categories")
def api_categories():
    return get_categories()
