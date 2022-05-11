from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    concept_id: str,
    *,
    client: Client,
    sab: Union[Unset, None, List[str]] = UNSET,
) -> Dict[str, Any]:
    url = "{}/concepts/{concept_id}/codes".format(client.base_url, concept_id=concept_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_sab: Union[Unset, None, List[str]] = UNSET
    if not isinstance(sab, Unset):
        if sab is None:
            json_sab = None
        else:
            json_sab = sab

    params: Dict[str, Any] = {
        "sab": json_sab,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
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
    concept_id: str,
    *,
    client: Client,
    sab: Union[Unset, None, List[str]] = UNSET,
) -> Response[List[str]]:
    """Returns a distinct list of code_id(s) that code the concept

    Args:
        concept_id (str):  Example: C0678222.
        sab (Union[Unset, None, List[str]]):

    Returns:
        Response[List[str]]
    """

    kwargs = _get_kwargs(
        concept_id=concept_id,
        client=client,
        sab=sab,
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
    sab: Union[Unset, None, List[str]] = UNSET,
) -> Optional[List[str]]:
    """Returns a distinct list of code_id(s) that code the concept

    Args:
        concept_id (str):  Example: C0678222.
        sab (Union[Unset, None, List[str]]):

    Returns:
        Response[List[str]]
    """

    return sync_detailed(
        concept_id=concept_id,
        client=client,
        sab=sab,
    ).parsed


async def asyncio_detailed(
    concept_id: str,
    *,
    client: Client,
    sab: Union[Unset, None, List[str]] = UNSET,
) -> Response[List[str]]:
    """Returns a distinct list of code_id(s) that code the concept

    Args:
        concept_id (str):  Example: C0678222.
        sab (Union[Unset, None, List[str]]):

    Returns:
        Response[List[str]]
    """

    kwargs = _get_kwargs(
        concept_id=concept_id,
        client=client,
        sab=sab,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    concept_id: str,
    *,
    client: Client,
    sab: Union[Unset, None, List[str]] = UNSET,
) -> Optional[List[str]]:
    """Returns a distinct list of code_id(s) that code the concept

    Args:
        concept_id (str):  Example: C0678222.
        sab (Union[Unset, None, List[str]]):

    Returns:
        Response[List[str]]
    """

    return (
        await asyncio_detailed(
            concept_id=concept_id,
            client=client,
            sab=sab,
        )
    ).parsed
