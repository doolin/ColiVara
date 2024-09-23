import base64
import random

import pytest
from ninja.testing import TestAsyncClient

from accounts.models import CustomUser

from .models import Collection
from .views import Bearer, router


# sanity check
async def test_sanity():
    assert 1 == 1


pytestmark = [pytest.mark.django_db]

""" Authentication tests """


@pytest.fixture
async def user(db):
    """
    Fixture to create a test user with a token.
    """
    # get or create a user
    user, _ = await CustomUser.objects.aget_or_create(
        username="test_user", token="valid_token"
    )
    return user


@pytest.fixture
def bearer():
    """
    Fixture to create an instance of the Bearer class.
    """
    return Bearer()


@pytest.fixture
def async_client():
    """
    Fixture to create an instance of the TestAsyncClient class.
    """
    return TestAsyncClient(router)


@pytest.fixture
async def collection(user):
    """
    Fixture to create a test collection.
    """
    return await Collection.objects.aget_or_create(
        name="Test Collection Fixture", metadata={"key": "value"}, owner=user
    )


async def test_valid_token(bearer, user):
    """
    Test that a valid token authenticates the user successfully.
    """
    request = None  # We don't need the request object for this test
    token = "valid_token"

    authenticated_user = await bearer.authenticate(request, token)

    assert authenticated_user is not None
    assert authenticated_user.username == user.username


async def test_invalid_token(bearer, user):
    """
    Test that an invalid token returns None (authentication fails).
    """
    request = None
    token = "invalid_token"

    authenticated_user = await bearer.authenticate(request, token)

    assert authenticated_user is None


async def test_missing_token(bearer):
    """
    Test that a missing token returns None.
    """
    request = None
    token = None  # No token provided

    authenticated_user = await bearer.authenticate(request, token)

    assert authenticated_user is None


""" Collection tests """


async def test_create_collection(async_client, user):
    response = await async_client.post(
        "/collections",
        json={"name": "Test Collection Fixture", "metadata": {"key": "value"}},
        headers={"Authorization": f"Bearer {user.token}"},
    )
    assert response.status_code == 200
    assert response.json() == {"id": 1, "message": "Collection created successfully"}


async def test_create_collection_unique(async_client, user, collection):
    response = await async_client.post(
        "/collections",
        json={"name": "Test Collection Fixture", "metadata": {"key": "value"}},
        headers={"Authorization": f"Bearer {user.token}"},
    )
    assert response.status_code == 409


async def test_get_collections(async_client, user, collection):
    response = await async_client.get(
        "/collections/1",
        headers={"Authorization": f"Bearer {user.token}"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Test Collection Fixture",
        "metadata": {"key": "value"},
    }


async def test_list_collection(async_client, user, collection):
    response = await async_client.get(
        "/collections",
        headers={"Authorization": f"Bearer {user.token}"},
    )
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Test Collection Fixture", "metadata": {"key": "value"}}
    ]


async def test_patch_collection(async_client, user, collection):
    response = await async_client.patch(
        "/collections/1",
        json={"name": "Test Collection Update", "metadata": {"key": "value"}},
        headers={"Authorization": f"Bearer {user.token}"},
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Collection updated successfully"}

    # now check if the collection was actually updated
    response = await async_client.get(
        "/collections/1",
        headers={"Authorization": f"Bearer {user.token}"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Test Collection Update",
        "metadata": {"key": "value"},
    }


async def test_delete_collection(async_client, user, collection):
    response = await async_client.delete(
        "/collections/1",
        headers={"Authorization": f"Bearer {user.token}"},
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Collection deleted successfully"}

    # now check if the collection was actually deleted
    response = await async_client.get(
        "/collections/1",
        headers={"Authorization": f"Bearer {user.token}"},
    )
    assert response.status_code == 404


""" Document tests """


async def test_create_document_pdf_url(async_client, user, collection):
    response = await async_client.post(
        "/collections/1/document",
        json={
            "name": "Test Document Fixture",
            "url": "https://pdfobject.com/pdf/sample.pdf",
        },
        headers={"Authorization": f"Bearer {user.token}"},
    )
    assert response.status_code == 200
    assert response.json() == {"id": 1, "message": "Document created successfully"}


async def test_create_document_pdf_base64(async_client, user, collection):
    # test_docs/ is a directory in the root of the project - we will use a sample PDF file from there

    with open("test_docs/sample.pdf", "rb") as f:
        # convert the file to base64
        base64_string = base64_string = base64.b64encode(f.read()).decode("utf-8")

    response = await async_client.post(
        "/collections/1/document",
        json={
            "name": "Test Document Fixture",
            "base64": base64_string,
        },
        headers={"Authorization": f"Bearer {user.token}"},
    )
    assert response.status_code == 200
    assert response.json() == {"id": 1, "message": "Document created successfully"}


async def test_create_document_docx_url(async_client, user, collection):
    url = "https://www.cte.iup.edu/cte/Resources/DOCX_TestPage.docx"
    response = await async_client.post(
        "/collections/1/document",
        json={
            "name": "Test Document Fixture",
            "url": url,
        },
        headers={"Authorization": f"Bearer {user.token}"},
    )
    assert response.status_code == 200
    assert response.json() == {"id": 1, "message": "Document created successfully"}


async def test_create_document_docx_base64(async_client, user, collection):
    with open("test_docs/sample.docx", "rb") as f:
        # convert the file to base64
        base64_string = base64.b64encode(f.read()).decode("utf-8")

    response = await async_client.post(
        "/collections/1/document",
        json={
            "name": "Test Document Fixture",
            "base64": base64_string,
        },
        headers={"Authorization": f"Bearer {user.token}"},
    )
    assert response.status_code == 200
    assert response.json() == {"id": 1, "message": "Document created successfully"}


# failing
async def test_create_document_webpage(async_client, user, collection):
    url = "https://gotenberg.dev/docs/getting-started/introduction"
    response = await async_client.post(
        "/collections/1/document",
        json={
            "name": "Test Document Fixture",
            "url": url,
        },
        headers={"Authorization": f"Bearer {user.token}"},
    )
    assert response.status_code == 200
    assert response.json() == {"id": 1, "message": "Document created successfully"}


# documents tests
# 5. web page url
# 6. Image url
# 7. Image base64
