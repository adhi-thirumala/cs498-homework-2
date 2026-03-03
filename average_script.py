import requests
import time

US_CENTRAL_URL = "http://34.56.172.18"
EUROPE_WEST_URL = "http://35.205.163.0"

REGISTER_ENDPOINT = "/register"
LIST_ENDPOINT = "/list"

NUM_REQUESTS = 10


def measure_latency(base_url, endpoint, method="GET", payload=None):
    times = []

    for i in range(NUM_REQUESTS):
        start = time.time()

        if method == "POST":
            response = requests.post(base_url + endpoint, json=payload)
        else:
            response = requests.get(base_url + endpoint)

        end = time.time()

        if response.status_code != 200:
            print(f"Warning: Received status {response.status_code}")

        times.append(end - start)

    return sum(times) / len(times)


def main():
    print("Measuring /register latency...")

    dummy_payload = {"username": "latency_test_user"}

    us_register_avg = measure_latency(
        US_CENTRAL_URL, REGISTER_ENDPOINT, "POST", dummy_payload
    )
    eu_register_avg = measure_latency(
        EUROPE_WEST_URL, REGISTER_ENDPOINT, "POST", dummy_payload
    )

    print("\nMeasuring /list latency...")

    us_list_avg = measure_latency(US_CENTRAL_URL, LIST_ENDPOINT)
    eu_list_avg = measure_latency(EUROPE_WEST_URL, LIST_ENDPOINT)

    print("\n===== AVERAGE LATENCIES =====")
    print(f"US-CENTRAL /register: {us_register_avg:.4f} seconds")
    print(f"EUROPE-WEST /register: {eu_register_avg:.4f} seconds")
    print(f"US-CENTRAL /list: {us_list_avg:.4f} seconds")
    print(f"EUROPE-WEST /list: {eu_list_avg:.4f} seconds")


if __name__ == "__main__":
    main()
