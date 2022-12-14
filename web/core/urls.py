from django.urls import path, register_converter

from django.conf import settings
from django.conf.urls.static import static

from .views import *
from .converts import *

register_converter(FloatUrlParameterConverter, "float")
register_converter(BooleanUrlParameterConverter, "bool")

urlpatterns = [
    # ===WEB urls==
    # Main urls.
    path('', WebTemp.index, name='index'),
    path('oferta', WebTemp.oferta, name="oferta"),
    path('send_question', WebTemp.send_question, name='send_question'),
    path('leave_request', WebTemp.leave_request, name='leave_request'),

    # ===Distributor urls==
    path('distributor/', DistributorTemp.distributor, name="distributor"),
    path('distributor/auth', DistributorTemp.auth, name="auth"),
    path('logout', DistributorTemp.logout_view, name="logout_view"),
    path('distributor/upload_csv_file', DistributorTemp.upload_csv_file, name="upload_csv_file"),
    path('distributor/profile', DistributorTemp.profile, name="profile"),
    path('distributor/cars', DistributorTemp.cars, name="cars"),
    path('distributor/save_data', DistributorTemp.save_data, name="save_data"),
    path('distributor/orders', DistributorTemp.orders, name="orders"),
    path('distributor/upload_documents', DistributorTemp.upload_documents, name="upload_documents"),
    path('distributor/distrib_entry_info', DistributorTemp.distribEntryInfo, name="distrib_entry_info"),
    path('distributor/agreements', DistributorTemp.agreements, name='agreements'),
    path('distributor/car_increase', DistributorTemp.car_increase, name='car_increase'),
    path('distributor/car_decrease', DistributorTemp.car_decrease, name='car_decrease'),

    # ===API urls===
    path("api/create_user/<int:user_id>/<str:first_name>/<str:username>",
         APITemp.CreateBotUserView.as_view(), name="create_bot_user"),
    path("api/set_name/<int:user_id>/<str:name>",
         APITemp.SetNameView.as_view(), name="set_name"),
    path("api/set_city/<int:user_id>/<str:city>",
         APITemp.SetCityView.as_view(), name="set_city"),
    path("api/check_phone/<int:user_id>",
         APITemp.CheckPhoneView.as_view(), name="check_phone"),
    path("api/set_phone/<int:user_id>/<int:phone>",
         APITemp.SetPhoneView.as_view(), name="set_phone"),
    path("api/get_all_marks/<int:min_price>/<int:max_price>",
         APITemp.GetAllMarksView.as_view(), name="get_all_marks"),
    path("api/get_all_bodies/<str:mark>/<int:min_price>/<int:max_price>",
         APITemp.GetAllBodiesView.as_view(), name="get_all_bodies"),
    path("api/get_all_fuel_types/<str:mark>/<str:body>/<int:min_price>/<int:max_price>",
         APITemp.GetAllFuelTypesView.as_view(), name="get_all_fuel_types"),
    path("api/find_car/<str:body>/<str:fuel_type>",
         APITemp.FindCarView.as_view(), name="find_car"),
    path("api/get_car_info/<int:id>",
         APITemp.GetCarInfoView.as_view(), name="get_car_info"),
    path("api/create_entry/<int:user_id>/<str:username>/<int:car_id>/<str:email>/<str:name>/<str:address>/<str:phone>",
         APITemp.CreateEntryView.as_view(), name="create_entry"),

     # ===Dealer urls===
     path("dealer", DealerTemp.index, name="dealer_index"),

    # ===WEB urls (JS)==
    path("get_cars/<int:min_price>/<int:max_price>/<str:mark>",
         WebTemp.get_cars, name="get_cars"),
    path("get_cars_by_body/<int:min_price>/<int:max_price>/<str:mark>/<str:body>",
         WebTemp.get_cars_by_body, name="get_cars_by_body"),
    path("get_cars_by_type_fuel/<int:min_price>/<int:max_price>/<str:mark>/<str:body>/<str:type_fuel>",
         WebTemp.get_cars_by_type_fuel, name="get_cars_by_type_fuel"),
    path('get_cars_by_transmission/<int:min_price>/<int:max_price>/<str:mark>/'
          '<str:body>/<str:type_fuel>/<str:transmission>',
          WebTemp.get_cars_by_transmission, name="get_cars_by_transmission"),
    path('get_cars_by_engine_volume/<int:min_price>/<int:max_price>/<str:mark>/<str:body>/<str:type_fuel>'
         '/<str:transmission>/<str:engine_volume>',
          WebTemp.get_cars_by_engine_volume, name="get_cars_engine_volume"),

    path('mailru-verificationefe11e8fecf3da53.html', WebTemp.mailru_verification, name="mailru_verification")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
