from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.services import auth_service

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('orders.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user, error = auth_service.authenticate_user(username, password)
        if error:
            flash(error, 'danger')
            return render_template('auth/login.html')

        login_user(user)
        next_page = request.args.get('next')
        return redirect(next_page or url_for('orders.index'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم تسجيل الخروج بنجاح.', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if current_user.role != 'admin':
        flash('غير مصرح لك بهذه العملية.', 'danger')
        return redirect(url_for('orders.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'waiter')

        user, error = auth_service.create_user(username, email, password, role)
        if error:
            flash(error, 'danger')
            return render_template('auth/register.html')

        flash(f'تم إنشاء المستخدم {username} بنجاح.', 'success')
        return redirect(url_for('auth.register'))

    return render_template('auth/register.html')
