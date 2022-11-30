from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class EmpresaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'empresa'
    verbose_name = _('empresa')


    def ready(self):
        import empresa.signals