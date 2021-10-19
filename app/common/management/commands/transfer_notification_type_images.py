from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from app.common.models import NotificationType


class Command(BaseCommand):
    help = 'transfer NotificationType images CharField from legacy db to ImageField'

    def handle(self, *args, **options):
        self.stdout.write('This process might take a few minutes to finish')
        nn = NotificationType.objects.all()
        for n in nn:
            try:
                if n.image:
                    im = ImageFile(open("/app/public/media/" + n.image, "rb"))
                    im.name = im.name.split('//')[1]
                    n.full_image = im
                    n.save()
            except FileNotFoundError:
                continue
        self.stdout.write(
            self.style.SUCCESS(
                'All NotificationType images successfully transferred'
            )
        )
