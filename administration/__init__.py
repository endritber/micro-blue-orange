from django.utils.module_loading import autodiscover_modules

def autodiscover():
   autodiscover_modules('admin')

default_app_config = 'administration.apps.AdminConfig'