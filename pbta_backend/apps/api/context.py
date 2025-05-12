import contextvars

user_context = contextvars.ContextVar("user_context", default=None)


def set_current_user(payload):
    user_context.set(payload)


def get_current_user():
    return user_context.get()
