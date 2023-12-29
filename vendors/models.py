from django.db import models
from django.utils import timezone
from django.db.models import Count, Avg
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator


# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=250)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True, validators=[RegexValidator(regex=r'^[A-Za-z0-9]+$')])
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    
    def calculate_on_time_delivery_rate(self):
        completed_pos = self.purchaseorder_set.filter(status='completed')
        on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now()).count()
        total_completed_pos = completed_pos.count()
        return (on_time_deliveries / total_completed_pos) * 100 if total_completed_pos > 0 else 0

    def calculate_quality_rating_avg(self):
        completed_pos = self.purchaseorder_set.filter(status='completed').exclude(quality_rating__isnull=True)
        return completed_pos.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0

    def calculate_average_response_time(self):
        completed_pos = self.purchaseorder_set.filter(status='completed', acknowledgment_date__isnull=False)
        response_times = [po.calculate_response_time() for po in completed_pos]
        return sum(response_times) / len(response_times) if response_times else 0

    def calculate_fulfillment_rate(self):
        all_pos = self.purchaseorder_set.count()
        successfully_fulfilled_pos = self.purchaseorder_set.filter(status='completed', quality_rating__isnull=True).count()
        return (successfully_fulfilled_pos / all_pos) * 100 if all_pos > 0 else 0
    
    
    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    # To calculate Response time
    def calculate_response_time(self):
        if self.acknowledgment_date:
            return (self.acknowledgment_date - self.issue_date).total_seconds() / 3600
        return None
    
    def __str__(self):
        return f"{self.po_number} - {self.vendor.name}"
    
class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"