from django.shortcuts import render

def hotspot_view(request):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hours = list(range(24))

    weekday = request.GET.get("weekday", "Monday")
    hour = int(request.GET.get("hour", 0))

    image_name = f"hotspot_{weekday}_{hour}.png"
    image_path = f"hotspots/{image_name}"

    return render(request, "hotspot.html", {
        "image_path": image_path,
        "weekdays": weekdays,
        "hours": hours,
        "selected_weekday": weekday,
        "selected_hour": hour
    })
