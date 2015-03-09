from django.apps import AppConfig
from django.db.models.signals import post_delete, post_save


class FeTSyConfig(AppConfig):
    name = 'fetsy'
    verbose_name = 'FeTSy'

    def ready(self):
        from .signals import model_change_logging
        post_save.connect(
            model_change_logging,
            dispatch_uid='fetsy_model_change_logging')
        post_delete.connect(
            model_change_logging,
            dispatch_uid='fetsy_model_change_logging')
