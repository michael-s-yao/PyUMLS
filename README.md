# PyUMLS

A Python client for the Unified Medical Language System (UMLS) REST API.

[![LICENSE](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.md)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/downloads/)
[![CONTACT](https://img.shields.io/badge/contact-michael.yao%40pennmedicine.upenn.edu-blue)](mailto:michael.yao@pennmedicine.upenn.edu)

## Overview

pyUMLS provides a simple, Pythonic interface to the National Library of Medicine's UMLS Terminology Services (UTS) REST API. This client allows you to search for medical concepts, retrieve detailed information about concepts, and navigate the relationships between them.

## Installation

```bash
pip install git+https://github.com/michael-s-yao/PyUMLS.git
```

## Requirements

- Python 3.8+
- A UMLS API key ([request access here](https://uts.nlm.nih.gov/uts/signup-login))

## Quick Start

```python
from pyumls import UMLS

# Initialize client with your API key.
# You can also set the UMLS_API_KEY environment variable.
client = UMLS("YOUR_UMLS_API_KEY")

# Search for concepts.
query = "Alzheimer's Disease"
search_results = client.search(query)
print(search_results)

# Get detailed information about a concept.
cui = "C0002395"
concept_info = client.get_concept(cui, "Concept")
print(concept_info)
```

## Features

  1. Search for concepts by terms or codes
  2. Retrieve detailed information about medical concepts (CUIs)
  3. Access source-specific concept information
  4. Retrieve semantic type information
  5. Find crosswalk/mappings between different source vocabularies

## API Reference

### UMLS Class

#### Initialization

```python
UMLS(
    api_key=os.environ.get("UMLS_API_KEY", ""), 
    version="current"
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_key` | str | Your UMLS API key. Defaults to the `UMLS_API_KEY` environment variable. |
| `version` | str | The UMLS version to use. Defaults to "current". |

#### Methods

##### Search

```python
client = search(
    query,
    input_type="atom",
    search_type="words",
    partial_search=False, 
    return_id_type="concept",
    page_size=32,
    page_number=1,
    **kwargs
)
```

Search for concepts by term or code.

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | str | The term to search for |
| `input_type` | str | Type of search parameter: "atom", "code", "sourceConcept", "sourceDescriptor", "sourceUi", or "tty" |
| `search_type` | str | Type of search to perform: "exact", "words", "leftTruncation", "rightTruncation", "normalizedString", or "normalizedWords" |
| `partial_search` | bool | Whether to return partial matches |
| `return_id_type` | str | Type of identifier to retrieve: "aui", "concept", "code", "sourceConcept", "sourceDescriptor", or "sourceUi" |
| `page_size` | int | Number of results per page |
| `page_number` | int | Page number to retrieve |

##### Get Concept

```python
client.get_concept(cui, return_type, **kwargs)
```

Retrieves information about a specific CUI.

| Parameter | Type | Description |
|-----------|------|-------------|
| `cui` | str | The Concept Unique Identifier (CUI) |
| `return_type` | str | Type of information to retrieve: "Concept", "Atom", "Definition", or "Relation" |

##### Get Source Concept

```python
client.get_source_concept(identifier, return_type, **params)
```

Retrieves information for a source concept.

| Parameter | Type | Description |
|-----------|------|-------------|
| `identifier` | str | The source-asserted identifier |
| `return_type` | str | Type of information to retrieve: "Concept", "Atom", "Parent", "Child", "Ancestor", "Descendant", or "Attribute" |

##### Get Source Description

```python
client.get_source_description(identifier, **kwargs)
```

Retrieves information for a source descriptor.

| Parameter | Type | Description |
|-----------|------|-------------|
| `identifier` | str | The source-asserted identifier |

##### Get Source Code

```python
client.get_source_code(identifier, **kwargs)
```

Retrieves information for a source code.

| Parameter | Type | Description |
|-----------|------|-------------|
| `identifier` | str | The source-asserted identifier |

##### Get Semantic Type

```python
client.get_semantic_type(tui, **kwargs)
```

Retrieves information for a semantic type.

| Parameter | Type | Description |
|-----------|------|-------------|
| `tui` | str | The Type Unique Identifier (TUI) |

##### Get Crosswalk

```python
client.get_crosswalk(source, identifier, target_source=None, **kwargs)
```

Retrieves mappings between different vocabulary sources.

| Parameter | Type | Description |
|-----------|------|-------------|
| `source` | str | The source vocabulary abbreviation |
| `identifier` | str | The source-asserted identifier |
| `target_source` | str | Optional filter by UMLS vocabulary |

## Contact

Questions and comments are welcome. Suggestions can be submitted through GitHub issues. Contact information is linked below.

[Michael Yao](mailto:michael.yao@pennmedicine.upenn.edu)

## License

This project is MIT licensed (see [LICENSE](LICENSE)).