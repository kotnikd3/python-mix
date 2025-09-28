import requests
from bs4 import BeautifulSoup
import json
import os
import re
import unicodedata


URL = "https://ezpps.org/clani/"


def scrape_data():
    response = requests.get(URL)
    response.raise_for_status()  # raise error if bad response

    soup = BeautifulSoup(response.text, "html.parser")

    therapists = []

    # Find all "child" blocks
    blocks = soup.find_all("div", class_="rt-col-md-3")
    for block in blocks:
        data = {}

        # name
        name_tag = block.select_one(".team-name a")
        data["name"] = name_tag.get_text(strip=True) if name_tag else None

        # title
        title_tag = block.select_one(".short-bio p")
        data["title"] = title_tag.get_text(strip=True).capitalize() if title_tag else None

        # image
        img_tag = block.select_one("img.rt-team-img")
        img_source = img_tag["src"] if img_tag else None
        if img_source and "EZPPS-clan-002-e1708984778513" not in img_source:
            data["image_source"] = img_source
        else:
            data["image_source"] = None

        # website
        website_tag = block.select_one(".tlp-website a")
        data["website"] = website_tag["href"] if website_tag else None

        # location
        location_tag = block.select_one(".tlp-location span")
        data["location"] = {
            "city": location_tag.get_text(strip=True) if location_tag else None,
            "address": None,
            "latitude": None,
            "longitude": None,
        }

        # email
        email_tag = block.select_one(".tlp-email a span")
        data["email"] = email_tag.get_text(strip=True) if email_tag else None

        # phone
        phone_tag = block.select_one(".tlp-phone a")
        data["phone"] = phone_tag.get_text(strip=True) if phone_tag else None

        data["show_on_map"] = False

        therapists.append(data)

    return therapists


def scrape_photos(therapists: dict):
    for person in therapists:
        name = formated_person_name(person["name"])
        
        person["id"] = name

        if not person.get("image_source"):
            person["image_name"] = None
            continue

        filename = name  + ".jpg"
        
        person["image_name"] = filename

        filepath = os.path.join("photos", filename)

        try:
            print(f"Downloading {person['name']} -> {filename}")
            res = requests.get(person["image_source"], stream=True)
            res.raise_for_status()
            with open(filepath, "wb") as f:
                for chunk in res.iter_content(8192):
                    f.write(chunk)
        except Exception as e:
            print(f"Failed to download {person['name']}: {e}")


def formated_person_name(name: str) -> str:
    # Transliterate to closest ASCII equivalent
    normalized = unicodedata.normalize("NFKD", name)
    ascii_name = normalized.encode("ascii", "ignore").decode("ascii")
    cleaned = re.sub(r"[^\w\s-]", "", ascii_name.lower())
    return cleaned.replace(" ", "-")


if __name__ == "__main__":
    therapists = scrape_data()

    # Manual correction, because first therapist have email under phone
    therapists[0]["email"] = therapists[0]["phone"]
    therapists[0]["phone"] = None

    # Create output folder
    os.makedirs("photos", exist_ok=True)

    scrape_photos(therapists=therapists)

        # save to JSON
    with open("members.json", "w", encoding="utf-8") as f:
        json.dump(therapists, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(therapists)} therapists to therapists.json")

