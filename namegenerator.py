import pathlib
import json

from names_dataset import NameDataset

country_list = [
    "AZ",
    "CN",
    "CH",
    "DE",
    "EG",
    "ES",
    "FI",
    "FR",
    "GR",
    "IE",
    "IN",
    "IQ",
    "IR",
    "IT",
    "JP",
    "MX",
    "NO",
    "TW",
    "US",
    "YE",
]


def get_random_first_names_by_country(country, gender):
    name_path = "/home/dev/Code/fatebot/namelist"
    f_name_path = pathlib.Path(
        f"{name_path}/{country}/first_names_{gender.lower()}.json")
    names = None
    # print(f_name_path)

    with open(f_name_path) as f:
        names = json.load(f)

    return names


def get_random_last_names_by_country(country):
    name_path = "/home/dev/Code/fatebot/namelist"
    l_name_path = pathlib.Path(f"{name_path}/{country}/last_names.json")
    names = None
    # print(l_name_path)

    with open(l_name_path) as f:
        names = json.load(f)

    return names


def generate_name_files_by_country_all_genders():
    nd = NameDataset()
    name_path = "/home/dev/Code/fatebot/namelist"
    for gender in ["Male", "Female"]:
        for country in country_list:
            first_names = nd.get_top_names(
                n=500, gender=gender, country_alpha2=country)

            pathlib.Path(
                f"{name_path}/{country}/").mkdir(parents=True, exist_ok=True)

            f_name_path = pathlib.Path(
                f"{name_path}/{country}/first_names_{gender.lower()}.json")

            with open(f_name_path, "w") as f:
                json.dump(first_names, f, indent=4)

    for country in country_list:
        surnames = nd.get_top_names(
            n=500, country_alpha2=country, use_first_names=False)
        l_name_path = pathlib.Path(f"{name_path}/{country}/last_names.json")

        with open(l_name_path, "w") as f:
            json.dump(surnames, f, indent=4)


if __name__ == "__main__":
    generate_name_files_by_country_all_genders()
    #print(get_random_first_names_by_country("US", "Male"))
