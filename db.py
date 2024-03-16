import sqlite3
import os
import shutil
import config
from models import Music, Playlist, ListModels

# class Music(BaseModel):
#     id: int
#     name: str
#     author: str
#     duration: str
#     path: str

class DB_Manager():
    def __init__(self):
        self.conexion = sqlite3.connect(config.DATA_BASE)
        
        with self.conexion:     
            cursor = self.conexion.cursor()
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS musics (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                author TEXT,
                                duration TIME NOT NULL,
                                path TEXT NOT NULL
                            )
                            ''')
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS playlists (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name VARCHAR(255) NOT NULL
                            )
                           ''')
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS playlist_music (
                                playlist_id INT,
                                music_id INT,
                                FOREIGN KEY (playlist_id) REFERENCES playlists(id),
                                FOREIGN KEY (music_id) REFERENCES musics(id),
                                PRIMARY KEY (playlist_id, music_id)
                            )
                           ''')
    
    def query_musics(self, query: str = "", params: tuple = ()) -> ListModels:
        response = ListModels()
        with self.conexion:
            try:
                cursor = self.conexion.cursor()
                cursor.execute(query, params)
                data = cursor.fetchall()
                if data:
                    for music_tuple in data:
                        music = Music(id=music_tuple[0], name=music_tuple[1], author=music_tuple[2], duration=music_tuple[3], path=music_tuple[4])
                        response.add(music)
                        
            except Exception as e:
                print(f"Error al realizar la consulta: {e}")
                response.set_as_exception()
                
            finally:
                return response
    
    def query_playlists(self, query: str = "", params: tuple = ()) -> ListModels:
        response = ListModels()
        with self.conexion:
            try:
                cursor = self.conexion.cursor()
                cursor.execute(query, params)
                data = cursor.fetchall()
                if data:
                    for playlist_tuple in data:
                        playlist = Playlist(id=playlist_tuple[0], name=playlist_tuple[1])
                        response.add(playlist)
            
            except Exception as e:
                print(f"Error al realizar la consulta: {e}")
                response.set_as_exception()
            
            finally:
                return response
    
    def validate_new_music(self, name: str = "", author: str = "") -> int | None:
        music_id = 0
        query = "SELECT * FROM musics WHERE name = ? AND author = ?"
        params = (name, author)
        with self.conexion:
            try:
                cursor = self.conexion.cursor()          
                cursor.execute(query, params)
                data = cursor.fetchall()
                if data:
                    music_id = data[0][0]
            except:
                print("Error en la validación")
                return None
        
        return music_id
    
    def validate_new_playlist(self, name: str = ""):
        playlist_id = 0
        playlist_id = self.get_playlist_id(name=name)
        return playlist_id
        

    def add_music(self, name: str, path: str, duration: str, author: str = "unknown") -> Music | None:
        query = "INSERT INTO musics (name, author, duration, path) VALUES (?, ?, ?, ?)"
        params = (name, author, duration, path)
        response = self.query_musics(query=query, params=params)
        if response == None:
            print("Error al agregar el nuevo registro")
            return None
        
        data = self.get_musics(path=path)
        if not data.len():
            return None
        else:
            return data.get()[0]
            
    
    def get_musics(self, all: bool = False, id: int = 0, name: str = "", author: str = "", path: str = "") -> ListModels:
        query = ""
        params = ()
        response = ListModels()
        
        if all:
            query = "SELECT * FROM musics"
            
        elif author:
            query = "SELECT * FROM musics WHERE LOWER(author) LIKE ?"
            params = (f"%{author.lower()}%",)
        
        elif name:
            query = "SELECT * FROM musics WHERE LOWER(name) LIKE ?"
            params = (f"%{name.lower()}%",)
        
        elif id:
            query = "SELECT * FROM musics WHERE id = ?"
            params = (id,)
            
        elif path:
            query = "SELECT * FROM musics WHERE path = ?"
            params = (path,)        
        
        if query:
            response = self.query_musics(query=query, params=params)
        
        if not response.len():
                print("No se encontraron canciones")
        return response
            
    
    def delete_musics(self, id: int = 0, all: bool = False) -> bool:
        if id:
            response = self.get_musics(id=id)
            if not response.len():
                print("MUSIC_PATH NO ENCONTRADO")
                response.set_as_exception()
            else:
                music_path = response.get()[0].path
                try:
                    print(f"Eliminando: {os.path.join(config.MAIN_PATH, music_path)}")
                    os.remove(os.path.join(config.MAIN_PATH, music_path))
                except:
                    print("Error al remover el directorio")
            
            
                query = "DELETE FROM musics WHERE id = ?"
                params = (id,)
                response = self.query_musics(query=query, params=params)
                if not response.is_exception:
                    query = "DELETE FROM playlist_music WHERE music_id = ?"
                    response = self.query_musics(query=query, params=params)
        
            if response.is_exception:
                return False
            else:
                return True
        elif all:
            try:
                print(f"Eliminando: {config.MUSIC_PATH}")
                shutil.rmtree(config.MUSIC_PATH)
            except:
                print("Error al remover el directorio")
            for table in ("musics", "playlists", "playlist_music"):
                query = f"DELETE FROM {table}"
                response = self.query_musics(query=query)
            if response == None:
                return False
            else:
                return True
        else:
            return False
            
    def add_playlist(self, name: str) -> int | None:
        #Que pasa si 2 playlists tienen el mismo nombre?  RESOLVER
        query = "INSERT INTO playlists(name) VALUES (?)"
        params = (name,)
        with self.conexion:
            try:
                cursor = self.conexion.cursor()
                cursor.execute(query, params)
                playlist_id = self.get_playlist_id(name=name)
                if not playlist_id:
                    return None
                else:
                    return playlist_id
            except Exception as e:
                print(e)
                return None

    def playlist_exists(self, id: int = 0) -> bool | None:
        exists = False
        query = "SELECT * FROM playlists WHERE id = ?"
        params = (id,)
        with self.conexion:
            try:
                cursor = self.conexion.cursor()
                cursor.execute(query, params)
                data = cursor.fetchall()
                if data:
                    exists = True
            except:
                exists = None
            finally:
                return exists
    
    def delete_playlists(self, id: int = 0) -> bool | None:
        if id:
            exists = self.playlist_exists(id=id)
            if exists == None:
                return None
            elif exists == False:
                return False
            
            query = "DELETE FROM playlists WHERE id = ?"
            params = (id,)
            complete = False
            with self.conexion:
                try:
                    cursor = self.conexion.cursor()
                    cursor.execute(query, params)
                    complete = True
                    try:
                        query = "DELETE FROM playlist_music WHERE playlist_id = ?"
                        cursor.execute(query, params)
                    except:
                        pass
                except:
                    complete = None
                finally:
                    return complete
                
        
    
    def get_playlist_id(self, name: str) -> int | None:
        query = "SELECT id FROM playlists WHERE name = ?"
        params = (name,)
        with self.conexion:
            try:
                cursor = self.conexion.cursor()
                cursor.execute(query, params)
                data = cursor.fetchall()
                if not data:
                    print("No se encontró la playlist")
                    return 0
                else:
                    return data[0][0]
            except Exception as e:
                print(e)
                return None
    
    def get_playlists(self, all: bool = False, id: int = 0, name: str = "") -> ListModels:
        query = ""
        params = ()
        response = ListModels()
        
        if all:
            query = "SELECT * FROM playlists"
        elif id:
            query = "SELECT * FROM playlists WHERE id = ?"
            params = (id,)
        elif name:
            query = "SELECT * FROM playlists WHERE LOWER(name) LIKE ?"
            params = (f"%{name.lower().strip()}%",)
        
        if query:
            response = self.query_playlists(query=query, params=params)
        
        if not response.len():
            print("No se encontraron playlists")
            
        return response        
    
    def exists_connection_m_t_p(self, playlist_id: int = 0, music_id: int = 0) -> bool | None:
        exists = False
        query = "SELECT * FROM playlist_music WHERE playlist_id = ? AND music_id = ?"
        params = (playlist_id, music_id)
        with self.conexion:
            try:
                cursor = self.conexion.cursor()
                cursor.execute(query, params)
                data = cursor.fetchall()
                if data:
                    exists = True
            except:
                exists = None
            finally:
                return exists        
                
         
    def add_music_to_playlist(self, playlist_id: int, music_id: int) -> bool | None:
        exists_conecction = self.exists_connection_m_t_p(playlist_id=playlist_id, music_id=music_id)
        if exists_conecction == None:
            return None
        elif exists_conecction == True:
            return False
        
        query = "INSERT INTO playlist_music(playlist_id, music_id) VALUES (?, ?);"
        params = (playlist_id, music_id)
        complete = False
        with self.conexion:
            try:
                cursor = self.conexion.cursor()
                cursor.execute(query, params)
                complete = True
            except Exception as e:
                print("No se logró asociar la canción a la playlist")
                print(e)
                complete = None
            finally:
                return complete
    
    def remove_music_of_playlist(self, playlist_id: int = 0, music_id: int = 0) -> bool | None:
        exists_connection = self.exists_connection_m_t_p(playlist_id=playlist_id, music_id=music_id)
        if exists_connection == None:
            return None
        elif exists_connection == False:
            return False

        query = "DELETE FROM playlist_music WHERE playlist_id = ? AND music_id = ?"
        params = (playlist_id, music_id)
        complete = False
        with self.conexion:
            try:
                cursor = self.conexion.cursor()
                cursor.execute(query, params)
                complete = True
            except:
                complete = None
            finally:
                return complete
    
    def get_musics_playlist(self, id: int = 0) -> ListModels:
        response = ListModels()
        if id:
            query = "SELECT * FROM musics JOIN playlist_music ON musics.id = playlist_music.music_id WHERE playlist_music.playlist_id = ?"
            params = (id,)
        
        if query:
            response = self.query_musics(query=query, params=params)
        
        return response
            
                
            
        