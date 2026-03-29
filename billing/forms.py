from django import forms
from .models import TransportBill

class TransportBillForm(forms.ModelForm):

    class Meta:
        model = TransportBill
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

    # ADD THIS PART BELOW
    def clean(self):
        cleaned_data = super().clean()

        consignee = cleaned_data.get("consignee_gstin")
        consignor = cleaned_data.get("consignor_gstin")

        # both empty
        if not consignee and not consignor:
            raise forms.ValidationError(
                "Either Consignee GSTIN or Consignor GSTIN must be provided."
            )

        # both filled
        if consignee and consignor:
            raise forms.ValidationError(
                "Only one GSTIN should be filled (Consignee OR Consignor)."
            )

        return cleaned_data