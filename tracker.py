import json
import sys
import speedtest
import logging
import time

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
times_tests_done = int(total_time*60 / frequency)
logging.info(f"Program will run {times_tests_done} tests over {total_time} hours")


def perform_speed_test():
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


perform_speed_test()

