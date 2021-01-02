import os
import json
import datetime

import requests
import tqdm

# Global variables as configs.
COOKIES = ''  # Paste the cookies string from GET /portal
USERID = ''  # possibly 6-digit user_id

# Initialize working folders.
WORKING_FOLDER = r'C:\Users\{username}\Desktop\行者数据导出'
JSON_FOLDER = os.path.join(WORKING_FOLDER, 'json')
GPX_FOLDER = os.path.join(WORKING_FOLDER, 'gpx')
for folder in [JSON_FOLDER, GPX_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)


# region Trivial helper functions.
def make_cookies(cookie_str: str):
    cookies = {}
    for item in cookie_str.split(";"):
        item = item.strip().split("=")
        cookies[item[0]] = item[1]
    return cookies


def get_json_filename(year: str, month: str) -> str:
    return f'{year}_{month}.json'


def get_gpx_filename(record_id: str, suffix: str) -> str:
    filename = f'{record_id}'
    if suffix is not None:
        filename += f'_{suffix}'
    filename += '.gpx'
    return filename


def load_json_files(year: str, input_folder: str) -> [json]:
    # 1. Load all monthly json files
    monthly_json_files = []
    months = [str(month) for month in range(1, 13)]
    for month in months:
        json_filename = get_json_filename(year, month)
        json_filepath = os.path.join(input_folder, json_filename)
        with open(json_filepath, 'r') as fd:
            json_file = json.load(fd)
            monthly_json_files.append(json_file)
    return monthly_json_files


def print_seconds_str(duration: int) -> (int, int, int):
    seconds = duration
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f'{hours} hours, {minutes} minutes, {seconds} seconds'


def print_summary(summary: dict):
    duration = summary['duration']
    distance = summary['distance']
    count = summary['count']
    elevation = summary['elevation']
    print(f'distance: {distance / 1e3} km; '
          f'duration: {print_seconds_str(duration)}; '
          f'average speed: {distance / 1e3 / duration * 3600:.2f} km/h; '
          f'count: {count}; '
          f'elevation: {elevation} m')
# endregion


def get_monthly_info(year: str, month: str) -> json:
    api = 'https://www.imxingzhe.com/api/v4/user_month_info'
    payload = {'user_id': USERID, 'year': year, 'month': month}
    response = requests.get(api, params=payload)
    return response.json()


def get_workouts(monthly_json: json) -> list[dict]:
    """
    Get essential workout info from monthly json.

    :param monthly_json: The monthly json response.
    :return: A dict containing workout id, duration, distance and elevation.
    """
    # Get an array of workout dictionaries.
    workouts = monthly_json['data']['wo_info']
    results = []
    for workout in workouts:
        d = dict()
        d['id'] = workout['id']  # workout id, used for downloading gpx
        d['duration'] = workout['duration']  # workout duration in seconds
        d['distance'] = workout['distance']  # distance in meters
        d['elevation'] = workout['elevation_gain']  # elevation in meters
        d['sport'] = workout['sport']
        d['upload_time'] = workout['upload_time']  # upload datetime of the workout
        results.append(d)
    return results


def get_monthly_summary(monthly_json: json) -> dict:
    """
    Get the summary of monthly workouts.
    Example:
    "st_info": {
        "sum_duration": 7063,
        "sum_distance": 43827,
        "sum_elevation_gain": 534,
        "count_distance": 3,
        "sum_credits": 50
    }

    :param monthly_json: The monthly json response.
    :return: A dict of summary.
    """
    return monthly_json['data']['st_info']

# ---Global variables might be used below.---


# region Download functions
def download_gpx(record_id: str, output_folder: str, suffix: str = None):
    api = f'http://www.imxingzhe.com/xing/{record_id}/gpx/'
    if len(COOKIES) == 0:
        print('Error: fill in your cookies to download.')
        exit(1)
    response = requests.get(api, cookies=make_cookies(COOKIES))

    # 行者默认文件名没有意义，故以记录ID与记录日期（由suffix传入）为标题。
    # disposition = response.headers['content-disposition']
    # suggested_filename = re.findall('filename=(.+)', disposition)[0]
    filename = get_gpx_filename(record_id, suffix)

    filepath = os.path.join(output_folder, filename)
    with open(filepath, 'wb') as fd:
        for chunk in response.iter_content(chunk_size=128):
            fd.write(chunk)
# endregion


# region Process all helper functions, global variables might be used.
def analyse_all_workouts(year: str, sports_type: int):
    """
    Do a detailed summary based on all workout records.
    Skip the workout with other sports type.

    :param year: The year of json files to read.
    :param sports_type: 1 for hiking, 3 for cycling
    :return:
    """
    # 1. Load all monthly json files
    monthly_json_files = load_json_files(year=year, input_folder=JSON_FOLDER)

    # 2. Read all workout IDs in (date, id) tuple
    summary_dict = {
        'duration': 0,
        'distance': 0,
        'elevation': 0,
        'count': 0
    }
    for json_file in monthly_json_files:
        workouts = get_workouts(monthly_json=json_file)
        for workout in workouts:
            if workout['sport'] != sports_type:
                continue
            summary_dict['duration'] += workout['duration']
            summary_dict['distance'] += workout['distance']
            summary_dict['elevation'] += workout['elevation']
            summary_dict['count'] += 1
    print_summary(summary_dict)


def analyse_all_workouts_by_month(year: str, sports_type: int):
    """
    Do a detailed summary based on all workout records.
    Skip the workout with other sports type.

    :param year: The year of json files to read.
    :param sports_type: 1 for hiking, 3 for cycling
    :return:
    """
    # 1. Load all monthly json files
    monthly_json_files = load_json_files(year=year, input_folder=JSON_FOLDER)

    # 2. Read all workout IDs in (date, id) tuple
    for json_file in monthly_json_files:
        summary_dict = {
            'duration': 0,
            'distance': 0,
            'elevation': 0,
            'count': 0
        }
        workouts = get_workouts(monthly_json=json_file)
        for workout in workouts:
            if workout['sport'] != sports_type:
                continue
            summary_dict['duration'] += workout['duration']
            summary_dict['distance'] += workout['distance']
            summary_dict['elevation'] += workout['elevation']
            summary_dict['count'] += 1
        print_summary(summary_dict)


def analyse_monthly_summary(year: str):
    """
    Do a rough summary based on the monthly report. It doesn't differentiate
    sports types, so cycling and hiking are mixed together.

    :param year: The year of json files to read.
    :return: None.
    """
    # 1. Load all monthly json files
    monthly_json_files = load_json_files(year=year, input_folder=JSON_FOLDER)

    # 2. Read all monthly summary
    summary_dicts = []
    for json_file in monthly_json_files:
        summary_dicts.append(get_monthly_summary(monthly_json=json_file))

    # 3. Simple analysis
    summary_dict = {
        'duration': sum(d['sum_duration'] for d in summary_dicts),
        'distance': sum(d['sum_distance'] for d in summary_dicts),
        'elevation': sum(d['sum_elevation_gain'] for d in summary_dicts),
        'count': sum(d['count_distance'] for d in summary_dicts)
    }
    print_summary(summary_dict)
    return


def download_all_gpx_files(year: str, sports_type: int):
    # 1. Load all monthly json files
    monthly_json_files = load_json_files(year=year, input_folder=JSON_FOLDER)

    # 2. Read all workout IDs in (date, id) tuple
    workout_ids = []
    for json_file in monthly_json_files:
        workouts = get_workouts(monthly_json=json_file)
        for workout in workouts:
            if workout['sport'] != sports_type:
                continue
            # The datetime of upload time in Beijing timezone.
            date = datetime.datetime.fromisoformat(workout['upload_time'])
            # Ex: 201209
            date_str = date.strftime('%y%m%d')
            workout_ids.append((date_str, workout['id']))

    # 3. Download all workout gpx files
    progress_bar = tqdm.tqdm(workout_ids)
    count = 1
    for record_date, record_id in progress_bar:
        filepath = os.path.join(GPX_FOLDER, get_gpx_filename(record_id, suffix=record_date))
        if not os.path.exists(filepath):
            # Omit existing gpx files to increase download speed.
            download_gpx(record_id=record_id, output_folder=GPX_FOLDER, suffix=f'{record_date}')
            progress_bar.set_description(f'Downloading {count}. {filepath}...')
        else:
            progress_bar.set_description(f'Omit {count}. {filepath}...')
        count += 1


def download_all_json_files(year: str):
    months = [str(month) for month in range(1, 13)]
    progress_bar = tqdm.tqdm(months)
    for month in progress_bar:
        monthly_json = get_monthly_info(year=year, month=month)
        json_filename = get_json_filename(year, month)
        json_filepath = os.path.join(JSON_FOLDER, json_filename)
        with open(json_filepath, 'w') as fd:
            json.dump(monthly_json, fd)
            progress_bar.set_description(f'Downloading {month} monthly data...')
# endregion


def main():
    # download_all_json_files(year='2020')
    # download_all_gpx_files('2020', sports_type=3)
    # analyse_monthly_summary('2020')
    # analyse_all_workouts_by_month('2020', sports_type=3)
    analyse_all_workouts('2020', sports_type=3)
    return


if __name__ == '__main__':
    main()
    exit(0)
