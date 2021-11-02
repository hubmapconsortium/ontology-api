from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SabCodeTerm")


@attr.s(auto_attribs=True)
class SabCodeTerm:
    """ """

    sab: Union[Unset, str] = UNSET
    code: Union[Unset, str] = UNSET
    term: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        sab = self.sab
        code = self.code
        term = self.term

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sab is not UNSET:
            field_dict["SAB"] = sab
        if code is not UNSET:
            field_dict["code"] = code
        if term is not UNSET:
            field_dict["term"] = term

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sab = d.pop("SAB", UNSET)

        code = d.pop("code", UNSET)

        term = d.pop("term", UNSET)

        sab_code_term = cls(
            sab=sab,
            code=code,
            term=term,
        )

        sab_code_term.additional_properties = d
        return sab_code_term

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
