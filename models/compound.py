from pydantic import BaseModel, Field
from typing import Optional, List

from models.mongo import MongoModel


class CompoundIn(BaseModel):
    """
    Input model for a chemical compound submitted by a user.
    All fields are optional, as the user may provide only known properties.
    The API will automatically assign a local file path (if files are uploaded/created)
    and will never request a PubChem CID (that is reserved for downloads).
    """
    cid: Optional[int] = None   
    path: Optional[str] = None  
    # Basic info
    iupac_name: Optional[str] = Field(None, description="Preferred IUPAC name")
    coordinate_type: Optional[str] = Field(None, description="2D or 3D coordinate type")

    # Composition and formula
    elements: Optional[List[str]] = Field(None, description="List of element symbols")
    molecular_formula: Optional[str] = Field(None, description="Molecular formula, e.g., C9H8O4")
    charge: Optional[int] = Field(None, description="Formal charge")

    # Linear representations
    connectivity_smiles: Optional[str] = Field(None, description="Canonical SMILES without stereochemistry")
    smiles: Optional[str] = Field(None, description="Isomeric and canonical SMILES (full)")
    inchi: Optional[str] = Field(None, description="Standard InChI")
    inchikey: Optional[str] = Field(None, description="InChIKey (hashed version)")

    # Physicochemical properties
    molecular_weight: Optional[float] = Field(None, description="Molecular weight in g/mol")
    exact_mass: Optional[float] = Field(None, description="Exact mass in Da")
    monoisotopic_mass: Optional[float] = Field(None, description="Monoisotopic mass in Da")
    xlogp: Optional[float] = Field(None, description="XLogP octanol-water partition coefficient")
    tpsa: Optional[float] = Field(None, description="Topological Polar Surface Area (Å²)")
    complexity: Optional[float] = Field(None, description="Molecular complexity rating")

    # Structural counts
    h_bond_donor_count: Optional[int] = Field(None, description="Number of hydrogen‑bond donors")
    h_bond_acceptor_count: Optional[int] = Field(None, description="Number of hydrogen‑bond acceptors")
    rotatable_bond_count: Optional[int] = Field(None, description="Number of rotatable bonds")
    heavy_atom_count: Optional[int] = Field(None, description="Number of non‑hydrogen atoms")
    isotope_atom_count: Optional[int] = Field(None, description="Number of isotopically enriched atoms")

    # Stereochemistry (atoms)
    atom_stereo_count: Optional[int] = Field(None, description="Total tetrahedral stereocenters")
    defined_atom_stereo_count: Optional[int] = Field(None, description="Stereocenters with defined configuration")
    undefined_atom_stereo_count: Optional[int] = Field(None, description="Stereocenters with undefined configuration")

    # Covalent units
    covalent_unit_count: Optional[int] = Field(None, description="Number of covalently bonded units")

    # Basic 3D properties
    volume_3d: Optional[float] = Field(None, description="Analytic volume of first conformer (Å³)")
    pharmacophore_features_3d: Optional[List[str]] = Field(None, description="List of 3D pharmacophore features")

    class Config:
        """OpenAPI example for a typical user‑submitted compound (Aspirin)"""
        json_schema_extra = {
            "example": {
                "iupac_name": "2-acetyloxybenzoic acid",
                "molecular_formula": "C9H8O4",
                "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
                "inchi": "InChI=1S/C9H8O4/c1-6(10)13-8-5-3-2-4-7(8)9(11)12/h2-5H,1H3,(H,11,12)",
                "inchikey": "BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
                "molecular_weight": 180.16,
                "exact_mass": 180.042258,
                "xlogp": 1.2,
                "h_bond_donor_count": 1,
                "h_bond_acceptor_count": 4,
                "rotatable_bond_count": 3
            }
        }
    
    
class CompoundDB(MongoModel):
    """
    MongoDB document model for chemical compounds.
    Supports both PubChem compounds (with cid) and lab compounds (without cid).
    """
    # Identifiers
    cid: Optional[int] = None                     # PubChem CID (None for lab compounds)
    path: Optional[str] = None                    # Local file path if downloaded

    # Basic info
    iupac_name: Optional[str] = None
    coordinate_type: Optional[str] = None

    # Composition and formula
    elements: Optional[List[str]] = None
    molecular_formula: Optional[str] = None
    charge: Optional[int] = None

    # Linear representations
    connectivity_smiles: Optional[str] = None
    smiles: Optional[str] = None
    inchi: Optional[str] = None
    inchikey: Optional[str] = None

    # Physicochemical properties
    molecular_weight: Optional[float] = None
    exact_mass: Optional[float] = None
    monoisotopic_mass: Optional[float] = None
    xlogp: Optional[float] = None
    tpsa: Optional[float] = None
    complexity: Optional[float] = None

    # Structural counts
    h_bond_donor_count: Optional[int] = None
    h_bond_acceptor_count: Optional[int] = None
    rotatable_bond_count: Optional[int] = None
    heavy_atom_count: Optional[int] = None
    isotope_atom_count: Optional[int] = None

    # Atom stereochemistry
    atom_stereo_count: Optional[int] = None
    defined_atom_stereo_count: Optional[int] = None
    undefined_atom_stereo_count: Optional[int] = None

    # Covalent units
    covalent_unit_count: Optional[int] = None

    # Basic 3D properties
    volume_3d: Optional[float] = None
    pharmacophore_features_3d: Optional[List[str]] = None