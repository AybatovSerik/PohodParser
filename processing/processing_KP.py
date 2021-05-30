import re

kp_level_map = {
     'Сложность:легкий, опыт не обязателен ': 1,
     'Сложность:опыт не обязателен, средняя сложность ': 2,
     'Сложность:средняя сложность, участникам с опытом ': 3,
     'Сложность:средняя сложность ': 3,
     'Сложность:легкий ': 1,
     'Сложность:опыт не обязателен ': 1,
     'Сложность:сложный, средняя сложность, участникам с опытом ': 4,
     'Сложность:легкий, опыт не обязателен, средняя сложность ': 2,
     'Сложность:легкий, участникам с опытом ': 2,
     'Сложность:сложный, участникам с опытом ': 5,
     'Сложность:легкий, средняя сложность ': 2,
     'Сложность:участникам с опытом ': 3,
     'Сложность:сложный ': 4,
     'Сложность:сложный, средняя сложность ': 4,
     'Сложность:опыт не обязателен, средняя сложность, участникам с опытом ': 2,
     'Сложность:легкий, опыт не обязателен, участникам с опытом ': 1,
     'Сложность:легкий, опыт не обязателен, средняя сложность, участникам с опытом ': 2,
     'Сложность:легкий, средняя сложность, участникам с опытом ': 2
}
# None -> 1
# Not in map -> 1, print url and level
# kp_level_map.get(x,0)

def parse_distance_kp(x_str):
    if x_str is None:
        return None
    x = x_str.split('(')[0]
    sum_of_dists = re.findall(r'Длина:[^0-9.]*([0-9]+)[^0-9.]*[\+и][^0-9.]*([0-9]+)', x)
    average_dists = re.findall(r'Длина:[^0-9.]*([0-9]+)[^0-9.]+([0-9]+)', x)
    solo_dist = re.findall(r'Длина:\s*([0-9]+)', x)
    if len(sum_of_dists)>0:
        return int(sum_of_dists[0][0]) + int(sum_of_dists[0][1])
    elif len(average_dists)>0:
        if int(average_dists[0][1]) < int(average_dists[0][0]):
            return int(average_dists[0][0])
        else:
            return (int(average_dists[0][0]) + int(average_dists[0][1]))//2
    elif len(solo_dist)>0:
        return int(solo_dist[0])
    else:
        return None

def parse_duration_kp(x_str):
    if x_str is None:
        return None
    x = x_str.split('(')[0]
    sum_of_dur = re.findall(r'Длительность:[^0-9.]*([0-9]+)[^0-9.]*[\+и][^0-9.]*([0-9]+)', x)
    average_dur = re.findall(r'Длительность:[^0-9.]*([0-9]+)[^0-9.]+([0-9]+)', x)
    solo_dur = re.findall(r'Длительность:\s*([0-9]+)', x)
    or_dur = re.findall(r'Длительность:[^0-9.]*([0-9]+)[^0-9.]*или[^0-9.]*([0-9]+)', x)
    if len(or_dur)>0:
        return (int(or_dur[0][0]) + int(or_dur[0][1]))//2
    elif len(sum_of_dur)>0:
        return int(sum_of_dur[0][0]) + int(sum_of_dur[0][1])
    elif len(average_dur)>0:
        if int(average_dur[0][1]) < int(average_dur[0][0]):
            return int(average_dur[0][0])
        else:
            return (int(average_dur[0][0]) + int(average_dur[0][1]))//2
    elif len(solo_dur)>0:
        return int(solo_dur[0])
    else:
        return None
