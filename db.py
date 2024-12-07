from app import app,db, SongCategories, SongRecommendations

with app.app_context():
    db.create_all(bind_key=None)  # Optional: Bind specific DB if needed
    SongRecommendations.__table__.create(db.engine)
    SongCategories.__table__.create(db.engine)
    print("Song table created successfully!")