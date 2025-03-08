#!/usr/bin/python3
"""
Return object classes for UMLS API.

Author(s):
    Michael Yao @michael-s-yao

Licensed under the MIT License. Copyright University of Pennsylvania 2025.
"""
from typing import Any, Dict, NamedTuple as UMLSResult, Sequence, Optional


class SearchResult(UMLSResult):
    ui: str
    rootSource: str
    uri: str
    name: str


class SourceAtomCluster(UMLSResult):
    ui: str
    suppressible: bool
    obsolete: bool
    rootSource: str
    atomCount: int
    cVMemberCount: int
    attributes: str
    atoms: str
    descendants: str
    ancestors: str
    parents: str
    children: str
    relations: str
    definitions: Optional[str]
    concepts: str
    defaultPreferredAtom: str
    name: str


class Concept(UMLSResult):
    ui: str
    suppressible: bool
    dateAdded: str
    majorRevisionDate: str
    status: str
    semanticTypes: Sequence[Dict[str, str]]
    atomCount: int
    attributeCount: 0
    cvMemberCount: 0
    atoms: str
    definitions: str
    relations: str
    defaultPreferredAtom: str
    relationCount: int
    name: str


class Atom(UMLSResult):
    ui: str
    suppressible: bool
    obsolete: bool
    rootSource: str
    termType: str
    code: str
    concept: str
    sourceConcept: str
    sourceDescriptor: str
    attributes: str
    parents: Optional[str]
    ancestors: Optional[str]
    children: Optional[str]
    descendants: Optional[str]
    relations: Optional[str]
    name: str
    language: str


class Definition(UMLSResult):
    sourceOriginated: bool
    rootSource: str
    value: str


class AtomClusterRelation(UMLSResult):
    ui: str
    suppressible: bool
    sourceUi: str
    obsolete: bool
    sourceOriginated: bool
    rootSource: str
    groupId: int
    attributeCount: int
    relatedFromId: str
    relatedFromIdName: str
    relationLabel: str
    additionalRelationLabel: str
    relatedId: str
    relatedIdName: str


class SemanticTypeGroup(UMLSResult):
    abbreviation: str
    expandedForm: str
    semanticTypeCount: int


class SemanticType(UMLSResult):
    abbreviation: str
    ui: str
    definition: str
    example: Optional[str]
    nonHuman: Optional[str]
    usageNote: str
    treeNumber: str
    semanticTypeGroup: SemanticTypeGroup
    name: str
    relations: Sequence[Dict[str, Any]]
    inverseRelations: Sequence[Dict[str, Any]]
    inheritedRelations: Sequence[Dict[str, Any]]
    inverseInheritedRelations: Sequence[Dict[str, Any]]
    childCount: int


class Attribute(UMLSResult):
    ui: str
    sourceUi: Optional[str]
    rootSource: str
    name: str
    value: str


class Relation(UMLSResult):
    relation: str
    type: str
    flag: str
    other: str
    inverseRelation: Optional[str] = None


class PairwiseRelation(UMLSResult):
    relation1: str
    relationType: str
    relation2: str
