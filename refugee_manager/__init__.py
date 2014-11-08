from django.apps import AppConfig


class RefugeeManagerAppConfig(AppConfig):
    name = 'refugee_manager'
    verbose_name = 'Case Management'


default_app_config = 'refugee_manager.RefugeeManagerAppConfig'
