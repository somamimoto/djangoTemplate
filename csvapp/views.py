import io
import csv
from datetime import datetime
from django.shortcuts import render
from .forms import CsvFileUploadForm
from .models import Product, SalesHistory


def csv_import(request):
    if request.method == 'POST':
        form = CsvFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            bfile = request.FILES['file']  # BytesIO() https://github.com/django/django/blob/main/django/http/request.py
            file = io.TextIOWrapper(bfile, encoding='utf-8')

            # To bulk insert database, organize the file data
            saleshistory_instances = []
            if form.cleaned_data['has_header']:  # Once form is_valid, it will have cleaned_data
                reader = csv.DictReader(file)
                for row in reader:
                    product_instance, _ = Product.objects.get_or_create(name=row['product'])
                    saleshistory_instances.append(
                        SalesHistory(
                            product=product_instance,
                            sales_num=int(row['num']),
                            sales_date=datetime.strptime(row['date'], "%Y/%m/%d")
                        )
                    )
                del reader
            else:
                reader = csv.reader(file)
                for row in reader:
                    product_instance, _ = Product.objects.get_or_create(name=row[0])
                    saleshistory_instances.append(
                        SalesHistory(
                            product=product_instance,
                            sales_num=row[1],
                            sales_date=datetime.strptime(row[2], "%Y/%m/%d")
                        )
                    )
                del reader
            SalesHistory.objects.bulk_create(saleshistory_instances)
        else:
            print(form.errors)
    else:
        form = CsvFileUploadForm()
    context = {'form': form,}
    return render(request, 'csvapp/csv_import.html', context)


def csv_export(request):
    context = {}
    return render(request, 'csvapp/csv_export.html', context)
