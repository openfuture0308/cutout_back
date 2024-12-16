from src.models import Price

class PriceCsvMapsModule:
    
    def __init__(self, file):
        self.file = file
        self.pricefile_name = "".join([i for i in self.file.name if not i.isdigit()]).split(
                "."
            )[0]
        self.cur_name = (
                self.file.readline()
                .decode("utf-8")
                .strip()
                .split("\t")[1]
                .split("$")[0]
                .strip()
            )
        
    def handle_uploaded_file(self):
        for line in self.file.readlines()[1:]:  # Skip header row
            line = line.decode("utf-8").strip()
            code_crl, cost_str = line.split("\t")
            price = float(cost_str.replace("$", ""))

            code_crl, wrhs = code_crl.split(".")  # Split CostCode
            # product, created = Product.objects.get_or_create(code_crl=code_crl)
            Price.objects.create(
                isactive_flag=True,
                pricefile_name=self.pricefile_name,
                cur_name=self.cur_name,
                code_crl=code_crl,
                price=price,
                wrhs=wrhs,
            )