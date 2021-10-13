from PIL import ImageFile
import calendar
import datetime
import time
from .models import Record

WEEKDAY = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

def getRecordsByDatetime(dt):
    return Record.objects.filter(expiryDate__year=dt.year, expiryDate__month=dt.month, expiryDate__day=dt.day)

def getBasicRecordByDatetime(request, dt):
    records = getRecordsByDatetime(dt).filter(user=request.user.id)
    return {"year":dt.year,
            "month":dt.month,
            "day":dt.day,
            "weekday":WEEKDAY[dt.weekday()],
            "records":records,
            "recordsIsRemoved": records.filter(isRemoved=True)}

def initIndexContext(request, numCards):
    dt = datetime.datetime.now() - datetime.timedelta(days=1)
    context = {}
    cards = []
    cards.append(getBasicRecordByDatetime(request, dt))
    cards[-1]["isPrev"] = True
    dt += datetime.timedelta(days=1)
    cards.append(getBasicRecordByDatetime(request, dt))
    cards[-1]["isToday"] = True
    dt += datetime.timedelta(days=1)
    for i in range(2, numCards):
        cards.append(getBasicRecordByDatetime(request, dt))
        dt += datetime.timedelta(days=1)
    context["cards"] = cards
    return context

def initDetailsContext(request):
    context = {}
    if 'year' in request.GET and 'month' in request.GET and 'day' in request.GET:
        dt = datetime.datetime(int(request.GET['year']), int(request.GET['month']), int(request.GET['day']))
    else:
        dt = datetime.datetime.now()
    records = getRecordsByDatetime(dt).filter(user=request.user)
    context['recordsIsRemoved'] = records.filter(isRemoved=True)
    context['recordsIsNotRemoved'] = records.filter(isRemoved=False)
    context['today'] = {'year':str(dt.year),'month':str(dt.month).zfill(2),'day':str(dt.day).zfill(2)}
    dt -= datetime.timedelta(days=1)
    context['prev'] = {'year':str(dt.year),'month':str(dt.month).zfill(2),'day':str(dt.day).zfill(2)}
    dt += datetime.timedelta(days=2)
    context['next'] = {'year':str(dt.year),'month':str(dt.month).zfill(2),'day':str(dt.day).zfill(2)}
    return context

def initCalendarContext(request):
    year = int(request.GET.get('year', 0))
    month = int(request.GET.get('month', 0))
    dt = datetime.datetime.now()
    if not (1900 <= year <= 3000) or not (1 <= month <= 12) :
        year = dt.year
        month = dt.month
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
    if dt.month == month and dt.year == year:
        checkToday = True
    day = dt.day
    weeks = []
    week = []
    curMonthRange = calendar.monthrange(year, month)
    if curMonthRange[0] != 6:
        if month == 1:
            pyear = year-1
            pmonth = 12
            prevMonthRange = calendar.monthrange(year-1, 12)
        else:
            pyear = year
            pmonth = month-1
            prevMonthRange = calendar.monthrange(year, month-1)
        for i in range(prevMonthRange[1]-curMonthRange[0], prevMonthRange[1]+1):
            week.append(getBasicRecordByDatetime(request, datetime.datetime(year=pyear,month=pmonth,day=i)))
            week[-1]["isNotThisMonth"] = True
    for i in range(1, curMonthRange[1]+1):
        week.append(getBasicRecordByDatetime(request, datetime.datetime(year=year,month=month,day=i)))
        if checkToday and day == i:
            week[-1]["isToday"] = True
        if len(week) == 7:
            weeks.append(week)
            week = []
    if week:
        if month == 12:
            year += 1
            month = 1
        else:
            month+=1
        for i in range(1, 7-len(week)+1):
            week.append(getBasicRecordByDatetime(request, datetime.datetime(year=year,month=month,day=i)))
            week[-1]["isNotThisMonth"] = True
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
