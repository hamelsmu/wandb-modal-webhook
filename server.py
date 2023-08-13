# see https://modal.com/docs/guide/webhooks
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from modal import Secret, Stub, Image, web_endpoint

auth_scheme = HTTPBearer()
img = Image.debian_slim().pip_install("fastapi==0.101.0", "pydantic==2.1.1")

stub = Stub("wandb-hook")
class Event(BaseModel):
    "Defines the payload your webhook will send."
    event_type: str
    event_author: str
    alias: str
    artifact_version: str
    artifact_version_string: str
    artifact_collection_name: str
    project_name: str
    entity_name: str

    def __str__(self):
        msg = 'Payload:\n========\n'
        for k,v in self.model_dump().items():
            msg += f'{k}={v}\n'
        return msg

@stub.function(secret=Secret.from_name("my-random-secret"), image=img)
@web_endpoint(method="POST")
async def f(event: Event, token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    import os

    print(event)
    if token.credentials != os.environ["AUTH_TOKEN"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect bearer token",
            headers={"WWW-Authenticate": "Bearer"},
            )
    return {"message": "Event processed successfully"}
