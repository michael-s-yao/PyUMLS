#!/usr/bin/python3
"""
Unified Medical Language System (UMLS) Python API Client.

Author(s):
    Michael Yao @michael-s-yao

Licensed under the MIT License. Copyright University of Pennsylvania 2025.
"""
import requests
import os
import urllib.parse
from typing import Any, Dict, Final, Optional

from .base import UMLSResult
from .utils import parse_json_results


class UMLS:
    base_url: Final[str] = "https://uts-ws.nlm.nih.gov/rest"

    def __init__(
        self,
        api_key: str = os.environ.get("UMLS_API_KEY", ""),
        version: str = "current"
    ):
        """
        Args:
            api_key: user UMLS API key. Default read from UMLS_API_KEY
                environment variable.
            version: The UMLS version to use (default is "current").
        """
        self.__api_key: Final[str] = api_key
        assert len(self.__api_key), "Please specify a UMLS API key."
        self.version: Final[str] = version
        self._session = requests.Session()

    def _get_request(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> UMLSResult:
        """
        Send a GET request to the UMLS API.
        Input:
            endpoint: the API endpoint to send a GET request to.
            params: optional query parameter(s) to include in the request.
        Returns:
            The response object from the API.
        """
        if params is None:
            params = {}
        params["apiKey"] = self.__api_key
        response = self._session.get(
            f"{self.base_url}/{endpoint}", params=params
        )
        response.raise_for_status()
        return parse_json_results(response.json()["result"])

    def search(
        self,
        query: str,
        input_type: str = "atom",
        search_type: str = "words",
        partial_search: bool = False,
        return_id_type: str = "concept",
        page_size: int = 32,
        page_number: int = 1,
        **kwargs
    ) -> UMLSResult:
        """
        Searches for concepts by term or code.
        Input:
            query: a human-readable term to search for.
            input_type: the data type to use as the search parameter.
            search_type: the type of search you wish to use.
            partial_search: whether to return partial matches for the query.
            return_id_type: the type of identifier to retrieve.
            page_size: the number of results to include per page.
            page_number: which page of results to fetch.
        Returns:
            Search results containing matching concepts.
        """
        assert input_type in [
            "atom",
            "code",
            "sourceConcept",
            "sourceDescriptor",
            "sourceUi",
            "tty"
        ]
        assert search_type in [
            "exact",
            "words",
            "leftTruncation",
            "rightTruncation",
            "normalizedString",
            "normalizedWords"
        ]
        assert return_id_type in [
            "aui",
            "concept",
            "code",
            "sourceConcept",
            "sourceDescriptor",
            "sourceUi"
        ]
        assert page_size > 0
        assert page_number > 0

        params = kwargs
        params.update({
            "string": query,
            "inputType": input_type,
            "searchType": search_type,
            "partialSearch": partial_search,
            "returnIdType": return_id_type,
            "pageSize": page_size,
            "pageNumber": page_number,
        })

        return self._get_request(f"search/{self.version}", params)

    def get_concept(self, cui: str, return_type: str, **kwargs) -> UMLSResult:
        """
        Retrieves information about a known CUI.
        Input:
            cui: the Concept Unique Identifier (CUI) to retrieve info about.
            return_type: the type of information to retrieve. One of
                [`Concept`, `Atom`, `Definition`, `Relation`].
        Returns:
            Information about the concept.
        """
        assert return_type in ["Concept", "Atom", "Definition", "Relation"]
        endpoint = f"content/{self.version}/CUI/{cui}/{return_type.lower()}s"
        endpoint = endpoint.replace("/concepts", "")
        return self._get_request(endpoint, **kwargs)

    def get_source_concept(
        self, identifier: str, return_type: str, **params
    ) -> UMLSResult:
        """
        Retrieves information for a source concept.
        Input:
            identifier: the source-asserted identifier.
            return_type: the type of information to retrieve. One of [
                `Concept`, `Atom`, `Parent`, `Child`, `Ancestor`, `Descendant`,
                `Attribute`].
        Returns:
            Information about the source concept.
        """
        endpoint = f"content/{self.version}/source/SNOMEDCT_US/"
        endpoint += urllib.parse.quote(identifier)
        assert return_type in [
            "Concept",
            "Atom",
            "Parent",
            "Child",
            "Ancestor",
            "Descendant",
            "Attribute"
        ]
        if return_type == "Concept":
            endpoint += ""
        elif return_type == "Child":
            endpoint += "/" + return_type.lower() + "ren"
        else:
            endpoint += "/" + return_type.lower() + "s"

        return self._get_request(endpoint, **params)

    def get_source_description(self, identifier: str, **kwargs) -> UMLSResult:
        """
        Retrieves information for a source descriptor.
        Input:
            identifier: the source-asserted identifier.
        Returns:
            Information for the source descriptor.
        """
        endpoint = f"content/{self.version}/source/MSH/{identifier}"
        return self._get_request(endpoint, **kwargs)

    def get_source_code(self, identifier: str, **kwargs) -> UMLSResult:
        """
        Retrieves information for a source code.
        Input:
            identifier: the source-asserted identifier.
        Returns:
            Information for the source code.
        """
        endpoint = f"content/{self.version}/source/LNC/{identifier}"
        return self._get_request(endpoint, **kwargs)

    def get_semantic_type(self, tui: str, **kwargs) -> UMLSResult:
        """
        Retrieves information for a known Semantic Type identifier (TUI).
        Input:
            tui: The Type Unique Identifier (TUI).
        Returns:
            Information about the semantic type
        """
        endpoint = f"semantic-network/{self.version}/TUI/{tui}"
        return self._get_request(endpoint, **kwargs)

    def get_crosswalk(
        self,
        source: str,
        identifier: str,
        target_source: Optional[str] = None,
        **kwargs
    ) -> UMLSResult:
        """
        Retrieves all source-asserted identifiers that share a UMLS CUI
        with a particular code.
        Input:
            source: the source vocabulary abbreviation.
            identifier: the source-asserted identifier.
            target_source: filter by an optional UMLS vocabulary.
        Returns:
            Crosswalk information for the specified concept.
        """
        params = kwargs
        if target_source:
            params["targetSource"] = target_source

        endpoint = f"crosswalk/{self.version}/source/{source}/"
        endpoint += f"{urllib.parse.quote(identifier)}"
        return self._get_request(endpoint, params)
