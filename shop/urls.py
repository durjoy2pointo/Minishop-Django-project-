from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    #=========================
    #      Product Views
    #=========================
    path('', views.index, name="index"),
    path('product/<int:pk>/', views.product_detail, name="product_detail"),
    path('shop/', views.shop_view, name='shop'),

    #=========================
    #      User Authentication
    #=========================
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    #=========================
    #      Cart and Checkout
    #=========================
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('buy-now/<int:pk>/', views.buy_now, name='buy_now'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),

    
    
    #=========================
    #      Address Views
    #=========================
    path('address/', views.add_address, name='add_address'),


    #=========================
    #      Static Pages
    #=========================
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('blog/', views.blog_view, name='blog'),

    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('order-history/',views.order_history,name='order_history'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
