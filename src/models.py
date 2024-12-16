from django.db import models
from django.utils import timezone


class Contact(models.Model):
    account_name = models.CharField(max_length=50, null=True)
    account_phone = models.CharField(max_length=50, null=True)
    account_type = models.CharField(max_length=50, null=True)
    account_description = models.CharField(max_length=50, null=True)
    account_id = models.CharField(
        max_length=50, null=True, db_column="account_id")
    account_source = models.CharField(max_length=50, null=True)
    alpha_name = models.CharField(max_length=50, null=True)
    billing_city = models.CharField(max_length=50, null=True)
    billing_country = models.CharField(max_length=50, null=True)
    billing_group = models.CharField(max_length=50, null=True)
    billing_state_province = models.CharField(max_length=50, null=True)
    billing_street = models.CharField(max_length=50, null=True)
    billing_zip_postal_Code = models.CharField(max_length=50, null=True)
    canopy_currency = models.CharField(max_length=50, null=True)
    canopy_customer_code = models.CharField(max_length=50, null=True)
    canopy_customer_key = models.CharField(max_length=50, null=True)
    canopy_pricing_grp = models.CharField(max_length=50, null=True)
    canopy_vendor_code = models.CharField(max_length=50, null=True)
    industry = models.CharField(max_length=50, null=True)
    ship_to_contact_name = models.CharField(max_length=50, null=True)
    ship_to_display = models.CharField(max_length=50, null=True)
    shipping_city = models.CharField(max_length=50, null=True)
    shipping_country = models.CharField(max_length=50, null=True)
    shipping_state_province = models.CharField(max_length=50, null=True)
    shipping_street = models.CharField(max_length=50, null=True)
    shipping_zip_postal_code = models.CharField(max_length=50, null=True)
    vendor_ship_from = models.CharField(max_length=50, null=True)
    website = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "contacts"


class ContactEmail(models.Model):
    account_name = models.CharField(max_length=50, null=True)
    account_phone = models.CharField(max_length=50, null=True)
    account_type = models.CharField(max_length=50, null=True)
    account_description = models.CharField(max_length=50, null=True)
    account_id = models.CharField(max_length=50, null=True)
    account_source = models.CharField(max_length=50, null=True)
    alpha_name = models.CharField(max_length=50, null=True)
    billing_city = models.CharField(max_length=50, null=True)
    billing_country = models.CharField(max_length=50, null=True)
    billing_group = models.CharField(max_length=50, null=True)
    billing_state_province = models.CharField(max_length=50, null=True)
    billing_street = models.CharField(max_length=50, null=True)
    billing_zip_postal_Code = models.CharField(max_length=50, null=True)
    canopy_currency = models.CharField(max_length=50, null=True)
    canopy_customer_code = models.CharField(max_length=50, null=True)
    canopy_customer_key = models.CharField(max_length=50, null=True)
    canopy_pricing_grp = models.CharField(max_length=50, null=True)
    canopy_vendor_code = models.CharField(max_length=50, null=True)
    industry = models.CharField(max_length=50, null=True)
    ship_to_contact_name = models.CharField(max_length=50, null=True)
    ship_to_display = models.CharField(max_length=50, null=True)
    shipping_city = models.CharField(max_length=50, null=True)
    shipping_country = models.CharField(max_length=50, null=True)
    shipping_state_province = models.CharField(max_length=50, null=True)
    shipping_street = models.CharField(max_length=50, null=True)
    shipping_zip_postal_code = models.CharField(max_length=50, null=True)
    vendor_ship_from = models.CharField(max_length=50, null=True)
    website = models.CharField(max_length=255, null=True)

    business_phone = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=50, null=True)
    business_fax = models.CharField(max_length=50, null=True)
    contact_cd = models.CharField(max_length=50, null=True)
    contact_display = models.CharField(max_length=50, null=True)
    contact_id = models.CharField(max_length=50, null=True)
    full_name = models.CharField(max_length=50, null=True)
    sms_opt_ou = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "contact_emails"


class Email(models.Model):
    business_phone = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=50, null=True)
    account_id = models.ForeignKey(
        Contact, related_name='emails_con', on_delete=models.CASCADE, null=True, blank=True, db_column="account_id")
    business_fax = models.CharField(max_length=50, null=True)
    contact_cd = models.CharField(max_length=50, null=True)
    contact_display = models.CharField(max_length=50, null=True)
    contact_id = models.CharField(max_length=50, null=True)
    full_name = models.CharField(max_length=50, null=True)
    sms_opt_ou = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "emails"


class ProgramData(models.Model):
    name = models.CharField(max_length=50, unique=True, default="code")
    description = models.CharField(max_length=255, default="description")

    class Meta:
        db_table = "programs"


class Product(models.Model):
    code_uid = models.CharField(max_length=50, null=True)
    code_crl = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True)
    code_pff = models.CharField(max_length=50, null=True)
    code_pffshort = models.CharField(max_length=50, null=True)
    code_cpm = models.CharField(max_length=50, null=True)
    code_mr = models.CharField(max_length=50, null=True)
    code_cfs = models.CharField(max_length=50, null=True)
    code_bmp = models.CharField(max_length=50, null=True)
    code_rmnm = models.CharField(max_length=50, null=True)
    code_skfp = models.CharField(max_length=50, null=True)
    code_mcf = models.CharField(max_length=50, null=True)
    code_nf = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True, blank=True)
    cut_type = models.CharField(max_length=50, null=True)
    species = models.CharField(max_length=50, null=True)
    product_type = models.CharField(max_length=50, null=True)
    eu_identity = models.CharField(max_length=50, null=True)
    age_days = models.CharField(max_length=50, null=True)
    freeze_down = models.CharField(max_length=50, null=True)
    case_size = models.CharField(max_length=50, null=True)
    bag_size = models.CharField(max_length=50, null=True)
    ecoli_test = models.CharField(max_length=50, null=True)
    pieces_box = models.CharField(max_length=50, null=True)
    bags_box = models.CharField(max_length=50, null=True)
    pff_gtin = models.CharField(max_length=50, null=True)
    gtin12 = models.CharField(max_length=50, null=True)
    gtin14 = models.CharField(max_length=50, null=True)
    notes = models.TextField(null=True, blank=True)
    programs = models.ManyToManyField(ProgramData, related_name="products")
    plants = models.ManyToManyField(Contact, related_name="products")

    class Meta:
        db_table = "products"


class ProductManual(models.Model):
    code_uid = models.CharField(max_length=50, null=True)
    code_crl = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True)
    code_pff = models.CharField(max_length=50, null=True)
    program = models.CharField(max_length=50, null=True)
    code_pffshort = models.CharField(max_length=50, null=True)
    code_cpm = models.CharField(max_length=50, null=True)
    code_mr = models.CharField(max_length=50, null=True)
    code_cfs = models.CharField(max_length=50, null=True)
    code_bmp = models.CharField(max_length=50, null=True)
    code_rmnm = models.CharField(max_length=50, null=True)
    code_skfp = models.CharField(max_length=50, null=True)
    code_mcf = models.CharField(max_length=50, null=True)
    code_nf = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True, blank=True)
    cut_type = models.CharField(max_length=50, null=True)
    species = models.CharField(max_length=50, null=True)
    product_type = models.CharField(max_length=50, null=True)
    eu_identity = models.CharField(max_length=50, null=True)
    age_days = models.CharField(max_length=50, null=True)
    freeze_down = models.CharField(max_length=50, null=True)
    case_size = models.CharField(max_length=50, null=True)
    bag_size = models.CharField(max_length=50, null=True)
    ecoli_test = models.CharField(max_length=50, null=True)
    pieces_box = models.CharField(max_length=50, null=True)
    bags_box = models.CharField(max_length=50, null=True)
    pff_gtin = models.CharField(max_length=50, null=True)
    gtin12 = models.CharField(max_length=50, null=True)
    gtin14 = models.CharField(max_length=50, null=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "ma_products"


class ProductPlant(models.Model):
    plant_id = models.ForeignKey(
        Contact, on_delete=models.RESTRICT, null=True, blank=True, db_column="plant_id"
    )
    product_id = models.ForeignKey(
        Product,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column="customer_id",
    )
    code = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "product_plants"


class Price(models.Model):
    isactive = models.CharField(max_length=50, null=True)
    code_crl = models.CharField(max_length=50, null=True)
    price = models.FloatField(null=False, blank=False, default=0.0)
    cur_unit = models.CharField(max_length=50, null=True)
    eft_date = models.CharField(max_length=50, null=True)
    file_name = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "prices"


class PriceManual(models.Model):
    isactive = models.BooleanField(default=True)
    code_crl = models.CharField(max_length=50, null=True)
    price = models.FloatField(null=False, blank=False, default=0.0)

    class Meta:
        db_table = "ma_prices"


class SlaughterReports(models.Model):
    animal_pk = models.CharField(max_length=50, null=True)
    animal_iden = models.CharField(max_length=50, null=True)
    slaughter_date = models.DateTimeField()
    producer_iden = models.ForeignKey(
        Contact,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column="producer_id",
    )
    live_weight = models.FloatField()
    hot_weight = models.FloatField()
    cold_weight = models.FloatField()
    age = models.CharField(max_length=50, null=True)
    receiving_order_iden = models.CharField(max_length=50, null=True)
    condemn_flag = models.BooleanField(default=False)
    lot_number = models.CharField(max_length=50, null=True)
    species = models.CharField(max_length=50, null=True)
    sex = models.CharField(max_length=50, null=True)
    manifest_iden = models.CharField(max_length=50, null=True)
    gradeprice_iden = models.ForeignKey(
        "GradePrice",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column="gradeprice_id",
    )
    csf_date = models.DateTimeField()

    class Meta:
        db_table = "slaughter_reps"


class SlaughterReportsManual(models.Model):
    animal_pk = models.CharField(max_length=50, null=True)
    animal_iden = models.CharField(max_length=50, null=True)
    slaughter_date = models.DateTimeField(default=timezone.now)
    owner = models.CharField(max_length=50, null=True)
    shipper = models.CharField(max_length=50, null=True)
    live_weight = models.FloatField(null=True, blank=True)
    hot_weight = models.FloatField(null=True, blank=True)
    cold_weight = models.FloatField(null=True, blank=True)
    age = models.CharField(max_length=50, null=True)
    receiving_order_id = models.CharField(max_length=50, null=True)
    condemn_flag = models.BooleanField(default=False)
    lot_number = models.CharField(max_length=50, null=True)
    species = models.CharField(max_length=50, null=True)
    sex = models.CharField(max_length=50, null=True)
    manifest_iden = models.CharField(max_length=50, null=True)
    grading = models.CharField(max_length=50, null=True)
    csf_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "ma_slaughter_reps"


class GradePrice(models.Model):
    start_time = models.DateField(null=True, blank=True)
    end_time = models.DateField(null=True, blank=True)
    grade_name = models.CharField(max_length=50, null=True)
    price = models.FloatField()

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # Metadata
    class Meta:
        db_table_comment = "Product price along with grade"
        db_table = "grade_prices"


class PlantCompareReport(models.Model):
    date = models.DateTimeField()

    class Meta:
        db_table = "plant_com_reps"


class CutInstruction(models.Model):
    factory_type = models.CharField(max_length=50, null=True)
    plant_id = models.ForeignKey(
        Contact, on_delete=models.RESTRICT, null=True, blank=True, db_column="plant_id"
    )
    product_id = models.ForeignKey(
        Product,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column="product_id",
    )
    date = models.DateTimeField()
    ecoli_testing = models.CharField(max_length=50, null=True)
    bags_amount = models.CharField(max_length=50, null=True)
    total_pieces = models.CharField(max_length=50, null=True)
    extra_code = models.CharField(max_length=50, null=True)
    comments = models.CharField(max_length=50, null=True)
    program_id = models.ForeignKey(
        ProgramData,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column="program_id",
    )
    attribute_name = models.CharField(max_length=50, null=True)
    customers = models.ManyToManyField(
        Contact, related_name="cut_instructions")

    class Meta:
        db_table = "cut_insts"


class CutInstructionCustomer(models.Model):
    cut_instruction_id = models.ForeignKey(
        CutInstruction,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column="cut_instruction_id",
    )
    contact_id = models.ForeignKey(
        Contact,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column="contact_id",
    )
    product_amount = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = "cut_inst_customers"


class Deck(models.Model):
    date = models.DateTimeField()

    class Meta:
        db_table = "decks"


class ProductReport(models.Model):
    date = models.DateTimeField()

    class Meta:
        db_table = "product_reps"


class BoxImport(models.Model):
    product_code = models.CharField(max_length=50, null=True)
    vendor_code = models.CharField(max_length=50, null=True)
    lot_code = models.CharField(max_length=50, null=True)
    lot_location = models.CharField(max_length=50, null=True)
    production_date = models.DateTimeField(
        auto_now=False, null=True, blank=True)
    exprie_date = models.DateTimeField(auto_now=False, null=True, blank=True)
    stock_qty = models.CharField(max_length=50, null=True)
    alt_qty = models.CharField(max_length=50, null=True)
    unit_cost = models.CharField(max_length=50, null=True)
    weight = models.CharField(max_length=50, null=True)
    po_number = models.CharField(max_length=50, null=True)
    pallet_id = models.CharField(max_length=50, null=True)
    pallet_location = models.CharField(max_length=50, null=True)
    lot_batch_number = models.CharField(max_length=50, null=True)
    create_po = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "box_imports"


class GradeSheet(models.Model):
    date = models.DateTimeField()

    class Meta:
        db_table = "grade_sheets"


class CutOutMail(models.Model):
    state_flag = models.IntegerField(null=True, blank=True)
    date = models.DateField()

    class Meta:
        db_table = "cutout_mails"


class CutOutMap(models.Model):
    mail_id = models.IntegerField(null=True, blank=True)
    date = models.DateField()
    lot_number = models.CharField(max_length=50, null=True, blank=True)
    hd_amount = models.IntegerField(null=True, blank=True)
    type_grade = models.CharField(max_length=50, null=True, blank=True)
    lw_in_kg = models.FloatField(null=True, blank=True)
    lw_avg_kg = models.FloatField(null=True, blank=True)
    lw_avg_lbs = models.FloatField(null=True, blank=True)
    hhw_in_kg = models.FloatField(null=True, blank=True)
    total_hhw_lbs = models.FloatField(null=True, blank=True)
    hhw_avg_kg = models.FloatField(null=True, blank=True)
    hhw_avg_lbs = models.FloatField(null=True, blank=True)
    yield_dress = models.CharField(max_length=50, null=True, blank=True)
    cw_in_kg = models.FloatField(null=True, blank=True)
    cw_shrink = models.CharField(max_length=50, null=True, blank=True)
    cw_avg_kg = models.FloatField(null=True, blank=True)
    cw_avg_lbs = models.FloatField(null=True, blank=True)
    live_dollar_per_kg = models.FloatField(null=True, blank=True)
    yield_cut = models.CharField(max_length=50, null=True, blank=True)
    hhw_dollar_per_kg = models.FloatField(null=True, blank=True)
    hhw_avg_kg_meat = models.FloatField(null=True, blank=True)
    hhw_avg_lbs_meat = models.FloatField(null=True, blank=True)
    yield_meat = models.CharField(max_length=50, null=True, blank=True)
    bulls_amount = models.IntegerField(null=True, blank=True)
    heifers_amount = models.IntegerField(null=True, blank=True)
    cows_amount = models.IntegerField(null=True, blank=True)
    doa_inpen = models.IntegerField(null=True, blank=True)
    hhw_dollar_per_lb = models.FloatField(null=True, blank=True)
    cost_hhw = models.FloatField(null=True, blank=True)
    cost_plant_hd = models.FloatField(null=True, blank=True)
    cost_plant = models.FloatField(null=True, blank=True)
    cost_fob = models.FloatField(null=True, blank=True)
    cost_sga_lb = models.FloatField(null=True, blank=True)
    cost_sga = models.FloatField(null=True, blank=True)
    cost_kill = models.FloatField(null=True, blank=True)
    sell_primal = models.FloatField(null=True, blank=True)
    sell_offal = models.FloatField(null=True, blank=True)
    sell_profit = models.FloatField(null=True, blank=True)
    sell_primal_hd = models.FloatField(null=True, blank=True)
    sell_offal_hd = models.FloatField(null=True, blank=True)
    margin = models.CharField(max_length=50, null=True, blank=True)
    sell_hd = models.FloatField(null=True, blank=True)
    cost_hd = models.FloatField(null=True, blank=True)
    profit_hd = models.FloatField(null=True, blank=True)
    eu_fx = models.FloatField(null=True, blank=True)
    primal_kgs = models.FloatField(null=True, blank=True)
    primal_avg_dollar_kg = models.FloatField(null=True, blank=True)
    kgs_hd_offal = models.FloatField(null=True, blank=True)
    yield_offals = models.CharField(max_length=50, null=True, blank=True)
    offal_kgs = models.FloatField(null=True, blank=True)
    offal_avg_dollar_kg = models.FloatField(null=True, blank=True)
    code_crl = models.CharField(max_length=50, null=True, blank=True)
    sell_kg = models.FloatField(null=True, blank=True)
    price_lb_usd = models.FloatField(null=True, blank=True)
    kgs_total = models.FloatField(null=True, blank=True)
    kgs_hd = models.FloatField(null=True, blank=True)
    value_total = models.FloatField(null=True, blank=True)
    wt_percent_cuts = models.CharField(max_length=50, null=True, blank=True)
    value_percent = models.CharField(max_length=50, null=True, blank=True)
    cogs_kg = models.FloatField(null=True, blank=True)
    cogs = models.FloatField(null=True, blank=True)
    fat_percent = models.CharField(max_length=50, null=True, blank=True)
    net_truck = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="NetTruck")
    net_truck_shrink = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="NetTruckShrink")
    price_back_to_farm = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="PriceBackToFarm")
    us_canada = models.CharField(max_length=50, null=True, blank=True)
    plant_name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "cutoutmaps"
        ordering = ['-date']


class HarvestReport(models.Model):
    date = models.DateField()
    plant = models.CharField(max_length=50, null=True)
    year = models.CharField(max_length=50, null=True)
    period = models.CharField(max_length=50, null=True)
    quarter = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=50, null=True)
    producer_id = models.CharField(max_length=50, null=True)
    producer_owner = models.CharField(max_length=255, null=True)
    count = models.CharField(max_length=50, null=True)
    m_utm = models.CharField(max_length=50, null=True)
    m_otm = models.CharField(max_length=50, null=True)
    f_utm = models.CharField(max_length=50, null=True)
    f_otm = models.CharField(max_length=50, null=True)
    f_cow = models.CharField(max_length=50, null=True)
    m_a1 = models.CharField(max_length=50, null=True)
    m_a2 = models.CharField(max_length=50, null=True)
    m_a3 = models.CharField(max_length=50, null=True)
    m_a4 = models.CharField(max_length=50, null=True)
    m_b1 = models.CharField(max_length=50, null=True)
    m_b2 = models.CharField(max_length=50, null=True)
    m_b3 = models.CharField(max_length=50, null=True)
    m_d1 = models.CharField(max_length=50, null=True)
    m_d2 = models.CharField(max_length=50, null=True)
    m_d3 = models.CharField(max_length=50, null=True)
    f_a1 = models.CharField(max_length=50, null=True)
    f_a2 = models.CharField(max_length=50, null=True)
    f_a3 = models.CharField(max_length=50, null=True)
    f_a4 = models.CharField(max_length=50, null=True)
    f_b1 = models.CharField(max_length=50, null=True)
    f_b2 = models.CharField(max_length=50, null=True)
    f_b3 = models.CharField(max_length=50, null=True)
    f_d1 = models.CharField(max_length=50, null=True)
    f_d2 = models.CharField(max_length=50, null=True)
    f_d3 = models.CharField(max_length=50, null=True)
    prior_yrs_b_h = models.CharField(max_length=255, null=True)
    prior_yrs_mature = models.CharField(max_length=255, null=True)
    total_avglive_lbs = models.CharField(max_length=50, null=True)
    plant_avglive_lbs = models.CharField(max_length=50, null=True)
    live_helper = models.CharField(max_length=255, null=True)
    live_bull_lbs_helper = models.CharField(max_length=255, null=True)
    live_heifers_lbs_helper = models.CharField(max_length=255, null=True)
    live_cow_lbs_helper = models.CharField(max_length=255, null=True)
    total_hhw_lbs = models.CharField(max_length=255, null=True)
    avg_hhw_lbs = models.CharField(max_length=255, null=True)
    hhw_helper = models.CharField(max_length=255, null=True)
    hhw_bull_lbs_helper = models.CharField(max_length=255, null=True)
    hhw_hei_lbs_helper = models.CharField(max_length=255, null=True)
    hhw_cow_lbs_helper = models.CharField(max_length=255, null=True)
    yield_to_plant_pcent = models.CharField(max_length=255, null=True)
    shrink_helper = models.CharField(max_length=255, null=True)
    avg_dol_per_lbs = models.CharField(max_length=255, null=True)
    dol_per_lb_helper = models.CharField(max_length=255, null=True)
    avg_dol_per_hd = models.CharField(max_length=255, null=True)
    dol_per_hd_helper = models.CharField(max_length=255, null=True)
    week = models.CharField(max_length=50, null=True)
    pre_year_prod_per_owner = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "harvest_reps"
