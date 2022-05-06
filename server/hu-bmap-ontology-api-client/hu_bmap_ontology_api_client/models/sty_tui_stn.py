from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="StyTuiStn")


@attr.s(auto_attribs=True)
class StyTuiStn:
    """
    Attributes:
        sty (Union[Unset, str]):  Example: Organic Chemical.
        tui (Union[Unset, str]):  Example: T109.
        stn (Union[Unset, str]):  Example: A1.4.1.2.1.
    """

    sty: Union[Unset, str] = UNSET
    tui: Union[Unset, str] = UNSET
    stn: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        sty = self.sty
        tui = self.tui
        stn = self.stn

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sty is not UNSET:
            field_dict["sty"] = sty
        if tui is not UNSET:
            field_dict["tui"] = tui
        if stn is not UNSET:
            field_dict["stn"] = stn

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sty = d.pop("sty", UNSET)

        tui = d.pop("tui", UNSET)

        stn = d.pop("stn", UNSET)

        sty_tui_stn = cls(
            sty=sty,
            tui=tui,
            stn=stn,
        )

        sty_tui_stn.additional_properties = d
        return sty_tui_stn

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
