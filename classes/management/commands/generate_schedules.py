from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta, time
from classes.models import FitnessClass, ClassSchedule


class Command(BaseCommand):
    help = 'Generate class schedules for all fitness classes until April 2027'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing schedules before generating new ones',
        )

    def handle(self, *args, **options):
        if options['clear']:
            ClassSchedule.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared all existing schedules'))

        fitness_classes = FitnessClass.objects.all()

        if not fitness_classes.exists():
            self.stdout.write(self.style.ERROR('No fitness classes found. Please load fixtures first.'))
            return

        class_schedules = {
            1: [(0, time(7, 0)), (3, time(7, 0)), (5, time(8, 0))],
            2: [(1, time(18, 0)), (4, time(18, 0))],
            3: [(2, time(6, 30)), (5, time(6, 30))],
            4: [(0, time(18, 30)), (3, time(18, 30))],
            5: [(1, time(12, 0)), (4, time(12, 0))],
            6: [(0, time(17, 0)), (2, time(17, 0)), (4, time(17, 0))],
            7: [(1, time(6, 0)), (3, time(6, 0)), (5, time(7, 0))],
            8: [(0, time(19, 0)), (2, time(19, 0))],
            9: [(1, time(7, 0)), (4, time(7, 0))],
            10: [(2, time(18, 0)), (5, time(10, 0))],
            11: [(0, time(12, 30)), (3, time(12, 30))],
            12: [(1, time(17, 0)), (4, time(17, 0))],
        }

        start_date = timezone.now().date()
        end_date = datetime(2027, 4, 30).date()

        total_created = 0
        current_date = start_date

        self.stdout.write(self.style.SUCCESS(f'Generating schedules from {start_date} to {end_date}'))

        while current_date <= end_date:
            day_of_week = current_date.weekday()

            for fitness_class in fitness_classes:
                if fitness_class.id in class_schedules:
                    schedule_times = class_schedules[fitness_class.id]

                    for scheduled_day, start_time in schedule_times:
                        if day_of_week == scheduled_day:
                            duration_minutes = fitness_class.duration
                            end_time = (datetime.combine(current_date, start_time)
                                        + timedelta(minutes=duration_minutes)).time()

                            schedule, created = ClassSchedule.objects.get_or_create(
                                fitness_class=fitness_class,
                                date=current_date,
                                start_time=start_time,
                                defaults={
                                    'end_time': end_time,
                                    'available_spots': fitness_class.max_capacity,
                                    'is_active': True,
                                }
                            )

                            if created:
                                total_created += 1

            current_date += timedelta(days=1)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {total_created} class schedules until {end_date}'
            )
        )
