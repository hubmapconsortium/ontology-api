from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.codes_codes_obj import CodesCodesObj
from ...types import UNSET, Response, Unset


def _get_kwargs(
    code_id: str,
    *,
    client: Client,
    sab: Union[Unset, None, List[str]] = UNSET,
) -> Dict[str, Any]:
    url = "{}/codes/{code_id}/codes".format(client.base_url, code_id=code_id)

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


def _parse_response(*, response: httpx.Response) -> Optional[List[CodesCodesObj]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = CodesCodesObj.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[CodesCodesObj]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    code_id: str,
    *,
    client: Client,
    sab: Union[Unset, None, List[str]] = UNSET,
) -> Response[List[CodesCodesObj]]:
    """Returns a list of code_ids {Concept, Code, SAB} that code the same concept(s) as the code_id,
    optionally restricted to source (SAB)

    Args:
        code_id (str):  Example: SNOMEDCT_US 254837009.
        sab (Union[Unset, None, List[str]]):

    Returns:
        Response[List[CodesCodesObj]]
    """

    kwargs = _get_kwargs(
        code_id=code_id,
        client=client,
        sab=sab,
    )

    response = httpx.get(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    code_id: str,
    *,
    client: Client,
    sab: Union[Unset, None, List[str]] = UNSET,
) -> Optional[List[CodesCodesObj]]:
    """Returns a list of code_ids {Concept, Code, SAB} that code the same concept(s) as the code_id,
    optionally restricted to source (SAB)

    Args:
        code_id (str):  Example: SNOMEDCT_US 254837009.
        sab (Union[Unset, None, List[str]]):

    Returns:
        Response[List[CodesCodesObj]]
    """

    return sync_detailed(
        code_id=code_id,
        client=client,
        sab=sab,
    ).parsed


async def asyncio_detailed(
    code_id: str,
    *,
    client: Client,
    sab: Union[Unset, None, List[str]] = UNSET,
) -> Response[List[CodesCodesObj]]:
    """Returns a list of code_ids {Concept, Code, SAB} that code the same concept(s) as the code_id,
    optionally restricted to source (SAB)

    Args:
        code_id (str):  Example: SNOMEDCT_US 254837009.
        sab (Union[Unset, None, List[str]]):

    Returns:
        Response[List[CodesCodesObj]]
    """

    kwargs = _get_kwargs(
        code_id=code_id,
        client=client,
        sab=sab,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    code_id: str,
    *,
    client: Client,
    sab: Union[Unset, None, List[str]] = UNSET,
) -> Optional[List[CodesCodesObj]]:
    """Returns a list of code_ids {Concept, Code, SAB} that code the same concept(s) as the code_id,
    optionally restricted to source (SAB)

    Args:
        code_id (str):  Example: SNOMEDCT_US 254837009.
        sab (Union[Unset, None, List[str]]):

    Returns:
        Response[List[CodesCodesObj]]
    """

    return (
        await asyncio_detailed(
            code_id=code_id,
            client=client,
            sab=sab,
        )
    ).parsed
