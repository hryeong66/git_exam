given_major_dict = {"인문" : 0, "사회" : 1, "교육" : 2, "공학" : 3, "자연" : 4 , "의약" : 5, "예체능" : 6}
########################## 신청 날짜 ###############################

def get_cleansed_application_period(raw_date_str):
    cur_year = datetime.now().year
    datetime_list = refind_application_date(raw_date_str)
    datetime_list.sort()
    period = []

    if len(datetime_list) >= 2:
        period.append(datetime_list[0])
        period.append(datetime_list[-1])
    elif len(datetime_list) == 1:  # 보통 날짜가 1개일 경우 마감 날짜
        period.append(datetime.strptime(f"{datetime_list[0].year}-01-01", "%Y-%m-%d"))
        period.append(datetime_list[0])
    else:  # 학교별로 상이한 경우 -> 해당 년의 전체 기간으로 넣어줌
        period.append(datetime.strptime(f"{cur_year}-01-01", "%Y-%m-%d"))
        period.append(datetime.strptime(f"{cur_year}-12-31", "%Y-%m-%d"))

    return period[0], period[1], datetime_list


def refind_application_date(raw_date_str):
    matches = list(datefinder.find_dates(raw_date_str))
    output = []
    for date in matches:
        date_str = date.strftime('%Y-%m-%d')
        application_datetime = datetime.strptime(date_str, "%Y-%m-%d")
        output.append(application_datetime)

    if output == []:
        annual_date = re.findall("매년 \d\d?", raw_date_str)
        if annual_date:
            output += refind_annual_date(annual_date)
        else:
            output += refind_korean_date(raw_date_str)
    return output


def refind_annual_date(date_list):
    month = re.findall("\d\d?", str(date_list))
    cur_year = datetime.now().year
    last_day = calendar.monthrange(int(cur_year), int(month[0]))[1]
    output = []

    first = f"{cur_year}-{month[0]}-01"
    last = f"{cur_year}-{month[0]}-{last_day}"
    output.append(datetime.strptime(first, "%Y-%m-%d"))
    output.append(datetime.strptime(last, "%Y-%m-%d"))
    return output
    
def refind_korean_date(raw_date_str):
    korean_date_str = raw_date_str.replace("년", "-")
    korean_date_str = korean_date_str.replace("월", "-")
    korean_date_str = korean_date_str.replace("일", "-")
    matches = list(datefinder.find_dates(korean_date_str))
    output = []
    for date in matches:
        date_str = date.strftime('%Y-%m-%d')
        application_datetime = datetime.strptime(date_str, "%Y-%m-%d")
        output.append(application_datetime)
    return output

