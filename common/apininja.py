from PIL import Image, ImageOps
import os.path

import requests

from config.config import config


def resize(img_path:str,max_width:int,max_height:int)->None:
    with Image.open(img_path) as im:
        im = ImageOps.exif_transpose(im)
        width, height = im.size

        if width <= max_width and height <= max_height:
            return  # already fits

        im.thumbnail((max_width, max_height), Image.LANCZOS)

        # Determine save format from original image or file extension
        fmt = im.format
        if not fmt:
            ext = os.path.splitext(img_path)[1].lower()
            fmt = {
                ".jpg": "JPEG",
                ".jpeg": "JPEG",
                ".png": "PNG",
                ".webp": "WEBP",
                ".gif": "GIF",
                ".bmp": "BMP",
                ".tiff": "TIFF"
            }.get(ext, None)

        save_kwargs = {}
        # If transparency exists and target format doesn't support it (e.g. JPEG), convert
        if im.mode in ("RGBA", "LA") and (fmt is None or fmt.upper() in ("JPEG", "BMP")):
            background = Image.new("RGB", im.size, (255, 255, 255))
            alpha = im.split()[-1]
            background.paste(im.convert("RGBA"), mask=alpha)
            im = background
            fmt = fmt or "JPEG"
            save_kwargs["quality"] = 85
        elif fmt and fmt.upper() == "JPEG" and im.mode != "RGB":
            im = im.convert("RGB")
            save_kwargs["quality"] = 85

        im.save(img_path, format=(fmt if fmt else None), **save_kwargs)

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

    def get_logo(self, airline_code:str, cached:bool=True)-> dict[str, str] | None:
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

        logo_types = {"": "logo_url", "B": "brandmark_url", "T": "tail_logo_url"}

        if cached:
            logos = {}
            for logo_pre, logo_type in logo_types.items():
                cache_file = f"{self.cache_dir}/{logo_pre}{airline_code}.png"
                if os.path.exists(cache_file):
                    logos[logo_type] = cache_file
            if len(logos)>0:
                return logos

        response = requests.get(f"https://api.api-ninjas.com/v1/airlines?iata={airline_code}",
                                headers={'X-Api-Key': self.api_key})
        if response.status_code == 200:
            data = response.json()[0]
            logos = {"logo_url": f"{self.cache_dir}/nologo.png"}
            for logo_pre,logo_type in logo_types.items():
                if logo_type in data:
                    logo_url = data[logo_type]
                    cache_file=f"{self.cache_dir}/{logo_pre}{airline_code}.png"
                    self.download_url(logo_url, cache_file)
                    resize(cache_file,150,100)
                    logos[logo_type]=cache_file
            return logos
        else:
            raise Exception(f"Error fetching logo: {response.status_code} - {response.text}")


if __name__=='__main__':
    ninja=Ninja(config.APININJASKEY, config.LOGOS)
    ninja.get_logo('TK',True)