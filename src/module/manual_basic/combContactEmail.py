from src.models import *
from src.utils.constants import *
import pandas as pd

from src.utils.constants import temp_sales_dir
from django.db.models import Prefetch
import json


class combContactEmail:

    # def __init__(self, table_name):
    #     self.table_name = table_name
    #     self.hd_list = header_names.get(table_name)

    def create(self):
        contacts = Contact.objects.prefetch_related(
            Prefetch(
                'emails_con',
                queryset=Email.objects.filter(
                    account_id=models.F('account_id')),
                to_attr='emails'
            )
        )

        # Initialize an empty list to store the final output.
        output = []

        # Loop through each contact and construct the JSON structure.
        for contact in contacts:
            # Keep track of whether it's the first record for this contact.
            is_first_record = True

            for email in contact.emails:
                # Prepare the data for each record.
                record = {
                    "account_name": contact.account_name if is_first_record else "",
                    "account_phone": contact.account_phone if is_first_record else "",
                    "account_type": contact.account_type if is_first_record else "",
                    "account_description": contact.account_description if is_first_record else "",
                    "account_id": contact.account_id if is_first_record else "",
                    "account_source": contact.account_source if is_first_record else "",
                    "alpha_name": contact.alpha_name if is_first_record else "",
                    "billing_city": contact.billing_city if is_first_record else "",
                    "billing_country": contact.billing_country if is_first_record else "",
                    "billing_group": contact.billing_group if is_first_record else "",
                    "billing_state_province": contact.billing_state_province if is_first_record else "",
                    "billing_street": contact.billing_street if is_first_record else "",
                    "billing_zip_postal_Code": contact.billing_zip_postal_Code if is_first_record else "",
                    "canopy_currency": contact.canopy_currency if is_first_record else "",
                    "canopy_customer_code": contact.canopy_customer_code if is_first_record else "",
                    "canopy_customer_key": contact.canopy_customer_key if is_first_record else "",
                    "canopy_pricing_grp": contact.canopy_pricing_grp if is_first_record else "",
                    "canopy_vendor_code": contact.canopy_vendor_code if is_first_record else "",
                    "industry": contact.industry if is_first_record else "",
                    "ship_to_contact_name": contact.ship_to_contact_name if is_first_record else "",
                    "ship_to_display": contact.ship_to_display if is_first_record else "",
                    "shipping_city": contact.shipping_city if is_first_record else "",
                    "shipping_country": contact.shipping_country if is_first_record else "",
                    "shipping_state_province": contact.shipping_state_province if is_first_record else "",
                    "shipping_street": contact.shipping_street if is_first_record else "",
                    "shipping_zip_postal_code": contact.shipping_zip_postal_code if is_first_record else "",
                    "vendor_ship_from": contact.vendor_ship_from if is_first_record else "",
                    "website": contact.website if is_first_record else "",
                    "business_phone": email.business_phone,
                    "email": email.email,
                    "first_name": email.first_name,
                    "last_name": email.last_name,
                    "title": email.title,
                    "business_fax": email.business_fax,
                    "contact_cd": email.contact_cd,
                    "contact_display": email.contact_display,
                    "contact_id": email.contact_id,
                    "full_name": email.full_name,
                    "sms_opt_ou": email.sms_opt_ou
                }

                # Add this record to the output list.
                output.append(record)

                # Set `is_first_record` to False after the first email entry.
                is_first_record = False

        # Convert the output to JSON format with pretty printing.
        try:
            for _, row in enumerate(output):
                ContactEmail.objects.create(
                    account_name=row["account_name"],
                    account_phone=row["account_phone"],
                    account_type=row["account_type"],
                    account_description=row["account_description"],
                    account_id=row["account_id"],
                    account_source=row["account_source"],
                    alpha_name=row["alpha_name"],
                    billing_city=row["billing_city"],
                    billing_country=row["billing_country"],
                    billing_group=row["billing_group"],
                    billing_state_province=row["billing_state_province"],
                    billing_street=row["billing_street"],
                    billing_zip_postal_Code=row["billing_zip_postal_Code"],
                    canopy_currency=row["canopy_currency"],
                    canopy_customer_code=row["canopy_customer_code"],
                    canopy_customer_key=row["canopy_customer_key"],
                    canopy_pricing_grp=row["canopy_pricing_grp"],
                    canopy_vendor_code=row["canopy_vendor_code"],
                    industry=row["industry"],
                    ship_to_contact_name=row["ship_to_contact_name"],
                    ship_to_display=row["ship_to_display"],
                    shipping_city=row["shipping_city"],
                    shipping_country=row["shipping_country"],
                    shipping_state_province=row["shipping_state_province"],
                    shipping_street=row["shipping_street"],
                    shipping_zip_postal_code=row["shipping_zip_postal_code"],
                    vendor_ship_from=row["vendor_ship_from"],
                    website=row["website"],
                    business_phone=row["business_phone"],
                    email=row["email"],
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    title=row["title"],
                    business_fax=row["business_fax"],
                    contact_cd=row["contact_cd"],
                    contact_display=row["contact_display"],
                    contact_id=row["contact_id"],
                    full_name=row["full_name"],
                    sms_opt_ou=row["sms_opt_ou"]
                )
            return True
        except:
            return False
