from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SabRelationshipConceptPrefterm")


@attr.s(auto_attribs=True)
class SabRelationshipConceptPrefterm:
    """ """

    sab: Union[Unset, str] = UNSET
    relationship: Union[Unset, str] = UNSET
    concept: Union[Unset, str] = UNSET
    perfterm: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        sab = self.sab
        relationship = self.relationship
        concept = self.concept
        perfterm = self.perfterm

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sab is not UNSET:
            field_dict["sab"] = sab
        if relationship is not UNSET:
            field_dict["relationship"] = relationship
        if concept is not UNSET:
            field_dict["concept"] = concept
        if perfterm is not UNSET:
            field_dict["perfterm"] = perfterm

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sab = d.pop("sab", UNSET)

        relationship = d.pop("relationship", UNSET)

        concept = d.pop("concept", UNSET)

        perfterm = d.pop("perfterm", UNSET)

        sab_relationship_concept_prefterm = cls(
            sab=sab,
            relationship=relationship,
            concept=concept,
            perfterm=perfterm,
        )

        sab_relationship_concept_prefterm.additional_properties = d
        return sab_relationship_concept_prefterm

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
