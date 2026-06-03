import hashlib
import secrets
from typing import Dict, List, Optional
from sqlmodel import Session, select
from .models import CartItem, Category, Contact, Order, OrderItem, Product, User
from .database import engine

# Seed data for the first version of the site
PRODUCTS = [
    Product(id=1, name="Cordless Drill Kit", description="Reliable performance with long battery life.", price=8900.0, slug="cordless-drill-kit"),
    Product(id=2, name="Safety Helmet", description="Durable protection for every construction site.", price=1250.0, slug="safety-helmet"),
    Product(id=3, name="Multi-Purpose Saw", description="Precise cutting across wood, plastic and metal.", price=5600.0, slug="multi-purpose-saw"),
]

CATEGORIES = [
    Category(id=1, name="Power Tools", description="Drills, saws, grinders and more."),
    Category(id=2, name="Hand Tools", description="Screwdrivers, hammers, pliers and fasteners."),
    Category(id=3, name="Safety Gear", description="Helmets, gloves, masks and protective wear."),
]

def _hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return hashed, salt

def create_user(name: str, email: str, password: str) -> User:
    password_hash, salt = _hash_password(password)
    user = User(name=name, email=email.lower().strip(), password_hash=password_hash, password_salt=salt)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def get_user_by_email(email: str) -> Optional[User]:
    with Session(engine) as session:
        return session.exec(select(User).where(User.email == email.lower().strip())).first()

def get_user_by_id(user_id: int) -> Optional[User]:
    with Session(engine) as session:
        return session.get(User, user_id)

def authenticate_user(email: str, password: str) -> Optional[User]:
    user = get_user_by_email(email)
    if user is None:
        return None
    hashed, _ = _hash_password(password, user.password_salt)
    return user if hashed == user.password_hash else None

def seed_database() -> None:
    with Session(engine) as session:
        has_products = session.exec(select(Product)).first() is not None
        has_categories = session.exec(select(Category)).first() is not None
        if not has_products:
            session.add_all(PRODUCTS)
        if not has_categories:
            session.add_all(CATEGORIES)
        session.commit()

def create_contact(name: str, email: str, message: str) -> Contact:
    with Session(engine) as session:
        contact = Contact(name=name, email=email, message=message)
        session.add(contact)
        session.commit()
        session.refresh(contact)
        return contact

def get_products() -> List[Product]:
    with Session(engine) as session:
        return session.exec(select(Product)).all()

def get_product_by_id(product_id: int) -> Optional[Product]:
    with Session(engine) as session:
        return session.get(Product, product_id)

def get_categories() -> List[Category]:
    with Session(engine) as session:
        return session.exec(select(Category)).all()

def get_cart_items(user_id: int) -> List[dict]:
    with Session(engine) as session:
        cart_items = session.exec(select(CartItem).where(CartItem.user_id == user_id)).all()
        product_ids = [item.product_id for item in cart_items]
        products = {product.id: product for product in session.exec(select(Product).where(Product.id.in_(product_ids))).all()}
        result = []
        for item in cart_items:
            product = products.get(item.product_id)
            if product is None:
                continue
            result.append({
                "product": product,
                "quantity": item.quantity,
                "subtotal": product.price * item.quantity,
            })
        return result

def get_cart_items_from_session(session_cart: Dict[str, int]) -> List[dict]:
    if not session_cart:
        return []
    product_ids = [int(product_id) for product_id in session_cart.keys()]
    with Session(engine) as session:
        products = {product.id: product for product in session.exec(select(Product).where(Product.id.in_(product_ids))).all()}
    cart_items = []
    for product_id, quantity in session_cart.items():
        product = products.get(int(product_id))
        if product is None:
            continue
        cart_items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": product.price * quantity,
        })
    return cart_items

def add_or_update_cart_item(user_id: int, product_id: int, quantity: int = 1) -> None:
    if quantity == 0:
        remove_cart_item(user_id, product_id)
        return
    with Session(engine) as session:
        cart_item = session.exec(
            select(CartItem).where(CartItem.user_id == user_id, CartItem.product_id == product_id)
        ).first()
        if cart_item:
            cart_item.quantity = max(0, cart_item.quantity + quantity)
            if cart_item.quantity == 0:
                session.delete(cart_item)
        else:
            if quantity > 0:
                session.add(CartItem(user_id=user_id, product_id=product_id, quantity=quantity))
        session.commit()

def remove_cart_item(user_id: int, product_id: int) -> None:
    with Session(engine) as session:
        cart_item = session.exec(
            select(CartItem).where(CartItem.user_id == user_id, CartItem.product_id == product_id)
        ).first()
        if cart_item:
            session.delete(cart_item)
            session.commit()

def clear_cart(user_id: int) -> None:
    with Session(engine) as session:
        items = session.exec(select(CartItem).where(CartItem.user_id == user_id)).all()
        for item in items:
            session.delete(item)
        session.commit()

def merge_session_cart(user_id: int, session_cart: Dict[str, int]) -> None:
    if not session_cart:
        return
    for product_id, quantity in session_cart.items():
        add_or_update_cart_item(user_id, int(product_id), int(quantity))

def create_order(user_id: Optional[int], name: str, email: str, items: List[dict]) -> Order:
    total = sum(item["subtotal"] for item in items)
    with Session(engine) as session:
        order = Order(user_id=user_id, name=name, email=email, total=total)
        session.add(order)
        session.commit()
        session.refresh(order)
        for item in items:
            session.add(
                OrderItem(
                    order_id=order.id,
                    product_id=item["product"].id,
                    quantity=item["quantity"],
                    price=item["product"].price,
                )
            )
        session.commit()
        return order

def get_order_by_id(order_id: int) -> Optional[Order]:
    with Session(engine) as session:
        return session.get(Order, order_id)
