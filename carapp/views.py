from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .utils import *


@require_http_methods(["GET"])
def get_center(request):
    if request.method == "GET":
        car_total, max_sale_name, most_sale = get_center_data()
        MaxModel = max_model()
        MostBrand = most_brand()
        AvgPrice = avg_price()
        ratio = get_ratio_data()
        return JsonResponse(
            {'car_total': car_total, 'max_sale_name': max_sale_name, 'car_most_sale': most_sale,
             'MaxModel': MaxModel, 'MostBrand': MostBrand, 'AvgPrice': AvgPrice, 'ratio': ratio}, )


@require_http_methods(["GET"])
def get_scrolldata(request):
    if request.method == "GET":
        scrolldata = get_scroll_data()
        return JsonResponse({'scrolldata': scrolldata})

@require_http_methods(["GET"])
def get_ratio(request):
    if request.method == "GET":
        ratio = get_ratio_data()
        return JsonResponse({'ratio': ratio})

@require_http_methods(["GET"])
def get_left(request):
    if request.method == "GET":
        oil_data,ele_data = get_left_data()
        words = get_wordcloud_data()
        return JsonResponse({'oil_data': oil_data, 'ele_data': ele_data, 'wordcloud_data': words})

@require_http_methods(["GET"])
def get_right(request):
    if request.method == "GET":
        pie_data = get_right_data()
        price_data = get_price_data()
        return JsonResponse({'pie_data': pie_data, 'price_data': price_data})

@require_http_methods(["GET"])
def get_bottom_left(request):
    if request.method == "GET":
        data = get_bottom_left_data()
        return JsonResponse({'data': data})

@require_http_methods(["GET"])
def get_bottom_right(request):
    if request.method == "GET":
        data = get_bottom_right_data()
        return JsonResponse({'data': data})