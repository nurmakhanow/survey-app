from django.contrib import admin


class NoCreatedUpdatedDeletedStackedInline(admin.StackedInline):
    exclude = ('created_at', 'updated_at', 'deleted_at')
