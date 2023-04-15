from django.shortcuts import render
from django.http.response import JsonResponse
from django.db.models import Q

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status
 
from dashboard.models import Data
from dashboard.serializers import DataSerializer

import json

@api_view(['GET', 'POST', 'DELETE'])
def data_list(request):
    # GET list of all data
    if request.method == 'GET':
        all_data = Data.objects.all()
        if d_id := request.GET.get('d_id', None):
            all_data = all_data.filter(d_id__startswith=d_id)
            # q &= Q(d_id__exact=d_id)
        q = Q()
        if title := request.GET.get('title', None):
        	if request.GET.get('get_all', None) == 'True':
	        	q &= Q(title__icontains=title)
        	else:
	        	q &= Q(title__exact=title)
        if stream_id := request.GET.get('stream_id', None):
        	if request.GET.get('get_all', None) == 'True':
	        	q &= Q(stream_id__icontains=stream_id)
        	else:
        		q &= Q(stream_id__exact=stream_id)

        if date := request.GET.get('date', None):
            q &= Q(date__exact=date)

        if title or stream_id or date is not None:
            all_data = all_data.filter(q)
        data_serialized = DataSerializer(all_data, many=True)
        return JsonResponse(data_serialized.data, safe=False)

    # POST new data
    elif request.method == 'POST':
        data_item = DataSerializer(data = (JSONParser().parse(request)))
        if data_item.is_valid():
            data_item.save()
            return JsonResponse(data_item.data, status = status.HTTP_201_CREATED)
        return JsonResponse(data_item.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE all data items
    # elif request.method == 'DELETE':
    #     count = Data.objects.all().delete()
    #     return JsonResponse({'message': '{} All data was deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)




@api_view(['GET'])
def patient_day_data(request, d_id, date):
    patient_data = Data.objects.filter(d_id__exact=d_id, date__exact=date)
    patient_data_serialized = DataSerializer(patient_data, many=True)

    new_json_o = {}
    for o_dict in patient_data_serialized.data:
        new_json_o[o_dict['title']] = o_dict['text']
    print(new_json_o)
    return JsonResponse(new_json_o, safe=False)


@api_view(['GET', 'PUT', 'DELETE'])
def data_detail(request, pk):
    # find data by primary key - id
    try: 
        data = Data.objects.get(pk = pk) 
    except Data.DoesNotExist: 
        return JsonResponse({'message': 'The requested Data item does not exist'}, status = status.HTTP_404_NOT_FOUND) 
    
    if request.method == 'GET': 
        data_item = DataSerializer(data) 
        return JsonResponse(data_item.data) 

    elif request.method == 'PUT': 
        data_item = DataSerializer(data, data = (JSONParser().parse(request))) 
        if data_itemdata_item.is_valid(): 
            data_item.save() 
            return JsonResponse(data_item.data) 
        return JsonResponse(data_item.errors, status=status.HTTP_400_BAD_REQUEST) 

    elif request.method == 'DELETE': 
        data.delete() 
        return JsonResponse({'message': 'Data item was deleted successfully!'}, status = status.HTTP_204_NO_CONTENT)