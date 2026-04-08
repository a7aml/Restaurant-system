from app import db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.menu_item import MenuItem
from app.models.table import Table

VALID_STATUSES = ('pending', 'preparing', 'ready', 'delivered', 'cancelled')


def get_all_orders() -> tuple[list[Order], str | None]:
    """Retrieve all orders ordered by most recent first."""
    try:
        orders = Order.query.order_by(Order.created_at.desc()).all()
        return orders, None
    except Exception as e:
        return [], str(e)


def get_active_orders() -> tuple[list[Order], str | None]:
    """Retrieve all non-cancelled, non-delivered orders."""
    try:
        orders = Order.query.filter(
            Order.status.notin_(['delivered', 'cancelled'])
        ).order_by(Order.created_at.asc()).all()
        return orders, None
    except Exception as e:
        return [], str(e)


def get_order_by_id(order_id: int) -> tuple[Order | None, str | None]:
    """Fetch a single order by ID."""
    try:
        order = Order.query.get(order_id)
        if order is None:
            return None, 'الطلب غير موجود.'
        return order, None
    except Exception as e:
        return None, str(e)


def create_order(
    table_id: int | str,
    user_id: int,
    item_ids: list[str],
    quantities: list[str],
    notes: str = '',
) -> tuple[Order | None, str | None]:
    """Create a new order with its associated order items."""
    try:
        table = Table.query.get(int(table_id))
        if table is None:
            return None, 'الطاولة غير موجودة.'

        order = Order(table_id=int(table_id), user_id=user_id, notes=notes)
        db.session.add(order)
        db.session.flush()  # get order.id before committing

        total = 0.0
        for item_id, qty in zip(item_ids, quantities):
            menu_item = MenuItem.query.get(int(item_id))
            if menu_item is None or not menu_item.is_available:
                continue
            quantity = max(1, int(qty))
            unit_price = float(menu_item.price)
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=menu_item.id,
                quantity=quantity,
                unit_price=unit_price,
            )
            db.session.add(order_item)
            total += unit_price * quantity

        order.total_price = total
        table.status = 'occupied'
        db.session.commit()
        return order, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)


def update_order_status(order_id: int, new_status: str) -> tuple[Order | None, str | None]:
    """Update the status of an existing order."""
    try:
        if new_status not in VALID_STATUSES:
            return None, 'حالة الطلب غير صحيحة.'

        order = Order.query.get(order_id)
        if order is None:
            return None, 'الطلب غير موجود.'

        order.status = new_status

        if new_status in ('delivered', 'cancelled'):
            table = Table.query.get(order.table_id)
            if table:
                table.status = 'available'

        db.session.commit()
        return order, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)


def cancel_order(order_id: int) -> tuple[bool, str | None]:
    """Cancel an order."""
    _, error = update_order_status(order_id, 'cancelled')
    if error:
        return False, error
    return True, None
