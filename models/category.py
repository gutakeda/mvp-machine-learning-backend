from app import db

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column("pk_category", db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)