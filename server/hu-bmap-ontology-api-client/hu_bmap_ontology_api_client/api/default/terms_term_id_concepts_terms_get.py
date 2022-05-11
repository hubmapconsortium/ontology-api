from typing import Any, Dict, List, Optional

import httpx

from ...client import Client
from ...models.concept_term import ConceptTerm
from ...types import Response


def _get_kwargs(
    term_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/terms/{term_id}/concepts/terms".format(client.base_url, term_id=term_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[ConceptTerm]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ConceptTerm.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[ConceptTerm]]:
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
) -> Response[List[ConceptTerm]]:
    """Returns an expanded list of concept(s) and preferred term(s) {Concept, Term} from an exact text
    match

    Args:
        term_id (str):  Example: Breast cancer.

    Returns:
        Response[List[ConceptTerm]]
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
) -> Optional[List[ConceptTerm]]:
    """Returns an expanded list of concept(s) and preferred term(s) {Concept, Term} from an exact text
    match

    Args:
        term_id (str):  Example: Breast cancer.

    Returns:
        Response[List[ConceptTerm]]
    """

    return sync_detailed(
        term_id=term_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    term_id: str,
    *,
    client: Client,
) -> Response[List[ConceptTerm]]:
    """Returns an expanded list of concept(s) and preferred term(s) {Concept, Term} from an exact text
    match

    Args:
        term_id (str):  Example: Breast cancer.

    Returns:
        Response[List[ConceptTerm]]
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
) -> Optional[List[ConceptTerm]]:
    """Returns an expanded list of concept(s) and preferred term(s) {Concept, Term} from an exact text
    match

    Args:
        term_id (str):  Example: Breast cancer.

    Returns:
        Response[List[ConceptTerm]]
    """

    return (
        await asyncio_detailed(
            term_id=term_id,
            client=client,
        )
    ).parsed
