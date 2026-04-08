from app import db
from app.models.table import Table


def get_all_tables() -> tuple[list[Table], str | None]:
    """Retrieve all tables ordered by table number."""
    try:
        tables = Table.query.order_by(Table.table_number).all()
        return tables, None
    except Exception as e:
        return [], str(e)


def get_available_tables() -> tuple[list[Table], str | None]:
    """Retrieve only available tables."""
    try:
        tables = Table.query.filter_by(status='available').order_by(Table.table_number).all()
        return tables, None
    except Exception as e:
        return [], str(e)


def get_table_by_id(table_id: int) -> tuple[Table | None, str | None]:
    """Fetch a single table by ID."""
    try:
        table = Table.query.get(table_id)
        if table is None:
            return None, 'الطاولة غير موجودة.'
        return table, None
    except Exception as e:
        return None, str(e)


def create_table(table_number: int | str, capacity: int | str) -> tuple[Table | None, str | None]:
    """Create a new table."""
    try:
        if Table.query.filter_by(table_number=int(table_number)).first():
            return None, 'رقم الطاولة مستخدم بالفعل.'
        table = Table(table_number=int(table_number), capacity=int(capacity))
        db.session.add(table)
        db.session.commit()
        return table, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)


def update_table(table_id: int, data: dict) -> tuple[Table | None, str | None]:
    """Update an existing table."""
    try:
        table = Table.query.get(table_id)
        if table is None:
            return None, 'الطاولة غير موجودة.'

        if 'table_number' in data:
            table.table_number = int(data['table_number'])
        if 'capacity' in data:
            table.capacity = int(data['capacity'])
        if 'status' in data:
            table.status = data['status']

        db.session.commit()
        return table, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)


def delete_table(table_id: int) -> tuple[bool, str | None]:
    """Delete a table by ID."""
    try:
        table = Table.query.get(table_id)
        if table is None:
            return False, 'الطاولة غير موجودة.'
        db.session.delete(table)
        db.session.commit()
        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)
