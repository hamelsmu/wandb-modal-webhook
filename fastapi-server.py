from fastapi import Depends, HTTPException, status, FastAPI
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

auth_scheme = HTTPBearer()
app = FastAPI()

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

    def print_payload(self):
        msg = 'Payload:\n========\n'
        for k,v in self.model_dump().items():
            msg += f'{k}={v}\n'
        return msg

@app.post("/")
def webhook(event: Event, 
            token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    "Receive the webhook and print the payload.  Uses a token to authenticate."
    print(event.print_payload())
    if token.credentials != 'secret-random-token':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect bearer token",
            headers={"WWW-Authenticate": "Bearer"},
            )
    return {"message": "Event processed successfully"}
