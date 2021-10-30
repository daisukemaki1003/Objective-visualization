import subprocess
import time


def change_wallpaper_apple_script(desktop_img_path):
	script = """
	/usr/bin/osascript<<END
	tell application "System Events"
	set picture of every desktop to POSIX file "%s"
	end tell
	END
	"""
	time.sleep(5)
	subprocess.Popen(script % desktop_img_path, shell=True)


def change_wallpaper_mac_wallpaper(desktop_img_path):
	command = ['wallpaper', str(desktop_img_path)]
	try:
		subprocess.check_call(command)
	except:
		print('Error')
