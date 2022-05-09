from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PathItemConceptRelationshipSabPrefterm")


@attr.s(auto_attribs=True)
class PathItemConceptRelationshipSabPrefterm:
    """
    Attributes:
        path (Union[Unset, str]):
        item (Union[Unset, str]):
        concept (Union[Unset, str]):  Example: C0006826.
        relationship (Union[Unset, str]):  Example: CHD.
        sab (Union[Unset, str]):  Example: ICD10AM.
        prefterm (Union[Unset, str]):  Example: Malignant Neoplasms.
    """

    path: Union[Unset, str] = UNSET
    item: Union[Unset, str] = UNSET
    concept: Union[Unset, str] = UNSET
    relationship: Union[Unset, str] = UNSET
    sab: Union[Unset, str] = UNSET
    prefterm: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        item = self.item
        concept = self.concept
        relationship = self.relationship
        sab = self.sab
        prefterm = self.prefterm

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if path is not UNSET:
            field_dict["path"] = path
        if item is not UNSET:
            field_dict["item"] = item
        if concept is not UNSET:
            field_dict["concept"] = concept
        if relationship is not UNSET:
            field_dict["relationship"] = relationship
        if sab is not UNSET:
            field_dict["sab"] = sab
        if prefterm is not UNSET:
            field_dict["prefterm"] = prefterm

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path", UNSET)

        item = d.pop("item", UNSET)

        concept = d.pop("concept", UNSET)

        relationship = d.pop("relationship", UNSET)

        sab = d.pop("sab", UNSET)

        prefterm = d.pop("prefterm", UNSET)

        path_item_concept_relationship_sab_prefterm = cls(
            path=path,
            item=item,
            concept=concept,
            relationship=relationship,
            sab=sab,
            prefterm=prefterm,
        )

        path_item_concept_relationship_sab_prefterm.additional_properties = d
        return path_item_concept_relationship_sab_prefterm

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
