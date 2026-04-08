from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services import menu_service

menu_bp = Blueprint('menu', __name__, url_prefix='/menu')


@menu_bp.route('/')
@login_required
def index():
    items, error = menu_service.get_all_menu_items()
    if error:
        flash('حدث خطأ أثناء تحميل قائمة الطعام.', 'danger')
        return redirect(url_for('orders.index'))
    return render_template('menu/index.html', items=items)


@menu_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.role != 'admin':
        flash('غير مصرح لك بهذه العملية.', 'danger')
        return redirect(url_for('menu.index'))

    if request.method == 'POST':
        data = {
            'name_ar': request.form.get('name_ar', '').strip(),
            'name_en': request.form.get('name_en', '').strip(),
            'description_ar': request.form.get('description_ar', '').strip(),
            'description_en': request.form.get('description_en', '').strip(),
            'price': request.form.get('price', 0),
            'category': request.form.get('category', '').strip(),
            'image_url': request.form.get('image_url', '').strip(),
        }
        item, error = menu_service.create_menu_item(data)
        if error:
            flash(error, 'danger')
            return render_template('menu/form.html', item=None)

        flash('تمت إضافة الصنف بنجاح.', 'success')
        return redirect(url_for('menu.index'))

    return render_template('menu/form.html', item=None)


@menu_bp.route('/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(item_id: int):
    if current_user.role != 'admin':
        flash('غير مصرح لك بهذه العملية.', 'danger')
        return redirect(url_for('menu.index'))

    item, error = menu_service.get_menu_item_by_id(item_id)
    if error:
        flash('الصنف غير موجود.', 'danger')
        return redirect(url_for('menu.index'))

    if request.method == 'POST':
        data = {
            'name_ar': request.form.get('name_ar', '').strip(),
            'name_en': request.form.get('name_en', '').strip(),
            'description_ar': request.form.get('description_ar', '').strip(),
            'description_en': request.form.get('description_en', '').strip(),
            'price': request.form.get('price', 0),
            'category': request.form.get('category', '').strip(),
            'image_url': request.form.get('image_url', '').strip(),
            'is_available': request.form.get('is_available') == 'on',
        }
        updated_item, error = menu_service.update_menu_item(item_id, data)
        if error:
            flash(error, 'danger')
            return render_template('menu/form.html', item=item)

        flash('تم تحديث الصنف بنجاح.', 'success')
        return redirect(url_for('menu.index'))

    return render_template('menu/form.html', item=item)


@menu_bp.route('/<int:item_id>/delete', methods=['POST'])
@login_required
def delete(item_id: int):
    if current_user.role != 'admin':
        flash('غير مصرح لك بهذه العملية.', 'danger')
        return redirect(url_for('menu.index'))

    _, error = menu_service.delete_menu_item(item_id)
    if error:
        flash(error, 'danger')
    else:
        flash('تم حذف الصنف بنجاح.', 'success')
    return redirect(url_for('menu.index'))
