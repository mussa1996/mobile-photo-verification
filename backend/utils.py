# backend/utils.py
from PIL import Image
import piexif

def check_photo_author(photo_path, expected_signature):
    """
    Check if the uploaded photo contains the expected signature in its EXIF metadata.
    It first checks the "Artist" tag (tag 315) and then an alternative tag like "XPComment".
    """
    try:
        img = Image.open(photo_path)
        exif_data = img.info.get("exif")
        if exif_data:
            exif_dict = piexif.load(exif_data)
            # Check the Artist tag (0th IFD tag 315)
            artist = exif_dict.get("0th", {}).get(piexif.ImageIFD.Artist, b'').decode('utf-8', errors='ignore')
            if artist == expected_signature:
                return True
            # Alternatively, check for XPComment tag (stored as UCS-2 in little endian)
            xpcomment = exif_dict.get("0th", {}).get(piexif.ImageIFD.XPComment, b'')
            if xpcomment:
                try:
                    comment = xpcomment.decode('utf-16le', errors='ignore').strip('\x00')
                    if comment == expected_signature:
                        return True
                except Exception:
                    pass
        return False
    except Exception as e:
        print("Error in check_photo_author:", e)
        return False
