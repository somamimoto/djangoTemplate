import io
import csv
from datetime import datetime
from django.shortcuts import render, redirect
from .forms import CsvFileUploadForm, CsvFileExportForm
from .models import Product, SalesHistory
from django.contrib import messages


def csv_import(request):
    if request.method == 'POST':
        form = CsvFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            bfile = request.FILES['file']  # BytesIO() https://github.com/django/django/blob/main/django/http/request.py
            file = io.TextIOWrapper(bfile, encoding='utf-8')

            # To bulk insert database, organize the file data
            saleshistory_instances = []
            # When You want to check if csv has header, you can consider to use csv.Sniffer
            if form.cleaned_data['has_header'] == 'True':  # Once form is_valid, it will have cleaned_data
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
    if request.method == 'POST':
        form = CsvFileExportForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['select_data'] == 'product_data':
                object_list = Product.objects.all()
            else:
                object_list = SalesHistory.objects.all()
            _object_list = list(object_list)
            header_cols = [field for field in _object_list[0].__dict__.keys() if field not in ['_state', 'id']]
            # If You want to get fields name from Model itself, use MyModel.model._meta.fileds
            rows = []
            for obj in _object_list:
                row_vals = []
                for h_col in header_cols:
                    row_vals.append(getattr(obj, h_col))
                rows.append(row_vals)
            with open('export.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(header_cols)
            with open('export.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerows(rows)
                messages.success(request, 'Csv export has been done!')
                return redirect('csvapp:csv_export')
        else:
            print(form.errors)
    else:
        form = CsvFileExportForm()
    product_instances = Product.objects.all()
    saleshistory_instances = SalesHistory.objects.all()
    context = {'product_instances': product_instances, 'saleshistory_instances': saleshistory_instances, 'form': form}
    return render(request, 'csvapp/csv_export.html', context)
