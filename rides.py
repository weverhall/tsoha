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
    sql = "SELECT * FROM rides ORDER BY name"
    return db.session.execute(sql).fetchall()

def check_ride_name(name):
    sql = "SELECT name FROM rides WHERE name=:name"
    return db.session.execute(sql, {"name":name}).fetchone()

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

def new_review(content, stars, user_id, ride_id):
    sql = """INSERT INTO reviews (content, stars, user_id, ride_id, sent_at)
             VALUES (:content, :stars, :user_id, :ride_id, NOW()::timestamp(0))"""
    db.session.execute(sql, {"content": content, "stars": stars, "user_id": user_id, "ride_id": ride_id})
    db.session.commit()

def remove_review(review_id):
    sql = "DELETE FROM reviews WHERE reviews.id=:review_id"
    db.session.execute(sql, {"review_id":review_id})
    db.session.commit()

def fetch_ride_reviews(ride_id):
    sql = """SELECT u.name, x.stars, x.content, x.sent_at
             FROM users u, reviews x
             WHERE x.user_id=u.id AND x.ride_id=:ride_id
             ORDER BY x.sent_at DESC"""
    return db.session.execute(sql, {"ride_id": ride_id}).fetchall()

def fetch_all_reviews():
    sql = """SELECT r.name, u.name, x.stars, x.content, x.sent_at, x.id, x.ride_id
             FROM reviews x
             JOIN rides r ON r.id=x.ride_id
             JOIN users u ON u.id=x.user_id
             ORDER BY r.name, x.sent_at DESC"""
    return db.session.execute(sql).fetchall()

def fetch_average_rating(ride_id):
    sql = "SELECT ROUND(AVG(stars), 1) FROM reviews WHERE ride_id=:ride_id"
    return db.session.execute(sql, {"ride_id": ride_id}).fetchone()

def fetch_top_averages():
    sql = """SELECT r.id, r.name, ROUND(AVG(x.stars), 1) 
             FROM reviews x 
             JOIN rides r ON r.id=x.ride_id 
             GROUP BY r.id, r.name 
             ORDER BY AVG(x.stars) DESC 
             LIMIT 3"""
    return db.session.execute(sql).fetchall()
