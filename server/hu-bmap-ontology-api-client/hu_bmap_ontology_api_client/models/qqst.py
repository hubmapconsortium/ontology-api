from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="QQST")


@attr.s(auto_attribs=True)
class QQST:
    """
    Attributes:
        query_tui (Union[Unset, str]):  Example: T072.
        query_stn (Union[Unset, str]):  Example: A1.
        semantic (Union[Unset, str]):  Example: Entity.
        tui (Union[Unset, str]):  Example: T071.
        stn (Union[Unset, str]):  Example: A.
    """

    query_tui: Union[Unset, str] = UNSET
    query_stn: Union[Unset, str] = UNSET
    semantic: Union[Unset, str] = UNSET
    tui: Union[Unset, str] = UNSET
    stn: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        query_tui = self.query_tui
        query_stn = self.query_stn
        semantic = self.semantic
        tui = self.tui
        stn = self.stn

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if query_tui is not UNSET:
            field_dict["queryTUI"] = query_tui
        if query_stn is not UNSET:
            field_dict["querySTN"] = query_stn
        if semantic is not UNSET:
            field_dict["semantic"] = semantic
        if tui is not UNSET:
            field_dict["TUI"] = tui
        if stn is not UNSET:
            field_dict["STN"] = stn

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        query_tui = d.pop("queryTUI", UNSET)

        query_stn = d.pop("querySTN", UNSET)

        semantic = d.pop("semantic", UNSET)

        tui = d.pop("TUI", UNSET)

        stn = d.pop("STN", UNSET)

        qqst = cls(
            query_tui=query_tui,
            query_stn=query_stn,
            semantic=semantic,
            tui=tui,
            stn=stn,
        )

        qqst.additional_properties = d
        return qqst

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
