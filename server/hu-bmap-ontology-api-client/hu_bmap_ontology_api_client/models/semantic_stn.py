from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SemanticStn")


@attr.s(auto_attribs=True)
class SemanticStn:
    """
    Attributes:
        semantic (Union[Unset, str]):  Example: Entity.
        stn (Union[Unset, str]):  Example: A.
    """

    semantic: Union[Unset, str] = UNSET
    stn: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        semantic = self.semantic
        stn = self.stn

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if semantic is not UNSET:
            field_dict["semantic"] = semantic
        if stn is not UNSET:
            field_dict["STN"] = stn

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        semantic = d.pop("semantic", UNSET)

        stn = d.pop("STN", UNSET)

        semantic_stn = cls(
            semantic=semantic,
            stn=stn,
        )

        semantic_stn.additional_properties = d
        return semantic_stn

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
