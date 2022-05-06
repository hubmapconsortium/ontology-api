from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SabDefinition")


@attr.s(auto_attribs=True)
class SabDefinition:
    """
    Attributes:
        sab (Union[Unset, str]):  Example: NCI.
        definition (Union[Unset, str]):  Example: A primary or metastatic malignant neoplasm involving the breast. The
            vast majority of cases are carcinomas arising from the breast parenchyma or the nipple. Malignant breast
            neoplasms occur more frequently in females than in males..
    """

    sab: Union[Unset, str] = UNSET
    definition: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        sab = self.sab
        definition = self.definition

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sab is not UNSET:
            field_dict["sab"] = sab
        if definition is not UNSET:
            field_dict["definition"] = definition

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sab = d.pop("sab", UNSET)

        definition = d.pop("definition", UNSET)

        sab_definition = cls(
            sab=sab,
            definition=definition,
        )

        sab_definition.additional_properties = d
        return sab_definition

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
