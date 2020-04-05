from django.apps import AppConfig


class TickerConfig(AppConfig):
    name = 'ticker'

    def ready(self):
        from portfolioapp.signals import printfunction
