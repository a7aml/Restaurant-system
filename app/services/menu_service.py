from app import db
from app.models.menu_item import MenuItem


def get_all_menu_items() -> tuple[list[MenuItem], str | None]:
    """Get all available menu items from the database."""
    try:
        items = MenuItem.query.filter_by(is_available=True).order_by(MenuItem.category, MenuItem.name_ar).all()
        return items, None
    except Exception as e:
        return [], str(e)


def get_all_menu_items_admin() -> tuple[list[MenuItem], str | None]:
    """Get all menu items including unavailable ones (admin view)."""
    try:
        items = MenuItem.query.order_by(MenuItem.category, MenuItem.name_ar).all()
        return items, None
    except Exception as e:
        return [], str(e)


def get_menu_item_by_id(item_id: int) -> tuple[MenuItem | None, str | None]:
    """Fetch a single menu item by ID."""
    try:
        item = MenuItem.query.get(item_id)
        if item is None:
            return None, 'الصنف غير موجود.'
        return item, None
    except Exception as e:
        return None, str(e)


def create_menu_item(data: dict) -> tuple[MenuItem | None, str | None]:
    """Create a new menu item."""
    try:
        item = MenuItem(
            name_ar=data['name_ar'],
            name_en=data['name_en'],
            description_ar=data.get('description_ar'),
            description_en=data.get('description_en'),
            price=float(data['price']),
            category=data['category'],
            image_url=data.get('image_url'),
            is_available=data.get('is_available', True),
        )
        db.session.add(item)
        db.session.commit()
        return item, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)


def update_menu_item(item_id: int, data: dict) -> tuple[MenuItem | None, str | None]:
    """Update an existing menu item."""
    try:
        item = MenuItem.query.get(item_id)
        if item is None:
            return None, 'الصنف غير موجود.'

        item.name_ar = data.get('name_ar', item.name_ar)
        item.name_en = data.get('name_en', item.name_en)
        item.description_ar = data.get('description_ar', item.description_ar)
        item.description_en = data.get('description_en', item.description_en)
        item.price = float(data.get('price', item.price))
        item.category = data.get('category', item.category)
        item.image_url = data.get('image_url', item.image_url)
        item.is_available = data.get('is_available', item.is_available)

        db.session.commit()
        return item, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)


def delete_menu_item(item_id: int) -> tuple[bool, str | None]:
    """Delete a menu item by ID."""
    try:
        item = MenuItem.query.get(item_id)
        if item is None:
            return False, 'الصنف غير موجود.'
        db.session.delete(item)
        db.session.commit()
        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)
