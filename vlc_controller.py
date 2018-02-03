import vlc
import os
from random import shuffle
from time import sleep
from threading import Thread

class MediaControl:
    PERMITTED_EXTENSIONS = ["wav"]
    AUDIO_NO_SONGS = "32722446.mp3"
    AUDIO_END_OF_PLAYLIST = "32722419.mp3"
    path = None
    path_inventory = []
    file_inventory = []
    song_inventory = []
    playlist = []
    vlc_instance = None
    player = None
    current_playlist_index = None
    skip_song_flag = None
    playlist_kill_flag = None
    def get_path_inventory(self):
        self.path = self.path.rstrip(os.sep)
        self.path_inventory = os.listdir(self.path)
    def get_file_inventory(self):
        if self.path_inventory == []:
            self.get_path_inventory()
        file_inventory = []
        for path in self.path_inventory:
            if os.path.isfile(self.path + os.sep + path):
                self.file_inventory.append(path)
    def get_song_inventory(self):
        if self.file_inventory == []:
            self.get_file_inventory()
        for file in self.file_inventory:
            if file[-3:] in self.PERMITTED_EXTENSIONS:
                self.song_inventory.append(file)
    def build_playlist(self):
        self.playlist=[]
        if self.song_inventory == []:
            self.get_song_inventory()
        for song in self.song_inventory:
            self.playlist.append(self.path + os.sep + song)
        shuffle(self.playlist)
        if self.playlist == []:
            self.playlist.append(self.AUDIO_NO_SONGS)
        else:
            self.playlist.append(self.AUDIO_END_OF_PLAYLIST)
    def inventory_unchanged(self):
        if self.path_inventory == os.listdir(self.path):
            return True
        else:
            return False
    def verify_path(self, path):
        return os.path.exists(path)
    def set_path(self, path):
        if self.verify_path(path):
            self.path = path.rstrip(os.sep)
        if self.path_inventory == [] or self.inventory_unchanged():
            return
        else:
            self.path_inventory = []
            self.file_inventory = []
            self.song_inventory = []
            self.playlist = []
    def __play_playlist(self):
        self.playlist_kill_flag = False
        self.current_playlist_index = -1
        while self.current_playlist_index != None:
            self.current_playlist_index += 1
            print(self.current_playlist_index)
            self.play_song(self.current_playlist_index)
            while self.player.get_state() != vlc.State.Ended and self.skip_song_flag == False and self.playlist_kill_flag == False:
                sleep(0.1)
            if self.player.get_state() == vlc.State.Playing:
                self.player.stop()
            self.skip_song_flag = False
            if self.current_playlist_index == len(self.playlist) -1 or self.playlist_kill_flag == True:
                self.current_playlist_index = None;
    def play_playlist(self):
        self.playlist_kill_flag = True
        sleep(0.1)
        Thread(target=self.__play_playlist).start()
    def pause(self):
        if self.player.get_state() in [vlc.State.Playing, vlc.State.Paused]:
            self.player.pause()
        else:
            self.play_playlist()
    def play_song(self, playlist_index):
        self.skip_song_flag = False
        self.current_media = self.vlc_instance.media_new(self.playlist[playlist_index])
        self.player.set_media(self.current_media)
        self.player.play()
    def __init__(self, path):
        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()
        self.set_path(path)
        self.build_playlist()



#a = MediaControl(r"c:\users\simon gurney\downloads")
#a.play_playlist()