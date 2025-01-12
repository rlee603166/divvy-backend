from typing import Annotated
import httpx
from twilio.rest import Client as TwilioClient
from supabase import create_client, Client as SupabaseClient
from functools import lru_cache
from fastapi import Depends, Request
from repositories import UserRepository, ReceiptRepository, FriendRepository, GroupRepository
from services import AuthService, UserService, TwilioService, MockTwilioService, ReceiptProcessor, MockAuthService
from config import Settings, get_settings

settings = get_settings()

"""
repositories
"""

@lru_cache()
def get_user_repository() -> UserRepository:
    return UserRepository()

@lru_cache()
def get_receipt_repository() -> ReceiptRepository:
    return ReceiptRepository()

@lru_cache()
def get_friend_repository() -> FriendRepository:
    return FriendRepository()

@lru_cache()
def get_group_repository() -> GroupRepository:
    return GroupRepository()

"""
services
"""

@lru_cache()
def get_auth_service(repo: Annotated[UserRepository, Depends(get_user_repository)]) -> AuthService:
    return AuthService(repository=repo)

@lru_cache()
def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
    auth: Annotated[AuthService, Depends(get_auth_service)],
    friend_repo: Annotated[FriendRepository, Depends(get_friend_repository)]
) -> UserService:
    return UserService(repository=repo, auth=auth, friend_repo=friend_repo)

@lru_cache()
def get_receipt_processor(
    repo: Annotated[ReceiptRepository, Depends(get_receipt_repository)]
) -> ReceiptProcessor:
    return ReceiptProcessor(repository=repo)


ReceiptProcessorDep = Annotated[ReceiptProcessor, Depends(get_receipt_processor)]
UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
FriendRepositoryDep = Annotated[FriendRepository, Depends(get_friend_repository)]
GroupRepositoryDep = Annotated[GroupRepository, Depends(get_group_repository)]
ReceiptRepositoryDep = Annotated[ReceiptRepository, Depends(get_receipt_repository)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]

"""
Third Part Clients
"""

@lru_cache()
def get_supabase_client() -> SupabaseClient:
    return create_client(
        settings.DATABASE_URL,
        settings.SUPABASE_KEY
    )


SupabaseClientDep = Annotated[SupabaseClient, Depends(get_supabase_client)]


@lru_cache()
def get_twilio_client() -> TwilioClient:
    return TwilioClient(
        settings.TWILIO_ASID,
        settings.TWILIO_AUTH_TOKEN
    )


TwilioClientDep = Annotated[TwilioClient, Depends(get_twilio_client)]


def get_twilio_service(
    request: Request,
    repo: Annotated[UserRepository, Depends(get_user_repository)],
    settings: Settings = Depends(get_settings),
):
    return TwilioService(
        repo=repo,
        account_sid=settings.TWILIO_ASID,
        auth_token=settings.TWILIO_AUTH_TOKEN,
        service_id=settings.TWILIO_SERVICE_ID,
        http_client=request.app.state.http_client
    )
    
TwilioServiceDep = Annotated[TwilioService, Depends(get_twilio_service)]


async def get_mock_auth_service() -> MockAuthService:
    return MockAuthService()

MockAuthServiceDep = Annotated[MockAuthService, Depends(get_mock_auth_service)]


async def get_mock_service() -> MockTwilioService:
    return MockTwilioService()


MockTwilioServiceDep = Annotated[MockTwilioService, Depends(get_mock_service)]
