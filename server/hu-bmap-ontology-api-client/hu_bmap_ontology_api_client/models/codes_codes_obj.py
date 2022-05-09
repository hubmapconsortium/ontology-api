from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CodesCodesObj")


@attr.s(auto_attribs=True)
class CodesCodesObj:
    """
    Attributes:
        concept (Union[Unset, str]):  Example: C0006142.
        code (Union[Unset, str]):  Example: CCS 2.5.
        sab (Union[Unset, str]):  Example: CCF.
    """

    concept: Union[Unset, str] = UNSET
    code: Union[Unset, str] = UNSET
    sab: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        concept = self.concept
        code = self.code
        sab = self.sab

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if concept is not UNSET:
            field_dict["concept"] = concept
        if code is not UNSET:
            field_dict["code"] = code
        if sab is not UNSET:
            field_dict["SAB"] = sab

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        concept = d.pop("concept", UNSET)

        code = d.pop("code", UNSET)

        sab = d.pop("SAB", UNSET)

        codes_codes_obj = cls(
            concept=concept,
            code=code,
            sab=sab,
        )

        codes_codes_obj.additional_properties = d
        return codes_codes_obj

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
