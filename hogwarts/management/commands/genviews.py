from django.core.management.base import BaseCommand, CommandError

from .base import get_app_config
from hogwarts.magic_views import generate_views


class Command(BaseCommand):
    help = "Code generation command"

    def add_arguments(self, parser):
        parser.add_argument("app", type=str)
        parser.add_argument("model", type=str)
        parser.add_argument(
            "--smart-mode", "-s",
            action="store_true",
            help="sets login required to create and update actions"
        )

    def handle(self, *args, **options):
        app_name: str = options["app"]
        model_name: str = options["model"]
        smart_mode: bool = options["smart_mode"]

        app_config = get_app_config(app_name)
        model = app_config.models.get(model_name.lower())
        if model is None:
            raise CommandError(f"Provided model '{model_name}' does not exist in app '{app_name}'")

        code = generate_views(model, smart_mode)

        path = f'{app_config.path}\\generated_views.py'
        with open(path, 'w') as file:
            file.write(code)

        self.stdout.write(
            self.style.SUCCESS(f"Generated CRUD views in {path}")
        )
