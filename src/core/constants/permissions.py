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

class PermissionPermissions(BasePermissionEnum):
    CAN_CREATE_PERMISSION = ("can_create_permission", "Permission to create a permission")
    CAN_VIEW_PERMISSIONS = ("can_view_permissions", "Permission to view all permissions")
    CAN_UPDATE_PERMISSION = ("can_update_permission", "Permission to update a permission")
    CAN_DELETE_PERMISSION = ("can_delete_permission", "Permission to delete a permission")

class ProfilePermissions(BasePermissionEnum):
    CAN_CREATE_PROFILE = ("can_create_profile", "Permission to create a profile")
    CAN_VIEW_PROFILES = ("can_view_profiles", "Permission to view all profiles")
    CAN_UPDATE_PROFILE = ("can_update_profile", "Permission to update a profile")
    CAN_DELETE_PROFILE = ("can_delete_profile", "Permission to delete a profile")

class ProfilePermissionPermissions(BasePermissionEnum):
    CAN_CREATE_PROFILE_PERMISSION = ("can_create_profile_permission", "Permission to create a profile permission")
    CAN_VIEW_PROFILE_PERMISSIONS = ("can_view_profile_permissions", "Permission to view all profile permissions")
    CAN_UPDATE_PROFILE_PERMISSION = ("can_update_profile_permission", "Permission to update a profile permission")
    CAN_DELETE_PROFILE_PERMISSION = ("can_delete_profile_permission", "Permission to delete a profile permission")

class UserPermissions(BasePermissionEnum):
    CAN_CREATE_USER = ("can_create_user", "Permission to create a user")
    CAN_VIEW_USERS = ("can_view_users", "Permission to view all users")
    CAN_UPDATE_USER = ("can_update_user", "Permission to update a user")
    CAN_DELETE_USER = ("can_delete_user", "Permission to delete a user")

class UserProfilePermissions(BasePermissionEnum):
    CAN_CREATE_USER_PROFILE = ("can_create_user_profile", "Permission to create a user profile")
    CAN_VIEW_USER_PROFILES = ("can_view_user_profiles", "Permission to view all user profiles")
    CAN_UPDATE_USER_PROFILE = ("can_update_user_profile", "Permission to update a user profile")
    CAN_DELETE_USER_PROFILE = ("can_delete_user_profile", "Permission to delete a user profile")

class CustomerPermissions(BasePermissionEnum):
    CAN_CREATE_CUSTOMER = ("can_create_customer", "Permission to create a customer")
    CAN_VIEW_CUSTOMERS = ("can_view_customers", "Permission to view all customers")
    CAN_UPDATE_CUSTOMER = ("can_update_customer", "Permission to update a customer")
    CAN_DELETE_CUSTOMER = ("can_delete_customer", "Permission to delete a customer")

class PersonPermissions(BasePermissionEnum):
    CAN_CREATE_PERSON = ("can_create_person", "Permission to create a person")
    CAN_VIEW_PERSONS = ("can_view_persons", "Permission to view all persons")
    CAN_UPDATE_PERSON = ("can_update_person", "Permission to update a person")
    CAN_DELETE_PERSON = ("can_delete_person", "Permission to delete a person")

class VideoPermissions(BasePermissionEnum):
    CAN_SEND_VIDEO = ("can_send_video", "Permission to send a video")
    CAN_VIEW_VIDEO = ("can_list_video", "Permission to list videos")
    CAN_DELETE_VIDEO = ("can_delete_video", "Permission to delete a video")

class ZipPermissions(BasePermissionEnum):
    CAN_DOWNLOAD_ZIP = ("can_download_zip", "Permission to download a zip file")
    CAN_VIEW_ZIPS = ("can_view_zips", "Permission to list contents of a zip file")
