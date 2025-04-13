class ResumeRouter:
    """
    A database router for directing model operations to specific databases.
    - 'analytics' app models use the 'analytics' database (MySQL).
    - All other apps use the 'default' database (PostgreSQL).
    - Note: 'resumes' app uses mongoengine, which bypasses Django's ORM.
    """

    def db_for_read(self, model, **hints):
        """Route read operations to the appropriate database."""
        if model._meta.app_label == 'analytics':
            return 'analytics'
        return 'default'

    def db_for_write(self, model, **hints):
        """Route write operations to the appropriate database."""
        if model._meta.app_label == 'analytics':
            return 'analytics'
        return 'default'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Control which database migrations are applied to."""
        if app_label == 'analytics':
            return db == 'analytics'
        return db == 'default'