from app import db


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id: int = db.Column(db.Integer, primary_key=True)
    order_id: int = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    menu_item_id: int = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)
    quantity: int = db.Column(db.Integer, nullable=False, default=1)
    unit_price: float = db.Column(db.Numeric(10, 2), nullable=False)
    notes: str = db.Column(db.Text)

    def __repr__(self) -> str:
        return f'<OrderItem order={self.order_id} item={self.menu_item_id}>'
