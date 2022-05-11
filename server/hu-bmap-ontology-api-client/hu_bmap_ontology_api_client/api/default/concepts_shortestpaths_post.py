from typing import Any, Dict, List, Optional

import httpx

from ...client import Client
from ...models.path_item_concept_relationship_sab_prefterm import PathItemConceptRelationshipSabPrefterm
from ...models.qconcept_tconcept_sab_rel import QconceptTconceptSabRel
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: QconceptTconceptSabRel,
) -> Dict[str, Any]:
    url = "{}/concepts/shortestpaths".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[PathItemConceptRelationshipSabPrefterm]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = PathItemConceptRelationshipSabPrefterm.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[PathItemConceptRelationshipSabPrefterm]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: QconceptTconceptSabRel,
) -> Response[List[PathItemConceptRelationshipSabPrefterm]]:
    """Return all paths of the relationship pattern specified within the selected sources

    Args:
        json_body (QconceptTconceptSabRel):

    Returns:
        Response[List[PathItemConceptRelationshipSabPrefterm]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.post(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: QconceptTconceptSabRel,
) -> Optional[List[PathItemConceptRelationshipSabPrefterm]]:
    """Return all paths of the relationship pattern specified within the selected sources

    Args:
        json_body (QconceptTconceptSabRel):

    Returns:
        Response[List[PathItemConceptRelationshipSabPrefterm]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: QconceptTconceptSabRel,
) -> Response[List[PathItemConceptRelationshipSabPrefterm]]:
    """Return all paths of the relationship pattern specified within the selected sources

    Args:
        json_body (QconceptTconceptSabRel):

    Returns:
        Response[List[PathItemConceptRelationshipSabPrefterm]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: QconceptTconceptSabRel,
) -> Optional[List[PathItemConceptRelationshipSabPrefterm]]:
    """Return all paths of the relationship pattern specified within the selected sources

    Args:
        json_body (QconceptTconceptSabRel):

    Returns:
        Response[List[PathItemConceptRelationshipSabPrefterm]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
