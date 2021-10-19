from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from app.post_core.models import Post


class Command(BaseCommand):
    help = 'transfer Post images CharFields from legacy db to ImageFields'

    def handle(self, *args, **options):
        self.stdout.write('This process might take a few minutes to finish')
        posts = Post.objects.all()
        for p in posts:
            try:
                if p.image:
                    im = ImageFile(open("/app/public/media/" + p.image, "rb"))
                    im.name = im.name.split('//')[1]
                    p.full_image = im
                if p.image_250:
                    im_250 = ImageFile(
                        open("/app/public/media/" + p.image_250, "rb")
                    )
                    im_250.name = im_250.name.split('//')[1]
                    p.full_image_250 = im_250
                if p.image_800:
                    im_800 = ImageFile(
                        open("/app/public/media/" + p.image_800, "rb")
                    )
                    im_800.name = im_800.name.split('//')[1]
                    p.full_image_800 = im_800
                p.save()
            except FileNotFoundError:
                continue
        self.stdout.write(
            self.style.SUCCESS('All Post images successfully transferred')
        )
