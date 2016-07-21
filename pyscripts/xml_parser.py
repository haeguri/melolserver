from xml.etree.ElementTree import parse
import json

json_obj = {}
week_whitelist = ('평일(상)', '평일(하)', '토요일(상)', '토요일(하)', '휴일(상)', '휴일(하)')

for line in range(1, 4):
    line = str(line)
    json_obj[line] = {}
    tree = parse("line"+line+".xml")
    root = tree.getroot()

    for row in root.findall("Row"):
        if row.find("요일별").text not in week_whitelist or row.find("열차번호").text != "출발":
            continue

        platform_name = row.find("역명").text
        t_week = row.find("요일별").text.split("(")
        week_day = t_week[0] # 평일, 토요일, 휴일
        direction = t_week[1][0] # 상, 하

        if platform_name not in json_obj[line]:
            json_obj[line][platform_name] = {}

        if week_day not in json_obj[line][platform_name]:
                json_obj[line][platform_name][week_day] = {}

        if direction not in json_obj[line][platform_name][week_day]:
            json_obj[line][platform_name][week_day][direction] = []

        for t in list(row.iter())[4:]:
            if t.text is not None:
                json_obj[line][platform_name][week_day][direction].append(t.text)

output = open('dg_metro.json', 'w')
json.dump(json_obj, output)