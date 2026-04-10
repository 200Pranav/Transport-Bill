from django.shortcuts import render, get_object_or_404
from .forms import TransportBillForm
from .models import TransportBill
from num2words import num2words

def create_bill(request, bill_id=None):
    bill = None
    if bill_id:
        bill = get_object_or_404(TransportBill, id=bill_id)

    if request.method == "POST":
        form = TransportBillForm(request.POST, instance=bill)

        if form.is_valid():
            bill = form.save(commit=False)

            gst_choice = request.POST.get("gst_choice")
            add_stamp = request.POST.get("add_stamp")
            gst_by_consignor = request.POST.get("gst_by_consignor")
            amount = float(request.POST.get("amount", 0))

            if gst_choice == "yes":
                cgst = amount * 0.09
                sgst = amount * 0.09
                grand_total = amount + cgst + sgst
            else:
                cgst = 0
                sgst = 0
                grand_total = amount

            bill.cgst = cgst
            bill.sgst = sgst
            bill.grand_total = grand_total
            bill.gst_choice = gst_choice
            bill.add_stamp = add_stamp
            bill.save()

            words = num2words(grand_total, lang='en_IN') + " rupees only"

            return render(request, "bill.html", {
                "bill": bill,
                "grand_total": grand_total,
                "words": words,
                "gst_by_consignor": gst_by_consignor
            })
        else:
            return render(request, "bill_form.html", {"form": form, "bill": bill})
    else:
        form = TransportBillForm(instance=bill)

    return render(request, "bill_form.html", {"form": form, "bill": bill})