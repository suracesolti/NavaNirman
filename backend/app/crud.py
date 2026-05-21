from typing import List, Optional
from sqlmodel import Session
from .models import Contact, Product, Category
from .database import engine

# Seed data for the first version of the site
PRODUCTS = [
    Product(id=1, name="Cordless Drill Kit", description="Reliable performance with long battery life.", price=8900.0, slug="cordless-drill-kit"),
    Product(id=2, name="Safety Helmet", description="Durable protection for every construction site.", price=1250.0, slug="safety-helmet"),
]

CATEGORIES = [
    Category(id=1, name="Power Tools", description="Drills, saws, grinders and more."),
    Category(id=2, name="Hand Tools", description="Screwdrivers, hammers, pliers and fasteners."),
    Category(id=3, name="Safety Gear", description="Helmets, gloves, masks and protective wear."),
]

def create_contact(name: str, email: str, message: str) -> Contact:
    with Session(engine) as session:
        contact = Contact(name=name, email=email, message=message)
        session.add(contact)
        session.commit()
        session.refresh(contact)
        return contact

def get_products() -> List[Product]:
    return PRODUCTS

def get_product_by_id(product_id: int) -> Optional[Product]:
    return next((product for product in PRODUCTS if product.id == product_id), None)

def get_categories() -> List[Category]:
    return CATEGORIES
