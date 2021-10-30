from datetime import datetime
import json

from gui import *
from save_to_img import *
from change_desktop_img import *


setting_json_path = '../settings/setting.json'
json_open = open(setting_json_path, 'r')
json_data = json.load(json_open)

accumulated_file = str(datetime.now().strftime('%Y%m%d%H%M%S'))
# json_data["accumulated_file"] = accumulated_file
desktop_img_path = '/Users/makidaisuke/Desktop/Projects/Objective-visualization/image/desktop_picture.jpg'
json_data["desktop_img_path"] = desktop_img_path


with open(setting_json_path, mode='w', encoding='utf-8') as file:
	json.dump(json_data, file, ensure_ascii=False, indent=2)


# run_gui()

SaveImage()

# change_wallpaper(desktop_img_path=desktop_img_path)
# change_wallpaper_mac_wallpaper(desktop_img_path=desktop_img_path)
