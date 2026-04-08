from app import db


class Table(db.Model):
    __tablename__ = 'tables'

    id: int = db.Column(db.Integer, primary_key=True)
    table_number: int = db.Column(db.Integer, unique=True, nullable=False)
    capacity: int = db.Column(db.Integer, nullable=False)
    status: str = db.Column(db.String(20), nullable=False, default='available')  # available / occupied / reserved

    orders = db.relationship('Order', backref='table', lazy='dynamic')

    def __repr__(self) -> str:
        return f'<Table {self.table_number}>'
