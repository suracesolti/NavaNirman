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
    update_user_profile,
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
    ensure_database_schema()
    seed_database()

def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    if user_id is None:
        return None
    return get_user_by_id(user_id)

def is_password_strong(password: str) -> bool:
    return (
        len(password) >= 8
        and re.search(r"\d", password)
        and re.search(r"[^A-Za-z0-9]", password)
    )

def ensure_database_schema():
    with engine.begin() as conn:
        def has_column(table_name: str, column_name: str) -> bool:
            result = conn.execute(text(f"PRAGMA table_info('{table_name}')")).all()
            return any(row[1] == column_name for row in result)

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


def send_order_confirmation_email(order):
    from_email = os.getenv("EMAIL_FROM", "no-reply@nawanirmanhardware.com")
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    subject = f"Nawa Nirman Order #{order.id} Confirmation"
    body = (
        f"Hello {order.name},\n\n"
        f"Thank you for your order #{order.id}.\n"
        f"Payment method: {order.payment_method}\n"
        f"Shipping address: {order.shipping_address or 'Not provided'}\n"
        f"Phone: {order.phone or 'Not provided'}\n"
        f"Order total: Rs. {order.total}\n\n"
        "We will update you once your order ships.\n\n"
        "Best regards,\n"
        "Nawa Nirman Hardware"
    )

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = from_email
    message["To"] = order.email
    message.set_content(body)

    if smtp_host and smtp_user and smtp_password:
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as smtp:
                smtp.login(smtp_user, smtp_password)
                smtp.send_message(message)
            return True
        except Exception as exc:
            print("Failed to send confirmation email:", exc)
            return False

    print("Confirmation email skipped. Configure SMTP_HOST, SMTP_USER, and SMTP_PASSWORD to enable email delivery.")
    print(body)
    return False


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
    return templates.TemplateResponse(request, "index.html", common_context(request))

@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse(request, "about.html", common_context(request))

@app.get("/categories")
def categories(request: Request):
    items = get_categories()
    return templates.TemplateResponse(request, "categories.html", common_context(request, {"categories": items}))

@app.get("/product")
def product_list(request: Request):
    products = get_products()
    return templates.TemplateResponse(request, "product.html", common_context(request, {"products": products}))

@app.get("/product/{product_id}")
def product_detail(request: Request, product_id: int):
    product = get_product_by_id(product_id)
    if product is None:
        return templates.TemplateResponse(
            request,
            "product.html",
            common_context(request, {"products": get_products(), "error": "Product not found."}),
        )
    return templates.TemplateResponse(request, "product.html", common_context(request, {"product": product}))

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
    return templates.TemplateResponse(request, "cart.html", common_context(request, {"cart_items": items, "total": total}))

@app.get("/checkout")
def checkout_page(request: Request):
    items = get_request_cart_items(request)
    if not items:
        return RedirectResponse(url="/cart", status_code=303)
    user = get_current_user(request)
    total = sum(item["subtotal"] for item in items)
    return templates.TemplateResponse(
        request,
        "checkout.html",
        common_context(
            request,
            {
                "cart_items": items,
                "total": total,
                "name": user.name if user else "",
                "email": user.email if user else "",
                "phone": user.phone or "",
                "address": user.address or "",
                    "payment_method": "cash",
            },
        ),
    )

@app.post("/checkout")
def checkout_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    payment_method: str = Form(...),
    shipping_address: str = Form(...),
    phone: str = Form(...),
    card_number: str = Form(""),
    card_expiry: str = Form(""),
    card_cvv: str = Form(""),
):
    items = get_request_cart_items(request)
    if not items:
        return RedirectResponse(url="/cart", status_code=303)
    if payment_method == "card" and not (card_number.strip() and card_expiry.strip() and card_cvv.strip()):
        error = "Please complete card details for card payment."
    else:
        error = None
    if error:
        user = get_current_user(request)
        total = sum(item["subtotal"] for item in items)
        return templates.TemplateResponse(
            request,
            "checkout.html",
            common_context(
                request,
                {
                    "cart_items": items,
                    "total": total,
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "address": shipping_address,
                    "payment_method": payment_method,
                    "error": error,
                },
            ),
        )
    user = get_current_user(request)
    order = create_order(
        user.id if user else None,
        name,
        email,
        items,
        payment_method,
        shipping_address,
        phone,
    )
    if user:
        clear_cart(user.id)
    else:
        request.session["cart"] = {}
    email_sent = send_order_confirmation_email(order)
    return RedirectResponse(
        url=f"/order/confirmation/{order.id}?email_sent={1 if email_sent else 0}",
        status_code=303,
    )

@app.get("/order/confirmation/{order_id}")
def order_confirmation(request: Request, order_id: int):
    order = get_order_by_id(order_id)
    if order is None:
        return RedirectResponse(url="/", status_code=303)
    email_sent = request.query_params.get("email_sent") == "1"
    return templates.TemplateResponse(
        request,
        "order_confirmation.html",
        common_context(request, {"order": order, "email_sent": email_sent}),
    )

@app.get("/profile")
def profile_page(request: Request):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse(
        request,
        "profile.html",
        common_context(request, {"success": request.query_params.get("saved") == "1"}),
    )

@app.post("/profile")
def profile_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    address: str = Form(""),
):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    existing_user = get_user_by_email(email)
    if existing_user and existing_user.id != user.id:
        return templates.TemplateResponse(
            request,
            "profile.html",
            common_context(request, {"error": "That email is already registered.", "success": False}),
        )
    update_user_profile(user.id, name, email, phone, address)
    return RedirectResponse(url="/profile?saved=1", status_code=303)

@app.get("/signup")
def signup_form(request: Request):
    return templates.TemplateResponse(request, "signup.html", common_context(request))

@app.post("/signup")
def signup_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    if get_user_by_email(email):
        return templates.TemplateResponse(
            request,
            "signup.html",
            common_context(request, {"error": "Email is already registered.", "name": name, "email": email}),
        )
    if not is_password_strong(password):
        return templates.TemplateResponse(
            request,
            "signup.html",
            common_context(
                request,
                {
                    "error": "Password must be at least 8 characters long and include a number and a special character.",
                    "name": name,
                    "email": email,
                },
            ),
        )
    user = create_user(name=name, email=email, password=password)
    merge_session_cart(user.id, request.session.get("cart", {}))
    request.session["user_id"] = user.id
    request.session["cart"] = {}
    return RedirectResponse(url="/cart", status_code=303)

@app.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse(request, "login.html", common_context(request))

@app.post("/login")
def login_submit(request: Request, email: str = Form(...), password: str = Form(...)):
    user = authenticate_user(email, password)
    if user is None:
        return templates.TemplateResponse(
            request,
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
        request,
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
