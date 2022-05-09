from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConceptTerm")


@attr.s(auto_attribs=True)
class ConceptTerm:
    """
    Attributes:
        concept (Union[Unset, str]):  Example: C0006826.
        term (Union[Unset, str]):  Example: LNC LA14283-8.
    """

    concept: Union[Unset, str] = UNSET
    term: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        concept = self.concept
        term = self.term

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if concept is not UNSET:
            field_dict["concept"] = concept
        if term is not UNSET:
            field_dict["term"] = term

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        concept = d.pop("concept", UNSET)

        term = d.pop("term", UNSET)

        concept_term = cls(
            concept=concept,
            term=term,
        )

        concept_term.additional_properties = d
        return concept_term

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
