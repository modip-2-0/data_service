import logging
import os
from fastapi import HTTPException
import pubchempy as pcp

from core.db import AsyncIOMotorClient
from crud.compound import CompoundIn, CompoundDB, create_compound

STORAGE_BASE = os.getenv("STORAGE_PATH", "./storage") 

async def download_compound(db: AsyncIOMotorClient, cid: int) -> CompoundDB:


    logging.info(f"Downloading compound CID={cid} from PubChem...")


    base_dir = os.path.join(STORAGE_BASE, "compounds")
    two_d_dir = os.path.join(base_dir, "2D")
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(two_d_dir, exist_ok=True)
    
    file_name = f"{cid}.sdf"
    path_3d = os.path.join(base_dir, file_name)       # Ruta si es 3D
    path_2d = os.path.join(two_d_dir, file_name)       # Ruta si es 2D


    try:
        compound = pcp.Compound.from_cid(cid)  
    except Exception as e:
        logging.error(f"Failed to fetch metadata for CID {cid}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Compound CID={cid} not found in PubChem")
    

    try:

        pcp.download('SDF', path_3d, identifier=cid, record_type='3d', overwrite=True)
        file_path = path_3d
        coordinate_type = "3D"

        logging.info(f"Successfully downloaded (3D) for CID {cid} to {path_3d}")
    except pcp.NotFoundError as e:

        logging.info(f"3D structure not available for CID {cid}. Downloading 2D.")
        try:
            pcp.download('SDF', path_2d, identifier=cid, overwrite=True)
            file_path = path_2d
            coordinate_type = "2D"
            logging.info(f"Successfully downloaded (2D) for CID {cid} to {path_2d}")
        except Exception as e2:
            logging.error(f"Failed to download 2D SDF for CID {cid}: {str(e2)}")
            raise HTTPException(status_code=500, detail="Error downloading compound file")
    except Exception as e:
        # Otro error inesperado
        logging.error(f"Unexpected error downloading CID {cid}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error downloading compound")
    
    # # --- 4. Validación extra: Verificar si realmente el archivo contiene coordenadas 3D ---
    # #    A veces PubChem devuelve un 3D con coordenadas en X, Y, pero Z = 0.0000 
    # #    (es decir, una estructura 2D disfrazada).
    # #    Si se descargó en la ruta 3D, se comprueba que tenga las tres coordenadas no nulas.
    # #    Si no las tiene, se mueve a la carpeta 2D.
    # if os.path.exists(path_3d):
    #     has_3d = False
    #     with open(path_3d, 'r') as f:
    #         # Leer primeras líneas; buscar bloque de coordenadas
    #         lines = f.readlines()
    #         # El bloque de átomos suele estar después de "M  END"
    #         atom_block = False
    #         for line in lines:
    #             if "M  END" in line:
    #                 break
    #             if atom_block:
    #                 parts = line.split()
    #                 if len(parts) >= 6 and parts[0].isdigit():
    #                     # Formato: "atom_number x y z element ..."
    #                     try:
    #                         z = float(parts[4])
    #                         if z != 0.0:
    #                             has_3d = True
    #                             break
    #                     except:
    #                         pass
    #             if line.startswith("M  END"):
    #                 atom_block = True
        
    #     if not has_3d:
    #         # Es una estructura 2D. Movemos el archivo a la carpeta 2D.
    #         import shutil
    #         os.rename(path_3d, path_2d)
    #         logging.info(f"Moved (non-3D) file for CID {cid} to 2D folder.")
    #         file_path = path_2d
    #         coordinate_type = "2D"
    #     else:
    #         file_path = path_3d
    #         coordinate_type = "3D"
    # else:
    #     # Si solo se descargó la versión 2D
    #     file_path = path_2d
    #     coordinate_type = "2D"


    # Build dictionary of fields for create_compound
    compound_dict = {
        "cid": compound.cid,
        "path": file_path,
        "iupac_name": compound.iupac_name,
        "coordinate_type": coordinate_type,
        "elements": compound.elements,
        "molecular_formula": compound.molecular_formula,
        "charge": compound.charge,
        "connectivity_smiles": compound.connectivity_smiles,
        "smiles": compound.smiles,
        "inchi": compound.inchi,
        "inchikey": compound.inchikey,
        "molecular_weight": compound.molecular_weight,
        "exact_mass": compound.exact_mass,
        "monoisotopic_mass": compound.monoisotopic_mass,
        "xlogp": compound.xlogp,
        "tpsa": compound.tpsa,
        "complexity": compound.complexity,
        "h_bond_donor_count": compound.h_bond_donor_count,
        "h_bond_acceptor_count": compound.h_bond_acceptor_count,
        "rotatable_bond_count": compound.rotatable_bond_count,
        "heavy_atom_count": compound.heavy_atom_count,
        "isotope_atom_count": compound.isotope_atom_count,
        "atom_stereo_count": compound.atom_stereo_count,
        "defined_atom_stereo_count": compound.defined_atom_stereo_count,
        "undefined_atom_stereo_count": compound.undefined_atom_stereo_count,
        "covalent_unit_count": compound.covalent_unit_count,
        "volume_3d": compound.volume_3d,
        "pharmacophore_features_3d": compound.pharmacophore_features_3d,
    }

    # Insert into database using the generic create_compound
    return await create_compound(db, CompoundIn(**compound_dict))
