from typing import TypeVar


class ServiceInterface:
    name: str

    @classmethod
    def get_instance(cls, service_pool) -> "SubtypeOfServiceInterface":
        return getattr(service_pool, cls.name)


SubtypeOfServiceInterface = TypeVar('SubtypeOfServiceInterface', bound=ServiceInterface)
