#!/usr/bin/python3
#   ______ ____   _____      _______     ___   ___          __     _      _      
#  |  ____/ __ \ / ____|    |  __ \ \   / / \ | \ \        / /\   | |    | |     
#  | |__ | |  | | (___      | |  | \ \_/ /|  \| |\ \  /\  / /  \  | |    | |     
#  |  __|| |  | |\___ \     | |  | |\   / | . ` | \ \/  \/ / /\ \ | |    | |     
#  | |___| |__| |____) |    | |__| | | |  | |\  |  \  /\  / ____ \| |____| |____ 
#  |______\____/|_____/     |_____/  |_|  |_| \_|   \/  \/_/    \_\______|______|
#                                                                                
#                                                                                
#  
#                                                                   Version 0.0.1
#  
#                                          Edwin van de Ven <edwin@simplycode.nl>
#
# This script assumes the dynamic wallpaper will start from midnight
# Provide the path to your xml file as the first arument; eg. python3 eos_dynwall /home/user/Pictures/mywalls.xml

import argparse
import os
import shutil
import subprocess
import time
from datetime import datetime

from bs4 import BeautifulSoup, Comment


def update_wall(xml_file):
    now = datetime.now()
    current_time = int((now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())
    home = os.path.expanduser("~")
    pictures_folder = os.path.join(home, "Pictures")
    light_dm_folder = os.environ['XDG_GREETER_DATA_DIR']
    light_dm_wall_folder = os.path.join(light_dm_folder, 'wallpaper')
    print(pictures_folder)
    print(int(current_time))


    with open(xml_file) as file:
        file_time = 0

        data = file.read()
        soup = BeautifulSoup(data)
        root = soup.background
        
        # remove comments
        for element in root(text=lambda text: isinstance(text, Comment)):
            element.extract()
        
        # print(root)
        children = root.children
        print(children)
        for tag in children:
            print("#####")
            print(tag)
            if tag.name == "static" or tag.name == "transition":
                print('static found')
                
                duration = int(float(tag.find('duration').get_text()))
                print(duration)
                file_time += duration
                print(file_time)
                
                if file_time > current_time:
                    print('this one!')
                    
                    
                    if tag.name == "static":
                        print('setting wallpaper')
                        wall_location = tag.find("file").get_text()
                        print(wall_location)
                        print(os.path.exists(wall_location))
                        result = subprocess.check_output([
                            "/usr/bin/gsettings",  
                            "set",  
                            "org.gnome.desktop.background", 
                            "picture-uri",  
                            "'file://%s'" % wall_location
                        ])
                        
                        # Lightdm copy
                        shutil.copy(wall_location, os.path.join(light_dm_wall_folder, 'wall.jpg'))
                        
                    else:
                        print('calculation transition')
                        print('current_time')
                        print(current_time)
                        
                        # 0 - 100 depending on time past since start of duration
                        t_start = file_time - duration
                        print(t_start)
                        
                        # how far has current time progressed after start time
                        t_progress = current_time - t_start 
                        print(t_progress)
                        t_percentage = int((t_progress / duration) * 100)
                        print(t_percentage)
                        
                        wall_from = tag.find("from").get_text()
                        wall_to = tag.find("to").get_text()
                        
                        print(wall_from)
                        print(wall_to)
                        
                        wall = os.path.join(pictures_folder, "wall.jpg")
                        wall_new = os.path.join(pictures_folder, "wall_new.jpg")
                        
                        result = subprocess.check_output([
                            "/usr/bin/composite",
                            "-blend",
                            str(t_percentage),
                            wall_to,
                            wall_from,
                            wall_new
                        ])
                        
                        print(result)
                        
                        os.rename(wall_new, wall)
                        
                        
                        result = subprocess.check_output([
                            "/usr/bin/gsettings",  
                            "set",  
                            "org.gnome.desktop.background", 
                            "picture-uri",  
                            "'file://%s'" % wall
                        ])
                        
                        # Lightdm copy
                        shutil.copy(wall, os.path.join(light_dm_wall_folder, 'wall.jpg'))
                        
                        
                    break
                
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("xml_file")
    args = parser.parse_args()
    
    xml_file = args.xml_file
    print(xml_file)    
    
    while 1 < 2:
        # Just keep going...
        update_wall(xml_file)
        print("Sleeping...")
        time.sleep(600)
        
        
    

