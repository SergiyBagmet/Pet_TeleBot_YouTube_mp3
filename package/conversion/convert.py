
from typing import Any, Callable, Dict, Optional
import os

from pytube import YouTube, Stream
from moviepy.editor import VideoFileClip




class ConvertErrorYouTube(Exception):
    def __init__(self, message):
        super().__init__(message)

class ConvertYouTube(YouTube):
    # TODO название? 
    def __init__(self, url: str, on_progress_callback: Callable[[Any, bytes, int], None] | None = None, on_complete_callback: Callable[[Any, str | None], None] | None = None, proxies: Dict[str, str] = None, use_oauth: bool = False, allow_oauth_cache: bool = True):
        super().__init__(url, on_progress_callback, on_complete_callback, proxies, use_oauth, allow_oauth_cache)
       
        self.stream_mp4 : Stream | None = None # стрим(дорожка видео мп4 с макс. качеством)
        self.path_mp4 : str | None = None # путь к скачаному фалу мп4
        self.path_mp3 : str | None = None # путь к конвентированому фалу мп3
       
    @ classmethod
    def valid_one_video_link(cls, link: str) -> None:
        if not link.startswith("https://www.youtube.com/watch?v="):
            raise ConvertErrorYouTube("Not valid link")

    def __get_stream_mp4(self) -> Stream | None:
        # выбираем из списка стримов mp4 с максимальним качеством
        if self.length > 641 : # продолжительность видео в секундах
            raise ConvertErrorYouTube("I can't load to long video")
        self.stream_mp4 = self.streams.filter(mime_type="video/mp4").get_highest_resolution()

    def __load_mp4_to_temp(self):
        # скачиваем вибраний стрим в папку темп если он есть ложим в поле путь к мп4 
        if self.stream_mp4 is None:
            raise ConvertErrorYouTube("Can't fount mp4 stream from this video")
        self.path_mp4 = self.stream_mp4.download(output_path="temp", max_retries=3) 

    def __from_mp4_to_mp3(self):
        # конвертируем из мп4 в мп3 ложим в поле путь мп3  
        if not os.path.exists(self.path_mp4):
            raise ConvertErrorYouTube(f"can't found mp4 file {self.path_mp4}")
        
        with VideoFileClip(self.path_mp4) as video:
            path_mp3 = os.path.splitext(self.path_mp4)[0] + ".mp3"
            audio = video.audio
            audio.write_audiofile(path_mp3)

        if not os.path.exists(path_mp3):
            raise ConvertErrorYouTube(f"can't found mp4 file {path_mp3}")    
        self.path_mp3 = path_mp3 

    def __del_mp4(self):
        # удаляем мп4 лодим в поле None
        self.path_mp4 = os.remove(self.path_mp4)
    
    def __mp3_to_bytes(self) -> bytes:
        # TODO а чо можно такое провернуть через os??
        with open(self.path_mp3, "rb") as file_mp3:
            return file_mp3.read()
       
    def link_to_mp3_transaction(self): 
        #TODO соответсвующее название метода которий делает все в нужном нам порядке подобие "транзакции"
        # получаем стрим - качаем - конвертируем  - удаляем мп4
        # после применения єтого метода можем визвать to_dict
        self.__get_stream_mp4()
        self.__load_mp4_to_temp()
        self.__from_mp4_to_mp3()
        self.__del_mp4()
        # подходит ли сюда по контексту  __mp3_to_bytes ?
        # TODO если на всех этапах ок(или на последнем получили файл мп3) 
        # то ли тут вернуть словарь(to_dict)/None
        
    def to_dict_db(self) -> dict | None:
        # словарь подготовка для записи в БД
        if self.path_mp3 is None:
            return None
        return {
            "link_id": self.video_id,
            "song" : self.title,
            "autor" : self.author,
            "sec" : self.length,
            "bytes": self.__mp3_to_bytes()
        }
        
if __name__ == "__main__":

    link = "https://www.youtube.com/watch?v=sVx1mJDeUjY"
    yt = ConvertYouTube(link)
    yt.link_to_mp3_transaction()
    print(yt.to_dict_db())





# url = YouTube(link)
# # song, autor, id , sec =  url.title, url.author url.video_id, url.length

# stream_video_mp4 = url.streams.filter(mime_type="video/mp4").get_highest_resolution()

# # mp4path = stream_video_mp4.download()
# mp3path = f"{song}.mp3"

# # def converttomp3(mp4file, mp3file):
# #     video = VideoFileClip(mp4file, audio_fps=44100)
# #     audio=video.audio
# #     audio.write_audiofile(mp3file)
# #     audio.close()
# #     video.close()

# # converttomp3(mp4path, mp3path)

# with open(mp3path, "rb" ) as file:
#     mp3bin = file.read()

# print(type(mp3bin))





