import wget
import requests
from bs4 import BeautifulSoup as bs
import urllib.request
import os
import platform
import sys

class Photos:
    def __init__(self, name, number_of_pics, folder_name):
        self.name = name
        self.url = f'https://www.google.com/search?q={self.name}&source=lnms&tbm=isch'
        self.folder_name = folder_name
        self.number_of_pics = number_of_pics
    
    def request_url_response(self):
        try:
            res = requests.get(self.url)
            soup = bs(res.text, 'html.parser')
            return soup
        except requests.exceptions.RequestException as e: 
            print(e)
            sys.exit(1)

    def request_images(self):
        arr = []
        counter = 0
        response = self.request_url_response()
        for elem in response.find_all('img'):
            if counter < self.number_of_pics:
                arr.append(elem['src'])
                counter += 1
            else:
                break
        return arr

    def change_directory(self):
        download_folder = os.path.expanduser("~")+"/Downloads/"
        path = download_folder + self.folder_name
        os.chdir(download_folder)
        if os.path.exists(path):
            os.chdir(path)
        else:
            os.mkdir(self.folder_name)
            os.chdir(path)
        return os.getcwd()
    
    def download_images(self):
        all_photos = self.request_images()
        the_path = self.change_directory()
        counter = 1
        if len(all_photos) > 0:  
            print('Beginning to Download')
            for elem in all_photos:
                urllib.request.urlretrieve(elem, f'{the_path}/picture{counter}.jpg')
                print(f'Downloaded Picture{counter}')
                counter += 1
        else:
            print(f'Failed to fetch photos of {self.name}')


if __name__ == "__main__":
    print('This program downloads pictures of the given input in the downloads folder')
    name_pic = str(input('Please enter name of the pictures you want to download: '))
    num = input('Please enter number of pictures you want to download: ')
    try:
        num_of_pics = int(num)
        if not num_of_pics > 0:
            print('Please enter valid number')
            sys.exit()
    except ValueError:
        print('Please enter valid number')
        sys.exit()
    folder_name = str(input('Please enter folder name: '))
    pictures = Photos(name_pic, num_of_pics, folder_name)
    pictures.download_images()