from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from shop.models import Book

class FieldsMixin():
	def dispatch(self, request, *args, **kwargs):
		self.fields = [
			"title", "book_author", "category",
			"description", "thumbnail", "publish","price",
			"is_free","book_available", "status",
		]
		if request.user.is_superuser:
			self.fields.append("author")
		return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
	def form_valid(self, form):
		if self.request.user.is_superuser:
			form.save()
		else:
			self.obj = form.save(commit=False)
			self.obj.author = self.request.user
			if not self.obj.status == 'i':
				self.obj.status = 'd'
		return super().form_valid(form)


class AuthorAccessMixin():
	def dispatch(self, request, id, *args, **kwargs):
		book = get_object_or_404(Book, id=id)
		if book.author == request.user and book.status in ['b', 'd'] or\
		request.user.is_superuser:
			return super().dispatch(request, *args, **kwargs)
		else:
			raise Http404("You can't see this page.")


class AuthorsAccessMixin():
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.is_superuser or request.user.is_author:
				return super().dispatch(request, *args, **kwargs)
			else:
				return redirect("shop:home")
		else:
			return redirect("login")


class SuperUserAccessMixin():
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_superuser:
			return super().dispatch(request, *args, **kwargs)
		else:
			raise Http404("You can't see this page.")