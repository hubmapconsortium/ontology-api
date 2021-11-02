from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FullCapacityTerm")


@attr.s(auto_attribs=True)
class FullCapacityTerm:
    """ """

    term: Union[Unset, str] = UNSET
    tty: Union[Unset, str] = UNSET
    code: Union[Unset, str] = UNSET
    concept: Union[Unset, str] = UNSET
    perfterm: Union[Unset, str] = UNSET
    semantic: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        term = self.term
        tty = self.tty
        code = self.code
        concept = self.concept
        perfterm = self.perfterm
        semantic = self.semantic

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if term is not UNSET:
            field_dict["term"] = term
        if tty is not UNSET:
            field_dict["tty"] = tty
        if code is not UNSET:
            field_dict["code"] = code
        if concept is not UNSET:
            field_dict["concept"] = concept
        if perfterm is not UNSET:
            field_dict["perfterm"] = perfterm
        if semantic is not UNSET:
            field_dict["semantic"] = semantic

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        term = d.pop("term", UNSET)

        tty = d.pop("tty", UNSET)

        code = d.pop("code", UNSET)

        concept = d.pop("concept", UNSET)

        perfterm = d.pop("perfterm", UNSET)

        semantic = d.pop("semantic", UNSET)

        full_capacity_term = cls(
            term=term,
            tty=tty,
            code=code,
            concept=concept,
            perfterm=perfterm,
            semantic=semantic,
        )

        full_capacity_term.additional_properties = d
        return full_capacity_term

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
