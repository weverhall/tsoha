from db import db


def fetch_rides():
    sql = "SELECT id, name FROM rides ORDER BY name"
    return db.session.execute(sql).fetchall()


def fetch_ride_data(ride_id):
    sql = "SELECT name, description FROM rides WHERE rides.id=:ride_id"
    return db.session.execute(sql, {"ride_id": ride_id}).fetchone()


def new_ride(name, description):
    sql = """INSERT INTO rides (name, description) VALUES (:name, :description)
             RETURNING id"""
    ride_id = db.session.execute(sql, {"name":name, "description":description}).fetchone()[0]
    db.session.commit()
    return ride_id
