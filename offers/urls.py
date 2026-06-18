from django.urls import path
from . import views

app_name = "offers"

urlpatterns = [
    # Player / Coach: received offers
    path("my/",              views.my_offers,       name="my_offers"),

    # Agent / Club: sent suggestions + compose
    path("suggestions/",    views.my_suggestions,  name="my_suggestions"),
    path("send/",           views.send_offer,       name="send_offer"),

    # Player / Coach: respond to an offer
    path("<int:pk>/respond/", views.respond_offer,  name="respond_offer"),
]
