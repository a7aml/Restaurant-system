from datetime import datetime
from app import db


class Order(db.Model):
    __tablename__ = 'orders'

    id: int = db.Column(db.Integer, primary_key=True)
    table_id: int = db.Column(db.Integer, db.ForeignKey('tables.id'), nullable=False)
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status: str = db.Column(db.String(20), nullable=False, default='pending')  # pending/preparing/ready/delivered/cancelled
    total_price: float = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    notes: str = db.Column(db.Text)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'<Order {self.id} - {self.status}>'
