from django.db import models

class TransportBill(models.Model):

    ms = models.CharField(max_length=200)
    ms_address1 = models.CharField(max_length=200, blank=True)
    ms_address2 = models.CharField(max_length=200, blank=True)

    bill_no = models.CharField(max_length=50)
    date = models.DateField()
    vehicle_no = models.CharField(max_length=50)

    consignee_gstin = models.CharField(max_length=20, blank=True, null=True)
    consignor_gstin = models.CharField(max_length=20, blank=True, null=True)
    
    invoice_no = models.CharField(max_length=50)
    gc_note_no = models.CharField(max_length=50)

    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)

    pkg = models.IntegerField()
    particular = models.CharField(max_length=200)
    weight = models.FloatField()
    amount = models.FloatField()

    # ✅ NEW FIELDS
    gst_choice = models.CharField(max_length=10, default="no")
    add_stamp = models.CharField(max_length=10, default="no")

    total = models.FloatField(blank=True, null=True)
    cgst = models.FloatField(blank=True, null=True)
    sgst = models.FloatField(blank=True, null=True)
    grand_total = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):

        self.total = self.amount

        # ✅ APPLY GST ONLY IF YES
        if self.gst_choice == "yes":
            cgst_amt = (self.total * 9) / 100
            sgst_amt = (self.total * 9) / 100

            self.cgst = cgst_amt
            self.sgst = sgst_amt
            self.grand_total = self.total + cgst_amt + sgst_amt

        else:
            # ✅ RESET GST
            self.cgst = 0
            self.sgst = 0
            self.grand_total = self.total

        super().save(*args, **kwargs)