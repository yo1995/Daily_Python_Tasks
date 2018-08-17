# -*- coding: utf-8 -*-
import time
import random


def read_food_list():
    with open('list.txt', 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        meal_list = []
        for line in lines:
            if '！' in line:
                [meal_name, meal_items] = line.split('！')
                item_list = []
                for item in meal_items.split(';')[:-2]:
                    #[item_weight, item_name] = item.split('：')
                    item_list.append(item.split('：'))
                meal = [meal_name, item_list]
                meal_list.append(meal)
        # print meal_list
        return meal_list

# def time_later_than(time1, time2):
#     #return (time1[0] > time2[0] or time1[0] == time2[0] and time1[1] >= time2[1] )
#     return 60*time1[0]+time1[1] > 60*time2[0]+time2[1]


def time_in_range(t, r):
    return r[0] <= t <= r[1]


def choose_random_food(l):
    weights = []
    # print l
    for item in l:
        weights.append(float(item[0]))
    random_number = random.uniform(0, sum(weights))
    weight_remain = random_number
    i = 0
    while weight_remain > 0:
        weight_remain -= weights[i]
        i += 1
    return l[i-1][1]


def main():
    # main function
    current_time = time.localtime(time.time())
    minute_number = current_time[4]
    minute_string = str(minute_number) if minute_number > 9 else '0' + str(minute_number)
    print("Hello, it's " + str(current_time[3]) + ':' + minute_string + ' now.')
    ct = current_time[3] + current_time[4]/100.0
    meal_sort = ''
    time_ranges = [[7.30,10], [10.50, 13.30], [16.30, 18.50],[19, 21.2], [21.21, 22.20]]
    meal_index = -1
    for time_range in time_ranges:
        meal_index += 1
        if time_in_range(ct, time_range):
            meal_sort = time_range[0]
            break
    if meal_sort:
        meal_list = read_food_list()
        choice_list = meal_list[meal_index]
        # print "You can have " + meal_sort + choice_list[0].decode('utf-8')
        print("You can have " + choice_list[0])
        food = choose_random_food(choice_list[1:][0])
        print(food + ' is recommended.')
    else:
        print("NOT MEAL TIME NOW")


if __name__ == '__main__':
    main()
