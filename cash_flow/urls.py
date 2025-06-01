from django.urls import path

from cash_flow.apps import CashFlowConfig
from cash_flow.views import MainListView, CashFlowCreateView, CashFlowUpdateView, CashFlowDeleteView, \
    ReferenceBooksListView, ReferenceBooksCreateView, ReferenceBooksUpdateView, ReferenceBooksDeleteView

app_name = CashFlowConfig.name

urlpatterns = [
    path("", MainListView.as_view(), name="main"),
    path("create_cash_flow/", CashFlowCreateView.as_view(), name="create_cash_flow"),
    path("<int:pk>/update_cash_flow/", CashFlowUpdateView.as_view(), name="update_cash_flow"),
    path("<int:pk>/delete_cash_flow/", CashFlowDeleteView.as_view(), name="delete_cash_flow"),
    path("reference_books/", ReferenceBooksListView.as_view(), name="reference_books"),
    path("reference_books_cud/<int:pk>/<str:model>/", ReferenceBooksUpdateView.as_view(), name="reference_books_cud"),
    path("reference_books_cud/new/<str:model>/", ReferenceBooksCreateView.as_view(), name="reference_books_new"),
    path("reference_books_cud/delete/<int:pk>/<str:model>/", ReferenceBooksDeleteView.as_view(),
         name="reference_books_delete"),
]
