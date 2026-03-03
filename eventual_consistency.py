import requests
import uuid

US_CENTRAL_URL = "http://34.58.199.16:8080"
EUROPE_WEST_URL = "http://35.205.163.0:8080"


REGISTER_ENDPOINT = "/register"
LIST_ENDPOINT = "/list"

ITERATIONS = 100


def main():
    not_found_count = 0

    for i in range(ITERATIONS):
        username = f"user_{uuid.uuid4().hex}"

        # Register in us-central
        register_response = requests.post(
            US_CENTRAL_URL + REGISTER_ENDPOINT,
            json={"username": username},
        )

        if register_response.status_code != 200:
            print(f"Register failed at iteration {i}")
            continue

        # Immediately query europe-west
        list_response = requests.get(EUROPE_WEST_URL + LIST_ENDPOINT)

        if list_response.status_code != 200:
            print(f"List failed at iteration {i}")
            continue

        users = list_response.json()

        if username not in str(users):
            not_found_count += 1

    print("\n===== EVENTUAL CONSISTENCY RESULTS =====")
    print(f"Total iterations: {ITERATIONS}")
    print(f"Username NOT found immediately: {not_found_count}")
    print(
        f"Percentage of replication lag occurrences: "
        f"{(not_found_count / ITERATIONS) * 100:.2f}%"
    )


if __name__ == "__main__":
    main()
