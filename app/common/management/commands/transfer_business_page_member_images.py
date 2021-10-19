from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from app.business.models import BusinessPageMember


class Command(BaseCommand):
    help = 'transfer BusinessPageMember images CharField from legacy db to ImageField'

    def handle(self, *args, **options):
        self.stdout.write('This process might take a few minutes to finish')
        bb = BusinessPageMember.objects.all()
        for b in bb:
            try:
                if b.avatar:
                    im = ImageFile(open("/app/public/media/" + b.avatar, "rb"))
                    im.name = im.name.split('//')[1]
                    b.full_avatar = im
                    b.save()
            except FileNotFoundError:
                continue
        self.stdout.write(
            self.style.SUCCESS(
                'All BusinessPageMember images successfully transferred'
            )
        )
