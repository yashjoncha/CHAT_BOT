"""
Django management command to optimize the Chemistry QA model using BootstrapFewShot.
"""

from django.core.management.base import BaseCommand
from chat.dspy_logic import optimize_chemistry_qa, save_optimized_model


class Command(BaseCommand):
    help = 'Optimize Chemistry QA model using BootstrapFewShot'

    def add_arguments(self, parser):
        parser.add_argument(
            '--max-demos',
            type=int,
            default=4,
            help='Maximum bootstrapped demos (default: 4)',
        )
        parser.add_argument(
            '--max-labeled',
            type=int,
            default=3,
            help='Maximum labeled demos (default: 3)',
        )
        parser.add_argument(
            '--max-rounds',
            type=int,
            default=1,
            help='Maximum optimization rounds (default: 1)',
        )

    def handle(self, *args, **options):
        max_demos = options['max_demos']
        max_labeled = options['max_labeled']
        max_rounds = options['max_rounds']

        self.stdout.write(self.style.SUCCESS('Starting model optimization...'))
        self.stdout.write(f'  Max bootstrapped demos: {max_demos}')
        self.stdout.write(f'  Max labeled demos: {max_labeled}')
        self.stdout.write(f'  Max rounds: {max_rounds}')
        self.stdout.write('')

        try:
            compiled_model = optimize_chemistry_qa(
                max_bootstrapped_demos=max_demos,
                max_labeled_demos=max_labeled,
                max_rounds=max_rounds
            )

            filepath = save_optimized_model(compiled_model)

            self.stdout.write(self.style.SUCCESS(f'\nOptimization complete!'))
            self.stdout.write(self.style.SUCCESS(f'Model saved to: {filepath}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Optimization failed: {str(e)}'))
            raise
