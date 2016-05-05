from django.contrib import admin
from .models import *
# Register your models here.
#admin.site.register(Region)
#admin.site.register(Country)
admin.site.register(Currency)
#admin.site.register(Office)
admin.site.register(PurchaseRequestStatus)
admin.site.register(FundCode)
admin.site.register(DeptCode)
admin.site.register(LinCode)
admin.site.register(ActivityCode)
admin.site.register(PurchaseRequest)
admin.site.register(Vendor)
admin.site.register(FinanceCodes)
admin.site.register(Unit)
admin.site.register(Item)
admin.site.register(RequestForQuotation)
admin.site.register(RequestForQuotationItem)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)
admin.site.register(GoodsReceivedNote)
admin.site.register(GoodsReceivedNoteItem)