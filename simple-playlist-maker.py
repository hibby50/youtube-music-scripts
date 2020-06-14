from ytmusicapi import YTMusic
import subprocess
import configparser
from tinytag import TinyTag

config = configparser.RawConfigParser()
config.read('./simple.cfg', 'utf-8')

ytmusic = YTMusic('headers_auth.json')

#music_files = subprocess.check_output("find %s" % config['music']['local'], shell=True)
#music_files = music_files.decode("utf-8").splitlines()

#music_tags = []
#for music_file in music_files:
#    music_tags.append(TinyTag.get(music_file))

playlist_files = subprocess.check_output('find %s -name "*m3u*"' % config['playlists']['local'], shell=True)
playlist_files = playlist_files.decode("utf-8").splitlines()

remote_songs = ytmusic.get_library_upload_songs(99999)
remote_playlists = ytmusic.get_library_playlists()
print(len(remote_songs))
playlist_content = {}

for playlist in playlist_files:
    f = open(playlist, "r")
#    playlist_content[playlist.strip(".m3u")] = f.readlines()
    for remote_playlist in remote_playlists:
        if remote_playlist["title"] in playlist:
            playlist_content[remote_playlist["playlistId"]] = f.readlines()

#for music_tag in music_tags:
#    print ( music_tag.genre)

for playlist in playlist_content:
    upload = []
    pl_tracks = ytmusic.get_playlist(playlist, 9999)["tracks"]
    pl_trackid = []
    for track in pl_tracks:
        pl_trackid.append(track["videoId"])
    for song in remote_songs:
        #print(str(song["title"]) + str(playlist_content[playlist]))
        if song["artist"] and song["album"] and song["title"]:
            upload += [song["videoId"] for pl_entry in playlist_content[playlist] if song["title"] in pl_entry \
                and song["artist"] in pl_entry and song["album"] in pl_entry and \
                song["videoId"] not in pl_trackid]
    print(ytmusic.add_playlist_items(playlist, upload))
#        if song["title"] in playlist_content[playlist]:
#            print(song["title"] + playlist_content[playlist])
#            #print(ytmusic.add_playlist_items(playlist, [song["videoid"]]))
