from django.apps import AppConfig

class AccountsConfig(AppConfig):
    name = 'src.apps.accounts'                                          # import path of this app
    default_auto_field = "django.db.models.BigAutoField"      # pk type for all models here
    verbose_name = "User Accounts"                            # optional: human-readable name