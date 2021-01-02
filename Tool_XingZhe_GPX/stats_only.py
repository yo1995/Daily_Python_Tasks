import os
import json

import requests
import tqdm


def get_json_filename(year: str, month: str) -> str:
    return f'{year}_{month}.json'


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


# region Helper functions, global variables might be used.
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
    # analyse_monthly_summary('2020')
    analyse_all_workouts('2020', sports_type=3)
    return


if __name__ == '__main__':
    # Global variables for config.
    USERID = '666666'  # n-digit user ID.
    WORKING_FOLDER = r'C:\Users\{YOUR_UNAME}\Desktop\行者数据导出'  # Path to temp folder.

    if not USERID or not WORKING_FOLDER:
        print('Please specify user ID and working folder to use the script.')
        exit(1)

    # Initialize working folders.
    JSON_FOLDER = os.path.join(WORKING_FOLDER, 'json')
    GPX_FOLDER = os.path.join(WORKING_FOLDER, 'gpx')
    for folder in [JSON_FOLDER, GPX_FOLDER]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # Run main.
    main()
    exit(0)
