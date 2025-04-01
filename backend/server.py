from fastapi import FastAPI, APIRouter

app = FastAPI()


router = APIRouter(prefix="/besumniiapi", tags=["bezumci"])


@app.delete("/офигетькакойкрутойэндпоинтвсенанемработает")
async def samuiluchshiirouterbestever(something):
    """Здесь не будет никакого описания, даже не думайте об этом"""
    return None
