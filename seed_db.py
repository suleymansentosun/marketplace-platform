import random
from sqlalchemy.orm import Session
from db.database import get_db
from fastapi import Depends
from db.models import DbAdvertisement, DbCategory, DbUser
from db.database import SessionLocal
from db.hash import Hash

def seed_db():
    db = SessionLocal()

    users = [
        {"username": "jan_jansen", "email": "jan.jansen@example.com", "password": "hashed_password"},
        {"username": "emma_de_vries", "email": "emma.devries@example.com", "password": "hashed_password"},
        {"username": "lucas_smit", "email": "lucas.smit@example.com", "password": "hashed_password"},
        {"username": "sofie_bakker", "email": "sofie.bakker@example.com", "password": "hashed_password"},
        {"username": "thomas_de_boer", "email": "thomas.deboer@example.com", "password": "hashed_password"},
        {"username": "lotte_de_groot", "email": "lotte.degroot@example.com", "password": "hashed_password"},
        {"username": "daan_kuiper", "email": "daan.kuiper@example.com", "password": "hashed_password"},
        {"username": "sanne_van_dijk", "email": "sanne.vandijk@example.com", "password": "hashed_password"},
        {"username": "max_vermeulen", "email": "max.vermeulen@example.com", "password": "hashed_password"},
        {"username": "zoe_muller", "email": "zoe.muller@example.com", "password": "hashed_password"},
        {"username": "jesse_klaver", "email": "jesse.klaver@example.com", "password": "hashed_password"},
        {"username": "fleur_visser", "email": "fleur.visser@example.com", "password": "hashed_password"},
        {"username": "lars_de_haan", "email": "lars.dehaan@example.com", "password": "hashed_password"},
        {"username": "roos_meijer", "email": "roos.meijer@example.com", "password": "hashed_password"},
        {"username": "milan_koning", "email": "milan.koning@example.com", "password": "hashed_password"},
        {"username": "anouk_schouten", "email": "anouk.schouten@example.com", "password": "hashed_password"},
        {"username": "bram_hofman", "email": "bram.hofman@example.com", "password": "hashed_password"},
        {"username": "noor_peeters", "email": "noor.peeters@example.com", "password": "hashed_password"},
        {"username": "levi_van_der_laan", "email": "levi.vanderlaan@example.com", "password": "hashed_password"},
        {"username": "maud_vos", "email": "maud.vos@example.com", "password": "hashed_password"},
        {"username": "jayden_kramer", "email": "jayden.kramer@example.com", "password": "hashed_password"},
        {"username": "iris_van_veen", "email": "iris.vanveen@example.com", "password": "hashed_password"},
        {"username": "mike_hendriks", "email": "mike.hendriks@example.com", "password": "hashed_password"},
        {"username": "amber_van_der_veen", "email": "amber.vanderveen@example.com", "password": "hashed_password"},
        {"username": "tim_van_dam", "email": "tim.vandam@example.com", "password": "hashed_password"},
        {"username": "esmee_janssen", "email": "esmee.janssen@example.com", "password": "hashed_password"},
        {"username": "stijn_schipper", "email": "stijn.schipper@example.com", "password": "hashed_password"},
        {"username": "sophie_dijkstra", "email": "sophie.dijkstra@example.com", "password": "hashed_password"},
        {"username": "sam_van_de_ven", "email": "sam.vandeven@example.com", "password": "hashed_password"},
        {"username": "mila_jacobs", "email": "mila.jacobs@example.com", "password": "hashed_password"},
        {"username": "sem_blom", "email": "sem.blom@example.com", "password": "hashed_password"},
        {"username": "lisanne_post", "email": "lisanne.post@example.com", "password": "hashed_password"},
        {"username": "niels_van_den_bosch", "email": "niels.vandenbosch@example.com", "password": "hashed_password"},
        {"username": "luna_hartman", "email": "luna.hartman@example.com", "password": "hashed_password"},
        {"username": "tijn_stevens", "email": "tijn.stevens@example.com", "password": "hashed_password"},
        {"username": "femke_kok", "email": "femke.kok@example.com", "password": "hashed_password"},
        {"username": "bo_de_wit", "email": "bo.dewit@example.com", "password": "hashed_password"},
        {"username": "brent_de_leeuw", "email": "brent.deleeuw@example.com", "password": "hashed_password"},
        {"username": "elisa_martens", "email": "elisa.martens@example.com", "password": "hashed_password"},
        {"username": "kevin_prins", "email": "kevin.prins@example.com", "password": "hashed_password"},
        {"username": "quinn_van_esch", "email": "quinn.vanesch@example.com", "password": "hashed_password"},
        {"username": "britt_scholten", "email": "britt.scholten@example.com", "password": "hashed_password"},
        {"username": "dean_timmermans", "email": "dean.timmermans@example.com", "password": "hashed_password"},
        {"username": "yara_koopman", "email": "yara.koopman@example.com", "password": "hashed_password"},
        {"username": "luca_van_dam", "email": "luca.vandam@example.com", "password": "hashed_password"},
        {"username": "mees_de_wit", "email": "mees.dewit@example.com", "password": "hashed_password"},
        {"username": "sophie_de_lange", "email": "sophie.delange@example.com", "password": "hashed_password"},
        {"username": "dylan_spruit", "email": "dylan.spruit@example.com", "password": "hashed_password"},
        {"username": "elin_van_den_berg", "email": "elin.vandenberg@example.com", "password": "hashed_password"}
    ]

    for user_data in users:
        user = DbUser(username=user_data["username"], email=user_data["email"], password=Hash.bcrypt(user_data["password"]))
        db.add(user)

    db.commit()

    all_users = db.query(DbUser).all()

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
            category_id=ads[i]['category_id'],
            owner_id = random.choice(all_users).id
        )
        db.add(ad)
    
    # Commit to save advertisements to the database
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_db()