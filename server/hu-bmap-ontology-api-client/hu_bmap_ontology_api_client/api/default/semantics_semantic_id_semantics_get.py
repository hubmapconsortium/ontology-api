from typing import Any, Dict, List, Optional

import httpx

from ...client import Client
from ...models.qqst import QQST
from ...types import Response


def _get_kwargs(
    semantic_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/semantics/{semantic_id}/semantics".format(client.base_url, semantic_id=semantic_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[QQST]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = QQST.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[QQST]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    semantic_id: str,
    *,
    client: Client,
) -> Response[List[QQST]]:
    """Returns a list of semantic_types {queryTUI, querySTN ,semantic, TUI_STN} of the semantic type

    Args:
        semantic_id (str):  Example: Physical Object.

    Returns:
        Response[List[QQST]]
    """

    kwargs = _get_kwargs(
        semantic_id=semantic_id,
        client=client,
    )

    response = httpx.get(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    semantic_id: str,
    *,
    client: Client,
) -> Optional[List[QQST]]:
    """Returns a list of semantic_types {queryTUI, querySTN ,semantic, TUI_STN} of the semantic type

    Args:
        semantic_id (str):  Example: Physical Object.

    Returns:
        Response[List[QQST]]
    """

    return sync_detailed(
        semantic_id=semantic_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    semantic_id: str,
    *,
    client: Client,
) -> Response[List[QQST]]:
    """Returns a list of semantic_types {queryTUI, querySTN ,semantic, TUI_STN} of the semantic type

    Args:
        semantic_id (str):  Example: Physical Object.

    Returns:
        Response[List[QQST]]
    """

    kwargs = _get_kwargs(
        semantic_id=semantic_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    semantic_id: str,
    *,
    client: Client,
) -> Optional[List[QQST]]:
    """Returns a list of semantic_types {queryTUI, querySTN ,semantic, TUI_STN} of the semantic type

    Args:
        semantic_id (str):  Example: Physical Object.

    Returns:
        Response[List[QQST]]
    """

    return (
        await asyncio_detailed(
            semantic_id=semantic_id,
            client=client,
        )
    ).parsed
