import json
import sys
import speedtest
import logging
import time
import datetime

logging.basicConfig(
    filename=f"{time.strftime('%Y%m%d_%H%M%S')}.log",
    encoding="utf-8",
    filemode="a",
    format="[{asctime}] {levelname}: {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logging.info("Application starting")

frequency  = float(input("At what frequency do you want to do the speed test (in minutes)? > "))
total_time = float(input("For how much time do you want to do the speed tests (in hours)? > "))
tests_per_file = float(input("How many test entries do you want per file (more = more RAM usage, less = more files)? > "))
number_of_tests = int(total_time * 60 / frequency)

logging.info(f"Program will run {number_of_tests} tests over {total_time} hours")
logging.info(f"Program will end at {datetime.datetime.now() + datetime.timedelta(hours=total_time)}")

current_file = "test_results0.json"

def load_data_into_file(test_id: int, download_speed: float, upload_speed: float,
                        download_time_taken: float, upload_time_taken: float, time_of_test: str):
    global  current_file

    try:
        with open(current_file, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    if len(data) >= tests_per_file:
        current_file = f"test_results{test_id % tests_per_file}.json"
        data = {}

    data[str(test_id)] = {
        "download_speed" : download_speed,
        "upload_speed" : upload_speed,
        "download_time_taken" : download_time_taken,
        "upload_time_taken" : upload_time_taken,
        "time_of_test" : time_of_test
    }

    with open(current_file, "w") as f:
        json.dump(data, f, indent=2)


def perform_speed_test(test_id: int):
    st = speedtest.Speedtest()

    servers = []

    for server_list in st.get_servers().values():
        for server in server_list:
            servers.append(server["id"])

    st.get_servers(servers)

    logging.info("Testing download speed...")
    time1 = time.time()
    download_speed = st.download() / 1000000
    time_download = time.time() - time1
    logging.info("Took {:.2f}s".format(time_download))

    logging.info("Testing upload speed...")
    time1 = time.time()
    upload_speed = st.upload() / 1000000
    time_upload = time.time() - time1
    logging.info("Took {:.2f}s".format(time_upload))

    logging.info("Download Speed: {:.2f} Mbps".format(download_speed))
    logging.info("Upload Speed: {:.2f} Mbps".format(upload_speed))

    load_data_into_file(test_id, download_speed, upload_speed, time_download, time_upload, str(datetime.datetime.now()))
    
    return time_upload + time_download


for i in range(number_of_tests):
    try:
        time_taken = perform_speed_test(i)
    except:
        logging.exception("Something went wrong: ")
        exit()
    logging.info(f"Sleeping for {frequency * 60 - time_taken}")
    time.sleep(frequency * 60 - time_taken)

