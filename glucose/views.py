import os
from django.db.models import query
from django.http.response import HttpResponse
from django.shortcuts import render

from csv import reader

from glucose.models import Device, GlucoseLevel, User

from django.http import JsonResponse


def levels_for_user(request):
    RESULTS_PER_PAGE = 25
    if request.method == "GET":
        user_id = request.GET.get("user_id")
        try:
            page_no = int(request.GET.get("page", 0))
        except ValueError:
            page_no = 0


        result_list = list(GlucoseLevel.objects.filter(user_id=user_id).values())
    
    #Simple way for pagination
    start_idx = page_no * RESULTS_PER_PAGE 
    start_idx = start_idx if start_idx < len(result_list) else 0
    end_idx = min(start_idx + RESULTS_PER_PAGE, len(result_list))

    return JsonResponse(result_list[start_idx : end_idx], safe=False)




def levels_for_id(request, id):
    glucose = None
    if request.method == "GET":
        glucose = GlucoseLevel.objects.filter(id=id).values().first()
    
    return JsonResponse(glucose, safe=False)



def highlow(request):
    high_values = []
    low_values = []
    if request.method == "GET":
        user_id = request.GET.get("user_id")
        try:
            high = int(request.GET.get("high", None))
        except ValueError:
            high = None

        try:
            low = int(request.GET.get("low", None))
        except ValueError:
            low = None

    
        if high is not None:
            high_values = list(GlucoseLevel.objects.filter(user_id=user_id, value__gt=high).values())

        if low is not None:
            low_values = list(GlucoseLevel.objects.filter(user_id=user_id, value__lt=low).values())


    data = {
        "low": low_values,
        "high": high_values
    }

    return JsonResponse(data)


def get_users(request):
    users = []
    if request.method == "GET":
        users = list(User.objects.all().values())
    
    return JsonResponse(users, safe=False) 


def load_data(request):
    if request.method == "POST":
        sent_file = request.FILES["user-data"]
        with open(sent_file, "r") as file:

            user_id = os.path.basename(file.name).replace(".csv", "")
            csv_reader = reader(file)
            
            #Skipping the first 3 lines and getting the user's name from them
            user_name = next(csv_reader)[4]
            next(csv_reader)
            next(csv_reader)

            #Check if user exists in the database and create it if not.        
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                user = User(id=user_id, name=user_name)
                user.save()

            #Looping over the real data
            for row in csv_reader:
                #If the row is empty, just ignore it
                if not row[0]:
                    continue

                device_name = row[0]
                device_serial = row[1]
                timestamp = row[2]
                recording_type = row[3]
                glucose_level = row[4]

                #This sample app will only use data recorded in a specific way
                if int(recording_type) != 0:
                    continue

                try:
                    device = Device.objects.get(serial_number=device_serial)
                except Device.DoesNotExist:
                    device = Device(serial_number=device_serial, name=device_name)
                    device.save()

                #Convert to datetime
                from datetime import datetime

                datetime_object = datetime.strptime(timestamp, '%d-%m-%Y %H:%M')

                
                glucose_level = GlucoseLevel(value = glucose_level, timestamp = datetime_object, recording_type=recording_type, device = device, user = user)
                glucose_level.save()

            

    return JsonResponse({"message": "Ok" })