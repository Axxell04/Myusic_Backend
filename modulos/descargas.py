
import os
import datetime
# import threading
# import pyperclip
from pytubefix import YouTube, Playlist

from modulos import conversor
# from modulos import online
from db import DB_Manager
# import conversor
# import online

class Core():
    def __init__(self) -> None:
        self.PATH_MUSIC = 'music'
        self.PATH_MP4 = os.path.join(self.PATH_MUSIC, 'mp4')
        self.PATH_PLAYLISTS = os.path.join(self.PATH_MUSIC, 'playlist')
        self.conversor = conversor.Core()
        self.db_manager = DB_Manager()

    def close(self):
        self.db_manager.close()

    def descargar(self, link='', music_name='') -> dict | None:
        if not os.path.exists(self.PATH_MUSIC):
            os.mkdir(self.PATH_MUSIC)
        if not os.path.exists(self.PATH_MP4):
            os.mkdir(self.PATH_MP4)
        # print(2)
        
        res = {
            "success": False,
            "message": "",
            "data": {}
        }
        
        #Si es una canción individual
        if not 'playlist' in link:
            try:
                # print(3)
                yt = YouTube(link, 'WEB')
                
                author = yt.author
                title = yt.title
                
                music_id = self.db_manager.validate_new_music(name=title, author=author)
                #print(4)
                if music_id == 0:
                    limit = 5
                    cont = 0
                    descarga_completa = False
                    music_path = ""
                    while not descarga_completa and cont < limit:
                        try:
                            print(f"-- Titulo: {title} --")
                            target_dir = os.path.join(self.PATH_PLAYLISTS, author)
                            caracteres_prohibidos = ['\\','/',':','*','?','"','<','>','|']
                            for caracter in caracteres_prohibidos:
                                if caracter in title:
                                    title = title.replace(caracter, '')
                            # vid_path = yt.streams.get_lowest_resolution().download(self.PATH_MP4)
                            music_path = yt.streams.get_audio_only().download(target_dir, f"{title}.mp3")
                            # print(f"PATH: {vid_path}")
                            # print(f'FILE NAME: {os.path.basename(vid_path)}')
                            descarga_completa = True
                            print('-- Descarga Completa --')
                        except Exception as e:
                            print(f"|| Error con la descarga, intento N° {cont} ||")
                            print(e)
                            
                        cont += 1
                    # music_path, conversion_completa = self.conversor.convertir(vid_path=vid_path, playlist_name=author)
                    print(music_path)

                    # if conversion_completa:
                    #     print("-- Conversión completa --")
                    # else:
                    #     print("|| Error en la conversión ||")
                    
                    music_data = {
                        "name": yt.title,
                        "author": yt.author,
                        "duration": f"0{str(datetime.timedelta(seconds=yt.length))}",
                        "path": music_path
                    }
                    
                    print(music_data)
                    
                    if music_data['name'] and music_data['author'] and music_data['duration'] and music_data['path']:
                        data = self.db_manager.add_music(name=music_data['name'], author=music_data['author'], duration=music_data['duration'], path=music_data['path'])
                        res['success'] = True
                        res['message'] = "Success"
                        res['data'] = data.model_dump()
                    else:
                        res['success'] = False
                        res['message'] = "Download error"

                    
                
                else:
                    res['success'] = False
                    if type(music_id) == int:
                        res['message'] = "Music already downloaded"
                    else:
                        res['message'] = "Failed validation"
                
            except Exception as e:
                print(f'|| Error al descargar la canción ||')
                res['success'] = False
                res['message'] = "Download failed"

            finally:
                return res
        
        #Si es una playlist
        else:
            try:
                if not os.path.exists(f"{self.PATH_MP4}/newpls/"):
                    os.mkdir(f"{self.PATH_MP4}/newpls/")
                
                playlist = Playlist(link)
                playlist_title = playlist.title
                
                #Comprobar si la playlist ya existe
                playlist_already_exists = False
                playlist_id = self.db_manager.validate_new_playlist(playlist_title)
                if playlist_id == None: #Si no se pudo validar su existencia, cancelar el proceso
                    res['success'] = False
                    res['message'] = "Failed validation"
                elif playlist_id == 0: #Si tras la validación no se retorna un id distinto de CERO, crear una nueva playlist
                    #Creando la nueva playlist en la tabla playlists
                    playlist_id = self.db_manager.add_playlist(name=playlist_title)
                    
                else: #La playlist ya existe
                    playlist_already_exists = True
                
                if not res['message']: #Si aún no se ha recivido un mensaje de respuesta, continuar con la descarga de las canciones
                    musics_data = []

                    try:
                        for video in playlist:
                            yt = YouTube(video)
                            
                            music_id = self.db_manager.validate_new_music(name=yt.title, author=yt.author)
                            
                            if music_id == 0:
                            
                                author = yt.author.replace(' ','')
                                limit = 5
                                cont = 0
                                descarga_completa = False
                                while not descarga_completa and cont < limit:
                                    try:
                                        print(f"-- Titulo: {yt.title} --")
                                        
                                        vid_path = yt.streams.get_lowest_resolution().download(f"{self.PATH_MP4}/newpls/")

                                        # vid_path = yt.streams.get_lowest_resolution().
                                        descarga_completa = True
                                        print('-- Descarga Completa --')
                                    except Exception as e:
                                        print(f"|| Error con la descarga, intento N° {cont} ||")
                                        print(e)
                                    cont += 1

                                music_path, conversion_completa = self.conversor.convertir(vid_path=vid_path, playlist_name=author)

                                if conversion_completa:
                                    print(f"PATH: {music_path} | Conversión completa")
                                    music_data = {
                                        "name": yt.title,
                                        "author": yt.author,
                                        "duration": f"0{str(datetime.timedelta(seconds=yt.length))}",
                                        "path": music_path
                                    }
                                    # print(music_data)
                                    
                                    #Añadiendo cada canción a la tabla musics
                                    music = self.db_manager.add_music(name=music_data['name'], author=music_data['author'], duration=music_data['duration'], path=music_data['path'])
                                    musics_data.append(music.model_dump())
                                    
                                    #Comprobar si se logró crear la nueva playlist
                                    if playlist_id:
                                        #Asociar cada canción a la nueva playlist
                                        self.db_manager.add_musics_to_playlist(playlist_id, [music.id])
                                    
                                else:
                                    print(f"PATH: {music_path} | Error de conversión")

                            else: #La canción ya está registrada o no se puedo validar su existencia
                                if type(music_id) == int: #Si music_id es de tipo INT significa que la canción ya está registrada
                                    if playlist_id: #Asociamos la canción ya registrada a la nueva playlist
                                        self.db_manager.add_musics_to_playlist(playlist_id, [music_id])
                                else: #Si music_id no es de tipo INT entonces es NONE, lo que significa que no se pudo realizar la validación
                                    pass #Simplemente no descargamos la canción y seguimos con la descarga de la playlist
                                    
                        if not musics_data:
                            res['success'] = False
                            if playlist_already_exists:
                                res['message'] = "Playlist already downloaded"
                            else:
                                res['message'] = "Download failed"
                        else:
                            res['success'] = True
                            if playlist_already_exists:
                                res['message'] = "Updated playlist"
                                res['data'] = musics_data
                            else:
                                res['message'] = "Success"
                                res['data'] = musics_data
                            

                        # print('-- Playlist descargada con éxito --')
                    except Exception as e:
                        print('|| Error al descargar la playlist ||')
                        print(e)
            except:
                print('|| Error al descargar la playlist ||')
                res['success'] = False
                res['message'] = "Download failed"
                
            finally:
                return res


# class Music_Link():
#     def __init__(self) -> None:
#         self.lib_imported = False
#         # self.online = online.Online(unit=True)
    
#     def search(self, music_name='') -> str:
#         if self.online.get_internet():
#             try:
#                 import pywhatkit
#                 link = pywhatkit.playonyt(music_name, open_video=False)
#                 # self.online.stop()
#                 return link
#             except Exception as e:
#                 print(e)
            


# downloader = Core()

# link = 'https://youtu.be/U29h5Ocgj30?si=EXZwTNwI2mW7OmDQ'
# # link = 'https://www.youtube.com/playlist?list=PLsIzLTThWwu3A_nt1Iz13SIOF4g41BoYe'
# # music_name = 'columbia'
# print(f"FUNCION DESCARGA | RETURN: {downloader.descargar(link)}")