from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TermRespObj")


@attr.s(auto_attribs=True)
class TermRespObj:
    """ """

    code_id: Union[Unset, str] = UNSET
    code_sab: Union[Unset, str] = UNSET
    code: Union[Unset, str] = UNSET
    concept: Union[Unset, str] = UNSET
    tty: Union[Unset, str] = UNSET
    term: Union[Unset, str] = UNSET
    matched: Union[Unset, str] = UNSET
    rel_type: Union[Unset, str] = UNSET
    rel_sab: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code_id = self.code_id
        code_sab = self.code_sab
        code = self.code
        concept = self.concept
        tty = self.tty
        term = self.term
        matched = self.matched
        rel_type = self.rel_type
        rel_sab = self.rel_sab

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if code_id is not UNSET:
            field_dict["code_id"] = code_id
        if code_sab is not UNSET:
            field_dict["code_sab"] = code_sab
        if code is not UNSET:
            field_dict["code"] = code
        if concept is not UNSET:
            field_dict["concept"] = concept
        if tty is not UNSET:
            field_dict["tty"] = tty
        if term is not UNSET:
            field_dict["term"] = term
        if matched is not UNSET:
            field_dict["matched"] = matched
        if rel_type is not UNSET:
            field_dict["rel_type"] = rel_type
        if rel_sab is not UNSET:
            field_dict["rel_sab"] = rel_sab

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code_id = d.pop("code_id", UNSET)

        code_sab = d.pop("code_sab", UNSET)

        code = d.pop("code", UNSET)

        concept = d.pop("concept", UNSET)

        tty = d.pop("tty", UNSET)

        term = d.pop("term", UNSET)

        matched = d.pop("matched", UNSET)

        rel_type = d.pop("rel_type", UNSET)

        rel_sab = d.pop("rel_sab", UNSET)

        term_resp_obj = cls(
            code_id=code_id,
            code_sab=code_sab,
            code=code,
            concept=concept,
            tty=tty,
            term=term,
            matched=matched,
            rel_type=rel_type,
            rel_sab=rel_sab,
        )

        term_resp_obj.additional_properties = d
        return term_resp_obj

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
