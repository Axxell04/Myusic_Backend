import threading
import asyncio
import sqlite3
import json
import os
import sys
import signal

from pydantic import BaseModel
from typing import Union

import uvicorn
from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from asyncio import TimeoutError

# from .modulos.descargas import Core as Downloader
import config
from models import ResData
from modulos.descargas import Core as Downloader
from db import DB_Manager

class Ws_Manager():
    def __init__(self) -> None:
        self.connections = {}
    
    async def add_connection(self, host: str, websocket: WebSocket):
        if host in self.connections:
            connection = self.connections.pop(host)
            try:
                await connection.close()
            except:
                pass
            
        self.connections.update({host: websocket})
        print(f"Cliente conectado: {websocket.client}")
        print(f"Clientes actuales: {self.get_connections()}")
        
    def get_connections(self) -> dict:
        return self.connections
    
    async def remove_connection(self, host: str):
        if host in self.connections:
            connection = self.connections.pop(host)
            try:
                await connection.close()
            except:
                pass
            print(f"Cliente desconectado: {connection.client}")
            print(f"Clientes actuales: {self.get_connections()}")
            
ws_Manager = Ws_Manager()            

db_manager = DB_Manager()

app = FastAPI()

origins = {
    "http://localhost:5173",
    "*"
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

webSocket_connection = None

@app.get("/off")
async def off():
    os.kill(os.getpid(), signal.SIGTERM)
    
    return {"message": "Servidor apagado"}


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
    <head>
    <title>Mi página web</title>
    </head>
    <body>
    <h1>Hola mundo</h1>
    </body>
    </html>
    """

@app.get("/download/{id}")
def download(id: int):
    db = DB_Manager()
    data = db.get_musics(id=id)
    print(data)
    if data:
        file_path = os.path.join(config.MAIN_PATH, data.get()[0].path)
        file_name = f"{data.get()[0].name}.mp3"
        try:
            return FileResponse(file_path, filename=file_name)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="File not found")
    return {"message": "Registro no encontrado"}

@app.get("/get_musics/")
def get_musics(value_search: str = ''):
    db = DB_Manager()
    musics = []
    if value_search:
        res_author = db.get_musics(author=value_search).get_models_dump()
        res_name = db.get_musics(name=value_search).get_models_dump() 
        musics.extend(res_name)
        musics.extend([music for music in res_author if music not in res_name])
    else:
        musics = db.get_musics(all=True).get_models_dump()

    return musics


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    global ws_Manager, db_manager
    await websocket.accept()
    host = websocket.client.host
    await ws_Manager.add_connection(host, websocket)

    try:
        while True:
            try:
                rec = await websocket.receive()
                print(f"REC: {rec}")
                if "text" in rec:
                    rec_data = json.loads(rec["text"])
                else:
                    # await websocket.close()
                    return None
                    # break
                print(rec_data)
                
                #Parametros de entrada
                command = rec_data.get("command", "")
                content= rec_data.get("content", "")
                
                #Modelo de respuesta
                res_data = ResData(command_received=command)
                message = ""
                response = {}

                if "download" == command:
                    async def download():
                        res_data_thread = ResData(command_received="download")
                        message_thread = ""
                        response_thread = {}
                        inst_downloader = Downloader()
                        try:
                            res_download = inst_downloader.descargar(link=content)        
                        except:
                            pass
                        finally:
                            inst_downloader.close()
                        
                        if res_download['success']:
                            message_thread = res_download['message']
                            response_thread = res_download['data']
                        else:
                            message_thread = res_download['message']
                            response_thread = res_download['data']
                        
                        res_data_thread.message = message_thread
                        res_data_thread.response = response_thread
                        
                        await websocket.send_json(res_data_thread.model_dump())   
                                    
                    def run_download():
                        asyncio.run(download())
                        # await download()
                    thread_download = threading.Thread(target=run_download, daemon=True)
                    thread_download.start()
                    #command = ""
                    res_data.command_received = ""
                    
                    
                elif "get_musics" == command:
                    if 'all' in content:
                        response = db_manager.get_musics(all=True).get_models_dump()
                    elif "author" in content:
                        response = db_manager.get_musics(author=content["author"]).get_models_dump()
                    elif "name" in content:
                        response = db_manager.get_musics(name=content["name"]).get_models_dump()
                    elif "id" in content:
                        response = db_manager.get_musics(id=content["id"]).get_models_dump()
                    
                    if response:
                        message = "Success"
                    else:
                        message = "Musics not found"
                        
                elif "delete_musics" == command:
                    if "id_list" in content:
                        check = db_manager.delete_musics(musics_id=content["id_list"])
                            
                    elif "all" in content:
                        check = db_manager.delete_musics(all=True)
                    
                    if check:
                        message = "Delete Success"
                    else:
                        message = "Delete Error"
                
                elif "create_playlist" == command:
                    if "name" in content:
                        valid = db_manager.validate_new_playlist(name=content["name"])
                        if valid == 0:
                            response = {"id": db_manager.add_playlist(name=content["name"])}
                        elif valid > 0:
                            response = {"id": valid}
                        else:
                            message = "Failed validation"
                    
                    if response:
                        if valid == 0:
                            message = "Success"
                        else:
                            message = "Playlist already created"
                    else:
                        if message:
                            message = f"Error creating playlist | {message}"
                        else:
                            message = "Error creating playlist"
                            
                elif "get_playlists" == command:
                    if "all" in content:
                        response = db_manager.get_playlists(all=True).get_models_dump()
                    elif "id" in content:
                        response = db_manager.get_playlists(id=content["id"]).get_models_dump()
                    elif "name" in content:
                        response = db_manager.get_playlists(name=content["name"]).get_models_dump()
                        
                    if response:
                        message = "Success"
                    else:
                        message = "Playlists not found"
                
                elif "delete_playlist" == command:
                    if "id" in content:
                        complete = db_manager.delete_playlists(id=content["id"])
                        if complete:
                            message = "Success"
                        elif complete == False:
                            message = "Playlist not found"
                        elif complete == None:
                            message = "Delete error"
                
                elif "add_musics_to_playlist"  == command:
                    if "musics_id" in content and "playlist_id" in content:
                        complete = db_manager.add_musics_to_playlist(playlist_id=content["playlist_id"], musics_id=content["musics_id"])
                    
                        if complete:
                            message = "Success"
                            pls_updated = db_manager.get_musics_playlist(id=content["playlist_id"]).get_models_dump()
                            response = {
                                "id": content["playlist_id"],
                                "pls_updated": pls_updated
                            }
                        elif complete == False:
                            # message = "The music is already in the playlist"
                            message = "Error adding music"
                        else:
                            message = "Error adding music"
                
                elif "get_musics_of_playlist" == command:
                    if "id" in content:
                        response = db_manager.get_musics_playlist(id=content["id"]).get_models_dump()
                    
                    if response:
                        message = "Success"
                    else:
                        message = "Musics not found"
                
                elif "remove_music_of_playlist" == command:
                    if "playlist_id" in content and "musics_id" in content:
                        if content["playlist_id"] == 0:
                            complete = db_manager.delete_musics(musics_id=content["musics_id"])
                        else:
                            complete = db_manager.remove_music_of_playlist(playlist_id=content["playlist_id"], musics_id=content["musics_id"])

                        if complete:
                            message = "Success"
                            pls_updated = []
                            if content["playlist_id"] != 0:
                                pls_updated = db_manager.get_musics_playlist(id=content["playlist_id"]).get_models_dump()
                            else:
                                pls_updated = db_manager.get_musics(all=True).get_models_dump()
                                
                            response = {
                                "id": content["playlist_id"],
                                "pls_updated": pls_updated
                            }
                        elif complete == False:
                            # message = "Connection not found"
                            message = "Delete error"
                        else:
                            message = "Delete error"
                
                elif not command:
                    pass
                else:
                    message = "Command not exists"
                    response = {}
                    
                res_data.message = message
                res_data.response = response    
                
                await websocket.send_json(res_data.model_dump())
            except TimeoutError:
                print("Tiempo de espera agotado")
    except WebSocketDisconnect as e:
        print(f"Error: {e}")
    # finally:
    #     await ws_Manager.remove_connection(host) 
        
        
        
if __name__ == "__main__":
    uvicorn.run(app, host=config.IP_SERVER, port=8000)
    