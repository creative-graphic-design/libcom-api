from fastapi import FastAPI, Response

from libcom_api.routers import gather_routers

app = FastAPI()


def include_routers(app: FastAPI) -> None:
    for router in gather_routers():
        app.include_router(router)


include_routers(app)


@app.get("/health")
def health() -> Response:
    return Response(content="OK", status_code=200)
