from django.urls import path
from .views import (
    BookList,
    BookCreate,
    BookUpdate,
    BookDelete,
    Profile,
)
app_name = "account"

urlpatterns = [
    path('', BookList.as_view(), name="home"),
    path('book/create', BookCreate.as_view(), name="book-create"),
    path('book/update/<uuid:id>', BookUpdate.as_view(), name="book-update"),
	path('book/delete/<uuid:id>', BookDelete.as_view(), name="book-delete"),
    path('profile/', Profile.as_view(), name="profile"),

]