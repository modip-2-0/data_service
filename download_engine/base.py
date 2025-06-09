from abc import ABC, abstractmethod
from typing import Any, List

class RemoteRepository(ABC):
    """
    Interfaz abstracta para cualquier repositorio remoto de datos (PubChem, ChEMBL, etc).
    """

    @abstractmethod
    async def search(self, query: str) -> List[Any]:
        """
        Busca recursos en el repositorio remoto según la consulta.
        """
        pass

    @abstractmethod
    async def download(self, identifier: Any) -> dict:
        """
        Descarga un recurso específico dado su identificador.
        """
        pass

class DownloadManager:
    """
    Clase gestora de descargas desacoplada del repositorio remoto.
    """

    def __init__(self, repository: RemoteRepository):
        self.repository = repository

    async def download_by_query(self, query: str) -> List[dict]:
        """
        Busca y descarga todos los recursos asociados a una consulta.
        """
        results = []
        ids = await self.repository.search(query)
        for identifier in ids:
            data = await self.repository.download(identifier)
            results.append(data)
        return results

# Ejemplo de implementación concreta para PubChem
class PubChemRepository(RemoteRepository):
    async def search(self, query: str) -> List[int]:
        from download_engine.entrez import search_bioassays
        return await search_bioassays(query)

    async def download(self, aid: int) -> dict:
        from download_engine.bioassay import download_bioassay
        # Aquí podrías adaptar para devolver el dict adecuado
        return await download_bioassay(None, aid)  # Pasa el db adecuado en uso real

# Uso:
# repo = PubChemRepository()
# manager = DownloadManager(repo)
# await manager.download_by_query("cancer")