#!/usr/bin/python3
"""
Utility functions.

Author(s):
    Michael Yao @michael-s-yao

Licensed under the MIT License. Copyright University of Pennsylvania 2025.
"""
from typing import Any, Dict, Sequence, Union

from . import base


def parse_json_results(
    results: Union[Dict[str, Any], Sequence[Dict[str, Any]]]
) -> Union[base.UMLSResult, Sequence[base.UMLSResult], Dict[str, Any]]:
    """
    Parses the JSON results returned from UMLS into expected Python objects.
    Input:
        results: a dictionary or list of dictionaries of the result(s).
    Returns:
        The result or list of result(s) as the expected Python object.
    """
    if isinstance(results, list):
        return list(map(lambda result: parse_json_results(result), results))

    for key, val in results.items():
        if isinstance(val, str) and val.upper() == "NONE":
            results[key] = None
        elif isinstance(val, list) or (
            isinstance(val, dict) and (
                val.get("classType", "") == "SemanticGroup"
            )
        ):
            results[key] = parse_json_results(val)

    if "classType" not in results.keys() and "relation" in results.keys():
        return base.Relation(**results)
    elif "classType" not in results.keys() and "relation1" in results.keys():
        return base.PairwiseRelation(**results)
    elif "classType" not in results.keys():
        return results

    if results["classType"] == "searchResults":
        return list(
            map(lambda result: base.SearchResult(**result), results["results"])
        )

    cls = getattr(
        base,
        results.pop("classType").replace("SemanticGroup", "SemanticTypeGroup")
    )
    return cls(**results)
