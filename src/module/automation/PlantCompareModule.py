from src.models import CutOutMap
from django.db.models import Sum

from datetime import datetime
from dateutil.relativedelta import relativedelta


class PlantCompareModule:

    def __init__(self, period):
        self.ws = []
        self.period = period
        self.start_date = datetime.now().date().replace(
            year=2023, month=11, day=15).strftime("%Y-%m-%d")
        self.end_date = datetime.now().date().strftime("%Y-%m-%d")
        self.header = ["HARVEST Date", "Plant", "# Head", "# Bulls", "# Heifers", "# Cows", "Live plant", "HHW Avg", "CHW Avg", "Yield at plant  %",
                       "Hot to Cold Shrink", "HHW price Paid $", "Cut Yield", "Meat Yield", "Fat in Cut Out % (W/Kidney CAN)", "Plant cost/head $", "Net profit %", "Net Profit per hd", "Net Profit for Kill"]
        self.list_total_avg = []

    def cow_filter(self, item):
        return item['cows_amount'] is None or item['cows_amount'] < item['hd_amount'] / 2
    # for cow category

    def reverse_filter(self, item):
        return not self.cow_filter(item)

    def append_cutout_all(self, cutout):
        plant_groups_no = {}
        for item in cutout:
            plant_name = item['plant_name']
            if plant_name not in plant_groups_no:
                plant_groups_no[plant_name] = []
            plant_groups_no[plant_name].append(item)

        # Add headers to the worksheet
        self.ws.append(self.header)

        # Process each plant group
        for plant_name, cutout_animals in plant_groups_no.items():
            for cutout_animal in cutout_animals:
                self.ws.append([
                    str(cutout_animal['date']),
                    cutout_animal['plant_name'],
                    cutout_animal['hd_amount'],
                    cutout_animal['bulls_amount'],
                    cutout_animal['heifers_amount'],
                    cutout_animal['cows_amount'],
                    cutout_animal['lw_avg_lbs'],
                    cutout_animal['hhw_avg_lbs'],
                    cutout_animal['cw_avg_lbs'],
                    cutout_animal['yield_dress'],
                    cutout_animal['cw_shrink'],
                    cutout_animal['hhw_dollar_per_lb'],
                    cutout_animal['yield_cut'],
                    cutout_animal['yield_meat'],
                    cutout_animal['fat_percent'],
                    cutout_animal['cost_plant_hd'],
                    cutout_animal['margin'],
                    cutout_animal['profit_hd'],
                    cutout_animal['sell_profit'],
                ])  # Add more fields if necessary`
            self.append_quartiles(cutout_animals, plant_name)
            self.append_cutout(cutout_animals, plant_name)
        self.calculate_total_avg(cutout)

    def append_cutout(self, cutout_animal, plant_name):
        count = len(cutout_animal)

        total_hd_amount = 0
        total_lw_avg_lbs = 0
        total_hhw_avg_lbs = 0
        total_yield_dress = 0
        total_hhw_dollar_per_lb = 0
        total_yield_cut = 0
        total_yield_meat = 0
        total_cost_plant_hd = 0
        total_margin = 0
        total_profit_hd = 0
        total_sell_profit = 0

        for cutout in cutout_animal:
            total_hd_amount += cutout['hd_amount']
            total_lw_avg_lbs += cutout['lw_avg_lbs']
            total_hhw_avg_lbs += cutout['hhw_avg_lbs']
            total_yield_dress += cutout['yield_dress']
            total_hhw_dollar_per_lb += cutout['hhw_dollar_per_lb']
            total_yield_cut += cutout['yield_cut']
            total_yield_meat += cutout['yield_meat']
            total_cost_plant_hd += cutout['cost_plant_hd']
            total_margin += cutout['margin']
            total_profit_hd += cutout['profit_hd']
            total_sell_profit += cutout['sell_profit']

        self.ws.append([
            f'{plant_name} Graded non weighted average',
            None,
            round(total_hd_amount / count),
            None,
            None,
            None,
            round(total_lw_avg_lbs / count * 10)/10,
            round(total_hhw_avg_lbs / count * 10)/10,
            None,
            round(total_yield_dress / count * 1000)/1000,
            None,
            round(total_hhw_dollar_per_lb / count * 100)/100,
            round(total_yield_cut / count * 1000)/1000,
            round(total_yield_meat / count * 1000)/1000,
            None,
            round(total_cost_plant_hd / count * 100)/100,
            round(total_margin / count * 1000) / 1000,
            round(total_profit_hd / count * 1000) / 1000,
            round(total_sell_profit / count * 1000) / 1000,
        ])

    def calculate_total_avg(self, cutout_data):
        total_hd_amount = 0
        total_lw_avg_lbs = 0
        total_hhw_avg_lbs = 0
        total_yield_dress = 0
        total_hhw_dollar_per_lb = 0
        total_yield_cut = 0
        total_yield_meat = 0
        total_cost_plant_hd = 0
        total_margin = 0
        total_profit_hd = 0
        total_sell_profit = 0
        count = len(cutout_data)
        if count == 0:
            return 0
        for cutout in cutout_data:
            if cutout['plant_name'] == 'BVY':
                continue
            total_hd_amount += cutout['hd_amount']
            total_lw_avg_lbs += cutout['lw_avg_lbs']
            total_hhw_avg_lbs += cutout['hhw_avg_lbs']
            total_yield_dress += cutout['yield_dress']
            total_hhw_dollar_per_lb += cutout['hhw_dollar_per_lb']
            total_yield_cut += cutout['yield_cut']
            total_yield_meat += cutout['yield_meat']
            total_cost_plant_hd += cutout['cost_plant_hd']
            total_margin += cutout['margin']
            total_profit_hd += cutout['profit_hd']
            total_sell_profit += cutout['sell_profit']

        # Calculate averages
        self.ws.append([
            'All Graded non weighted average',
            None,
            round(total_hd_amount / count),
            None,
            None,
            None,
            round(total_lw_avg_lbs / count * 10)/10,
            round(total_hhw_avg_lbs / count * 10)/10,
            None,
            round(total_yield_dress / count * 1000)/1000,
            None,
            round(total_hhw_dollar_per_lb / count * 100)/100,
            round(total_yield_cut / count * 1000)/1000,
            round(total_yield_meat / count * 1000)/1000,
            None,
            round(total_cost_plant_hd / count * 100)/100,
            round(total_margin / count * 1000) / 1000,
            round(total_profit_hd / count * 1000) / 1000,
            round(total_sell_profit / count * 1000) / 1000,
        ])

    def append_quartiles(self, cutout_animal, plant_name):
        # Sort data by yield_dress
        sorted_data = sorted(
            cutout_animal, key=lambda x: x['yield_dress'] or 0, reverse=True)
        count = len(sorted_data)

        if count < 4:
            return

        # Split data into quartiles
        q1 = sorted_data[:count // 4]
        q2 = sorted_data[count // 4: count // 2]
        q3 = sorted_data[count // 2: 3 * count // 4]
        q4 = sorted_data[3 * count // 4:]
        # Helper to calculate averages

        def calculate_avg(data):
            if not data:
                # Adjust the number of columns to match the header
                return [None] * 18
            total_hd_amount = sum(d['hd_amount'] for d in data)
            total_lw_avg_lbs = sum(d['lw_avg_lbs'] or 0 for d in data)
            total_hhw_avg_lbs = sum(d['hhw_avg_lbs'] or 0 for d in data)
            total_yield_dress = sum(d['yield_dress'] or 0 for d in data)
            total_hhw_dollar_per_lb = sum(
                d['hhw_dollar_per_lb'] or 0 for d in data)
            total_yield_cut = sum(d['yield_cut'] or 0 for d in data)
            total_yield_meat = sum(d['yield_meat'] or 0 for d in data)
            total_cost_plant_hd = sum(d['cost_plant_hd'] or 0 for d in data)
            total_margin = sum(d['margin'] or 0 for d in data)
            total_profit_hd = sum(d['profit_hd'] or 0 for d in data)
            total_sell_profit = sum(d['sell_profit'] or 0 for d in data)
            count = len(data)
            if count == 0:
                return 0
            return [
                None,
                round(total_hd_amount / count),
                None,
                None,
                None,
                round(total_lw_avg_lbs / count * 10) / 10,
                round(total_hhw_avg_lbs / count * 10) / 10,
                None,
                round(total_yield_dress / count * 1000) / 1000,
                None,
                round(total_hhw_dollar_per_lb / count * 100) / 100,
                round(total_yield_cut / count * 1000) / 1000,
                round(total_yield_meat / count * 1000) / 1000,
                None,
                round(total_cost_plant_hd / count * 100) / 100,
                round(total_margin / count * 1000) / 1000,
                round(total_profit_hd / count * 1000) / 1000,
                round(total_sell_profit / count * 1000) / 1000,
            ]

        # Add rows for each quartile
        self.ws.append([f"{plant_name} Top Quartile"] + calculate_avg(q1))
        self.ws.append([f"{plant_name} 2nd Quartile"] + calculate_avg(q2))
        self.ws.append([f"{plant_name} 3rd Quartile"] + calculate_avg(q3))
        self.ws.append([f"{plant_name} BOTTOM Quartile"] + calculate_avg(q4))

    def get_report(self):
        # Create an in-memory Excel workbook
        cutout_maps = CutOutMap.objects.filter()
        cutout_maps_cow = cutout_maps.filter(date__range=[self.period["start_d"], self.period["end_d"]]).values(
            'date', 'lot_number', 'plant_name', 'hd_amount', 'bulls_amount',
            'heifers_amount', 'cows_amount', 'doa_inpen', 'lw_avg_lbs', 'hhw_avg_lbs',
            'cw_avg_lbs', 'yield_dress', 'cw_shrink', 'hhw_dollar_per_lb',
            'yield_cut', 'yield_meat', 'fat_percent', 'cost_plant_hd', 'margin', 'profit_hd', 'sell_profit').order_by().annotate(
            Sum("lot_number")
        ).order_by('plant_name', 'date')
        list_cutout = list(cutout_maps_cow)
        filterd_cutout = []
        for _, item in enumerate(list_cutout):
            item['hd_amount'] = item['hd_amount'] - \
                item['doa_inpen'] if item['doa_inpen'] is not None else item['hd_amount']
            item['lw_avg_lbs'] = round(
                item['lw_avg_lbs']) if item['lw_avg_lbs'] is not None else None
            item['hhw_avg_lbs'] = round(
                item['hhw_avg_lbs']) if item['hhw_avg_lbs'] is not None else None
            item['cw_avg_lbs'] = round(
                item['cw_avg_lbs']) if item['cw_avg_lbs'] is not None else None
            item['yield_dress'] = round(float(
                (item['yield_dress'][:-1]))*10)/1000 if item['yield_dress'] is not None else None
            item['cw_shrink'] = round(
                float((item['cw_shrink'][:-1]))*10)/1000 if item['cw_shrink'] is not None else None
            item['yield_cut'] = round(
                float((item['yield_cut'][:-1]))*10)/1000 if item['yield_cut'] is not None else None
            item['yield_meat'] = round(float(
                (item['yield_meat'][:-1]))*10)/1000 if item['yield_meat'] is not None else None
            item['margin'] = round(float(
                (item['margin'][:-1]))*10)/1000 if item['margin'] is not None else None
            item['fat_percent'] = round(
                float((item['fat_percent'][:-1]))*10)/1000 if item['fat_percent'] != '0' and item['fat_percent'] != '0%' else None
            item['profit_hd'] = item['profit_hd'] if item['profit_hd'] is not None else None
            item['sell_profit'] = item['sell_profit'] if item['sell_profit'] is not None else None
            filterd_cutout.append(item)
        cutout_no = list(filter(self.cow_filter, filterd_cutout))
        cutout_cow = list(filter(self.reverse_filter, filterd_cutout))

        self.append_cutout_all(cutout_no)

        self.append_cutout_all(cutout_cow)
        return self.ws
