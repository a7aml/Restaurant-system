from datetime import datetime
from app import db


class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    id: int = db.Column(db.Integer, primary_key=True)
    name_ar: str = db.Column(db.String(128), nullable=False)
    name_en: str = db.Column(db.String(128), nullable=False)
    description_ar: str = db.Column(db.Text)
    description_en: str = db.Column(db.Text)
    price: float = db.Column(db.Numeric(10, 2), nullable=False)
    category: str = db.Column(db.String(64), nullable=False)
    image_url: str = db.Column(db.String(256))
    is_available: bool = db.Column(db.Boolean, default=True, nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    order_items = db.relationship('OrderItem', backref='menu_item', lazy='dynamic')

    def __repr__(self) -> str:
        return f'<MenuItem {self.name_en}>'
