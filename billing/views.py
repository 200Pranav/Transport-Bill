from django.shortcuts import render
from .forms import TransportBillForm
from num2words import num2words

def create_bill(request):

    if request.method == "POST":
        form = TransportBillForm(request.POST)

        if form.is_valid():

            bill = form.save(commit=False)   # ✅ IMPORTANT CHANGE

            # ✅ GET VALUES
            gst_choice = request.POST.get("gst_choice")
            add_stamp = request.POST.get("add_stamp")
            gst_by_consignor = request.POST.get("gst_by_consignor")

            amount = float(request.POST.get("amount", 0))

            # ✅ GST CALCULATION FIX
            if gst_choice == "yes":
                cgst = amount * 0.09
                sgst = amount * 0.09
                grand_total = amount + cgst + sgst
            else:
                cgst = 0
                sgst = 0
                grand_total = amount

            # ✅ SAVE VALUES IN MODEL
            bill.cgst = cgst
            bill.sgst = sgst
            bill.grand_total = grand_total
            bill.gst_choice = gst_choice
            bill.add_stamp = add_stamp

            bill.save()   # ✅ SAVE AFTER MODIFICATION

            # ✅ WORDS
            words = num2words(grand_total, lang='en_IN') + " rupees only"

            return render(request, "bill.html", {
                "bill": bill,
                "grand_total": grand_total,
                "words": words,
                "gst_by_consignor": gst_by_consignor
            })

        else:
            return render(request, "bill_form.html", {"form": form})
    else:
        form = TransportBillForm()

    return render(request, "bill_form.html", {"form": form})