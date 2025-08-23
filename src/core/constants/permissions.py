from enum import Enum
from typing import Dict, List, Optional

class BasePermissionEnum(str, Enum):

    def __new__(cls, value, description):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

    @classmethod
    def keys(cls):
        return list(cls.__members__.keys())

    @classmethod
    def values(cls):
        return [member.value for member in cls]

    @classmethod
    def descriptions(cls):
        return [member.description for member in cls]
    
    @classmethod
    def values_and_descriptions(cls):
        return [{"name": member.value, "description": member.description} for member in cls]
    
    @classmethod
    def list_only_values(cls, only: Optional[List[str]] = None):
        if only:
            return [
                member.value
                for name, member in cls.__members__.items()
                if any(filter_value.upper() in name for filter_value in only)
            ]
        return cls.values()
    
    @classmethod
    def list_except_values(cls, except_: Optional[List[str]] = None):
        if except_:
            return [
                member.value
                for name, member in cls.__members__.items()
                if all(filter_value.upper() not in name for filter_value in except_)
            ]
        return cls.values()
    
    @classmethod
    def permission_and_description_as_dict(cls) -> Dict[str, str]:
        return {member.value: member.description for member in cls}

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)
