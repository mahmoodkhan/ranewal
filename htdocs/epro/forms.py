from django.core.urlresolvers import reverse_lazy, reverse
from django.core.exceptions import ValidationError

from django.db.models import Sum
from django import forms
from django.forms import ModelForm, inlineformset_factory, HiddenInput, Textarea

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from django.views.generic.edit import CreateView, UpdateView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Reset, Button, HTML, Layout, Field, Div, Column
from crispy_forms.bootstrap import FormActions, AppendedText

from .models import Country, Office, Currency, UserProfile, PurchaseRequest, Item, FinanceCodes, ItemAttachment


"""
A generic method used for setting up similar bootstrap properties on crispy forms
"""
def setup_boostrap_helpers(formtag=False):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-sm-2'
    helper.field_class = 'col-sm-10'
    helper.html5_required = True
    helper.form_show_labels = True
    helper.error_text_inline = True
    helper.help_text_inline = True
    helper.form_show_errors = True
    helper.form_tag = formtag
    return helper


class PurchaseRequestForm(forms.ModelForm):
    approverOne = forms.CharField(label=_('Approver1'), max_length=100, required=False,
         help_text="<span style='color:red'>*</span> This is the person who manages the Fund")
    approverTwo = forms.CharField(label=_('Approver2'), max_length=100, required=False,
        help_text="Refer to your <abbr title='Approval Authority Matrix'>AAM</abbr> to determine if you need to specify a second approval.")
    originating_office = forms.CharField(label=_("Originating Office"), max_length=100, required=False,
        help_text="<span style='color:red'>*</span> The Office in which this PR is originated")
    pr_currency = forms.CharField(label=_("PR Currency"), max_length=100, required=True,
        help_text="<span style='color:red'>*</span> This the currency in which the transaction occurs.")

    class Meta:
        model = PurchaseRequest
        fields = ['country', 'project_reference', 'delivery_address', 'dollar_exchange_rate', 'required_date', 'originator']
        widgets = {'originator': forms.HiddenInput()}
        labels = {
            'country': _('Originating Country'),
            'office': _('Originating Office'),
            'dollar_exchange_rate': _('USD Exchange rate'),
        }

    def clean_approverOne(self):
        approverOne = self.cleaned_data.get('approverOne', None)
        if not approverOne:
            raise ValidationError("ApproverOne is required.")
        return approverOne

    def clean_originating_office(self):
        originating_office = self.cleaned_data.get('originating_office', None)
        if not originating_office:
            raise ValidationError("Originating Office is required.")
        return originating_office

    def clean_pr_currency(self):
        pr_currency = self.cleaned_data.get('pr_currency', None)
        if not pr_currency:
            raise ValidationError("PR Currency is required")
        return pr_currency

    def __init__(self, *args, **kwargs):
        pr_pk = kwargs.pop('pk', None)
        country_id = kwargs.pop('country_id', None)
        super(PurchaseRequestForm, self).__init__(*args, **kwargs)
        self.fields['country'].empty_label = ''
        self.fields['project_reference'].widget.attrs['placeholder'] = _('Project Reference')
        self.fields['delivery_address'].widget.attrs['placeholder'] = _('Delivery Address')
        self.fields['dollar_exchange_rate'].widget.attrs['placeholder'] = _('USD Exchange Rate')
        self.fields['required_date'].widget.attrs['placeholder'] = _('Required Date')
        self.helper = setup_boostrap_helpers(formtag=True)
        #self.helper.form_class = 'form-inline'
        self.helper.attrs = {'id': 'id_prform', }
        self.helper.form_action = reverse_lazy('pr_edit' if pr_pk else 'pr_new', kwargs = {'pk': pr_pk} if pr_pk else None)
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-sm btn-primary'))
        self.helper.add_input(Reset('reset', 'Reset', css_class='btn-sm btn-warning'))
        self.helper.form_show_labels = False
        self.helper.label_class = 'col-sm-0'
        self.helper.field_class = 'col-xs-12'
        self.helper.layout = Layout(
            Div(
                Div(
                    Column(
                        Field('country',),
                        css_class="col-sm-6",
                    ),
                    Column(
                        Field('originating_office',),
                        css_class="col-sm-6",
                    ),
                    css_class="row",
                ),
                Div(
                    Column(
                        Field('project_reference',),
                        css_class="col-sm-12",
                    ),
                    css_class="row",
                ),
                Div(
                    Column(
                        Field('delivery_address',),
                        css_class="col-sm-6",
                    ),
                    Column(
                        Field('required_date',),
                        css_class="col-sm-6",
                    ),
                    css_class="row",
                ),
                Div(
                    Column(
                        Field('pr_currency',),
                        css_class="col-xs-6",
                    ), Column(
                        Field('dollar_exchange_rate',),
                        css_class="col-xs-6",
                    ),
                    css_class="row",
                ),
                Div(
                    Column(
                        Field('approverOne',),
                        css_class="col-sm-6",
                    ), Column(
                        Field('approverTwo',),
                        css_class="col-sm-6",
                    ),
                    css_class="row",
                ),
                css_class="col-xs-12",
            ),
        )

class PurchaseRequestItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['purchase_request', 'quantity', 'unit', 'description', 'price_estimated_local', ]
        widgets = {'purchase_request': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        item_id = kwargs.pop('pk', None)
        super(PurchaseRequestItemForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['rows'] = 3
        self.helper = setup_boostrap_helpers(formtag=True)

        if item_id:
            url = 'item_edit'
            url_params = {'pk': item_id}
        else:
            url = 'item_new'
            url_params = {'pr': kwargs['initial']['purchase_request']}

        self.fields['unit'].empty_label = ''
        self.helper.form_action = reverse_lazy(url, kwargs=url_params)
        self.helper.form_id = 'id_pr_item_form'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn-sm btn-primary'))
        self.helper.add_input(Reset('reset', 'Reset', css_class='btn-sm btn-warning'))


class PurchaseRequestItemAttachmentForm(forms.ModelForm):
    class Meta:
        model = ItemAttachment
        fields = ['item', 'file',]
        widgets = {'item': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(PurchaseRequestItemAttachmentForm, self).__init__(*args, **kwargs)
        self.fields['file'].label = ''
        self.fields['file'].widget.attrs.update({"style": "visibility:hidden;"})
        self.helper = setup_boostrap_helpers(formtag=True)
        self.helper.form_id = 'id_attachment_form'
        self.helper.form_class = "dropzone"
        self.helper.form_action = reverse_lazy("item_attachment_new", kwargs={"pk": kwargs['initial'].get('item', 0)})
        #self.helper.add_input(Submit('submit', 'Upload', css_class='btn-sm btn-primary'))

    def clean_file(self):
        file = self.cleaned_data['file']
        if file:
            #print(file.content_type)
            #print(file.size)
            pass
        return file

    def save(self, commit=True):
        instance = super(PurchaseRequestItemAttachmentForm, self).save(commit=False)
        instance.file_type = self.cleaned_data['file'].content_type
        instance.file_size = self.cleaned_data['file'].size
        if commit:
            instance.save()
        return instance


class FinanceCodesForm(forms.ModelForm):
    """
    To add entries, this form has to be instantiated with initial values of item_id and form_action
    To edit entries, this form has to be instantiated with initial value of form_action.
    """
    class Meta:
        model = FinanceCodes
        fields = ['item', 'gl_account', 'fund_code', 'dept_code', 'office_code', 'lin_code', 'activity_code', 'employee_id', 'allocation_percent', ]
        labels = {'allocation_percent': _('Allocation %'), }
        widgets = {'item': forms.HiddenInput()}

    def clean_gl_account(self):
        gl_account = self.cleaned_data.get('gl_account', None)
        try:
            gl_account_length = len(str(int(gl_account)))
        except Exception as e:
            raise ValidationError(_("GL Account must be a five digits number"))

        if gl_account_length > 4 or gl_account_length < 4:
            raise ValidationError(_("GL Account must be a four digits number"))
        return gl_account

    def clean_allocation_percent(self):
        allocation_percent = self.cleaned_data.get('allocation_percent', None)
        try:
            allocation_percent = float(allocation_percent)
        except Exception as e:
            raise ValidationError(_("Allocation Percent must be a number"))

        item = self.cleaned_data.get('item', None)
        if not item:
            raise ValidationError(_("Finance Codes must be added to an Item"))

        if not allocation_percent:
            raise ValidationError(_("Allocation_percent is required."))

        total = item.finance_codes.aggregate(Sum('allocation_percent'))
        if not self.instance.pk and total['allocation_percent__sum']:
            if ( float(total['allocation_percent__sum']) + allocation_percent) > 100:
                raise ValidationError(_("Allocations cannot be more than 100%"))
        else:
            if allocation_percent > 100:
                raise ValidationError(_("Allocations cannot be more than 100%"))
        return allocation_percent

    def __init__(self, *args, **kwargs):
        finance_codes_id = kwargs.pop('pk', None)
        super(FinanceCodesForm, self).__init__(*args, **kwargs)
        self.helper = setup_boostrap_helpers(formtag=True)
        if finance_codes_id:
            form_action = "financecodes_edit"
            params = {"pk": finance_codes_id}
        else:
            form_action = "financecodes_new"
            params = {"item_id": kwargs['initial'].get('item', None)}
        #print("form_action: %s params: %s" % (form_action, params))
        self.helper.form_action = reverse_lazy(form_action, kwargs=params)
        self.fields['fund_code'].empty_label = ''
        self.fields['dept_code'].empty_label = ''
        self.fields['office_code'].empty_label = ''
        self.fields['gl_account'].widget.attrs['placeholder'] = _('GL Account')
        self.helper.form_id = 'id_finance_codes_form'
        self.helper.label_class = 'col-sm-offset-0 col-sm-5'
        self.helper.field_class = 'col-sm-7'
        self.helper.layout = Layout(
            Div(
                Column(
                    Field('gl_account',),
                    Field('fund_code',),
                    Field('dept_code',),
                    Field('office_code',),
                    css_class="col-sm-6",
                ), Column(
                    Field('lin_code',),
                    Field('activity_code',),
                    Field('employee_id',),
                    Field(AppendedText('allocation_percent', '%'),),
                    css_class="col-sm-6",
                ),
                css_class="row",
            ),
            Div(
                Column(
                    FormActions(
                        Submit('save', 'Save changes', css_id='id_submit_finance_codes_btn', css_class='btn-sm btn-primary'),
                        Reset('reset', 'Cancel', css_id='id_cancel_finance_codes_btn', css_class='btn-sm btn-warning')
                    ),
                    css_class="col-sm-12",
                ),
                css_class="row",
            ),
        )
