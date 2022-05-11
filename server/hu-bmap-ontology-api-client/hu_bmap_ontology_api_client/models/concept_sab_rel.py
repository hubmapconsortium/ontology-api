from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConceptSabRel")


@attr.s(auto_attribs=True)
class ConceptSabRel:
    """
    Attributes:
        query_concept_id (Union[Unset, str]):  Example: C2720507.
        sab (Union[Unset, List[str]]):  Example: ['SNOMEDCT_US', 'HGNC'].
        rel (Union[Unset, List[str]]):  Example: ['isa', 'isa'].
    """

    query_concept_id: Union[Unset, str] = UNSET
    sab: Union[Unset, List[str]] = UNSET
    rel: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        query_concept_id = self.query_concept_id
        sab: Union[Unset, List[str]] = UNSET
        if not isinstance(self.sab, Unset):
            sab = self.sab

        rel: Union[Unset, List[str]] = UNSET
        if not isinstance(self.rel, Unset):
            rel = self.rel

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if query_concept_id is not UNSET:
            field_dict["query_concept_id"] = query_concept_id
        if sab is not UNSET:
            field_dict["sab"] = sab
        if rel is not UNSET:
            field_dict["rel"] = rel

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        query_concept_id = d.pop("query_concept_id", UNSET)

        sab = cast(List[str], d.pop("sab", UNSET))

        rel = cast(List[str], d.pop("rel", UNSET))

        concept_sab_rel = cls(
            query_concept_id=query_concept_id,
            sab=sab,
            rel=rel,
        )

        concept_sab_rel.additional_properties = d
        return concept_sab_rel

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
