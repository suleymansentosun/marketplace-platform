from sqlalchemy.orm import Session
from db.database import get_db
from fastapi import Depends
from db.models import DbAdvertisement, DbCategory
from db.database import SessionLocal

def seed_db():
    db = SessionLocal()

    categories = [
        "Electronics", "Furniture", "Clothing", "Books", "Sports", 
        "Toys", "Vehicles", "Real Estate"
    ]
    
    # Create and add categories
    for cat_name in categories:
        category = DbCategory(name=cat_name)
        db.add(category)
    
    # Commit to save categories to the database
    db.commit()
    
    # Retrieve all categories from the database
    all_categories = db.query(DbCategory).all()

    # Sample advertisements
    ads = [
        {"title": "Laptop", "price": 500, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 1},
        {"title": "Sofa", "price": 300, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 2},
        {"title": "T-shirt", "price": 20, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 3},
        {"title": "Novel", "price": 15, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 4},
        {"title": "Bicycle", "price": 150, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 5},
        {"title": "Action Figure", "price": 25, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 6},
        {"title": "Car", "price": 20000, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 7},
        {"title": "Apartment", "price": 150000, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 8},
        {"title": "Smartphone", "price": 300, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 1},
        {"title": "Dining Table", "price": 400, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 2},
        {"title": "Jacket", "price": 100, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 3},
        {"title": "Cookbook", "price": 25, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 4},
        {"title": "Tent", "price": 80, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 5},
        {"title": "Board Game", "price": 30, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 6},
        {"title": "Motorcycle", "price": 5000, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 7},
        {"title": "House", "price": 250000, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 8},
        {"title": "Headphones", "price": 150, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 1},
        {"title": "Coffee Table", "price": 150, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 2},
        {"title": "Sneakers", "price": 70, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 3},
        {"title": "Magazines", "price": 10, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 4},
        {"title": "Camping Gear", "price": 120, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 5},
        {"title": "Puzzle", "price": 20, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 6},
        {"title": "Truck", "price": 30000, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 7},
        {"title": "Condo", "price": 200000, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 8},
        {"title": "Smartwatch", "price": 250, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 1},
        {"title": "Bookshelf", "price": 80, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 2},
        {"title": "Sweater", "price": 50, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 3},
        {"title": "Novel Set", "price": 45, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 4},
        {"title": "Fishing Rod", "price": 60, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 5},
        {"title": "Dollhouse", "price": 90, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 6},
        {"title": "Van", "price": 12000, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 7},
        {"title": "Office Space", "price": 100000, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 8},
        {"title": "Tablet", "price": 200, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 1},
        {"title": "Recliner", "price": 350, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 2},
        {"title": "Scarf", "price": 25, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 3},
        {"title": "Biography", "price": 18, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 4},
        {"title": "Golf Clubs", "price": 150, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 5},
        {"title": "Remote Control Car", "price": 70, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 6},
        {"title": "SUV", "price": 25000, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 7},
        {"title": "Townhouse", "price": 180000, "description": "sample description", "condition": "used", "delivery": "pickup", "category_id": 8},
    ]

    # Create and add advertisements
    for i in range(40):
        ad = DbAdvertisement(
            title=f"{ads[i]['title']}",
            price=f"{ads[i]['price']}",
            description=f"{ads[i]['description']}",
            condition=f"{ads[i]['condition']}",
            delivery=f"{ads[i]['delivery']}",
            category_id=ads[i]['category_id']
        )
        db.add(ad)
    
    # Commit to save advertisements to the database
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_db()