from django import forms

# Define the form for uploading Excel files and selecting the table (model)


class ExcelUploadForm(forms.Form):
    table_choices = [
        ("price", "Price"),
        ("program", "Program"),
        ("contact", "Contact"),
        ("email", "Email"),
        ("product", "Product"),
        ("product_manual", "ProductManual"),
        ("slaughter_rep", "SlaughtRep"),
        ("price_csv_manual", "PriceCsvManual"),
        ("harvest_report", "HarvestReport"),
        # Add other tables here...
    ]
    table_name = forms.ChoiceField(choices=table_choices)
    file = forms.FileField()


class SalesForceExcelUploadForm(forms.Form):
    table_choices = [
        ("contact", "Contact"),
        ("email", "Email"),
        # Add other tables here...
    ]
    table_name = forms.ChoiceField(choices=table_choices)
    file = forms.FileField()


class CutOutMapUploadForm(forms.Form):
    table_choices = [
        ("cutoutmap", "cutoutmap"),
        # Add other tables here...
    ]
    table_name = forms.ChoiceField(choices=table_choices)
    file = forms.FileField()


class ACutOutUploadForm(forms.Form):
    choices_plant = [
        ("CPM", "CPM"),
        ("BMP", "BMP"),
        ("PFF", "PFF"),
        ("BVY", "BVY"),
        ("LNTZ", "LNTZ"),
        # Add other tables here...
    ]
    plant_name = forms.ChoiceField(choices=choices_plant)
    file = forms.FileField()


class CSVUploadForm(forms.Form):
    file = forms.FileField()
