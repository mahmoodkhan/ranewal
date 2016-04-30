from django.conf.urls import include, url
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import TemplateView

from rest_framework.urlpatterns import format_suffix_patterns

from epro.views import *


urlpatterns = [
    url(r'^$', PurchaseRequestListView.as_view(), name='pr_list'),
    url(r'^pr/add/$', PurchaseRequestCreateView.as_view(), name='pr_new'),
    url(r'^pr/edit/(?P<pk>\d+)/$', PurchaseRequestUpdateView.as_view(), name='pr_edit'),
    url(r'^pr/(?P<pk>\d+)/$', PurchaseRequestDetailView.as_view(), name='pr_view'),
    url(r'^pr/del/(?P<pk>\d+)/$', PurchaseRequestDeleteView.as_view(), name='pr_del'),

    url(r'^pr/apply_default_codes_to_all/(?P<pr_id>\d+)/$', ApplyDefaultFinanceCodesToAllItems.as_view(), name='apply_default_codes_to_all'),
    url(r'^pr/set_default_codes/(?P<item_id>\d+)/$', SetDefaultFinanceCodesForPR.as_view(), name='set_pr_default_codes'),
    url(r'^pr/unset_default_finance_codes/(?P<item_id>\d+)/$', UnsetDefaultCodesForPR.as_view(), name='unset_default_finance_codes'),

    url(r'^pr/item/add/(?P<pr>\d+)/$', PurchaseRequestItemCreateView.as_view(), name='item_new'),
    url(r'^pr/item/edit/(?P<pk>\d+)/$', PurchaseRequestItemUpdateView.as_view(), name='item_edit'),
    #url(r'^item/view/(?P<pk>\d+)/$', PurchaseRequestItemDetailView.as_view(), name='item_view'),
    url(r'^pr/item/del/(?P<pk>\d+)/$', PurchaseRequestItemDeleteView.as_view(), name='item_del'),

    url(r'^pr/item/financecodes/add/(?P<item_id>\d+)/$', FinanceCodesCreateView.as_view(), name='financecodes_new'),
    url(r'^pr/item/financecodes/edit/(?P<pk>\d+)/$', FinanceCodesUpdateView.as_view(), name='financecodes_edit'),
    #url(r'^pr/item/financecodes/view/$', FinanceCodesDetailView.as_view(), name='financecodes_view'),
    url(r'^pr/item/financecodes/del/(?P<pk>\d+)/$', FinanceCodesDeleteView.as_view(), name='financecodes_del'),

    url(r'^pr/item/attachments/add/(?P<pk>\d+)/$', ItemAttachmentCreateView.as_view(), name='item_attachment'),
]

urlpatterns = format_suffix_patterns(urlpatterns)