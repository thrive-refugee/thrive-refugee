# -*- coding: utf-8 -*-

from django.apps import AppConfig


VERSION = (0, 3, 0, 'beta', 0)


def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '%s pre-alpha' % version
    else:
        version = '%s %s' % (version, VERSION[3])
        if VERSION[3] != 'final':
            version = '%s %s' % (version, VERSION[4])

    return version


class SwingtimeAppConfig(AppConfig):
    name = 'swingtime'
    _zero_width_space = '\u200B'  # used to make it last alphabetically, better option: http://stackoverflow.com/questions/398163/ordering-admin-modeladmin-objects-in-django-admin
    verbose_name = _zero_width_space + 'Calendar Configuration'


default_app_config = 'swingtime.SwingtimeAppConfig'
