from django.db import models
import uuid
from django.urls import reverse
from accounts.models import User
from django.utils import timezone
from django.utils.html import format_html
# Create your models here.
class BookManager(models.Manager):
	def published(self):
		return self.filter(status='p')


class CategoryManager(models.Manager):
	def active(self):
		return self.filter(status=True)


class Category(models.Model):
	parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name='children', verbose_name="زیردسته")
	title = models.CharField(max_length=200, verbose_name="عنوان دسته‌بندی")
	slug = models.SlugField(max_length=100, unique=True, verbose_name="آدرس دسته‌بندی")
	status = models.BooleanField(default=True, verbose_name="آیا نمایش داده شود؟")
	position = models.IntegerField(verbose_name="پوزیشن")

	class Meta:
		verbose_name = "دسته‌بندی"
		verbose_name_plural = "دسته‌بندی ها"
		ordering = ['parent__id', 'position']

	def __str__(self):
		return self.title

	objects = CategoryManager()

class Book(models.Model):
	STATUS_CHOICES = (
		('d', 'پیش‌نویس'),		 # draft
		('p', "منتشر شده"),		 # publish
		('i', "در حال بررسی"),	 # investigation
		('b', "برگشت داده شده"), # back
	)
	
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='books', verbose_name="نویسنده")
	title = models.CharField(max_length=200, verbose_name="عنوان کتاب")
	book_author = models.CharField(max_length=200, verbose_name="نویسنده کتاب")
	category = models.ManyToManyField(Category, verbose_name="دسته‌بندی", related_name="books")
	description = models.TextField(verbose_name="محتوا")
	price = models.FloatField(null=True, blank=True,verbose_name="قیمت")
	thumbnail = models.ImageField(upload_to="images", verbose_name="تصویر کتاب")
	publish = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	is_free = models.BooleanField(default=False, verbose_name="کتاب رایگان")
	book_available = models.BooleanField(default=False,verbose_name="موجود")
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت")

	
	class Meta:
		verbose_name = "کتاب"
		verbose_name_plural = "کتب"
		ordering = ['-publish']


	def __str__(self):
		return self.title


	def get_absolute_url(self):
		return reverse("account:home")


	def thumbnail_tag(self):
		return format_html("<img width=100 height=75 style='border-radius: 5px;' src='{}'>".format(self.thumbnail.url))
	thumbnail_tag.short_description = "عکس"	

	def category_to_str(self):
		return "، ".join([category.title for category in self.category.active()])
	category_to_str.short_description = "دسته‌بندی"

	objects = BookManager()