import requests
import logging
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_swapi_people(limit: int) -> Optional[List[Dict]]:
    """
    Fetch a specified number of people from the Star Wars API (SWAPI).

    Args:
        limit: Maximum number of people to retrieve.

    Returns:
        A list of dictionaries, each containing data about a person,
        or None if an error occurs.
    """
    items = []
    url = "https://swapi.dev/api/people/"

    while len(items) < limit:
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            items.extend(data["results"])
            logger.info(f"Fetched {len(data['results'])} people, total so far: {len(items)}")
            url = data["next"]  # may become None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None

        if url is None:
            logger.info("No more pages available.")
            break

    return items[:limit]

def main():
    try:
        limit = int(input("How many Star Wars characters do you want to download? "))
        if limit <= 0:
            print("Please enter a positive number.")
            return
    except ValueError:
        print("Invalid input. Please enter an integer.")
        return

    people = fetch_swapi_people(limit)
    if people:
        for person in people:
            print(person["name"])
    else:
        print("Failed to download data.")

if __name__ == "__main__":
    main()
