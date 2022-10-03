from db import db


def new_ride(name, description, location_id, material_id, drop_id):
    sql = """INSERT INTO rides (name, description, location_id, material_id, drop_id, visibility) 
             VALUES (:name, :description, :location_id, :material_id, :drop_id, 1)
             RETURNING id"""
    ride_id = db.session.execute(sql, {"name":name, "description":description,\
            "location_id":location_id, "material_id":material_id, "drop_id":drop_id}).fetchone()[0]
    db.session.commit()
    return ride_id

def fetch_ride_data(ride_id):
    sql = """SELECT r.name, r.description, l.category, m.category, d.category
             FROM rides r
             JOIN location_categories l ON l.id=r.location_id
             JOIN material_categories m ON m.id=r.material_id
             JOIN drop_categories d ON d.id=r.drop_id
             WHERE r.id=:ride_id"""
    return db.session.execute(sql, {"ride_id": ride_id}).fetchone()

def fetch_rides():
    sql = "SELECT id, name FROM rides ORDER BY name"
    return db.session.execute(sql).fetchall()
