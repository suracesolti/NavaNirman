import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel
from .database import engine
from .crud import create_contact, get_product_by_id, get_products, get_categories

app = FastAPI(title="Nawa Nirman Backend")
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/")
def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/categories")
def categories(request: Request):
    items = get_categories()
    return templates.TemplateResponse("categories.html", {"request": request, "categories": items})

@app.get("/product")
def product_list(request: Request):
    products = get_products()
    return templates.TemplateResponse("product.html", {"request": request, "products": products})

@app.get("/product/{product_id}")
def product_detail(request: Request, product_id: int):
    product = get_product_by_id(product_id)
    if product is None:
        return templates.TemplateResponse("product.html", {"request": request, "products": get_products(), "error": "Product not found."})
    return templates.TemplateResponse("product.html", {"request": request, "product": product})

@app.get("/contact")
def contact_form(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@app.post("/contact")
def submit_contact(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    create_contact(name=name, email=email, message=message)
    return RedirectResponse(url="/contact", status_code=303)

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
