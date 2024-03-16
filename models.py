from typing import Union
from pydantic import BaseModel, ConfigDict

class Music(BaseModel):
    id: int
    name: str
    author: str
    duration: str
    path: str
    
class Playlist(BaseModel):
    id: int
    name: str
    
class ResData(BaseModel):
    command_received: str
    message: str = ""
    response: Union[dict|list|bool] = {}

class ListModels():
    def __init__(self) -> None:
        self.list_models = []
        self.is_exception = False
    
    def add(self, model: BaseModel):
        self.list_models.append(model)
    
    def get(self):
        return self.list_models
    
    def len(self):
        return len(self.list_models)
    
    def get_models_dump(self):
        list_models_dump = []
        if self.list_models:
            for model in self.list_models:
                list_models_dump.append(model.model_dump())
        return list_models_dump
    
    def set_as_exception(self):
        self.is_exception = True