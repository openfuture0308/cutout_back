from src.models import CutOutMap

from django.db.models import F, Value
from django.db.models.functions import Coalesce, Concat

cutout_maps = CutOutMap.objects.filter(
    hd_amount__lt=Coalesce(F('cows_amount') * 2, Value(0))
).update(
    lot_number=Concat(F('lot_number'), Value('-COW'))
)
list_cutout = list(cutout_maps)
