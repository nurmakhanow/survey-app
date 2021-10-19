from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from app.users.models import Users


class Command(BaseCommand):
    help = 'transfer Users images CharField from legacy db to ImageField'

    def handle(self, *args, **options):
        self.stdout.write('This process might take a few minutes to finish')
        uu = Users.objects.all()
        for u in uu:
            try:
                if u.avatar:
                    im = ImageFile(open("/app/public/media/" + u.avatar, "rb"))
                    im.name = im.name.split('//')[1]
                    u.full_avatar = im
                    u.save()
                if u.avatar_160:
                    im = ImageFile(
                        open("/app/public/media/" + u.avatar_160, "rb")
                    )
                    im.name = im.name.split('//')[1]
                    u.full_avatar_160 = im
                    u.save()
            except FileNotFoundError:
                continue
        self.stdout.write(
            self.style.SUCCESS('All Users images successfully transferred')
        )
