from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# MODEL
# ---------------------------
class Producto(BaseModel):
    nombre: str
    precio: float

# "Base de datos" temporal en memoria
productos = [
    {"id": 1, "nombre": "Camiseta Negra", "precio": 15000},
    {"id": 2, "nombre": "Pantalón Gris", "precio": 25000},
]

# ---------------------------
# CRUD
# ---------------------------

# LISTAR todos
@app.get("/productos")
def obtener_productos():
    return productos

# OBTENER por ID
@app.get("/productos/{id}")
def obtener_producto(id: int):
    for p in productos:
        if p["id"] == id:
            return p
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# CREAR producto
@app.post("/productos")
def crear_producto(prod: Producto):
    nuevo_id = productos[-1]["id"] + 1 if productos else 1
    nuevo = {"id": nuevo_id, **prod.dict()}
    productos.append(nuevo)
    return {"mensaje": "Producto creado", "producto": nuevo}

# EDITAR producto
@app.put("/productos/{id}")
def editar_producto(id: int, prod: Producto):
    for p in productos:
        if p["id"] == id:
            p.update(prod.dict())
            return {"mensaje": "Producto actualizado", "producto": p}
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# ELIMINAR producto
@app.delete("/productos/{id}")
def eliminar_producto(id: int):
    for p in productos:
        if p["id"] == id:
            productos.remove(p)
            return {"mensaje": "Producto eliminado"}
    raise HTTPException(status_code=404, detail="Producto no encontrado")
