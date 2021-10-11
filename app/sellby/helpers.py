from PIL import ImageFile
import calendar
import datetime
import time

WEEKDAY = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

def initIndexContext(numCards):
    datetimeNow = datetime.datetime.now() - datetime.timedelta(days=1)
    context = {}
    cards = []
    cards.append({"year":datetimeNow.year,"month":datetimeNow.month,"day":datetimeNow.day, "weekday":WEEKDAY[datetimeNow.weekday()], "isPrev":True})
    datetimeNow += datetime.timedelta(days=1)
    cards.append({"year":datetimeNow.year,"month":datetimeNow.month,"day":datetimeNow.day, "weekday":WEEKDAY[datetimeNow.weekday()], "isToday":True})
    datetimeNow += datetime.timedelta(days=1)
    for i in range(2, numCards):
        cards.append({"year":datetimeNow.year,"month":datetimeNow.month,"day":datetimeNow.day, "weekday":WEEKDAY[datetimeNow.weekday()]})
        datetimeNow += datetime.timedelta(days=1)
    context["cards"] = cards
    return context

def initCalendarContext(year, month):
    datetimeNow = datetime.datetime.now()
    if not (1900 <= year <= 3000) or not (1 <= month <= 12) :
        year = datetimeNow.year
        month = datetimeNow.month
    context = {"curCalendar":"{}.{}".format(year, str(month).zfill(2))}
    if month == 1:
        context["pyear"] = year-1
        context["pmonth"] = 12
    else:
        context["pyear"] = year
        context["pmonth"] = month-1
    if month == 12:
        context["nyear"] = year+1
        context["nmonth"] = 1
    else:
        context["nyear"] = year
        context["nmonth"] = month+1
    checkToday = False
    if datetimeNow.month == month and datetimeNow.year == year:
        checkToday = True
    day = datetimeNow.day
    weeks = []
    week = []
    curMonthRange = calendar.monthrange(year, month)
    if curMonthRange[0] != 6:
        if month == 1:
            prevMonthRange = calendar.monthrange(year-1, 12)
        else:
            prevMonthRange = calendar.monthrange(year, month-1)
        for i in range(prevMonthRange[1]-curMonthRange[0], prevMonthRange[1]+1):
            week.append({"date":i,"isNotThisMonth":True})
    for i in range(1, curMonthRange[1]+1):
        week.append({"date":i})
        if checkToday and day == i:
            week[-1]["isToday"] = True
        if len(week) == 7:
            weeks.append(week)
            week = []
    if week:
        for i in range(1, 7-len(week)+1):
            week.append({"date":i,"isNotThisMonth":True})
        weeks.append(week)
    context["month"] = weeks
    return context

def saveExpiryImage(request):
    f = request.FILES.get('expiry-date-image')
    p = ImageFile.Parser()
    while 1:
        s = f.read(1024)
        if not s:
            break
        p.feed(s)
    img = p.close()
    img.save('./data/{}{}{}'.format(request.POST.get('expiry-date'),time.time(),request.FILES.get('expiry-date-image').name))
