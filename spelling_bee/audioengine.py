import requests


class Audio:
    def __init__(self, filename, website_address, path_to_audio_files):
        self.website_address = website_address
        self.filename = filename
        self.link = self.website_address + self.filename + '.mp3'
        self.path_to_audio_files = path_to_audio_files

    def load_audio(self):
        response = requests.get(self.link)
        if not self.filename.isalpha() or response.status_code is not 200:
            raise FileNotFoundError
        else:
            return response

    def save_audio_file(self):
        file_contents = self.load_audio().content
        with open(self.path_to_audio_files+self.filename+'.mp3', 'wb') as f:
            f.write(file_contents)

    def get_audio_file(self):
        self.save_audio_file()
        return open(self.path_to_audio_files+self.filename+'.mp3', 'rb')

    def send_voice_message(self, user_id, bot):
        bot.send_voice(user_id, self.get_audio_file())


class Pronunciation(Audio):
    def __init__(self, filename):
        self.website_address = 'https://howjsay.com/mp3/'
        self.filename = filename
        self.path_to_audio_files = '/Users/ian/PycharmProjects/yasmine/audio/pronunciation/'
        super().__init__(self.filename, self.website_address, self.path_to_audio_files)
