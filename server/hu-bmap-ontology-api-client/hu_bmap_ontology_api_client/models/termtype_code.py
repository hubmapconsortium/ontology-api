from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TermtypeCode")


@attr.s(auto_attribs=True)
class TermtypeCode:
    """
    Attributes:
        termtype (Union[Unset, str]):  Example: LA.
        code (Union[Unset, str]):  Example: LNC LA14283-8.
    """

    termtype: Union[Unset, str] = UNSET
    code: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        termtype = self.termtype
        code = self.code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if termtype is not UNSET:
            field_dict["termtype"] = termtype
        if code is not UNSET:
            field_dict["code"] = code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        termtype = d.pop("termtype", UNSET)

        code = d.pop("code", UNSET)

        termtype_code = cls(
            termtype=termtype,
            code=code,
        )

        termtype_code.additional_properties = d
        return termtype_code

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
