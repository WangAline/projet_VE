import os
from PIL import Image
import piexif

def add_exif_data(image_path, latitude, longitude, camera_make, camera_model, iso, exposure_time, f_number,
                  contrast, brightness, saturation, sharpness):
    # Open the image
    img = Image.open(image_path)

    # Create or load EXIF data
    try:
        exif_dict = piexif.load(img.info.get('exif', b''))
    except ValueError:
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "Interop": {}, "1st": {}}

    # Function to convert to DMS (degrees, minutes, seconds)
    def convert_to_dms(degrees):
        deg = int(degrees)
        minutes = int((degrees - deg) * 60)
        seconds = (degrees - deg - minutes / 60) * 3600
        return ((deg, 1), (minutes, 1), (int(seconds * 100), 100))

    # Add GPS Data
    lat_dms = convert_to_dms(abs(latitude))
    lon_dms = convert_to_dms(abs(longitude))
    exif_dict['GPS'][piexif.GPSIFD.GPSLatitude] = lat_dms
    exif_dict['GPS'][piexif.GPSIFD.GPSLongitude] = lon_dms
    exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef] = 'N' if latitude >= 0 else 'S'
    exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] = 'E' if longitude >= 0 else 'W'

    # Add Camera and Photo Metadata
    exif_dict['0th'][piexif.ImageIFD.Make] = camera_make.encode('utf-8')  # Camera Make
    exif_dict['0th'][piexif.ImageIFD.Model] = camera_model.encode('utf-8')  # Camera Model
    exif_dict['Exif'][piexif.ExifIFD.ISOSpeedRatings] = iso  # ISO
    exif_dict['Exif'][piexif.ExifIFD.ExposureTime] = (exposure_time[0], exposure_time[1])  # Exposure Time
    exif_dict['Exif'][piexif.ExifIFD.FNumber] = (f_number[0], f_number[1])  # F-number

    # Add Advanced Photo Attributes
    exif_dict['Exif'][piexif.ExifIFD.Contrast] = contrast  # 0 = Normal, 1 = Soft, 2 = Hard
    exif_dict['Exif'][piexif.ExifIFD.BrightnessValue] = (brightness, 100)  # Brightness as a rational number
    exif_dict['Exif'][piexif.ExifIFD.Saturation] = saturation  # 0 = Normal, 1 = Low, 2 = High
    exif_dict['Exif'][piexif.ExifIFD.Sharpness] = sharpness  # 0 = Normal, 1 = Soft, 2 = Hard

    # Save the image with the updated EXIF data
    exif_bytes = piexif.dump(exif_dict)
    img.save(image_path, exif=exif_bytes)
    print(f"EXIF data added to: {image_path}")

def process_images_in_folder(folder_path, latitude, longitude, camera_make, camera_model, iso, exposure_time, f_number,
                             contrast, brightness, saturation, sharpness):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.lower().endswith(('.jpg', '.jpeg')):  # Process JPEG images only
            add_exif_data(file_path, latitude, longitude, camera_make, camera_model, iso, exposure_time, f_number,
                          contrast, brightness, saturation, sharpness)

# Example usage
folder_path = './images_test'  # Replace with the folder containing your images
latitude = 40.7128   # Example latitude
longitude = -74.0060  # Example longitude
camera_make = "Canon"
camera_model = "EOS 5D Mark IV"
iso = 100
exposure_time = (1, 125)  # Exposure time: 1/125 seconds
f_number = (18, 10)  # F-number: f/1.8

# Advanced photo settings (values depend on EXIF standard)
contrast = 0        # 0 = Normal, 1 = Soft, 2 = Hard
brightness = 50     # Brightness as an integer (e.g., 50%)
saturation = 1      # 0 = Normal, 1 = Low, 2 = High
sharpness = 2       # 0 = Normal, 1 = Soft, 2 = Hard

process_images_in_folder(folder_path, latitude, longitude, camera_make, camera_model, iso, exposure_time, f_number,
                         contrast, brightness, saturation, sharpness)
