from django.urls import path
from .views import (
	BookList,
	BookDetail,
	BookPreview,
	CategoryList,
)
app_name = 'shop'

urlpatterns = [
    path('', BookList.as_view(), name="home"),
	path('page/<int:page>', BookList.as_view(), name="home"),
	path('book/<uuid:id>', BookDetail.as_view(), name="detail"),
	path('preview/<uuid:id>', BookPreview.as_view(), name="preview"),
	path('category/<slug:slug>', CategoryList.as_view(), name="category"),
	path('category/<slug:slug>/page/<int:page>', CategoryList.as_view(), name="category"),
]