
class Roles:
    """
    Available roles for the application
    """
    NORMAL = 'NORMAL'
    ADMIN = 'ADMIN'

    @classmethod
    def get_allowed_roles_per_role(cls, role: str):
        if role == cls.ADMIN:
            return [cls.NORMAL, cls.ADMIN]
        elif role == cls.NORMAL:
            return [cls.NORMAL]

    @classmethod
    def get_all_roles(cls):
        return [cls.NORMAL, cls.ADMIN]
