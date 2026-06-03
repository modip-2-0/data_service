import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from api.dependencies import AsyncMongoDB
from crud.target import create_target_doc, get_target_by_id, get_targets_by_user, delete_all_targets

router = APIRouter(prefix="/target", tags=["Targets"])

# ================== CONFIGURACIÓN DE ALMACENAMIENTO ==================
STORAGE_BASE = os.getenv("STORAGE_PATH", "./storage")
TARGETS_DIR = os.path.join(STORAGE_BASE, "targets")
BOXES_DIR   = os.path.join(STORAGE_BASE, "boxes")

os.makedirs(TARGETS_DIR, exist_ok=True)
os.makedirs(BOXES_DIR, exist_ok=True)

def save_upload_file(upload_file: UploadFile, destination_dir: str) -> str:
    """Guarda un archivo subido con nombre único y retorna la ruta completa."""
    ext = os.path.splitext(upload_file.filename)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(destination_dir, unique_name)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path
# ====================================================================

@router.post("/create", status_code=201)
async def create_target(
    db: AsyncMongoDB,
    name: str = Form(...),
    receptor: str = Form(...),
    user: str = Form(...),
    pdbqt_file: UploadFile = File(...),
    config_file: UploadFile = File(...)
):
    """
    Crea un nuevo target:
    - name: nombre descriptivo
    - receptor: organismo (humano, bovino, etc.)
    - user: identificador del usuario (email)
    - pdbqt_file: archivo .pdbqt del receptor
    - config_file: archivo de configuración de docking (por ejemplo, la caja)
    """
    # Validación opcional de extensión
    if not pdbqt_file.filename.endswith('.pdbqt'):
        raise HTTPException(status_code=400, detail="pdbqt_file must have .pdbqt extension")

    # Guardar archivos
    try:
        pdbqt_path = save_upload_file(pdbqt_file, TARGETS_DIR)
        config_path = save_upload_file(config_file, BOXES_DIR)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload error: {str(e)}")

    # Preparar documento para MongoDB
    doc = {
        "name": name,
        "receptor": receptor,
        "user": user,
        "pdbqt_path": pdbqt_path,
        "config_path": config_path
    }

    # Guardar en DB (si falla, borrar archivos para no dejar basura)
    try:
        target_db = await create_target_doc(db, doc)
        return target_db
    except HTTPException:
        os.unlink(pdbqt_path) if os.path.exists(pdbqt_path) else None
        os.unlink(config_path) if os.path.exists(config_path) else None
        raise

@router.get("/{target_id}")
async def get_target(db: AsyncMongoDB, target_id: str):
    return await get_target_by_id(db, target_id)

@router.get("/user/{username}")
async def list_user_targets(db: AsyncMongoDB, username: str):
    return await get_targets_by_user(db, username)

@router.delete("/drop")
async def drop_all(db: AsyncMongoDB):
    return await delete_all_targets(db)