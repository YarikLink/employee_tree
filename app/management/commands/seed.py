import random
import datetime
from django.core.management.base import BaseCommand
from app.models import Employee
from django_seed import Seed
import faker

seeder = Seed.seeder()

positions = ['Manager', 'Senior manager', 'Middle Manager', 'Junior Manager', 'DevOps', 'Developer', 'HR']

class Command(BaseCommand):
    help = 'Seeds the database with employees'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of employees to create')

    def handle(self, *args, **options):
        count = options['count']

        Employee.objects.update_or_create(
            name='Benjamin Button',
            position='CEO',
            date=datetime.date.today(),
            email='benjaminbutton@gmail.com',
            manager=None
        )

        for i in range(1, count):
            name = seeder.faker.name()
            position = random.choice(positions)
            date = datetime.date.today() - datetime.timedelta(days=random.randint(0, 365*10))
            email = seeder.faker.email()
            manager = None if i == 0 else Employee.objects.order_by('?').first()
            Employee.objects.create(name=name, position=position, date=date, email=email, manager=manager)

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {count} employees'))