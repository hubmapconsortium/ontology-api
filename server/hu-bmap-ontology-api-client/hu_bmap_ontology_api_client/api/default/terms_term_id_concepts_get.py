from typing import Any, Dict, List, Optional, cast

import httpx

from ...client import Client
from ...types import Response


def _get_kwargs(
    term_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/terms/{term_id}/concepts".format(client.base_url, term_id=term_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[str]]:
    if response.status_code == 200:
        response_200 = cast(List[str], response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[str]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    term_id: str,
    *,
    client: Client,
) -> Response[List[str]]:
    """Returns a list of concepts associated with the text string

    Args:
        term_id (str):  Example: Breast cancer.

    Returns:
        Response[List[str]]
    """

    kwargs = _get_kwargs(
        term_id=term_id,
        client=client,
    )

    response = httpx.get(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    term_id: str,
    *,
    client: Client,
) -> Optional[List[str]]:
    """Returns a list of concepts associated with the text string

    Args:
        term_id (str):  Example: Breast cancer.

    Returns:
        Response[List[str]]
    """

    return sync_detailed(
        term_id=term_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    term_id: str,
    *,
    client: Client,
) -> Response[List[str]]:
    """Returns a list of concepts associated with the text string

    Args:
        term_id (str):  Example: Breast cancer.

    Returns:
        Response[List[str]]
    """

    kwargs = _get_kwargs(
        term_id=term_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    term_id: str,
    *,
    client: Client,
) -> Optional[List[str]]:
    """Returns a list of concepts associated with the text string

    Args:
        term_id (str):  Example: Breast cancer.

    Returns:
        Response[List[str]]
    """

    return (
        await asyncio_detailed(
            term_id=term_id,
            client=client,
        )
    ).parsed
