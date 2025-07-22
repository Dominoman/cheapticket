import os.path

import requests

from config.config import config


class Ninja:
    def __init__(self, api_key,cache_dir:str):
        self.api_key = api_key
        self.cache_dir = cache_dir

    @staticmethod
    def download_url(url: str, dest_path: str) -> None:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    def get_logo(self, airline_code:str, cached:bool=True)->str:
        """
        Fetches the logo URL for a given airline code.

        Args:
            cached:
            airline_code (str): The IATA code of the airline.

        Returns:
            str: The URL of the airline's logo.
        """
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        cache_file = f"{self.cache_dir}/{airline_code}.jpg"
        if cached:
            if os.path.exists(cache_file):
                return cache_file

        response = requests.get(f"https://api.api-ninjas.com/v1/airlines?iata={airline_code}",
                                headers={'X-Api-Key': self.api_key})
        if response.status_code == 200:
            logo_url = response.json()[0]["logo_url"]
            self.download_url(logo_url, cache_file)
            return cache_file
        else:
            raise Exception(f"Error fetching logo: {response.status_code} - {response.text}")

if __name__=="__main__":
    ninja = Ninja(config.APININJASKEY, config.LOGOS)
    print(ninja.get_logo("BR"))
