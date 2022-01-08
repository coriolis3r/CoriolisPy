import requests


def check_connection(url, timeout=3):
    try:
        req = requests.get(url, timeout=timeout)

        # HTTP errors are not raised by default, this statement does that
        resp = req.raise_for_status()

        print(resp)
        print("Device connected to internet.")

    except requests.HTTPError as e:
        print("Checking HTTP failed, status code {0}.".format(
            e.response.status_code))

    except requests.ConnectionError:
        print("No internet connection available.")


if __name__ == "__main__":
    check_connection('http://www.google.com/')