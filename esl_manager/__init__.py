from django.apps import AppConfig


class ESLManagerAppConfig(AppConfig):
    name = 'esl_manager'
    verbose_name = 'ESL'


default_app_config = 'esl_manager.ESLManagerAppConfig'
