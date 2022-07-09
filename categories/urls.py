from django.urls import path 
from . import views 
from django.views.generic import TemplateView
urlpatterns = [
    path('mine/', views.ManageProductListView.as_view(), name='manage_product_list'),
    path('create/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/category/<slug:category>/', TemplateView.as_view(), name='category_show'),
    path('<pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('<pk>/delete/',views.ProductDeleteView.as_view(), name='product_delete'),
    path('<pk>/subcategory/', views.ProductSubcategoryUpdateView.as_view(), name='product_subcategory_update'),
    path('subcategory/<int:subcategory_id>/content/<model_name>/create/', views.ContentCreateUpdateView.as_view(), name='subcategory_content_create'),
    path('subcategory/<int:subcategory_id>/content/<model_name>/<id>/', views.ContentCreateUpdateView.as_view(), name='subcategory_content_update'),
    path('subcategory/<int:subcategory_id>/', views.SubcategoryContentListView.as_view(), name='subcategory_content_list'),
    path('subcategory/order/', views.SubcategoryOrderView.as_view(), name='subcategory_order'),
    path('content/order/', views.ContentOrderView.as_view(), name='content_order'),
    path('category/<slug:category>/', views.ProductListView.as_view(), name='product_list_category'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),

     ]