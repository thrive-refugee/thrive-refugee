from django.apps import AppConfig


class EmploymentManagerAppConfig(AppConfig):
    name = 'employment_manager'
    verbose_name = 'Employment Program'


default_app_config = 'employment_manager.EmploymentManagerAppConfig'
