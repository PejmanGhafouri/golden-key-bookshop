from django.contrib import admin
from .models import Book, Category

# Register your models here.
def make_published(modeladmin, request, queryset):
        rows_updated = queryset.update(status='p')
        if rows_updated == 1:
            message_bit = "منتشر شد."
        else:
            message_bit = "منتشر شدند."
        modeladmin.message_user(request, "{} مقاله {}".format(rows_updated, message_bit))
make_published.short_description = "انتشار کتب انتخاب شده"

def make_draft(modeladmin, request, queryset):
        rows_updated = queryset.update(status='d')
        if rows_updated == 1:
            message_bit = "پیش‌نویس شد."
        else:
            message_bit = "پیش‌نویس شدند."
        modeladmin.message_user(request, "{} مقاله {}".format(rows_updated, message_bit))
make_draft.short_description = "پیش‌نویس شدن کتب انتخاب شده"


class CategoryAdmin(admin.ModelAdmin):
	list_display = ('position', 'title','parent','status')
	list_filter = (['status'])
	search_fields = ('title', 'slug')
	prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)


class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'thumbnail_tag', 'author','is_free','price','book_available','status', 'category_to_str')
	list_filter = ('publish','status', 'author')
	search_fields = ('title', 'description')
	ordering = ['-status', '-publish']
	actions = [make_published, make_draft]


admin.site.register(Book, BookAdmin)
