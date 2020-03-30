import requests
import json
import DataHandler

with open("data/login.json") as login:
    qt_user = json.load(login)

with open("data/settings.json", "r") as file:
    settings = json.load(file)


def error_check(response):
    if response.status_code != 200:
        raise RuntimeError(
            f"Error fetching: {response.status_code}, Check the api and try again."
        )


def main():
    with requests.Session() as s:
        response = s.post(settings["base_url"] + settings["default_ext"], qt_user)
        error_check(response)
        for count, link in enumerate(settings["links"]):
            file_name = settings["files"][count]
            response = s.get(settings["base_url"] + link)
            error_check(response)
            data = DataHandler.DataHandler().convert(response, link)
            if DataHandler.DataHandler().compare(data, file_name):
                DataHandler.DataHandler().updater(data, file_name)
                DataHandler.DataHandler().data_sender(
                    data, settings["email"], settings["key"], file_name
                )


if __name__ == "__main__":
    main()
