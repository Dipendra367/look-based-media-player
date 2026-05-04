import vlc

class MediaPlayer:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.is_paused = False

    def load(self, file_path):
        media = self.instance.media_new(file_path)
        self.player.set_media(media)

    def play(self):
        if self.is_paused:
            self.player.play()
            self.is_paused = False

    def pause(self):
        if not self.is_paused:
            self.player.pause()
            self.is_paused = True

    def start(self):
        self.player.play()
        self.is_paused = False

    def stop(self):
        self.player.stop()

    def is_playing(self):
        return self.player.is_playing()

    def forward(self, seconds=10):
        current = self.player.get_time()  # milliseconds
        self.player.set_time(current + seconds * 1000)

    def backward(self, seconds=10):
        current = self.player.get_time()
        new_time = max(0, current - seconds * 1000)
        self.player.set_time(new_time)

    def get_position(self):
        return self.player.get_position()  # 0.0 to 1.0

    def set_position(self, pos):
        self.player.set_position(pos)  # 0.0 to 1.0

    def get_time(self):
        return self.player.get_time()

    def get_length(self):
        return self.player.get_length()