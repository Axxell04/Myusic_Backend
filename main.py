import threading
import sqlite3
import json
import os
import sys
import signal

from pydantic import BaseModel
from typing import Union

import uvicorn
from fastapi import FastAPI, HTTPException, Request, WebSocket
from fastapi.websockets import WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse

# from .modulos.descargas import Core as Downloader
import config
from models import ResData
from modulos.descargas import Core as Downloader
from db import DB_Manager

db_manager = DB_Manager()

app = FastAPI()

inst_downloader = Downloader()

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


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    global webSocket_connection, db_manager
    await websocket.accept()
    webSocket_connection = websocket
    try:
        while True:
            rec = await websocket.receive()
            rec_data = json.loads(rec["text"])
            
            #Parametros de entrada
            command = rec_data.get("command", "")
            content= rec_data.get("content", "")
            
            #Modelo de respuesta
            res_data = ResData(command_received=command)
            message = ""
            response = {}

            if "download" == command:
                try:
                    res_download = inst_downloader.descargar(link=content)        
                except:
                    pass
                
                if res_download['success']:
                    message = res_download['message']
                    response = res_download['data']
                else:
                    message = res_download['message']
                    response = res_download['data']                    
                
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
                    
            elif "delete_music" == command:
                if "id" in content:
                    check = db_manager.delete_musics(id=content["id"])
                        
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
            
            elif "add_music_to_playlist"  == command:
                if "music_id" in content and "playlist_id" in content:
                    complete = db_manager.add_music_to_playlist(playlist_id=content["playlist_id"], music_id=content["music_id"])
                
                if complete:
                    message = "Success"
                elif complete == False:
                    message = "The music is already in the playlist"
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
                if "playlist_id" in content and "music_id" in content:
                    complete = db_manager.remove_music_of_playlist(playlist_id=content["playlist_id"], music_id=content["music_id"])

                    if complete:
                        message = "Success"
                    elif complete == False:
                        message = "Connection not found"
                    else:
                        message = "Delete error"
                    
            else:
                message = "Command not exists"
                response = {}
                
            res_data.message = message
            res_data.response = response    
            
            await websocket.send_json(res_data.model_dump())
        
    except Exception as e:
        print(f"Cliente desconectado: {e}")
        
        
if __name__ == "__main__":
    uvicorn.run(app, host=config.IP_SERVER, port=8000)
    