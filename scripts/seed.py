#!/usr/bin/env python3
"""Seed the Stars & Pines V2 database with real property data.

Phase 0.5 — Reality Capture.

Populates:
- Rooms (from actual Stars & Pines room list)
- Beds (for dorm rooms)
- Menu items (from menuprices.txt)
- Staff (Raman Ji, Mona)
- Inventory categories and items
- Lily the dog (in guide_entries when that table exists)

Usage:
    python scripts/seed.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api.db import get_db


def seed_rooms():
    """Insert actual Stars & Pines rooms."""
    rooms = [
        ("R01", "Turquoise Room", "private", 2500, 2),
        ("R02", "Yellow Room", "private", 2500, 2),
        ("R03", "Star Suite", "private", 5000, 2),
        ("R04", "Ridge Room", "private", 1800, 2),
        ("D01", "Dorm 1", "dorm", 600, 6),
        ("D02", "Dorm 2", "dorm", 700, 6),
    ]
    with get_db() as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO rooms (id, name, type, base_price, capacity) VALUES (?, ?, ?, ?, ?)",
            rooms,
        )
    print(f"  Seeded {len(rooms)} rooms")


def seed_beds():
    """Insert beds for dorm rooms."""
    beds = [
        # Dorm 1
        ("D01-1", "D01", "Bed 1"),
        ("D01-2", "D01", "Bed 2"),
        ("D01-3", "D01", "Bed 3"),
        ("D01-4", "D01", "Bed 4"),
        ("D01-5", "D01", "Bed 5"),
        ("D01-6", "D01", "Bed 6"),
        # Dorm 2
        ("D02-1", "D02", "Bed 1"),
        ("D02-2", "D02", "Bed 2"),
        ("D02-3", "D02", "Bed 3"),
        ("D02-4", "D02", "Bed 4"),
        ("D02-5", "D02", "Bed 5"),
        ("D02-6", "D02", "Bed 6"),
    ]
    with get_db() as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO beds (id, room_id, label) VALUES (?, ?, ?)",
            beds,
        )
    print(f"  Seeded {len(beds)} beds")


def seed_menu():
    """Insert menu items from the actual Stars & Pines menu."""
    items = [
        # Hot drinks
        ("M001", "Masala Chai", "beverages", 55, 5),
        ("M002", "Americano", "beverages", 155, 5),
        ("M003", "Ginger Lemon Honey", "beverages", 122, 5),
        ("M004", "Hot Chocolate", "beverages", 233, 5),
        ("M005", "Cappuccino", "beverages", 222, 5),
        ("M006", "Latte", "beverages", 222, 5),
        # Cafe kitchen
        ("M007", "Maggi", "mains", 60, 10),
        ("M008", "Omelette (Plain)", "breakfast", 180, 10),
        ("M009", "Paratha (Aloo)", "breakfast", 122, 15),
        ("M010", "Butter Toast", "breakfast", 50, 5),
        ("M011", "Thukpa (Veg)", "mains", 130, 15),
        ("M012", "Curd", "mains", 40, 2),
        # Bread & extras
        ("M013", "Plain Naan", "mains", 35, 5),
        ("M014", "Butter Naan", "mains", 45, 5),
        ("M015", "Banana", "mains", 20, 1),
    ]
    with get_db() as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO menu_items (id, name, category, price, prep_time_min) VALUES (?, ?, ?, ?, ?)",
            items,
        )
    print(f"  Seeded {len(items)} menu items")


def seed_staff():
    """Insert staff members."""
    staff = [
        ("S02", "Raman Ji", "kitchen", "5678", None),
        ("S03", "Mona", "manager", "9012", None),
    ]
    with get_db() as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO staff (id, name, role, pin, phone) VALUES (?, ?, ?, ?, ?)",
            staff,
        )
    print(f"  Seeded {len(staff)} staff members")


def seed_inventory():
    """Insert inventory categories and sample items."""
    categories = [
        ("cat-grocery", "Grocery"),
        ("cat-fv", "Fruits & Vegetables"),
        ("cat-beverages", "Beverages"),
        ("cat-kitchen", "Kitchen Supplies"),
    ]
    with get_db() as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO inventory_categories (id, name) VALUES (?, ?)",
            categories,
        )

    items = [
        # Grocery
        ("inv-dal", "cat-grocery", "Dal", "kg", 5.0, 1.0),
        ("inv-atta", "cat-grocery", "Atta (Flour)", "kg", 10.0, 2.0),
        ("inv-rice", "cat-grocery", "Rice", "kg", 8.0, 2.0),
        ("inv-oil", "cat-grocery", "Cooking Oil", "litre", 3.0, 0.5),
        ("inv-salt", "cat-grocery", "Salt", "kg", 2.0, 0.5),
        ("inv-masala", "cat-grocery", "Masala Mix", "kg", 1.0, 0.2),
        ("inv-maggi", "cat-grocery", "Maggi Packets", "pcs", 24.0, 6.0),
        # Fruits & Vegetables
        ("inv-onion", "cat-fv", "Onion", "kg", 3.0, 1.0),
        ("inv-tomato", "cat-fv", "Tomato", "kg", 3.0, 1.0),
        ("inv-potato", "cat-fv", "Potato", "kg", 5.0, 1.0),
        ("inv-ginger", "cat-fv", "Ginger", "kg", 0.5, 0.1),
        ("inv-garlic", "cat-fv", "Garlic", "kg", 0.5, 0.1),
        # Beverages
        ("inv-tea", "cat-beverages", "Tea Leaves", "kg", 1.0, 0.2),
        ("inv-coffee", "cat-beverages", "Coffee Powder", "kg", 0.5, 0.1),
        ("inv-milk", "cat-beverages", "Milk", "litre", 4.0, 1.0),
        ("inv-sugar", "cat-beverages", "Sugar", "kg", 3.0, 1.0),
        # Kitchen Supplies
        ("inv-napkins", "cat-kitchen", "Paper Napkins", "pcs", 100.0, 20.0),
        ("inv-soap", "cat-kitchen", "Guest Soap", "pcs", 12.0, 3.0),
    ]
    with get_db() as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO inventory_items (id, category_id, name, unit, current_stock, threshold) VALUES (?, ?, ?, ?, ?, ?)",
            items,
        )
    print(f"  Seeded {len(categories)} categories, {len(items)} inventory items")


def seed_places():
    """Insert places/attractions for the guest portal Places Guide."""
    places = [
        ("place-kasar-devi", "Kasar Devi Temple", "Visible from the balcony. A small shrine that grew over decades. Vivekananda meditated here.", 0.3, "0.3 km", 3, 5, "🛕", "temple", '["temple","heritage"]', 1, 1),
        ("place-balta-village", "Balta Village", "A quiet village trail through pine and rhododendron. Takes twenty minutes.", 0.1, "0.1 km", 2, 5, "🏘", "village", '["village","walk"]', 1, 2),
        ("place-balta-waterfall", "Balta Waterfall", "Hidden waterfall through pine forests. A short walk from the village trail.", 1.5, "1.5 km", 5, 10, "💧", "nature", '["nature","waterfall"]', 1, 3),
        ("place-lagoon", "The Lagoon", "Natural pool formed by seasonal streams. A quiet spot for a dip.", 3.0, "3 km", 10, 18, "🏊", "nature", '["nature","swimming"]', 1, 4),
        ("place-chittai", "Chittai Temple", "Ancient temple dedicated to Golu Devta. Known for bells hung by devotees.", 5.0, "5 km", 15, 25, "🛕", "temple", '["temple","cultural"]', 1, 5),
        ("place-karni-mata", "Karni Mata Temple", "Hilltop temple with sweeping valley views. Popular with locals.", 4.0, "4 km", 12, 20, "🛕", "temple", '["temple","viewpoint"]', 1, 6),
        ("place-vivekanand-gufa", "Vivekanand Dhyan Gufa", "Meditation cave where Swami Vivekananda sat in deep contemplation.", 6.0, "6 km", 18, 30, "🧘", "spiritual", '["spiritual","cave"]', 1, 7),
        ("place-katarmal", "Katarmal Sun Temple", "Ancient sun temple with intricate stone carvings. One of the oldest in the region.", 8.0, "8 km", 20, 35, "🏛", "temple", '["temple","heritage"]', 1, 8),
        ("place-ntd", "Bright End Corner (NTD)", "Sunset point with panoramic Himalayan views. Named after the British era.", 9.0, "9 km", 22, 38, "🌅", "viewpoint", '["viewpoint","sunset"]', 1, 9),
        ("place-almora-zoo", "Almora Zoo", "Small hill zoo with local Himalayan fauna. Good for a quick visit.", 10.0, "10 km", 25, 40, "🦌", "nature", '["family","nature"]', 1, 10),
        ("place-lakhudiyaar", "Lakhudiyaar Caves", "Ancient rock-cut caves with prehistoric inscriptions and carvings.", 12.0, "12 km", 30, 50, "🏔", "caves", '["caves","heritage"]', 1, 11),
    ]
    with get_db() as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO places (id, name, description, distance_km, distance_text, taxi_time_min, bike_time_min, icon, category, tags, is_active, sort_order) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            places,
        )
    print(f"  Seeded {len(places)} places")


def seed_perool():
    """Insert Perool product categories and products."""
    categories = [
        ("perool-clothing", "Clothing", "👗", 1),
        ("perool-furnishing", "Furnishing", "🏠", 2),
        ("perool-bathroom", "Bathroom", "🛁", 3),
        ("perool-accessories", "Accessories", "👜", 4),
        ("perool-organic", "Organic", "🌿", 5),
        ("perool-art", "Art", "🎨", 6),
    ]
    with get_db() as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO perool_categories (id, name, icon, sort_order) VALUES (?, ?, ?, ?)",
            categories,
        )

    products = [
        # Clothing
        ("perool-kimono", "perool-clothing", "Kimonos", "Hand-dyed mountain kimonos", "👘", None, 1),
        ("perool-muffler", "perool-clothing", "Mufflers", "Woven wool mufflers", "🧣", None, 2),
        ("perool-tops", "perool-clothing", "Tops", "Cotton and linen tops", "👚", None, 3),
        ("perool-summer-dress", "perool-clothing", "Summer Dresses", "Light frocks for warm days", "👗", None, 4),
        ("perool-sweater", "perool-clothing", "Sweaters", "Hand-knit mountain wool", "🧶", None, 5),
        # Furnishing
        ("perool-carpet", "perool-furnishing", "Carpets", "Hand-woven Himalayan carpets", "🟫", None, 1),
        ("perool-yoga-mat", "perool-furnishing", "Yoga Mats", "Natural fibre yoga mats", "🧘", None, 2),
        ("perool-runner", "perool-furnishing", "Runners / Throws", "Decorative runners and throws", "🛋", None, 3),
        # Bathroom
        ("perool-bath-salt", "perool-bathroom", "Bath Salts", "Himalayan mineral bath salts", "🧂", None, 1),
        ("perool-organic-soap", "perool-bathroom", "Organic Soaps", "Handmade herbal soaps", "🧼", None, 2),
        # Accessories
        ("perool-yoga-bag", "perool-accessories", "Yoga Bags", "Canvas yoga carry bags", "🎒", None, 1),
        ("perool-laptop-bag", "perool-accessories", "Laptop Bags", "Hand-stitched laptop sleeves", "💼", None, 2),
        ("perool-scrunchie", "perool-accessories", "Scrunchies", "Fabric scrunchies", "🎀", None, 3),
        ("perool-coaster", "perool-accessories", "Coasters", "Hand-painted wooden coasters", "☕", None, 4),
        ("perool-candle", "perool-accessories", "Candles", "Beeswax mountain candles", "🕯", None, 5),
        # Organic
        ("perool-organic-soap2", "perool-organic", "Organic Soaps", "Chemical-free herbal soaps", "🧼", None, 1),
        ("perool-achaar", "perool-organic", "Achaar", "Homemade mountain pickles", "🫙", None, 2),
        ("perool-herbal-tea", "perool-organic", "Herbal Teas", "Wild-harvested herb blends", "🍵", None, 3),
        # Art
        ("perool-painting", "perool-art", "Paintings", "Original ridge landscape art", "🖼", None, 1),
    ]
    with get_db() as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO perool_products (id, category_id, name, description, icon, price, sort_order) VALUES (?, ?, ?, ?, ?, ?, ?)",
            products,
        )
    print(f"  Seeded {len(categories)} Perool categories, {len(products)} products")


def seed_all():
    """Run all seed functions."""
    print("Seeding Stars & Pines V2 database...")
    seed_rooms()
    seed_beds()
    seed_menu()
    seed_staff()
    seed_inventory()
    seed_places()
    seed_perool()
    print("Done.")


if __name__ == "__main__":
    seed_all()
