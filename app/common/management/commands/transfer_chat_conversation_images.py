from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from app.chat.models import ChatConversation


class Command(BaseCommand):
    help = 'transfer ChatConverstaion images CharField from legacy db to ImageField'

    def handle(self, *args, **options):
        self.stdout.write('This process might take a few minutes to finish')
        cc = ChatConversation.objects.all()
        for c in cc:
            try:
                if c.image:
                    im = ImageFile(open("/app/public/media/" + c.image, "rb"))
                    im.name = im.name.split('//')[1]
                    c.full_image = im
                    c.save()
            except FileNotFoundError:
                continue
        self.stdout.write(
            self.style.SUCCESS(
                'All ChatConversation images successfully transferred'
            )
        )
