from src.models import *
from src.utils.constants import *
import pandas as pd
import os
from io import BytesIO
import tempfile
import pyexcel as p

from src.utils.constants import temp_sales_dir


class salesforceExcel:

    def __init__(self, table_name):
        self.table_name = table_name
        self.hd_list = header_names.get(table_name)

    def removeNan(self, value):
        seriesRow = pd.Series(value)
        return seriesRow.where(pd.notnull(seriesRow), None)

    def create(self, file):
        os.makedirs(temp_sales_dir, exist_ok=True)
        temp_file_path = os.path.join(temp_sales_dir, file.name)
        df = pd.read_excel(file, header=None, engine="openpyxl")
        df = df.reset_index(drop=True)
        updated_data = df.drop(0)  # Drop the first row
        # Set the new header to be the second row
        updated_data.columns = updated_data.iloc[0]
        df = updated_data.drop(1)
        print(self.hd_list)
        for _, row in df.iterrows():
            row = self.removeNan(row)
            match self.table_name:
                case "contact":
                    Contact.objects.create(
                        account_name=row[self.hd_list[0]],
                        account_phone=row[self.hd_list[1]],
                        account_type=row[self.hd_list[2]],
                        account_description=row[self.hd_list[3]],
                        account_id=row[self.hd_list[4]],
                        account_source=row[self.hd_list[5]],
                        alpha_name=row[self.hd_list[6]],
                        billing_city=row[self.hd_list[7]],
                        billing_country=row[self.hd_list[8]],
                        billing_group=row[self.hd_list[9]],
                        billing_state_province=row[self.hd_list[10]],
                        billing_street=row[self.hd_list[11]],
                        billing_zip_postal_Code=row[self.hd_list[12]],
                        canopy_currency=row[self.hd_list[13]],
                        canopy_customer_code=str(
                            row[self.hd_list[14]]).split(".")[0],
                        canopy_customer_key=row[self.hd_list[15]],
                        canopy_pricing_grp=row[self.hd_list[16]],
                        canopy_vendor_code=row[self.hd_list[17]],
                        industry=row[self.hd_list[18]],
                        ship_to_contact_name=row[self.hd_list[19]],
                        ship_to_display=row[self.hd_list[20]],
                        shipping_city=row[self.hd_list[21]],
                        shipping_country=row[self.hd_list[22]],
                        shipping_state_province=row[self.hd_list[23]],
                        shipping_street=row[self.hd_list[24]],
                        shipping_zip_postal_code=row[self.hd_list[25]],
                        vendor_ship_from=row[self.hd_list[26]],
                        website=row[self.hd_list[27]]
                    )
                case "email":
                    contact, created = Contact.objects.get_or_create(
                        account_id=row[self.hd_list[5]])
                    Email.objects.create(
                        business_phone=row[self.hd_list[0]],
                        email=row[self.hd_list[1]],
                        first_name=row[self.hd_list[2]],
                        last_name=row[self.hd_list[3]],
                        title=row[self.hd_list[4]],
                        account_id=contact,
                        business_fax=row[self.hd_list[6]],
                        contact_cd=row[self.hd_list[7]],
                        contact_display=row[self.hd_list[8]],
                        contact_id=row[self.hd_list[9]],
                        full_name=row[self.hd_list[10]],
                        sms_opt_ou=row[self.hd_list[11]]
                    )
