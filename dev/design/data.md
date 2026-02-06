# Data subpackage design

Subpackage: src/data

metpyx daata will live in the metpyx/data/ directory. This will be a subpackage of metpyx.
I was thinking of implementing two main classes: XRayQuality and OperationalQuantity.
XRayQuality will store and provide access to the information about a standard x-ray qualities (series, name, filtration parameters).
OperationalQuantity will store and provide access to the information about a standard operational quantity (name, irradiation angles,
mono-energetic conversion coefficients, source).

### Summary for users

The data subpackage holds curated, ready-to-use reference data used across MetPyX: standard x-ray qualities (the named beam
conditions like "N60", "H200") and operational quantities (dose-related quantities such as H*(10), H'(0.07), Hp(...)).

In plain words, this subpackage lets you:
- Look up which standard x-ray qualities are available and what their filtration (inherent and additional) is.
- Ask simple questions such as "what series does this quality belong to?", "what is the voltage encoded in this quality name?",
  and "what are the combined filtration materials and thicknesses for a given quality?".
- Enumerate operational quantities, check which irradiation angles are supported for each quantity, and retrieve human-friendly
  symbols for display.

Typical user workflow:
1. Import the helper class you need, e.g. `from metpyx.data import Qualities` or
   `from metpyx.data import OperationalQuantities`.
2. Create an instance (or use a module-level helper if provided): `q = Qualities()` or `oq = OperationalQuantities()`.
3. Use convenience methods to validate inputs and fetch metadata (example: `q.get_filtration('N60')` or
   `oq.get_irradiation_angles('h_prime_3')`).

This subpackage is intentionally read-only data + lookup utilities: it is not responsible for simulations or conversions, but it
provides the canonical reference values those processes rely on.

### Summary for developers

This subpackage is a small, dependency-free data layer that provides two focused helpers (implemented as classes) and the raw
reference dictionaries they expose. Its goals are to centralize canonical values and to offer a stable, validated API for other
parts of the codebase (simulations, reporting, tests).

Design and implementation notes:
- Data lives as module-level constants (private dicts) and the classes expose safe copies via instance attributes.
- The `Qualities` implementation stores three main dictionaries: `_SERIES`, `_INHERENT_FILTRATION`, and
  `_ADDITIONAL_FILTRATION`. Instance attributes `series`, `inherent_filtration`, and `additional_filtration` are shallow copies
  built in __init__ so callers cannot mutate module globals accidentally.
- The `OperationalQuantities` implementation stores `_OPERATIONAL_QUANTITIES` mapping internal keys to metadata dicts; instances
  expose `operational_quantities` as a copy.
- Public API is intentionally small and synchronous: validation and simple lookups only; errors are communicated by raising
  `ValueError` for unknown inputs.

Developer checklist / recommendations:
- Keep the data dictionaries authoritative and immutable; always return copies for callers that may mutate the result.
- Add type annotations (dataclasses or TypedDict) for meta dictionaries to make IDEs and linters helpful.
- Provide a normalization/alias layer for human symbols vs internal keys (see OperationalQuantities notes below).
- Add unit tests that exercise edge cases (unknown series/quality, filtration merge with overlapping materials, empty additional
  filtration, unsupported angles).

## Qualities class

Class: OperationalQuantities
Module: src/metpyx/data/quantities.py

### Summary for users

The `Qualities` helper gives you a canonical catalog of standard x-ray beam qualities and the filtration specifications that
define them. In everyday use you can:
- Ask which series exist (L, N, W, H) and list the qualities inside a series.
- Query the numeric voltage encoded in a quality name (for example `get_voltage('N60')` -> `60`).
- Retrieve filtration information:
  - `inherent` filtration (what the tube/head provides),
  - `additional` filtration (filters added for the quality), and
  - the combined filtration where like materials are summed.

A typical user flow looks like:
1. `q = Qualities()`
2. `q.get_all_qualities()` or `q.get_qualities('N')`
3. `q.get_filtration('N60')` to get the combined filtration dictionary (material -> thickness)

### Summary for developers

Implementation details (from `src/metpyx/data/qualities.py`):
- Private module-level dictionaries:
  - `_SERIES` maps series code -> list[str] of quality names.
  - `_INHERENT_FILTRATION` maps series -> quality -> {material: thickness}.
  - `_ADDITIONAL_FILTRATION` maps series -> quality -> {material: thickness}.
- Instance attributes (set in `__init__`) are shallow copies of the above to avoid accidental mutation of the module constants:
  - `self.series`, `self.inherent_filtration`, `self.additional_filtration`.

Public methods provided and their behavior:
- `is_series(series: str) -> bool` : validate series codes.
- `is_quality(quality: str) -> bool` : check if a quality is present in any series.
- `get_all_series() -> list[str]` and `get_all_qualities() -> list[str]` : enumeration helpers.
- `get_qualities(series: str) -> list[str]` : returns the qualities for a series or raises `ValueError`.
- `get_series(quality: str) -> str` : returns the series code (first character of quality) or raises `ValueError`.
- `get_voltage(quality: str) -> int` : parses the numeric voltage or raises `ValueError`.
- `get_filtration(quality: str, inherent=False, additional=False) -> dict` : returns one of the filtration dicts or the combined
  filtration (adds additional thicknesses to inherent, summing materials that appear in both).

Error modes and edge cases:
- Unknown inputs raise `ValueError` with clear messages.
- Combined filtration sums overlapping material thicknesses; ensure callers expect this behavior.
- The data currently uses plain dictionaries and numeric values; consider validating numeric types on load.

Developer improvements to consider:
- Add explicit TypedDict or dataclass types for filtration records for stronger typing.
- Add caching or memoization for commonly-requested combined filtration results if performance matters.
- Add explicit unit tests for corner cases (empty additional filtration, same-material sums, unknown quality names).

## OperationalQuantities class

Class: OperationalQuantities
Module: src/metpyx/data/quantities.py

### Summary for users

The `OperationalQuantities` helper stores a small catalog of operational dose quantities and the irradiation angles
supported for each quantity. Use it to:
- See which operational quantities exist and display a human-friendly symbol (e.g. "H*(10)").
- Validate whether a requested irradiation angle is supported for a specific quantity.
- Retrieve metadata that downstream code can use to select conversion coefficients or to drive simulations.

Common user steps:
1. `oq = OperationalQuantities()`
2. `oq.get_all_quantities()` to get internal keys or `oq.get_all_quantities(symbol=True)` to get human symbols.
3. `oq.get_quantity('h_star_10')` for the metadata, `oq.get_irradiation_angles('h_star_10')` for angles.
4. `oq.is_quantity_angle('h_prime_3', 30)` to validate a requested angle.

### Summary for developers

Implementation details (from `src/metpyx/data/quantities.py`):
- Data model: `_OPERATIONAL_QUANTITIES` is a dict mapping an internal key -> metadata dict with fields:
  - `symbol` (str): human-friendly printed symbol, e.g. "H*(10)".
  - `type` (str): small category like 'ambient', 'directional', or 'personal'.
  - `depth` (float|int): reference depth in mm (e.g. 0.07, 3, 10).
  - `phantom` (str|None): optional phantom geometry for personal dose quantities (e.g. 'slab', 'cylinder', 'rod').
  - `angles` (list[int]): list of supported irradiation angles in degrees.
- `__init__` creates `self.operational_quantities` as a copy of the private mapping.
- Provided methods:
  - `get_all_quantities(symbol=False)` : returns internal keys or symbols when `symbol=True`.
  - `is_quantity(quantity)` : membership check for internal keys.
  - `is_quantity_angle(quantity, angle)` : returns True iff the quantity exists and angle is in the quantity's angle list.
  - `get_quantity(quantity)` : returns the metadata dict or raises `ValueError`.
  - `get_irradiation_angles(quantity)` : convenience wrapper returning the `angles` list.
  - `get_symbol(quantity)` : convenience wrapper returning the `symbol`.

Developer notes, caveats and recommended improvements:
- Key naming consistency: the current module mixes lowercase keys (`h_prime_07`) with capitalized keys (`H_p_07_rod`). Prefer a single
  naming style (snake_case lowercase) for internal keys. Document the chosen convention.
- Consider introducing an alias/normalization layer so callers can provide either the human symbol ("H*(10)") or the internal key.
  For example, build `symbol_to_key` mapping at initialization.
- Replace bare metadata dicts with a small dataclass or TypedDict to get type safety and clearer field names; this simplifies tests
  and improves IDE support.
- Validate the `angles` lists on load (types, duplicates, sorted order) so callers don't have to defensively check.
- Add unit tests for membership, angle validation, symbol mapping, and error messages.
- If the operational quantities list grows or needs to be extended from external data sources (CSV/JSON), provide a loader and
  a clear data schema with validation.

