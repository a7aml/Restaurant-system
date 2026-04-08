from app import db
from app.models.user import User


def authenticate_user(username: str, password: str) -> tuple[User | None, str | None]:
    """Authenticate a user by username and password."""
    try:
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            return None, 'اسم المستخدم أو كلمة المرور غير صحيحة.'
        return user, None
    except Exception as e:
        return None, str(e)


def create_user(username: str, email: str, password: str, role: str) -> tuple[User | None, str | None]:
    """Create a new user account."""
    try:
        if User.query.filter_by(username=username).first():
            return None, 'اسم المستخدم مستخدم بالفعل.'
        if User.query.filter_by(email=email).first():
            return None, 'البريد الإلكتروني مستخدم بالفعل.'

        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)


def get_user_by_id(user_id: int) -> tuple[User | None, str | None]:
    """Fetch a user by their ID."""
    try:
        user = User.query.get(user_id)
        if user is None:
            return None, 'المستخدم غير موجود.'
        return user, None
    except Exception as e:
        return None, str(e)


def get_all_users() -> tuple[list[User], str | None]:
    """Retrieve all users."""
    try:
        users = User.query.order_by(User.created_at.desc()).all()
        return users, None
    except Exception as e:
        return [], str(e)
