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
    path("", WebObj.index, name="index"),
    path("oferta", WebObj.oferta, name="oferta"),
    path("send_question", WebObj.send_question, name="send_question"),
    path("leave_request", WebObj.leave_request, name="leave_request"),

    # Distributor
    path("distributor", DistributorObj.distributor, name="distributor"),
    path("distributor/auth", DistributorObj.auth, name="auth"),
    path("logout", DistributorObj.logout_view, name="logout_view"),
    path("distributor/upload_csv_file", DistributorObj.upload_csv_file, name="upload_csv_file"),
    path("distributor/profile", DistributorObj.profile, name="profile"),
    path("distributor/cars",  DistributorObj.cars, name="cars"),
    path("distributor/save_data", DistributorObj.save_data, name="save_data"),
    path("distributor/orders", DistributorObj.orders, name="orders"),
    path("distributor/upload_documents", DistributorObj.upload_documents, name="upload_documents"),
    path("distributor/distrib_entry_info", DistributorObj.distribEntryInfo, name="distrib_entry_info"),
    path("distributor/change_entry_status", DistributorObj.changeEntryStatus, name="change_entry_status"),

    # ===API urls===
    path("api/create_user/<int:user_id>/<str:first_name>/<str:username>",
         APIObj.CreateBotUserView.as_view(), name="create_bot_user"),
    path("api/set_name/<int:user_id>/<str:name>",
         APIObj.SetNameView.as_view(), name="set_name"),
    path("api/set_city/<int:user_id>/<str:city>",
         APIObj.SetCityView.as_view(), name="set_city"),
    path("api/check_phone/<int:user_id>",
         APIObj.CheckPhoneView.as_view(), name="check_phone"),
    path("api/set_phone/<int:user_id>/<int:phone>",
         APIObj.SetPhoneView.as_view(), name="set_phone"),
    path("api/get_all_marks/<int:min_price>/<int:max_price>",
         APIObj.GetAllMarksView.as_view(), name="get_all_marks"),
    path("api/get_all_bodies/<str:mark>/<int:min_price>/<int:max_price>",
         APIObj.GetAllBodiesView.as_view(), name="get_all_bodies"),
    path("api/get_all_fuel_types/<str:mark>/<str:body>/<int:min_price>/<int:max_price>",
         APIObj.GetAllFuelTypesView.as_view(), name="get_all_fuel_types"),
    path("api/find_car/<str:body>/<str:fuel_type>",
         APIObj.FindCarView.as_view(), name="find_car"),
    path("api/get_car_info/<int:id>",
         APIObj.GetCarInfoView.as_view(), name="get_car_info"),
    path("api/create_entry/<int:user_id>/<str:username>/<int:car_id>/<str:email>/<str:name>/<str:address>/<str:phone>",
         APIObj.CreateEntryView.as_view(), name="create_entry"),

    # ===Counts===
    path("get_cars/<int:min_price>/<int:max_price>/<str:mark>",
         WebObj.get_cars, name="get_cars"),
    path("get_cars_by_body/<int:min_price>/<int:max_price>/<str:mark>/<str:body>",
         WebObj.get_cars_by_body, name="get_cars_by_body"),
    path("get_cars_by_type_fuel/<int:min_price>/<int:max_price>/<str:mark>/<str:body>/<str:type_fuel>",
         WebObj.get_cars_by_type_fuel, name="get_cars_by_type_fuel"),
    path("get_cars_by_transmission/<int:min_price>/<int:max_price>/<str:mark>/<str:body>/<str:type_fuel>/<str:transmission>",
          WebObj.get_cars_by_transmission, name="get_cars_by_transmission"),
    path("get_cars_by_engine_volume/<int:min_price>/<int:max_price>/<str:mark>/<str:body>/<str:type_fuel>/<str:transmission>/<str:engine_volume>",
          WebObj.get_cars_by_engine_volume, name="get_cars_engine_volume")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
