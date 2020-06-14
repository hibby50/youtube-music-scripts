from ytmusicapi import YTMusic
import subprocess
import unittest
import configparser
import time
from multiprocessing import Pool

config = configparser.RawConfigParser()
config.read('./simple.cfg', 'utf-8')

ytmusic = YTMusic('headers_auth.json')

music_files = subprocess.check_output("find %s" % config['music']['local'], shell=True)
music_files = music_files.decode("utf-8").splitlines()

def upload (music_file):
    if music_file.endswith("flac") or music_file.endswith("mp3"):
        response = ytmusic.upload_song(music_file)
        retries = 0
        while str(response) == "<Response [500]>":
            if retries < 100:
                time.sleep(20)
                response = ytmusic.upload_song(music_file)
                retries += 1
            else:
                print("failed to upload " + music_file)
                return "failed to upload " + music_file

        if str(response) == "<Response [409]>":
            print("already in remote library: " + music_file)
            return "already in remote library: " + music_file
        else:
            print(str(response) + music_file)
            return str(response) + music_file
    else:
        return "error"

if __name__ == '__main__':
    pool = Pool(30)
    pool.map(upload, music_files)
