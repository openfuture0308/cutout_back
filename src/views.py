from django.core.serializers import serialize
from django.db import transaction
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

import json
import os
from rest_framework.decorators import api_view
from .models import *
from .utils.constants import *
import openpyxl
import pandas as pd
from .forms import ExcelUploadForm, CSVUploadForm, CutOutMapUploadForm, ACutOutUploadForm, SalesForceExcelUploadForm
from .module.automation.CutoutmapsModule import CutoutmapsModule
from .module.automation.PriceCsvMapsModule import PriceCsvMapsModule
from .module.automation.PlantCompareModule import PlantCompareModule
from .module.manual_basic.singleHeaderExcel import singleHeaderExcel
from .module.manual_basic.salesforceExcel import salesforceExcel
from .module.manual_basic.combContactEmail import combContactEmail
import traceback


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.http import JsonResponse
import datetime
# Create your views here.


class CutOutView(APIView):

    permission_classes = (IsAuthenticated, )
    cutoutmapsModule = CutoutmapsModule()

    def get(self, request, *args, **kwargs):
        lot_number = kwargs.get("lotNum", "")
        # lot_number = request.parser_context["kwargs"]["lotNum"]
        try:
            if lot_number == "":
                cutout = list(CutOutMap.objects.all().values())
            else:
                cutout = list(CutOutMap.objects.filter(
                    lot_number=lot_number).values())
        except CutOutMap.DoesNotExist:
            return HttpResponse(
                json.dumps({"msg": "Invalid Company"}),
                status=400,
                content_type="application/json",
            )
        values_list = []

        for item in cutout:
            # Convert date to string and exclude the first two fields
            item = {key: (str(value) if isinstance(
                value, (datetime.date, datetime.datetime)) else value) for key, value in item.items()}
            # Exclude first two values
            values_list.append(list(item.values())[2:])
        print(values_list)
        return HttpResponse(
            json.dumps({"msg": values_list}),
            status=200,
            content_type="application/json",
        )

    def post(self, request):
        file = request.FILES.get("cutout")
        data = {
            "plant_name": request.POST.get("plant_name"),
            "bull_amount": request.POST.get("bull_amount"),
            "heifer_amount": request.POST.get("heifer_amount"),
            "cow_amount": request.POST.get("cow_amount"),
            "eu_rate": request.POST.get("eu_rate"),
        }
        try:
            result = self.cutoutmapsModule.save(file, data)
            return HttpResponse(
                json.dumps({"msg": result}),
                status=200,
                content_type="application/json",)

        except Exception:
            print(traceback.format_exc())
            return HttpResponse(
                json.dumps({"msg": "Check your excel file!"}),
                status=500,
                content_type="application/json",
            )

    def put(self, request):
        if request.method == "PUT":
            data = request.data.get("data")
            cutoutmapsModule = CutoutmapsModule()
            try:
                cutoutmapsModule.update(data[1:])
            except Exception:
                print(traceback.format_exc())
                return HttpResponse(
                    json.dumps({"msg": 0}),
                    status=500,
                    content_type="application/json",
                )
            return HttpResponse(
                json.dumps({"msg": 1}),
                status=200,
                content_type="application/json",)

    def delete(self, request, *args, **kwargs):
        lot_number = request.parser_context["kwargs"]["lotNum"]
        try:
            # Filter objects with the given lot_number and delete them
            deleted_count, _ = CutOutMap.objects.filter(
                lot_number=lot_number).delete()

            # Check if any records were deleted
            if deleted_count > 0:
                return HttpResponse(
                    json.dumps({"msg": 1}),
                    status=200,
                    content_type="application/json",
                )
            else:
                return HttpResponse(
                    json.dumps({"msg": 0}),
                    status=200,
                    content_type="application/json",
                )

        except Exception as e:
            print(traceback.format_exc())
            return HttpResponse(
                json.dumps({"msg": 0, "error": str(e)}),
                status=500,
                content_type="application/json",
            )


class PlantCompareView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        return True

    def post(self, request):
        start_d = datetime.datetime.strptime(
            request.data["start_date"], "%m-%d-%Y").strftime("%Y-%m-%d")
        end_d = datetime.datetime.strptime(
            request.data["end_date"], "%m-%d-%Y").strftime("%Y-%m-%d")
        period = {"start_d": start_d,
                  "end_d": end_d}
        try:
            PlantCompareModule1 = PlantCompareModule(period)
            result = PlantCompareModule1.get_report()
            return JsonResponse({"msg": result}, status=200)

        except Exception:
            print(traceback.format_exc())
            return HttpResponse(
                json.dumps({"msg": []}),
                status=500,
                content_type="application/json",
            )


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def index(request):
    return HttpResponse(
        json.dumps({"msg": "You are connected!"}),
        status=200,
        content_type="application/json",)


@api_view(["GET"])
def com_contact_email(request):
    combContactEmail1 = combContactEmail()
    result = combContactEmail1.create()
    if result:
        return render(request, "index.html")
    else:
        return render(
            request,
            "error.html",
            {
                "message": "Invalid columns in the Excel file."
            }
        )


def csv_price_upload(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            # Extract the deck name from the filename by removing numbers
            PriceCsvMaps = PriceCsvMapsModule(file)
            PriceCsvMaps.handle_uploaded_file()
            return render(request, "csvPriceUploadSuccess.html")
    else:
        form = CSVUploadForm()
    return render(request, "csvPriceUpload.html", {"form": form})


def get_cutout(request):
    mailid = request.GET.get("mailid")

    if mailid:
        # Define the file path based on the mailid
        file_path = f"temp/mail_{mailid}.xlsx"

        # Check if the file exists in the given location
        if os.path.exists(file_path):
            # Open the file and prepare it for download
            with open(file_path, "rb") as excel_file:
                # Create an HttpResponse object and attach the file
                response = HttpResponse(
                    excel_file.read(),
                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
                # Set the appropriate content-disposition header to force download
                response["Content-Disposition"] = (
                    f"attachment; filename=mail_{mailid}.xlsx"
                )
                return response
        else:
            # If the file doesn't exist, raise a 404 error
            raise Http404(f"File mail_{mailid}.xlsx does not exist.")

    # If mailid is not provided, return a bad request response
    return HttpResponse("Please provide a mailid.", status=400)


def get_cutoutmaps(request):
    # Get the mail ID from the request
    mailid = request.GET.get("mailid")

    # If the mailid is provided, query the CutOutMap objects
    if mailid:
        # Query the database for CutOutMap objects filtered by mail_id
        cutout_maps = CutOutMap.objects.filter(mail_id=mailid)

        # Create an in-memory Excel workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "CutOut Maps"

        # Define the first header row (technical column names)
        headers = cutout_maps.headers
        # Define the second row (descriptions)
        descriptions = cutout_maps.descriptions

        # Add the first header row to the worksheet
        ws.append(headers)

        # Add the second row (descriptive headers)
        ws.append(descriptions)

        # Add the data from the CutOutMap objects
        for cutout in cutout_maps:
            ws.append(
                [
                    cutout.date,
                    cutout.lot_number,
                    cutout.hd_amount,
                    cutout.type_grade,
                    cutout.lw_in_kg,
                    cutout.lw_avg_kg,
                    cutout.lw_avg_lbs,
                    cutout.hhw_in_kg,
                    cutout.hhw_avg_kg_yield,
                    cutout.hhw_avg_lbs,
                    cutout.yield_dress,
                    cutout.cw_in_kg,
                    cutout.cw_shrink,
                    cutout.cw_avg_kg,
                    cutout.cw_avg_lbs,
                    cutout.live_dollar_per_kg,
                    cutout.yield_cut,
                    cutout.hhw_dollar_per_kg,
                    cutout.hhw_avg_kg_yield,
                    cutout.hhw_avg_lbs_yield,
                    cutout.yield_meat,
                    cutout.bulls_amount,
                    cutout.heifers_amount,
                    cutout.cows_amount,
                    cutout.mature,
                    cutout.hhw_hd_dollar_kg,
                    cutout.cost_hhw,
                    cutout.cost_plant_hd,
                    cutout.cost_plant,
                    cutout.cost_fob,
                    cutout.cost_sga_lb,
                    cutout.cost_sga,
                    cutout.cost_kill,
                    cutout.sell_primal,
                    cutout.sell_offal,
                    cutout.sell_profit,
                    cutout.sell_primal_hd,
                    cutout.sell_offal_hd,
                    cutout.margin,
                    cutout.sell_hd,
                    cutout.cost_hd,
                    cutout.profit_hd,
                    cutout.eu_fx,
                    cutout.primal_kgs,
                    cutout.primal_avg_dollar_kg,
                    cutout.kgs_hd_offal,
                    cutout.yield_offals,
                    cutout.offal_kgs,
                    cutout.offal_avg_dollar_kg,
                    cutout.code_crl,
                    cutout.sell_kg,
                    cutout.kgs_total,
                    cutout.kgs_hd,
                    cutout.value_total,
                    cutout.wt_percent_cuts,
                    cutout.value_percent,
                    cutout.cogs_kg,
                    cutout.cogs,
                ]
            )  # Add more fields if necessary

        # Create an HttpResponse object with the proper Excel file MIME type
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = (
            f"attachment; filename=CutOutMaps_{mailid}.xlsx"
        )

        # Save the Excel file into the response
        wb.save(response)

        return response

    # Return some response if mailid is not provided
    return HttpResponse("Please provide a mailid.", status=400)


@csrf_exempt
def upload_excel(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            table_name = form.cleaned_data["table_name"]
            excel_file = request.FILES["file"]
            file_name = excel_file.name
            # Read the Excel file into a DataFrame
            try:
                if table_name == "price_csv_manual" or table_name == "price":
                    df = excel_file.readlines()[1:]
                else:
                    df = pd.read_excel(excel_file, engine="openpyxl")
            except Exception as e:
                return render(
                    request, "error.html", {"message": "Invalid file format."}
                )
            # Check if the columns in the DataFrame match the model fields
            required_columns = header_names.get(table_name)
            df.columns = df.columns.str.strip()
            for col in required_columns:
                if not col in df.columns:
                    print(col)
            if not table_name == "price_csv_manual" and not table_name == "price":
                if not all(col in df.columns for col in required_columns):
                    return render(
                        request,
                        "error.html",
                        {
                            "message": f"Invalid columns in the Excel file. Expected columns: {required_columns}"
                        },
                    )

            # Insert data into the appropriate table
            try:
                with transaction.atomic():
                    singleHeaderExcel1 = singleHeaderExcel(
                        table_name, file_name)
                    singleHeaderExcel1.insert_data(df)
            except Exception as e:
                return render(request, "error.html", {"message": str(e)})

            return redirect("display_data", table_name=table_name)
    else:
        form = ExcelUploadForm()

    return render(request, "upload.html", {"form": form})


# upload data from salesforce(Contact)
@csrf_exempt
def upload_excel_salesforce(request):
    if request.method == "POST":
        form = SalesForceExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            table_name = form.cleaned_data["table_name"]
            file = request.FILES["file"]
            salesExcel = salesforceExcel(table_name)
            salesExcel.create(file)
            return redirect("display_data", table_name=table_name)
    else:
        form = SalesForceExcelUploadForm()

    return render(request, "upload.html", {"form": form})


@csrf_exempt
def upload_cutoutmap_excel(request):
    if request.method == "POST" and request.FILES["file"]:
        form = CutOutMapUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES["file"]
            # Create a FileSystemStorage instance
            fs = FileSystemStorage(location="temp/")
            mail_count = 0
            if not CutOutMail.objects.exists():
                mail_count = 1
            else:
                latest_entry = CutOutMail.objects.latest(
                    "id"
                )  # Get the latest entry by 'id'
                mail_count = latest_entry.id + 1

            # Save the file manually
            filename = fs.save(
                "./mail_" + str(mail_count) + ".xlsx", excel_file)
            try:
                cutoutmapsModule1 = CutoutmapsModule()
                cutoutmapsModule1.save(mail_count)
                return redirect("display_data", table_name="CutOutMap")
            except Exception as e:
                return render(request, "error.html", {"message": str(e)})
    else:
        form = CutOutMapUploadForm()

    return render(request, "upload.html", {"form": form})


@csrf_exempt
def display_data(request, table_name):
    match table_name:
        case "program":
            data = ProgramData.objects.all()
            header_nam = header_names.get("program")
        case "contact":
            data = Contact.objects.all()
            header_nam = header_names.get("contact")
        case "email":
            data = Email.objects.all()
            header_nam = header_names.get("price_csv_manual")
        case "product":
            data = Product.objects.all()
            header_nam = header_names.get("product")
        case "CutOutMap":
            data = CutOutMap.objects.all()
            header_nam = header_names.get("CutOutMap")
        case "product_manual":
            data = ProductManual.objects.all()
            header_nam = header_names.get("product_manual")
        case "slaughter_rep":
            data = SlaughterReportsManual.objects.all()
            header_nam = header_names.get("slaughter_rep")
        case "price_csv_manual":
            data = PriceManual.objects.all()
            header_nam = header_names.get("price_csv_manual")
        case "price":
            # data = Price.objects.all()
            data = []
            header_nam = header_names.get("price")
        case "harvest_report":
            # data = Price.objects.all()
            data = []
            header_nam = header_names.get("harvest_report")
        case _:
            return render(
                request, "error.html", {
                    "message": "Invalid table name selected."}
            )
    rows = []
    for row in data:
        row_dict = model_to_dict(row)

        # Remove the first key-value pair (i.e., the first column)
        first_key = next(iter(row_dict))  # Get the first key
        row_dict.pop(first_key)  # Remove the first key-value pair

        rows.append(row_dict)

    return render(
        request,
        "display.html",
        {
            "data": rows,
            "header_name": header_nam,
            "table_name": table_name,
        },
    )
