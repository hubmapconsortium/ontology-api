from typing import Any, Dict, List, Optional

import httpx

from ...client import Client
from ...models.semantic_stn import SemanticStn
from ...types import Response


def _get_kwargs(
    tui_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/tui/{tui_id}/semantics".format(client.base_url, tui_id=tui_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[SemanticStn]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SemanticStn.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[SemanticStn]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    tui_id: str,
    *,
    client: Client,
) -> Response[List[SemanticStn]]:
    """Returns a list of symantic_types {semantic, STN} of the type unique id (tui)

    Args:
        tui_id (str):  Example: T200.

    Returns:
        Response[List[SemanticStn]]
    """

    kwargs = _get_kwargs(
        tui_id=tui_id,
        client=client,
    )

    response = httpx.get(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    tui_id: str,
    *,
    client: Client,
) -> Optional[List[SemanticStn]]:
    """Returns a list of symantic_types {semantic, STN} of the type unique id (tui)

    Args:
        tui_id (str):  Example: T200.

    Returns:
        Response[List[SemanticStn]]
    """

    return sync_detailed(
        tui_id=tui_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    tui_id: str,
    *,
    client: Client,
) -> Response[List[SemanticStn]]:
    """Returns a list of symantic_types {semantic, STN} of the type unique id (tui)

    Args:
        tui_id (str):  Example: T200.

    Returns:
        Response[List[SemanticStn]]
    """

    kwargs = _get_kwargs(
        tui_id=tui_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    tui_id: str,
    *,
    client: Client,
) -> Optional[List[SemanticStn]]:
    """Returns a list of symantic_types {semantic, STN} of the type unique id (tui)

    Args:
        tui_id (str):  Example: T200.

    Returns:
        Response[List[SemanticStn]]
    """

    return (
        await asyncio_detailed(
            tui_id=tui_id,
            client=client,
        )
    ).parsed
