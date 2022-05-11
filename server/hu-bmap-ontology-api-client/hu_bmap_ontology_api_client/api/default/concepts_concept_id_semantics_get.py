from typing import Any, Dict, List, Optional

import httpx

from ...client import Client
from ...models.sty_tui_stn import StyTuiStn
from ...types import Response


def _get_kwargs(
    concept_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/concepts/{concept_id}/semantics".format(client.base_url, concept_id=concept_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[StyTuiStn]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = StyTuiStn.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[StyTuiStn]]:
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
) -> Response[List[StyTuiStn]]:
    """Returns a list of semantic_types {Sty, Tui, Stn} of the concept

    Args:
        concept_id (str):  Example: C0304055.

    Returns:
        Response[List[StyTuiStn]]
    """

    kwargs = _get_kwargs(
        concept_id=concept_id,
        client=client,
    )

    response = httpx.get(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    concept_id: str,
    *,
    client: Client,
) -> Optional[List[StyTuiStn]]:
    """Returns a list of semantic_types {Sty, Tui, Stn} of the concept

    Args:
        concept_id (str):  Example: C0304055.

    Returns:
        Response[List[StyTuiStn]]
    """

    return sync_detailed(
        concept_id=concept_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    concept_id: str,
    *,
    client: Client,
) -> Response[List[StyTuiStn]]:
    """Returns a list of semantic_types {Sty, Tui, Stn} of the concept

    Args:
        concept_id (str):  Example: C0304055.

    Returns:
        Response[List[StyTuiStn]]
    """

    kwargs = _get_kwargs(
        concept_id=concept_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    concept_id: str,
    *,
    client: Client,
) -> Optional[List[StyTuiStn]]:
    """Returns a list of semantic_types {Sty, Tui, Stn} of the concept

    Args:
        concept_id (str):  Example: C0304055.

    Returns:
        Response[List[StyTuiStn]]
    """

    return (
        await asyncio_detailed(
            concept_id=concept_id,
            client=client,
        )
    ).parsed
