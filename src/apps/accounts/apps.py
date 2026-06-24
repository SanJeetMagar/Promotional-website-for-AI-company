from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = "src.apps.accounts"
    label = "accounts"      # <– app label Django uses
    def ready(self):
        import src.apps.accounts.signals