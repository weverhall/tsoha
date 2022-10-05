from db import db


def new_ride(name, description, location_id, material_id, drop_id):
    sql = """INSERT INTO rides (name, description, location_id, material_id, drop_id) 
             VALUES (:name, :description, :location_id, :material_id, :drop_id)
             RETURNING id"""
    ride_id = db.session.execute(sql, {"name":name, "description":description,\
            "location_id":location_id, "material_id":material_id, "drop_id":drop_id}).fetchone()[0]
    db.session.commit()
    return ride_id

def remove_ride(ride_id):
    sql = "DELETE FROM rides WHERE rides.id=:ride_id"
    db.session.execute(sql, {"ride_id":ride_id})
    db.session.commit()

def fetch_ride_data(ride_id):
    sql = """SELECT r.name, r.description, l.category, m.category, d.category
             FROM rides r
             JOIN location_categories l ON l.id=r.location_id
             JOIN material_categories m ON m.id=r.material_id
             JOIN drop_categories d ON d.id=r.drop_id
             WHERE r.id=:ride_id
             ORDER BY r.name"""
    return db.session.execute(sql, {"ride_id": ride_id}).fetchone()

def fetch_all_rides():
    sql = "SELECT id, name FROM rides ORDER BY name"
    return db.session.execute(sql).fetchall()

def search(query):
    sql = """SELECT r.id, r.name, r.description, l.category, m.category, d.category
             FROM rides r
             JOIN location_categories l ON l.id=r.location_id
             JOIN material_categories m ON m.id=r.material_id
             JOIN drop_categories d ON d.id=r.drop_id
             WHERE r.name ILIKE :query
             OR r.description ILIKE :query
             OR l.category ILIKE :query
             OR m.category ILIKE :query
             OR d.category ILIKE :query
             ORDER BY r.name"""
    return db.session.execute(sql, {"query":"%"+query+"%"}).fetchall()
