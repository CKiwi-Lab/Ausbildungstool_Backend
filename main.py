from fastapi import FastAPI
# Eine Instanz der FastAPI-App erstellen
app = FastAPI(title="Mein erstes Backend", description="Ein einfaches FastAPI-Projekt")
# Eine einfache GET-Route definieren
@app.get("/")
def read_root():
    return {"message": "Hello World! Dein Backend funktioniert!"}
# Eine weitere Route für Tests (z. B. mit Query-Parametern)
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}