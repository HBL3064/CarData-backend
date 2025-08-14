from django.db import models
from django.db.models import Q
from carapp.models import CarData


def get_center_data():
    all_data = CarData.objects.all()
    car_total = len(all_data)
    car_maxsale_name = CarData.objects.filter(car_rank='1').first().series_name
    car_mostsale = CarData.objects.filter(car_rank='1').first().car_count
    return car_total, car_maxsale_name, car_mostsale


def max_model():
    all_data = CarData.objects.all()
    max_model_dict = {}
    for data in all_data:
        if data.level in max_model_dict:
            max_model_dict[data.level] += 1
        else:
            max_model_dict[data.level] = 1
    max_model = sorted(max_model_dict.items(), key=lambda x: x[1], reverse=True)[0][0]
    return max_model


def most_brand():
    all_data = CarData.objects.all()
    most_brand_dict = {}
    for data in all_data:
        if data.brand_name in most_brand_dict:
            most_brand_dict[data.brand_name] += 1
        else:
            most_brand_dict[data.brand_name] = 1
    most_brand = sorted(most_brand_dict.items(), key=lambda x: x[1], reverse=True)[0][0]
    return most_brand


def avg_price():
    all_data = CarData.objects.all()
    all_price = 0
    for data in all_data:
        all_price += (float(data.min_price) + float(data.max_price)) / 2
    avg_price = round(all_price / len(all_data), 2)
    return avg_price


def get_scroll_data():
    all_data = CarData.objects.all().order_by('car_rank')
    scroll_data = []
    for data in all_data[:100]:
        scroll_data.append({
            'name': data.series_name,
            'value': data.car_count,
        })
    return scroll_data


def get_ratio_data():
    all_data = CarData.objects.all()
    fuel_forml_dict = {}
    for data in all_data:
        if data.fuel_forml in fuel_forml_dict:
            fuel_forml_dict[data.fuel_forml] += 1
        else:
            fuel_forml_dict[data.fuel_forml] = 1
    oil_ratio = round(fuel_forml_dict['汽油'] / len(all_data), 2)
    ele_ratio = round(fuel_forml_dict['纯电动'] / len(all_data), 2)
    mixed_ratio = round((1 - oil_ratio - ele_ratio)* 100, 2)
    ratio = {
        'oil_ratio': oil_ratio * 100,
        'ele_ratio': ele_ratio * 100,
        'mixed_ratio': mixed_ratio,
    }
    return ratio

def get_left_data():
    all_oil_data = CarData.objects.filter(fuel_forml='汽油').order_by('car_rank')
    oil_data = []
    for data in all_oil_data:
        oil_data.append([data.series_name, data.car_count,data.fuel_forml])

    all_ele_data = CarData.objects.filter(fuel_forml='纯电动').order_by('car_rank')
    ele_data = []
    for data in all_ele_data:
        ele_data.append([data.series_name, data.car_count, data.fuel_forml])
    return oil_data[:20],ele_data[:20]

def get_wordcloud_data():
    all_data = CarData.objects.all().values('series_name', 'car_count').order_by('car_rank')
    wordcloud_data = []
    for data in all_data:
        wordcloud_data.append({
            'name': data['series_name'],
            'value': data['car_count'],
        })
    return wordcloud_data

def get_right_data():
    all_data = CarData.objects.all().values('brand_name', 'car_count')
    pie_data_dict = {}
    for data in all_data:
        if data['brand_name'] in pie_data_dict:
            pie_data_dict[data['brand_name']] += data['car_count']
        else:
            pie_data_dict[data['brand_name']] = data['car_count']
    sort_data = sorted(pie_data_dict.items(), key=lambda x: x[1], reverse=True)[:10]
    pie_data = []
    for k,v in sort_data:
        pie_data.append({
            'value': v,
            'name': k,
        })
    return pie_data

def get_price_data():
    ten_low = CarData.objects.filter(max_price__lte=10)
    ten_to_fifteen = CarData.objects.filter(Q(max_price__gt=10)&Q(max_price__lte=20))
    fif_to_twenty = CarData.objects.filter(Q(max_price__gt=20) & Q(max_price__lte=30))
    twenty_to_tf = CarData.objects.filter(Q(max_price__gt=30)&Q(max_price__lte=40))
    tf_high = CarData.objects.filter(Q(max_price__gte=40))
    data = [
        {
            'name':'10w以下',
            'value': len(ten_low),
        },
        {
            'name': '10w-20w',
            'value': len(ten_to_fifteen),
        },
        {
            'name': '20w-30w',
            'value': len(fif_to_twenty),
        },
        {
            'name': '30w-40w',
            'value': len(twenty_to_tf),
        },
        {
            'name': '40w以上',
            'value': len(tf_high),
        },
    ]
    return data

def get_bottom_left_data():
    top10_data = CarData.objects.all().order_by('car_rank')[:100]
    data = []
    for item in top10_data:
        data.append({
            'id': item.series_id,
            'rank': item.car_rank,
            'img_url':item.image,
            'info':{
                'name':item.series_name,
                'brand_name':item.brand_name,
                'level':item.level,
            },
            'price':f'{item.min_price}-{item.max_price}w',
            'sale':item.car_count,
            'market_time':item.market_time,
        })
    return data

def get_bottom_right_data():
    all_data = CarData.objects.all().order_by('car_rank')[:20]
    data = []
    for item in all_data:
        data.append({
            'id': item.series_id,
            'name': item.series_name,
            'sale': item.car_count,
            'price': round((item.min_price+item.max_price)/2, 2),
        })
    return data