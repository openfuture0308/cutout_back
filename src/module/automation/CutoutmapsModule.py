from spire.xls import *
from spire.xls.common import *
from datetime import datetime
from src.models import CutOutMap, CutOutMail
from src.utils.constants import temp_dir, listUsPlant, listCanadaPlant, listExchangeStr, header_cutoutmap
import re
import os
import pyexcel as p
from dataclasses import fields

pattern = r"^\d+ ([BCHM])\w*$"


class CutoutmapsModule:
    workbook = None
    sheet = None

    def convert_to_list(self, cutOutMapObjs):
        result = []
        result.append(header_cutoutmap)
        for index, cutOutMapObj in enumerate(cutOutMapObjs):
            item_res = []
            i = 0
            for key, value in enumerate(vars(cutOutMapObj).items()):
                if i > 2:
                    item_res.append(value[1])
                i += 1
            result.append(item_res)
        return result

    def is_valid_float(self, value):
        if value not in ['#N/A', '', 'NaN', 'NoneType', None]:
            try:
                valueC = float(value)
                if valueC > 0:
                    return True
                else:
                    return False
            except ValueError:
                return False
        return False

    def convertXlsToXlsx(self, filepath):
        p.save_book_as(file_name=filepath,
                       dest_file_name='./temp/created.xlsx')
        return './temp/created.xlsx'

    def getCellValue(self, row, col):
        cellType = self.sheet.GetCellType(row, col, False)
        value = self.sheet.Range[row, col].Value
        if str(cellType) != "TRangeValueType.Formula":
            return self.checkValue(value.strip())
        else:
            return self.workbook.CaculateFormulaValue(value)

    def checkValue(self, value):
        if value == '':
            return None
        else:
            return value

    def getCell(self, cellvalue):
        cellvalue = cellvalue.strip().upper()
        # Assuming sheet.rows gives total number of rows
        for row in range(1, len(self.sheet.Rows) + 1):
            # Assuming sheet.columns gives total number of columns
            for col in range(1, len(self.sheet.Columns) + 1):
                cell_value = self.sheet.Range[row, col].Value
                if cell_value.strip().upper() == cellvalue:
                    return [row, col]

        return None

    def getCellInclude(self):
        # Assuming sheet.rows gives total number of rows
        for row in range(1, len(self.sheet.Rows) + 1):
            # Assuming sheet.columns gives total number of columns
            for col in range(11, len(self.sheet.Columns) + 1):
                cell_value = str(self.sheet.Range[row, col].Value).upper()
                for idx, strExchange in enumerate(listExchangeStr):
                    if strExchange in cell_value:
                        return [row, col, idx]
        return None

    def searchAnimalNum(self):
        matching_items = []

        # Assuming sheet.rows gives total number of rows
        for row in range(1, len(self.sheet.Rows) + 1):
            # Assuming sheet.columns gives total number of columns
            for col in range(11, len(self.sheet.Columns) + 1):
                cell_value = self.sheet.Range[row, col].Value.strip()
                if re.match(pattern, cell_value, re.IGNORECASE):
                    matching_items.append(cell_value)

        return matching_items

    def parse_date(self, date_str):
        formats = ['%b %d, %Y', '%B %d, %Y', '%B %d , %Y', '%b. %d, %Y', '%b %d %Y', '%b %d/%Y',
                   '%m-%d-%Y', '%m/%d/%y', "%m/%d/%Y", '%m/%d/%Y %I:%M:%S %p']
        date_str = date_str.replace("Sept ", "Sep ").strip()
        date_str = date_str.replace("Sept. ", "Sep. ").strip()
        # date_str = date_str.replace("/", " ")
        for fmt in formats:
            try:
                date = datetime.strptime(date_str, fmt)
                return date.strftime("%Y-%m-%d")
            except ValueError:
                continue
        raise ValueError(f"Date format not recognized: {date_str}")

    def update(self, data):
        cutOutMapDatas = []
        lot_number = data[0][1]
        deleted_count, _ = CutOutMap.objects.filter(
            lot_number=lot_number).delete()
        for item in data:
            cutOutMapData = CutOutMap()
            cutOutMapData.mail_id = None
            cutOutMapData.date = item[0]
            cutOutMapData.lot_number = item[1]
            cutOutMapData.hd_amount = item[2]
            cutOutMapData.type_grade = item[3]
            cutOutMapData.lw_in_kg = item[4]
            cutOutMapData.lw_avg_kg = item[5]
            cutOutMapData.lw_avg_lbs = item[6]
            cutOutMapData.hhw_in_kg = item[7]
            cutOutMapData.total_hhw_lbs = item[8]
            cutOutMapData.hhw_avg_kg = item[9]
            cutOutMapData.hhw_avg_lbs = item[10]
            cutOutMapData.yield_dress = item[11]
            cutOutMapData.cw_in_kg = item[12]
            cutOutMapData.cw_shrink = item[13]
            cutOutMapData.cw_avg_kg = item[14]
            cutOutMapData.cw_avg_lbs = item[15]
            cutOutMapData.live_dollar_per_kg = item[16]
            cutOutMapData.yield_cut = item[17]
            cutOutMapData.hhw_dollar_per_kg = item[18]
            cutOutMapData.hhw_avg_kg_meat = item[19]
            cutOutMapData.hhw_avg_lbs_meat = item[20]
            cutOutMapData.yield_meat = item[21]
            cutOutMapData.bulls_amount = item[22]
            cutOutMapData.heifers_amount = item[23]
            cutOutMapData.cows_amount = item[24]
            cutOutMapData.doa_inpen = item[25]
            cutOutMapData.hhw_dollar_per_lb = item[26]
            cutOutMapData.cost_hhw = item[27]
            cutOutMapData.cost_plant_hd = item[28]
            cutOutMapData.cost_plant = item[29]
            cutOutMapData.cost_fob = item[30]
            cutOutMapData.cost_sga_lb = item[31]
            cutOutMapData.cost_sga = item[32]
            cutOutMapData.cost_kill = item[33]
            cutOutMapData.sell_primal = item[34]
            cutOutMapData.sell_offal = item[35]
            cutOutMapData.sell_profit = item[36]
            cutOutMapData.sell_primal_hd = item[37]
            cutOutMapData.sell_offal_hd = item[38]
            cutOutMapData.margin = item[39]
            cutOutMapData.sell_hd = item[40]
            cutOutMapData.cost_hd = item[41]
            cutOutMapData.profit_hd = item[42]
            cutOutMapData.eu_fx = item[43]
            cutOutMapData.primal_kgs = item[44]
            cutOutMapData.primal_avg_dollar_kg = item[45]
            cutOutMapData.kgs_hd_offal = item[46]
            cutOutMapData.yield_offals = item[47]
            cutOutMapData.offal_kgs = item[48]
            cutOutMapData.offal_avg_dollar_kg = item[49]
            cutOutMapData.code_crl = item[50]
            cutOutMapData.sell_kg = item[51]
            cutOutMapData.price_lb_usd = item[52]
            cutOutMapData.kgs_total = item[53]
            cutOutMapData.kgs_hd = item[54]
            cutOutMapData.value_total = item[55]
            cutOutMapData.wt_percent_cuts = item[56]
            cutOutMapData.value_percent = item[57]
            cutOutMapData.cogs_kg = item[58]
            cutOutMapData.cogs = item[59]
            cutOutMapData.fat_percent = item[60]
            cutOutMapData.net_truck = item[61]
            cutOutMapData.net_truck_shrink = item[62]
            cutOutMapData.price_back_to_farm = item[63]
            cutOutMapData.us_canada = item[64]
            cutOutMapData.plant_name = item[65]

            cutOutMapDatas.append(cutOutMapData)
        CutOutMap.objects.bulk_create(cutOutMapDatas)

    def save(self, file, data):
        plant_name = data["plant_name"]
        bulls_amount = float(data["bull_amount"]
                             ) if data["bull_amount"] != "" else 0
        heifers_amount = float(
            data["heifer_amount"]) if data["heifer_amount"] != "" else 0
        cows_amount = float(data["cow_amount"]
                            ) if data["cow_amount"] != "" else 0
        eu_fx = float(data["eu_rate"]) if data["eu_rate"] != "" else 0
        doa_inpen = 0

        filename, file_extension = os.path.splitext(file.name)
        temp_dir_plant = os.path.join(temp_dir, plant_name)
        if not os.path.exists(temp_dir_plant):
            os.makedirs(temp_dir_plant)
        temp_file_path = os.path.join(temp_dir_plant, file.name)
        with open(temp_file_path, 'wb+') as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)

        file_path = self.convertXlsToXlsx(
            temp_file_path) if file_extension == ".xls" else temp_file_path
        self.workbook = Workbook()

        # Load an Excel file
        self.workbook.LoadFromFile(file_path)
        sheet = self.workbook.Worksheets[0]
        self.sheet = sheet
        i_date = self.getCell("Date")
        date = self.getCellValue(
            i_date[0], i_date[1]+1) if i_date is not None else None           # Date
        date = self.parse_date(date)
        lot_number = (plant_name + str(date)[2:]).replace("-", "")
        i_hd_amount = self.getCell("# of head")

        hd_amount = self.getCellValue(
            i_hd_amount[0], i_hd_amount[1]+1) if i_hd_amount is not None else None

        # # of head
        i_type = self.getCell("Grade")
        type = self.getCellValue(
            i_type[0], i_type[1]+1) if i_type is not None else None   # Grade
        if cows_amount is not None:
            if float(cows_amount) * 2 > float(hd_amount):
                lot_number += "-COW"

        if CutOutMap.objects.filter(lot_number=lot_number).exists():
            return "You already uploaded this data!"
        fat_percent = 0
        us_canada = ''
        if plant_name in listCanadaPlant:
            us_canada = 'Canada'
        elif plant_name in listUsPlant:
            us_canada = 'US'
        else:
            us_canada = ''
        i_lw_in_kg = self.getCell("Live Weight in Kg")
        i_lw_in_kg = self.getCell(
            "Live Weight (Plant) in Kg") if i_lw_in_kg is None else i_lw_in_kg
        i_lw_in_kg = [5, 1] if i_lw_in_kg is None else i_lw_in_kg
        lw_in_kg = round(float(self.getCellValue(i_lw_in_kg[0], i_lw_in_kg[1]+1)), 2) if i_lw_in_kg is not None and self.getCellValue(
            i_lw_in_kg[0], i_lw_in_kg[1]+1) is not None else None
        # Live Weight in Kg
        lw_avg_kg = round(float(lw_in_kg)/float(hd_amount),
                          2) if lw_in_kg is not None and hd_amount is not None else None   # kg
        lw_avg_lbs = round(float(lw_avg_kg)*2.2046,
                           2) if lw_avg_kg is not None else None      # lbs
        i_hhw_in_kg = self.getCell("HHW Weight in Kg") if self.getCell(
            "HHW Weight in Kg") is not None else [6, 1]
        hhw_in_kg = round(float(self.getCellValue(i_hhw_in_kg[0], i_hhw_in_kg[1]+1)), 2) if i_hhw_in_kg is not None and self.getCellValue(
            i_hhw_in_kg[0], i_hhw_in_kg[1]+1) is not None else None
        # HHW Weight in Kg
        total_hhw_lbs = round(float(hhw_in_kg) * 2.2046,
                              2) if hhw_in_kg is not None else None
        hhw_avg_kg = round(float(hhw_in_kg)/float(hd_amount),
                           2) if hhw_in_kg is not None and hd_amount is not None else None   # kg
        hhw_avg_lbs = round(float(hhw_avg_kg)*2.2046,
                            2) if hhw_avg_kg is not None else None    # lbs
        yield_dress = str(round(float(hhw_in_kg)/float(lw_in_kg) * 100,
                                2)) + "%" if hhw_in_kg is not None and lw_in_kg is not None else None    # Dressing yield
        i_cw_in_kg = self.getCell("Cold Weight in Kg") if self.getCell(
            "Cold Weight in Kg") is not None else [7, 1]
        cw_in_kg = round(float(self.getCellValue(i_cw_in_kg[0], i_cw_in_kg[1]+1)), 2) if i_cw_in_kg is not None and self.getCellValue(
            i_cw_in_kg[0], i_cw_in_kg[1]+1) is not None else None
        # HHW Weight in Kg
        cw_avg_kg = round(float(cw_in_kg)/float(hd_amount),
                          2) if cw_in_kg is not None and hd_amount is not None else None   # kg
        cw_avg_lbs = round(float(cw_avg_kg)*2.2046,
                           2) if cw_avg_kg is not None else None    # lbs
        cw_shrink = str(round((float(cw_in_kg)/float(hhw_in_kg) - 1) * 100,
                              2)) + "%" if cw_in_kg is not None and hhw_in_kg is not None else None      # Shrink

        i_live_dollar_per_kg = self.getCell("Live price in KG") if self.getCell(
            "Live price in KG") is not None else [8, 1]
        live_dollar_per_kg = self.getCellValue(
            i_live_dollar_per_kg[0], i_live_dollar_per_kg[1]+1) if i_live_dollar_per_kg is not None else None
        # Live price in KG

        i_total_kg_meat = self.getCell("per head total KG meat")
        i_total_offal_kg_meat = self.getCell(
            "per head total KG by-products (offals)")
        i_code = self.getCell("Code")
        i_sell_kg = self.getCell("Sales Price #1 per kg")
        i_kgs_hd = self.getCell("Average kg per head")
        i_value_total = self.getCell("Total")
        i_wt_percent_cuts = self.getCell("% weight of cuts")
        i_value_percent = self.getCell("% Value from av. kg sales price")
        i_cogs_kg = self.getCell("Product Inventory cost value/kg")
        i_cogs = self.getCell("Product Inventory cost")
        i_kgs_total = self.getCell("Total  kg")
        yield_cut = str(round(float(self.getCellValue(i_total_kg_meat[0], 3)) * 100, 2)) + "%" if i_total_kg_meat is not None and self.getCellValue(
            i_total_kg_meat[0], 3) is not None else None      # Cut yield

        i_hhw_dollar_per_kg = self.getCell("HHW price in KG") if self.getCell(
            "HHW price in KG") is not None else [9, 1]
        hhw_dollar_per_lb = round(float(self.getCellValue(
            i_hhw_dollar_per_kg[0]+1, i_hhw_dollar_per_kg[1]+1)), 2) if i_hhw_dollar_per_kg is not None and self.getCellValue(
            i_hhw_dollar_per_kg[0]+1, i_hhw_dollar_per_kg[1]+1) is not None else None
        hhw_dollar_per_lb_real = float(self.getCellValue(
            i_hhw_dollar_per_kg[0]+1, i_hhw_dollar_per_kg[1]+1)) if i_hhw_dollar_per_kg is not None and self.getCellValue(
            i_hhw_dollar_per_kg[0]+1, i_hhw_dollar_per_kg[1]+1) is not None else None
        # Live price in lbs
        hhw_dollar_per_kg = round(float(hhw_dollar_per_lb_real)*2.2046,
                                  2) if hhw_dollar_per_lb_real is not None else None    # HHW price in KG

        hhw_avg_kg_meat = round(float(self.getCellValue(i_total_kg_meat[0], 2)), 2) if i_total_kg_meat is not None and self.getCellValue(
            i_total_kg_meat[0], 2) is not None else None     # kg
        hhw_avg_lbs_meat = round(float(
            hhw_avg_kg_meat)*2.2046, 2) if hhw_avg_kg_meat is not None else None    # lbs

        yield_meat = self.getCellValue(
            i_total_kg_meat[0], i_kgs_total[1]) if i_total_kg_meat is not None else None
        # Meat Yield
        yield_meat = str(round(float(yield_meat)/float(lw_in_kg) * 100,
                               2)) + "%" if yield_meat is not None and lw_in_kg is not None else None

        cost_hhw = round(float(hhw_dollar_per_kg)*float(hhw_in_kg),
                         2) if hhw_dollar_per_kg is not None and hhw_in_kg is not None else None
        # COST of HHW Bison

        i_cost_plant_hd = self.getCell("PLANT COST per head") if self.getCell(
            "PLANT COST per head") is not None else [11, 1]
        cost_plant_hd = round(float(self.getCellValue(i_cost_plant_hd[0], i_cost_plant_hd[1]+1)), 2) if i_cost_plant_hd is not None and self.getCellValue(
            i_cost_plant_hd[0], i_cost_plant_hd[1]+1) is not None else None
        # PLANT COST per head
        cost_plant = round(float(cost_plant_hd)*float(hd_amount),
                           2) if cost_plant_hd is not None and hd_amount is not None else None             # PLANT COST
        # COST FOB Lacombe
        cost_fob = round(float(cost_hhw)+float(cost_plant),
                         2) if cost_hhw is not None and cost_plant is not None else None
        i_cost_sga_lb_value = self.getCell("Selling, General, Admin. COST") if self.getCell(
            "Selling, General, Admin. COST") is not None else [13, 1]
        # Selling, General, Admin. COST
        cost_sga_lb_value = self.getCellValue(
            i_cost_sga_lb_value[0], i_cost_sga_lb_value[1]+1) if i_cost_sga_lb_value is not None else None
        cost_sga_lb = None
        if cost_sga_lb_value != None:
            if "1b" in cost_sga_lb_value or "lb" in cost_sga_lb_value or "LB" in cost_sga_lb_value:
                cost_sga_lb_value = cost_sga_lb_value[0:len(
                    cost_sga_lb_value)-3]
            cost_sga_lb = float(cost_sga_lb_value)
        i_cost_sga = self.getCell("Inventory COGS")
        cost_sga = round(float(self.getCellValue(i_cost_sga[0] - 1, i_cost_sga[1] - 1)), 2) if i_cost_sga is not None and self.getCellValue(
            i_cost_sga[0] - 1, i_cost_sga[1] - 1) is not None else None
        # Total COST for kill
        cost_kill = round(float(cost_fob)+float(cost_sga),
                          2) if cost_fob is not None and cost_sga is not None else None

        sell_primal = round(float(self.getCellValue(i_total_kg_meat[0], i_value_total[1])), 2) if i_total_kg_meat is not None and i_value_total is not None and self.is_valid_float(self.getCellValue(
            i_total_kg_meat[0], i_value_total[1])) else None
        # Sales price Revenue
        # By-products Revenue
        sell_offal = self.getCellValue(
            i_total_offal_kg_meat[0], i_value_total[1]) if i_total_offal_kg_meat is not None and i_value_total is not None else 0.0
        sell_offal = 0.0 if sell_offal is None else round(float(sell_offal), 2)

        if sell_offal == 0:
            i_sell_offal = self.getCell(
                "By-products Revenue")
            sell_offal = self.getCellValue(
                i_sell_offal[0], i_sell_offal[1] + 2) if i_sell_offal is not None else 0.0

        sell_profit = round(float(sell_primal)+float(sell_offal)-float(cost_kill),
                            2) if sell_primal is not None and sell_offal is not None and cost_kill is not None else 0.0
        # NET PROFIT FOR KILL
        # Primal per head (Column G is 7)
        sell_primal_hd = round(float(sell_primal)/float(hd_amount),
                               2) if sell_primal is not None and hd_amount is not None else None
        # Offal per head (Column G is 7)
        sell_offal_hd = round(float(sell_offal)/float(hd_amount),
                              2) if sell_offal is not None and hd_amount is not None else 0.0
        # MARGIN (Column F is 6)
        margin = str(round(float(sell_profit)/float(cost_kill) * 100,
                           2)) + "%" if sell_profit is not None and cost_kill is not None else None

        sell_hd = round((float(sell_primal)+float(sell_offal))/float(hd_amount),
                        # Sales price Revenue
                        2) if sell_primal is not None and sell_offal is not None and hd_amount is not None else None
        # Total cost per hd
        cost_hd = round(float(cost_kill)/float(hd_amount),
                        2) if cost_kill is not None and hd_amount is not None else None
        # NET PROFIT per hd
        profit_hd = round(float(sell_hd)-float(cost_hd),
                          2) if sell_hd is not None and cost_hd is not None else None
        cutOutMapsDatas = []
        is_price_lb_usd = False
        i_price_lb_usd = self.getCell("Price/lb")
        if i_price_lb_usd is not None and us_canada == 'US':
            is_price_lb_usd = True
        if i_code is not None:
            rowindex = i_code[0]+1

            while self.getCellValue(rowindex, 1) == None:
                rowindex += 1
            # while self.getCellValue(rowindex, 1) != None or self.getCellValue(rowindex, i_sell_kg[1]) != None:
            while self.getCellValue(rowindex, 1) != "per head total KG meat":
                kgs_total = self.getCellValue(
                    rowindex, i_kgs_total[1])  # Total  kg
                if self.is_valid_float(kgs_total):
                    cutOutMapData = CutOutMap()

                    # cutOutMapData.mail_id = mailid

                    cutOutMapData.date = date
                    cutOutMapData.lot_number = lot_number
                    cutOutMapData.plant_name = plant_name
                    cutOutMapData.us_canada = us_canada
                    cutOutMapData.hd_amount = hd_amount
                    cutOutMapData.lw_in_kg = lw_in_kg
                    cutOutMapData.lw_avg_kg = lw_avg_kg
                    cutOutMapData.lw_avg_lbs = lw_avg_lbs
                    cutOutMapData.hhw_in_kg = hhw_in_kg
                    cutOutMapData.total_hhw_lbs = total_hhw_lbs
                    cutOutMapData.hhw_avg_kg = hhw_avg_kg
                    cutOutMapData.hhw_avg_lbs = hhw_avg_lbs
                    cutOutMapData.yield_dress = yield_dress
                    cutOutMapData.cw_in_kg = cw_in_kg
                    cutOutMapData.cw_shrink = cw_shrink
                    cutOutMapData.cw_avg_kg = cw_avg_kg
                    cutOutMapData.cw_avg_lbs = cw_avg_lbs
                    cutOutMapData.live_dollar_per_kg = live_dollar_per_kg
                    cutOutMapData.yield_cut = yield_cut
                    cutOutMapData.hhw_dollar_per_kg = hhw_dollar_per_kg
                    cutOutMapData.hhw_avg_kg_meat = hhw_avg_kg_meat
                    cutOutMapData.hhw_avg_lbs_meat = hhw_avg_lbs_meat
                    cutOutMapData.yield_meat = yield_meat
                    cutOutMapData.bulls_amount = bulls_amount
                    cutOutMapData.heifers_amount = heifers_amount
                    cutOutMapData.cows_amount = cows_amount
                    cutOutMapData.doa_inpen = doa_inpen
                    cutOutMapData.hhw_dollar_per_lb = hhw_dollar_per_lb
                    cutOutMapData.cost_hhw = cost_hhw
                    cutOutMapData.cost_plant_hd = cost_plant_hd
                    cutOutMapData.cost_plant = cost_plant
                    cutOutMapData.cost_fob = cost_fob
                    cutOutMapData.cost_sga_lb = cost_sga_lb
                    cutOutMapData.cost_sga = cost_sga
                    cutOutMapData.cost_kill = cost_kill
                    cutOutMapData.sell_primal = sell_primal
                    cutOutMapData.sell_offal = sell_offal
                    cutOutMapData.sell_profit = sell_profit
                    cutOutMapData.sell_primal_hd = sell_primal_hd
                    cutOutMapData.sell_offal_hd = sell_offal_hd
                    cutOutMapData.margin = margin
                    cutOutMapData.sell_hd = sell_hd
                    cutOutMapData.cost_hd = cost_hd
                    cutOutMapData.profit_hd = profit_hd
                    cutOutMapData.eu_fx = eu_fx
                    cutOutMapData.kgs_total = kgs_total
                    if is_price_lb_usd:
                        cutOutMapData.price_lb_usd = round(float(self.getCellValue(
                            rowindex, i_price_lb_usd[1]
                        )), 2) if self.is_valid_float(self.getCellValue(rowindex, i_sell_kg[1])) else None
                    cutOutMapData.code_crl = self.getCellValue(
                        rowindex, i_code[1])  # Code
                    cutOutMapData.sell_kg = round(float(self.getCellValue(rowindex, i_sell_kg[1])), 2) if self.is_valid_float(self.getCellValue(
                        rowindex, i_sell_kg[1])) else None
                    # Sales Price #1 per kg
                    cutOutMapData.kgs_hd = round(float(self.getCellValue(rowindex, i_kgs_hd[1])), 2) if self.getCellValue(
                        rowindex, i_kgs_hd[1]) is not None else None
                    # Average kg per head
                    cutOutMapData.value_total = round(float(self.getCellValue(rowindex, i_value_total[1])), 2) if self.is_valid_float(self.getCellValue(
                        rowindex, i_value_total[1])) else None
                    # TBD
                    val_percent = str(round(float(self.checkValue(self.getCellValue(rowindex, i_wt_percent_cuts[1]))) * 100, 2)) + "%" if i_wt_percent_cuts is not None and self.checkValue(
                        self.getCellValue(rowindex, i_wt_percent_cuts[1])) is not None else None
                    cutOutMapData.wt_percent_cuts = val_percent
                    if "FAT" in self.getCellValue(rowindex, i_code[1] + 1) or "Kidney" in self.getCellValue(rowindex, i_code[1] + 1):
                        fat_percent += float(
                            val_percent[:-1]) if val_percent is not None else 0.0
                    # % weight of cuts
                    cutOutMapData.value_percent = str(round(float(self.getCellValue(rowindex, i_value_percent[1])) * 100, 2)) + "%" if self.getCellValue(
                        rowindex, i_value_percent[1]) is not None else None
                    # % Value from av. kg sales price
                    cutOutMapData.cogs_kg = round(float(self.getCellValue(rowindex, i_cogs_kg[1])), 2) if self.getCellValue(
                        rowindex, i_cogs_kg[1]) is not None else None
                    # Product Inventory cost value/kg
                    cutOutMapData.cogs = round(float(self.getCellValue(rowindex, i_cogs[1])), 2) if self.is_valid_float(self.getCellValue(
                        rowindex, i_cogs[1])) else None
                    # Product Inventory cost
                    cutOutMapsDatas.append(cutOutMapData)
                    # cutOutMapData.mail_id = mailid

                rowindex += 1
            # while self.getCellValue(rowindex, 1) != "per head total KG meat":
            #     rowindex += 1

            primal_kgs = round(float(self.getCellValue(rowindex, i_kgs_total[1])), 2) if self.getCellValue(
                rowindex, i_kgs_total[1]) is not None else None  # Total KG
            primal_avg_dollar_kg = round(float(self.getCellValue(rowindex, i_kgs_hd[1])), 2) if self.is_valid_float(self.getCellValue(
                rowindex, i_kgs_hd[1])) else None  # TBD
            rowindex += 1
            count = 0
            while self.getCellValue(rowindex, 1) != "per head total KG by-products (offals)":
                if self.getCellValue(rowindex, 1) == None and self.getCellValue(rowindex, 2) == None and self.getCellValue(rowindex, 3) == None and self.getCellValue(rowindex, 4) == None and self.getCellValue(rowindex, 5) == None and self.getCellValue(rowindex, 6) == None and self.getCellValue(rowindex, 7) == None and self.getCellValue(rowindex, 8) == None and self.getCellValue(rowindex, 9) == None:
                    break
                kgs_total = self.getCellValue(
                    rowindex, i_kgs_total[1])  # Total  kg
                if self.is_valid_float(kgs_total):
                    cutOutMapData = CutOutMap()

                    # cutOutMapData.mail_id = mailid

                    cutOutMapData.date = date
                    cutOutMapData.lot_number = lot_number
                    cutOutMapData.plant_name = plant_name
                    cutOutMapData.us_canada = us_canada
                    cutOutMapData.hd_amount = hd_amount
                    cutOutMapData.lw_in_kg = lw_in_kg
                    cutOutMapData.lw_avg_kg = lw_avg_kg
                    cutOutMapData.lw_avg_lbs = lw_avg_lbs
                    cutOutMapData.hhw_in_kg = hhw_in_kg
                    cutOutMapData.total_hhw_lbs = total_hhw_lbs
                    cutOutMapData.hhw_avg_kg = hhw_avg_kg
                    cutOutMapData.hhw_avg_lbs = hhw_avg_lbs
                    cutOutMapData.yield_dress = yield_dress
                    cutOutMapData.cw_in_kg = cw_in_kg
                    cutOutMapData.cw_shrink = cw_shrink
                    cutOutMapData.cw_avg_kg = cw_avg_kg
                    cutOutMapData.cw_avg_lbs = cw_avg_lbs
                    cutOutMapData.live_dollar_per_kg = live_dollar_per_kg
                    cutOutMapData.yield_cut = yield_cut
                    cutOutMapData.hhw_dollar_per_kg = hhw_dollar_per_kg
                    cutOutMapData.hhw_avg_kg_meat = hhw_avg_kg_meat
                    cutOutMapData.hhw_avg_lbs_meat = hhw_avg_lbs_meat
                    cutOutMapData.yield_meat = yield_meat
                    cutOutMapData.bulls_amount = bulls_amount
                    cutOutMapData.heifers_amount = heifers_amount
                    cutOutMapData.cows_amount = cows_amount
                    cutOutMapData.doa_inpen = doa_inpen
                    cutOutMapData.hhw_dollar_per_lb = hhw_dollar_per_lb
                    cutOutMapData.cost_hhw = cost_hhw
                    cutOutMapData.cost_plant_hd = cost_plant_hd
                    cutOutMapData.cost_plant = cost_plant
                    cutOutMapData.cost_fob = cost_fob
                    cutOutMapData.cost_sga_lb = cost_sga_lb
                    cutOutMapData.cost_sga = cost_sga
                    cutOutMapData.cost_kill = cost_kill
                    cutOutMapData.sell_primal = sell_primal
                    cutOutMapData.sell_offal = sell_offal
                    cutOutMapData.sell_profit = sell_profit
                    cutOutMapData.sell_primal_hd = sell_primal_hd
                    cutOutMapData.sell_offal_hd = sell_offal_hd
                    cutOutMapData.margin = margin
                    cutOutMapData.sell_hd = sell_hd
                    cutOutMapData.cost_hd = cost_hd
                    cutOutMapData.profit_hd = profit_hd
                    cutOutMapData.eu_fx = eu_fx
                    cutOutMapData.kgs_total = kgs_total
                    if is_price_lb_usd:
                        cutOutMapData.price_lb_usd = round(float(self.getCellValue(
                            rowindex, i_price_lb_usd[1]
                        )), 2) if self.is_valid_float(self.getCellValue(rowindex, i_sell_kg[1])) else None
                    cutOutMapData.code_crl = self.getCellValue(
                        rowindex, i_code[1])  # Code
                    cutOutMapData.sell_kg = round(float(self.getCellValue(rowindex, i_sell_kg[1])), 2) if self.is_valid_float(self.getCellValue(
                        rowindex, i_sell_kg[1])) else None
                    # Sales Price #1 per kg
                    cutOutMapData.kgs_hd = round(float(self.getCellValue(rowindex, i_kgs_hd[1])), 2) if self.getCellValue(
                        rowindex, i_kgs_hd[1]) is not None else None
                    # Average kg per head
                    cutOutMapData.value_total = round(float(self.getCellValue(rowindex, i_value_total[1])), 2) if self.is_valid_float(self.getCellValue(
                        rowindex, i_value_total[1])) else None
                    # TBD
                    val_percent = str(round(float(self.checkValue(self.getCellValue(rowindex, i_wt_percent_cuts[1]))) * 100, 2)) + "%" if i_wt_percent_cuts is not None and self.checkValue(
                        self.getCellValue(rowindex, i_wt_percent_cuts[1])) is not None else None
                    cutOutMapData.wt_percent_cuts = val_percent
                    if "FAT" in self.getCellValue(rowindex, i_code[1] + 1) or "Kidney" in self.getCellValue(rowindex, i_code[1] + 1):
                        fat_percent += float(
                            val_percent[:-1]) if val_percent is not None else 0.0
                    # % weight of cuts
                    cutOutMapData.value_percent = str(round(float(self.getCellValue(rowindex, i_value_percent[1])) * 100, 2)) + "%" if self.getCellValue(
                        rowindex, i_value_percent[1]) is not None else None
                    # % Value from av. kg sales price
                    cutOutMapData.cogs_kg = round(float(self.getCellValue(rowindex, i_cogs_kg[1])), 2) if self.getCellValue(
                        rowindex, i_cogs_kg[1]) is not None else None
                    # Product Inventory cost value/kg
                    cutOutMapData.cogs = round(float(self.getCellValue(rowindex, i_cogs[1])), 2) if self.is_valid_float(self.getCellValue(
                        rowindex, i_cogs[1])) else None
                    # Product Inventory cost
                    cutOutMapsDatas.append(cutOutMapData)
                    count += 1
                rowindex += 1
            offal_kgs = round(float(self.getCellValue(
                rowindex, i_kgs_total[1])), 2) if count > 0 and self.getCellValue(
                rowindex, i_kgs_total[1]) is not None else 0  # Total KG

            kgs_hd_offal = round(float(self.getCellValue(rowindex, 2)), 2) if offal_kgs > 0 and self.getCellValue(
                rowindex, 2) is not None else None
            # per head total KG by-products(offals)
            yield_offals = str(round(float(self.getCellValue(rowindex, 3)) * 100, 2)) + "%" if offal_kgs > 0 and self.getCellValue(
                rowindex, 3) is not None else None
            # per head total KG by-products (offals)
            offal_avg_dollar_kg = round(float(self.checkValue(self.getCellValue(rowindex, i_kgs_hd[1]))), 2) if offal_kgs > 0 and self.checkValue(
                self.getCellValue(rowindex, i_kgs_hd[1])) is not None else None
            # TBD
        for cutOutMapsData in cutOutMapsDatas:
            cutOutMapsData.primal_kgs = primal_kgs
            cutOutMapsData.primal_avg_dollar_kg = primal_avg_dollar_kg
            cutOutMapsData.kgs_hd_offal = kgs_hd_offal
            cutOutMapsData.yield_offals = yield_offals
            cutOutMapsData.offal_kgs = offal_kgs
            cutOutMapsData.offal_avg_dollar_kg = offal_avg_dollar_kg
            cutOutMapsData.fat_percent = str(round(fat_percent, 2)) + '%'
        CutOutMap.objects.bulk_create(cutOutMapsDatas)
        CutOutMail.objects.create(state_flag=2, date=datetime.now())
        result = self.convert_to_list(cutOutMapsDatas)
        return result
