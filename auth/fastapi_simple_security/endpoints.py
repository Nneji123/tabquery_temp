"""Endpoints defined by the dependency.
"""
import os
from typing import List, Optional
import bcrypt

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from fastapi_simple_security._security_secret import secret_based_security
from fastapi_simple_security._sqlite_access import sqlite_access

api_key_router = APIRouter()

show_endpoints = "FASTAPI_SIMPLE_SECURITY_HIDE_DOCS" not in os.environ


def hash_password(password: str) -> str:
    if password is not None:
        try:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(str(password).encode("utf-8"), salt)
            return hashed.decode("utf-8")
        except Exception as e:
            print(e)
    else:
        return "Invalid Password entered"


@api_key_router.get(
    "/new",
    dependencies=[Depends(secret_based_security)],
    include_in_schema=show_endpoints,
)
def get_new_api_key(
    name: str = Query(
        None,
        description="set API key name",
    ),
    email: str = Query(
        None,
        description="set API key email",
    ),
    password: str = Query(
        None,
        description="set API key password",
    ),
    never_expires: bool = Query(
        False,
        description="if set, the created API key will never be considered expired",
    ),
) -> str:
    """
    Returns:
        api_key: a newly generated API key
    """
    if password is not None:
        password = hash_password(password)
    return sqlite_access.create_key(name, email, password, never_expires)


@api_key_router.get(
    "/revoke",
    dependencies=[Depends(secret_based_security)],
    include_in_schema=show_endpoints,
)
def revoke_api_key(
    api_key: str = Query(..., alias="api-key", description="the api_key to revoke")
):
    """
    Revokes the usage of the given API key

    """
    return sqlite_access.revoke_key(api_key)


@api_key_router.get(
    "/renew",
    dependencies=[Depends(secret_based_security)],
    include_in_schema=show_endpoints,
)
def renew_api_key(
    api_key: str = Query(..., alias="api-key", description="the API key to renew"),
    expiration_date: str = Query(
        None,
        alias="expiration-date",
        description="the new expiration date in ISO format",
    ),
):
    """
    Renews the chosen API key, reactivating it if it was revoked.
    """
    return sqlite_access.renew_key(api_key, expiration_date)


class UsageLog(BaseModel):
    api_key: str
    name: Optional[str]
    is_active: bool
    never_expire: bool
    expiration_date: str
    latest_query_date: Optional[str]
    total_queries: int


class UsageLogs(BaseModel):
    logs: List[UsageLog]


@api_key_router.get(
    "/logs",
    dependencies=[Depends(secret_based_security)],
    response_model=UsageLogs,
    include_in_schema=show_endpoints,
)
def get_api_key_usage_logs():
    """
    Returns usage information for all API keys
    """
    # TODO Add some sort of filtering on older keys/unused keys?

    return UsageLogs(
        logs=[
            UsageLog(
                api_key=row[0],
                is_active=row[1],
                never_expire=row[2],
                expiration_date=row[3],
                latest_query_date=row[4],
                total_queries=row[5],
                name=row[6],
            )
            for row in sqlite_access.get_usage_stats()
        ]
    )
