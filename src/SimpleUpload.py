from .models import *
from .forms import ExcelUploadForm
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
import pandas as pd
from django.db import transaction


field_name = {
    "program": [
        "name",
        "description",
    ],
    "contact": [
        "acc_name",
        "acc_phone",
        "acc_type",
        "acc_desc",
        "acc_id",
        "alpha_name",
        "bil_city",
        "bil_country",
        "bil_group",
        "bil_state",
        "bil_street",
        "bil_zip_postal_code",
        "cano_currency",
        "cano_customer_code",
        "cano_customer_key",
        "cano_vendor_code",
        "industry",
        "ship_to_contact_name",
        "ship_to_display",
        "shipping_city",
        "shipping_country",
        "shipping_state",
        "shipping_street",
        "shipping_zip_postal_code",
        "alias",
    ],
    "product": [
        "status",
        "code_crl",
        "description",
        "species",
        "product_type",
        "age_days",
        "freeze_down",
        "case_size",
        "bag_size",
        "ecoli_test",
        "pieces_box",
        "bags_box",
        "gtin12",
        "gtin14",
        "pack_type",
        "net_wgt",
        "growss_wt",
        "dim_l",
        "dim_w",
        "dim_h",
        "dim_um",
        "pallet_tier",
        "pallet_layers",
    ],
}

tbl_names = {
    "program": ["name", "description"],
    "contact": [
        "Account Name",
        "Account Phone",
        "Account Type",
        "Account Description",
        "Account ID",
        "Alpha Name",
        "Billing City",
        "Billing Country",
        "Billing Group",
        "Billing State/Province",
        "Billing Street",
        "Billing Zip/Postal Code",
        "Canopy Currency",
        "Canopy Customer Code",
        "Canopy Customer Key",
        "Canopy Vendor Code",
        "Industry",
        "Ship To Contact Name",
        "Ship-To-Display",
        "Shipping City",
        "Shipping Country",
        "Shipping State/Province",
        "Shipping Street",
        "Shipping Zip/Postal Code",
        "Alias",
    ],
    "product": [
        "STATUS ",
        "DISCRIPTION",
        "SPECIES",
        "PRODUCT_TYPE",
        "AGE DAYS",
        "FREEZE_DOWN",
        "CASE_SIZE",
        "BAG_SIZE",
        "ECOLI_TEST",
        "PIECES_BOX",
        "BAGS_BOX",
        "GTIN12",
        "GTIN14",
        "PACK_TYPE",
        "NET_WGT",
        "GROSS_WT",
        "DIM_L",
        "DIM_W",
        "DIM_H",
        "DIM_UM",
        "PALLET_TIER",
        "PALLET_LAYERS",
        "CODE_CRL",
    ],
}


# Helper function to map the dataframe to the correct model and fields
def insert_data(table_name, df):
    if table_name == "program":
        for _, row in df.iterrows():
            Program.objects.create(
                name=row[tbl_names["program"][0]],
                description=row[tbl_names["program"][1]],
            )
    elif table_name == "contact":
        for _, row in df.iterrows():
            Contact.objects.create(
                acc_name=row[tbl_names["contact"][0]],
                acc_phone=row[tbl_names["contact"][1]],
                acc_type=row[tbl_names["contact"][2]],
                acc_desc=row[tbl_names["contact"][3]],
                acc_id=row[tbl_names["contact"][4]],
                alpha_name=row[tbl_names["contact"][5]],
                bil_city=row[tbl_names["contact"][6]],
                bil_country=row[tbl_names["contact"][7]],
                bil_group=row[tbl_names["contact"][8]],
                bil_state=row[tbl_names["contact"][9]],
                bil_street=row[tbl_names["contact"][10]],
                bil_zip_postal_code=row[tbl_names["contact"][11]],
                cano_currency=row[tbl_names["contact"][12]],
                cano_customer_code=row[tbl_names["contact"][13]],
                cano_customer_key=row[tbl_names["contact"][14]],
                cano_vendor_code=row[tbl_names["contact"][15]],
                industry=row[tbl_names["contact"][16]],
                ship_to_contact_name=row[tbl_names["contact"][17]],
                ship_to_display=row[tbl_names["contact"][18]],
                shipping_city=row[tbl_names["contact"][19]],
                shipping_country=row[tbl_names["contact"][20]],
                shipping_state=row[tbl_names["contact"][21]],
                shipping_street=row[tbl_names["contact"][22]],
                shipping_zip_postal_code=row[tbl_names["contact"][23]],
                alias=row[tbl_names["contact"][24]],
            )
    elif table_name == "product":
        for _, row in df.iterrows():
            Product.objects.create(
                status=(True if row[tbl_names["product"][0]] == "ACTIVE" else False),
                code_crl=row[tbl_names["product"][22]],
                description=row[tbl_names["product"][1]],
                species=row[tbl_names["product"][2]],
                product_type=row[tbl_names["product"][3]],
                age_days=row[tbl_names["product"][4]],
                freeze_down=row[tbl_names["product"][5]],
                case_size=row[tbl_names["product"][6]],
                bag_size=row[tbl_names["product"][7]],
                ecoli_test=row[tbl_names["product"][8]],
                pieces_box=row[tbl_names["product"][9]],
                bags_box=row[tbl_names["product"][10]],
                gtin12=row[tbl_names["product"][11]],
                gtin14=row[tbl_names["product"][12]],
                pack_type=row[tbl_names["product"][13]],
                net_wgt=row[tbl_names["product"][14]],
                growss_wt=row[tbl_names["product"][15]],
                dim_l=row[tbl_names["product"][16]],
                dim_w=row[tbl_names["product"][17]],
                dim_h=row[tbl_names["product"][18]],
                dim_um=row[tbl_names["product"][19]],
                pallet_tier=row[tbl_names["product"][20]],
                pallet_layers=row[tbl_names["product"][21]],
            )


def simply_upload(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            table_name = form.cleaned_data["table_name"]
            excel_file = request.FILES["file"]

            # Read the Excel file into a DataFrame
            try:
                df = pd.read_excel(excel_file, engine="openpyxl")
            except Exception as e:
                return render(
                    request, "error.html", {"message": "Invalid file format."}
                )

            # Check if the columns in the DataFrame match the model fields
            required_columns = tbl_names.get(table_name)
            for col in required_columns:
                # if not all(col in df.columns for col in required_columns):
                if not col in df.columns:
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
                    insert_data(table_name, df)
            except Exception as e:
                return render(request, "error.html", {"message": str(e)})

            return redirect("display_data", table_name=table_name)
    else:
        form = ExcelUploadForm()

    return render(request, "upload.html", {"form": form})


def simply_display(request, table_name):
    if table_name == "program":
        data = Program.objects.all()
        field_nam = field_name.get("program")
        header_nam = tbl_names.get("program")
    elif table_name == "contact":
        data = Contact.objects.all()
        field_nam = field_name.get("contact")
        header_nam = tbl_names.get("contact")
    elif table_name == "product":
        data = Product.objects.all()
        field_nam = field_name.get("product")
        header_nam = tbl_names.get("product")
    else:
        return render(
            request, "error.html", {"message": "Invalid table name selected."}
        )
    rows = []
    for row in data:
        row_dict = model_to_dict(row)

        # Remove the first key-value pair (i.e., the first column)
        first_key = next(iter(row_dict))  # Get the first key
        row_dict.pop(first_key)  # Remove the first key-value pair

        rows.append(row_dict)

    return {
        "rows": rows,
        "field_nam": field_nam,
        "header_nam": header_nam,
        "table_name": table_name,
    }
