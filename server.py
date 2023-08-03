# see https://modal.com/docs/guide/webhooks
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from modal import Secret, Stub, web_endpoint
import json

auth_scheme = HTTPBearer()

stub = Stub("wandb-hook")
class Event(BaseModel):
    event_type: str
    event_author: str
    alias: str
    artifact_version: str
    artifact_version_string: str
    artifact_collection_name: str
    project_name: str
    entity_name: str


@stub.function(secret=Secret.from_name("my-random-secret"))
@web_endpoint(method="POST")
async def f(event: Event, token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    import os
    print(f'wandb payload:\n{event.event_type=}\n{event.event_author=}\n{event.alias=}\n{event.artifact_version=}\n{event.artifact_version_string=}\n{event.artifact_collection_name=}\n{event.project_name=}\n{event.entity_name=}')
    if token.credentials != os.environ["AUTH_TOKEN"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect bearer token",
            headers={"WWW-Authenticate": "Bearer"},
            )
    return {"message": "Event processed successfully"}
