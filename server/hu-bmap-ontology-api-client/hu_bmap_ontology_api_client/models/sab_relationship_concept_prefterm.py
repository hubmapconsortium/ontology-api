from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SabRelationshipConceptPrefterm")


@attr.s(auto_attribs=True)
class SabRelationshipConceptPrefterm:
    """
    Attributes:
        sab (Union[Unset, str]):  Example: ICD10AM.
        relationship (Union[Unset, str]):  Example: CHD.
        concept (Union[Unset, str]):  Example: C0006826.
        prefterm (Union[Unset, str]):  Example: Malignant Neoplasms.
    """

    sab: Union[Unset, str] = UNSET
    relationship: Union[Unset, str] = UNSET
    concept: Union[Unset, str] = UNSET
    prefterm: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        sab = self.sab
        relationship = self.relationship
        concept = self.concept
        prefterm = self.prefterm

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sab is not UNSET:
            field_dict["sab"] = sab
        if relationship is not UNSET:
            field_dict["relationship"] = relationship
        if concept is not UNSET:
            field_dict["concept"] = concept
        if prefterm is not UNSET:
            field_dict["prefterm"] = prefterm

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sab = d.pop("sab", UNSET)

        relationship = d.pop("relationship", UNSET)

        concept = d.pop("concept", UNSET)

        prefterm = d.pop("prefterm", UNSET)

        sab_relationship_concept_prefterm = cls(
            sab=sab,
            relationship=relationship,
            concept=concept,
            prefterm=prefterm,
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
