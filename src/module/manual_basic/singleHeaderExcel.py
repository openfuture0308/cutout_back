from src.models import *
from src.utils.constants import *
import pandas as pd
from datetime import datetime
import re

currency_items = ["US", "VA", "CAN", "EU"]
plant_fields = ["CODE_CRL", "CODE_PFF", "CODE_CPM", "CODE_MR",
                "CODE_CFS", "CODE_BMP", "CODE_RMNM", "CODE_SKFP", "CODE_NF"]
plant_list = ["CRL", "PFF", "CPM", "MR",
              "CFS", "BMP", "RMNM", "SKFP", "NF"]

nonDot = [
    "CODE_UID",
    "CODE_CRL",
    "STATUS ",
    "CODE_PFF",
    "PROGRAM",
    "CODE_PFFshort",
    "CODE_CPM",
    "CODE_MR",
    "CODE_CFS",
    "CODE_BMP",
    "CODE_RMNM",
    "CODE_SKFP",
    "CODE_MCF",
    "CODE_NF",]


class singleHeaderExcel:

    def __init__(self, table_name=None, file_name=None):
        self.table_name = table_name
        self.file_name = file_name
        self.hd_list = header_names.get(table_name)

    def dicCheckValue(self, value):
        seriesRow = pd.Series(value)
        row = seriesRow.where(pd.notnull(seriesRow), None)
        processed_values = {}
        for index, header in enumerate(self.hd_list):
            if len(str(row[header]).split(".")) > 1 and header in nonDot:
                processed_values[header] = str(row[header]).split(".")[0]
            else:
                processed_values[header] = row[header]
        return processed_values

    def removeNan(self, value):
        seriesRow = pd.Series(value)
        return seriesRow.where(pd.notnull(seriesRow), None)

    def insert_data(self, df):
        match self.table_name:
            case "program":
                for _, row in df.iterrows():
                    ProgramData.objects.create(
                        name=row[self.hd_list[0]],
                        description=row[self.hd_list[1]]
                    )
            case "contact":
                Contact.objects.all().delete()
                for _, row in df.iterrows():
                    row = self.removeNan(row)
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
                Email.objects.all().delete()
                for index, row in df.iterrows():
                    row = self.removeNan(row)
                    Email.objects.create(
                        business_phone=row[self.hd_list[0]],
                        email=row[self.hd_list[1]],
                        first_name=row[self.hd_list[2]],
                        last_name=row[self.hd_list[3]],
                        title=row[self.hd_list[4]],
                        account_id=row[self.hd_list[5]],
                        business_fax=row[self.hd_list[6]],
                        contact_cd=row[self.hd_list[7]],
                        contact_display=row[self.hd_list[8]],
                        contact_id=row[self.hd_list[9]],
                        full_name=row[self.hd_list[10]],
                        sms_opt_ou=row[self.hd_list[11]]
                    )
            case "contact_email":
                ContactEmail.objects.all().delete()
                for index, row in df.iterrows():
                    row = self.removeNan(row)
                    ContactEmail.objects.create(
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
                        website=row[self.hd_list[27]],

                        business_phone=row[self.hd_list[0]],
                        email=row[self.hd_list[1]],
                        first_name=row[self.hd_list[2]],
                        last_name=row[self.hd_list[3]],
                        title=row[self.hd_list[4]],
                        business_fax=row[self.hd_list[6]],
                        contact_cd=row[self.hd_list[7]],
                        contact_display=row[self.hd_list[8]],
                        contact_id=row[self.hd_list[9]],
                        full_name=row[self.hd_list[10]],
                        sms_opt_ou=row[self.hd_list[11]]
                    )
            case "product_manual":
                for _, row in df.iterrows():
                    rowRe = self.dicCheckValue(row)
                    product = ProductManual.objects.create(
                        code_uid=rowRe[self.hd_list[0]],
                        code_crl=rowRe[self.hd_list[1]],
                        status=rowRe[self.hd_list[2]],
                        code_pff=rowRe[self.hd_list[3]],
                        program=rowRe[self.hd_list[4]],
                        code_pffshort=rowRe[self.hd_list[5]],
                        code_cpm=rowRe[self.hd_list[6]],
                        code_mr=rowRe[self.hd_list[7]],
                        code_cfs=rowRe[self.hd_list[8]],
                        code_bmp=rowRe[self.hd_list[9]],
                        code_rmnm=rowRe[self.hd_list[10]],
                        code_skfp=rowRe[self.hd_list[11]],
                        code_mcf=rowRe[self.hd_list[12]],
                        code_nf=rowRe[self.hd_list[13]],
                        description=rowRe[self.hd_list[14]],
                        cut_type=rowRe[self.hd_list[15]],
                        species=rowRe[self.hd_list[16]],
                        product_type=rowRe[self.hd_list[17]],
                        eu_identity=rowRe[self.hd_list[18]],
                        age_days=rowRe[self.hd_list[19]],
                        freeze_down=rowRe[self.hd_list[20]],
                        case_size=rowRe[self.hd_list[21]],
                        bag_size=rowRe[self.hd_list[22]],
                        ecoli_test=rowRe[self.hd_list[23]],
                        pieces_box=rowRe[self.hd_list[24]],
                        bags_box=rowRe[self.hd_list[25]],
                        pff_gtin=rowRe[self.hd_list[26]],
                        gtin12=rowRe[self.hd_list[27]],
                        gtin14=rowRe[self.hd_list[28]],
                        notes=rowRe[self.hd_list[29]]
                    )

            case "product":
                for _, row in df.iterrows():
                    programs1 = []
                    plant1 = []
                    rowRe = self.dicCheckValue(row)
                    listProgram = str(rowRe["PROGRAMS"]).strip().split(
                        ",") if rowRe["PROGRAMS"] is not None else []
                    for i, item in enumerate(plant_fields):
                        plant_code = rowRe.get(plant_fields[i])
                        if plant_code is not None:
                            contactForPlant, created = Contact.objects.get_or_create(
                                account_description=plant_list[i])
                            plant1.append(
                                {"plant": contactForPlant, "plant_code": plant_code})
                    for code in listProgram:
                        program, created = ProgramData.objects.get_or_create(
                            name=code)
                        programs1.append(program)
                    product1 = Product.objects.create(
                        code_uid=rowRe[self.hd_list[0]],
                        code_crl=rowRe[self.hd_list[1]],
                        status=rowRe[self.hd_list[2]],
                        code_pff=rowRe[self.hd_list[3]],
                        code_pffshort=rowRe[self.hd_list[5]],
                        code_cpm=rowRe[self.hd_list[6]],
                        code_mr=rowRe[self.hd_list[7]],
                        code_cfs=rowRe[self.hd_list[8]],
                        code_bmp=rowRe[self.hd_list[9]],
                        code_rmnm=rowRe[self.hd_list[10]],
                        code_skfp=rowRe[self.hd_list[11]],
                        code_mcf=rowRe[self.hd_list[12]],
                        code_nf=rowRe[self.hd_list[13]],
                        description=rowRe[self.hd_list[14]],
                        cut_type=rowRe[self.hd_list[15]],
                        species=rowRe[self.hd_list[16]],
                        product_type=rowRe[self.hd_list[17]],
                        eu_identity=rowRe[self.hd_list[18]],
                        age_days=rowRe[self.hd_list[19]],
                        freeze_down=rowRe[self.hd_list[20]],
                        case_size=rowRe[self.hd_list[21]],
                        bag_size=rowRe[self.hd_list[22]],
                        ecoli_test=rowRe[self.hd_list[23]],
                        pieces_box=rowRe[self.hd_list[24]],
                        bags_box=rowRe[self.hd_list[25]],
                        pff_gtin=rowRe[self.hd_list[26]],
                        gtin12=rowRe[self.hd_list[27]],
                        gtin14=rowRe[self.hd_list[28]],
                        notes=rowRe[self.hd_list[29]]
                    )
                    if programs1:
                        product1.programs.set(programs1)
                    if plant1:
                        for plant in plant1:
                            ProductPlant.objects.create(
                                plant_id=plant["plant"],
                                product_id=product1,
                                code=plant["plant_code"]
                            )

            case "slaughter_rep":
                for _, row in df.iterrows():
                    rowRe = self.dicCheckValue(row)
                    print(rowRe)
                    if rowRe[self.hd_list[0]] == None:
                        continue
                    SlaughterReportsManual.objects.create(
                        animal_pk=rowRe[self.hd_list[0]],
                        animal_iden=rowRe[self.hd_list[1]],
                        slaughter_date=datetime.strptime(str(rowRe[self.hd_list[2]]).split('.')[
                                                         0], "%Y-%m-%d %H:%M:%S"),
                        owner=rowRe[self.hd_list[3]],
                        shipper=rowRe[self.hd_list[4]],
                        live_weight=float(
                            str(rowRe[self.hd_list[5]]).replace('kg', '').strip()),
                        hot_weight=float(
                            str(rowRe[self.hd_list[6]]).replace('kg', '').strip()),
                        cold_weight=rowRe[self.hd_list[7]],
                        age=rowRe[self.hd_list[8]],
                        receiving_order_id=rowRe[self.hd_list[9]],
                        condemn_flag=rowRe[self.hd_list[10]],
                        lot_number=rowRe[self.hd_list[11]],
                        species=rowRe[self.hd_list[12]],
                        sex=rowRe[self.hd_list[13]],
                        manifest_iden=rowRe[self.hd_list[14]],
                        grading=rowRe[self.hd_list[15]],
                        csf_date=datetime.strptime(str(rowRe[self.hd_list[16]]).split('.')[
                                                   0], "%Y-%m-%d %H:%M:%S"),
                    )

            case "price_csv_manual":
                for row in df:
                    row = row.decode("utf-8").strip()
                    code_crl, cost_str = row.split("\t")
                    price = float(cost_str.replace("$", ""))
                    PriceManual.objects.create(
                        isactive_flag=True,
                        code_crl=code_crl,
                        price=price,
                    )

            case "price":
                match = re.search(r"\d{8}", self.file_name)
                pattern = r"(" + "|".join(currency_items) + r")"
                match_cur = re.search(pattern, self.file_name)
                cur_unit_match = match_cur.group(0) if match_cur else None
                cur_unit = None
                file_name = None
                match cur_unit_match:
                    case "US":
                        cur_unit = "USD"
                        file_name = "US_COST"
                    case "CAN":
                        cur_unit = "CAD"
                        if "fin" in self.file_name.lower():
                            file_name = "CAN_FIN_COST"
                        else:
                            file_name = "CAN_COST"
                    case "VA":
                        cur_unit = "CAD"
                        file_name = "VA_CAN_COST"
                    case "EU":
                        cur_unit = "EURO"
                        file_name = "EU_COST"
                    case _:
                        cur_unit = None
                        file_name = None
                date = str(datetime.strptime(match.group(
                    0), "%Y%m%d").date()) if match else None
                for row in df:
                    row = row.decode("utf-8").strip()
                    if not row:
                        continue
                    code_crl, cost_str = row.split("\t")
                    price = float(cost_str.replace("$", ""))
                    code_crl = code_crl.strip().replace("-", ".")
                    try:
                        if Price.objects.filter(
                            code_crl=code_crl,
                            price=price,
                            cur_unit=cur_unit,
                            eft_date=date
                        ):
                            continue
                        else:
                            Price.objects.get_or_create(
                                isactive="False",
                                code_crl=code_crl,
                                price=price,
                                cur_unit=cur_unit,
                                eft_date=date,
                                file_name=file_name
                            )
                    except:
                        continue

            case "harvest_report":
                for _, row in df.iterrows():
                    row = self.removeNan(row)
                    HarvestReport.objects.create(
                        date=row[self.hd_list[0]],
                        plant=row[self.hd_list[1]],
                        year=row[self.hd_list[2]],
                        period=row[self.hd_list[3]],
                        quarter=row[self.hd_list[4]],
                        location=row[self.hd_list[5]],
                        producer_id=row[self.hd_list[6]],
                        producer_owner=row[self.hd_list[7]],
                        count=row[self.hd_list[8]],
                        m_utm=row[self.hd_list[9]],
                        m_otm=row[self.hd_list[10]],
                        f_utm=row[self.hd_list[11]],
                        f_otm=row[self.hd_list[12]],
                        f_cow=row[self.hd_list[13]],
                        m_a1=row[self.hd_list[14]],
                        m_a2=row[self.hd_list[15]],
                        m_a3=row[self.hd_list[16]],
                        m_a4=row[self.hd_list[17]],
                        m_b1=row[self.hd_list[18]],
                        m_b2=row[self.hd_list[19]],
                        m_b3=row[self.hd_list[20]],
                        m_d1=row[self.hd_list[21]],
                        m_d2=row[self.hd_list[22]],
                        m_d3=row[self.hd_list[23]],
                        f_a1=row[self.hd_list[24]],
                        f_a2=row[self.hd_list[25]],
                        f_a3=row[self.hd_list[26]],
                        f_a4=row[self.hd_list[27]],
                        f_b1=row[self.hd_list[28]],
                        f_b2=row[self.hd_list[29]],
                        f_b3=row[self.hd_list[30]],
                        f_d1=row[self.hd_list[31]],
                        f_d2=row[self.hd_list[32]],
                        f_d3=row[self.hd_list[33]],
                        prior_yrs_b_h=row[self.hd_list[34]],
                        prior_yrs_mature=row[self.hd_list[35]],
                        total_avglive_lbs=row[self.hd_list[36]],
                        plant_avglive_lbs=row[self.hd_list[37]],
                        live_helper=row[self.hd_list[38]],
                        live_bull_lbs_helper=row[self.hd_list[39]],
                        live_heifers_lbs_helper=row[self.hd_list[40]],
                        live_cow_lbs_helper=row[self.hd_list[41]],
                        total_hhw_lbs=row[self.hd_list[42]],
                        avg_hhw_lbs=row[self.hd_list[43]],
                        hhw_helper=row[self.hd_list[44]],
                        hhw_bull_lbs_helper=row[self.hd_list[45]],
                        hhw_hei_lbs_helper=row[self.hd_list[46]],
                        hhw_cow_lbs_helper=row[self.hd_list[47]],
                        yield_to_plant_pcent=row[self.hd_list[48]],
                        shrink_helper=row[self.hd_list[49]],
                        avg_dol_per_lbs=row[self.hd_list[50]],
                        dol_per_lb_helper=row[self.hd_list[51]],
                        avg_dol_per_hd=row[self.hd_list[52]],
                        dol_per_hd_helper=row[self.hd_list[53]],
                        week=row[self.hd_list[54]],
                        pre_year_prod_per_owner=row[self.hd_list[55]],
                    )

            case _:
                print("The table_name doesn't matter, what matters is solving problems.")
