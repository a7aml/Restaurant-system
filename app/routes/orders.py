from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services import order_service, menu_service, table_service

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


@orders_bp.route('/')
@login_required
def index():
    orders, error = order_service.get_all_orders()
    if error:
        flash('حدث خطأ أثناء تحميل الطلبات.', 'danger')
        return render_template('orders/index.html', orders=[])
    return render_template('orders/index.html', orders=orders)


@orders_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        table_id = request.form.get('table_id')
        notes = request.form.get('notes', '').strip()
        item_ids = request.form.getlist('item_ids')
        quantities = request.form.getlist('quantities')

        order, error = order_service.create_order(
            table_id=table_id,
            user_id=current_user.id,
            item_ids=item_ids,
            quantities=quantities,
            notes=notes,
        )
        if error:
            flash(error, 'danger')
        else:
            flash('تم إنشاء الطلب بنجاح.', 'success')
            return redirect(url_for('orders.detail', order_id=order.id))

    tables, _ = table_service.get_available_tables()
    items, _ = menu_service.get_all_menu_items()
    return render_template('orders/form.html', tables=tables, items=items)


@orders_bp.route('/<int:order_id>')
@login_required
def detail(order_id: int):
    order, error = order_service.get_order_by_id(order_id)
    if error:
        flash('الطلب غير موجود.', 'danger')
        return redirect(url_for('orders.index'))
    return render_template('orders/detail.html', order=order)


@orders_bp.route('/<int:order_id>/status', methods=['POST'])
@login_required
def update_status(order_id: int):
    new_status = request.form.get('status')
    _, error = order_service.update_order_status(order_id, new_status)
    if error:
        flash(error, 'danger')
    else:
        flash('تم تحديث حالة الطلب.', 'success')
    return redirect(url_for('orders.detail', order_id=order_id))


@orders_bp.route('/<int:order_id>/cancel', methods=['POST'])
@login_required
def cancel(order_id: int):
    _, error = order_service.cancel_order(order_id)
    if error:
        flash(error, 'danger')
    else:
        flash('تم إلغاء الطلب.', 'success')
    return redirect(url_for('orders.index'))
