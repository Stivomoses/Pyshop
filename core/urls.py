from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('new-arrivals', views.new_arrivals, name='new_arrivals'),
    path('top-discounts', views.top_discounts, name='top_discounts'),
    path('bargainable-prices', views.bargainable_prices, name='bargainable_prices'),
    path('products/<int:product_id>',
         views.product_details, name='product_details'),
    path('brands', views.brands, name='brands'),
    path('brands/<int:brand_id>', views.brand_products, name='brand_products'),
    path('brands/<int:brand_id>/<int:product_id>',
         views.brand_products_details, name='brand_products_details'),
    path('add-product', views.add_product, name='add_product')
]
