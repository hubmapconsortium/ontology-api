from typing import Any, Dict, List, Optional

import httpx

from ...client import Client
from ...models.sab_definition import SabDefinition
from ...types import Response


def _get_kwargs(
    concept_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/concepts/{concept_id}/definitions".format(client.base_url, concept_id=concept_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[SabDefinition]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SabDefinition.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[SabDefinition]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    concept_id: str,
    *,
    client: Client,
) -> Response[List[SabDefinition]]:
    """Returns a list of definitions {Sab, Definition} of the concept

    Args:
        concept_id (str):  Example: C0006142.

    Returns:
        Response[List[SabDefinition]]
    """

    kwargs = _get_kwargs(
        concept_id=concept_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    concept_id: str,
    *,
    client: Client,
) -> Optional[List[SabDefinition]]:
    """Returns a list of definitions {Sab, Definition} of the concept

    Args:
        concept_id (str):  Example: C0006142.

    Returns:
        Response[List[SabDefinition]]
    """

    return sync_detailed(
        concept_id=concept_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    concept_id: str,
    *,
    client: Client,
) -> Response[List[SabDefinition]]:
    """Returns a list of definitions {Sab, Definition} of the concept

    Args:
        concept_id (str):  Example: C0006142.

    Returns:
        Response[List[SabDefinition]]
    """

    kwargs = _get_kwargs(
        concept_id=concept_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    concept_id: str,
    *,
    client: Client,
) -> Optional[List[SabDefinition]]:
    """Returns a list of definitions {Sab, Definition} of the concept

    Args:
        concept_id (str):  Example: C0006142.

    Returns:
        Response[List[SabDefinition]]
    """

    return (
        await asyncio_detailed(
            concept_id=concept_id,
            client=client,
        )
    ).parsed
