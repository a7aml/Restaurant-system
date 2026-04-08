from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services import table_service

tables_bp = Blueprint('tables', __name__, url_prefix='/tables')


@tables_bp.route('/')
@login_required
def index():
    tables, error = table_service.get_all_tables()
    if error:
        flash('حدث خطأ أثناء تحميل الطاولات.', 'danger')
        return render_template('tables/index.html', tables=[])
    return render_template('tables/index.html', tables=tables)


@tables_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.role != 'admin':
        flash('غير مصرح لك بهذه العملية.', 'danger')
        return redirect(url_for('tables.index'))

    if request.method == 'POST':
        table_number = request.form.get('table_number')
        capacity = request.form.get('capacity')

        table, error = table_service.create_table(table_number, capacity)
        if error:
            flash(error, 'danger')
            return render_template('tables/form.html', table=None)

        flash('تمت إضافة الطاولة بنجاح.', 'success')
        return redirect(url_for('tables.index'))

    return render_template('tables/form.html', table=None)


@tables_bp.route('/<int:table_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(table_id: int):
    if current_user.role != 'admin':
        flash('غير مصرح لك بهذه العملية.', 'danger')
        return redirect(url_for('tables.index'))

    table, error = table_service.get_table_by_id(table_id)
    if error:
        flash('الطاولة غير موجودة.', 'danger')
        return redirect(url_for('tables.index'))

    if request.method == 'POST':
        data = {
            'table_number': request.form.get('table_number'),
            'capacity': request.form.get('capacity'),
            'status': request.form.get('status'),
        }
        _, error = table_service.update_table(table_id, data)
        if error:
            flash(error, 'danger')
            return render_template('tables/form.html', table=table)

        flash('تم تحديث الطاولة بنجاح.', 'success')
        return redirect(url_for('tables.index'))

    return render_template('tables/form.html', table=table)


@tables_bp.route('/<int:table_id>/delete', methods=['POST'])
@login_required
def delete(table_id: int):
    if current_user.role != 'admin':
        flash('غير مصرح لك بهذه العملية.', 'danger')
        return redirect(url_for('tables.index'))

    _, error = table_service.delete_table(table_id)
    if error:
        flash(error, 'danger')
    else:
        flash('تم حذف الطاولة بنجاح.', 'success')
    return redirect(url_for('tables.index'))
