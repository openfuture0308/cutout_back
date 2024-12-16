from . import views
from django.urls import path

urlpatterns = [
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('cutout/', views.CutOutView.as_view(), name='cutout-create'),
    path('cutout/<str:lotNum>/', views.CutOutView.as_view(), name='cutout-get'),
    path('plant_compare/', views.PlantCompareView.as_view(), name='plant_compare'),

    path("", views.index, name="index"),
    path("upload/", views.upload_excel, name="upload_excel"),
    # path("get_json_contacts/", views.get_json_contacts, name="get_json_contacts"),
    path("upload_sales/", views.upload_excel_salesforce,
         name="upload_excel_salesforce"),
    # display cutoutmap
    path(
        "upload_cutoutmap_excel/",
        views.upload_cutoutmap_excel,
        name="upload_cutoutmap_excel",
    ),
    path("data/<str:table_name>/", views.display_data, name="display_data"),
    # apis start
    # contact_email
    path("com_contact_email/", views.com_contact_email, name="com_contact_email"),
    # path("saveCutoutmaps/", views.save_cutoutmaps_view, name="saveCutoutmaps"),
    path("getCutoutmaps/", views.get_cutoutmaps, name="getCutoutmaps"),
    path("getCutout/", views.get_cutout, name="getCutout"),
    # apis end
    path("csv_price_upload/", views.csv_price_upload, name="csvPriceUpload"),
]
