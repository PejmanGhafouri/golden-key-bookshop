from django.shortcuts import render
from django.views.generic import ListView, DetailView
from accounts.models import User
from django.shortcuts import render, get_object_or_404

# from django.http import HttpResponse, JsonResponse, Http404
from .models import Book , Category
# Create your views here.
class BookList(ListView):
	queryset = Book.objects.published()
	paginate_by = 8


class BookDetail(DetailView):
	slug_url_kwarg = 'id'
	slug_field = 'id'

	def get_object(self):
		id = self.kwargs.get('id')
		return get_object_or_404(Book.objects.published(), id=id)
		

class BookPreview(DetailView):
	slug_url_kwarg = 'id'
	slug_field = 'id'
	
	def get_object(self):
		id = self.kwargs.get('id')
		return get_object_or_404(Book, id=id)


class CategoryList(ListView):
	paginate_by = 8
	template_name = 'shop/category_list.html'

	def get_queryset(self):
		global category
		slug = self.kwargs.get('slug')
		category = get_object_or_404(Category.objects.active(), slug=slug)
		return category.books.published()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['category'] = category
		return context

