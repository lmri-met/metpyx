# MetPyX Design overview

## Purpose

MetPyX provides tooling for x-ray metrology labs to store standard x-ray qualities and operational data, run spectra
simulations, compute derived integral and operational quantities, and perform sensitivity analysis in spectrum and
derived quantities due to x-ray tube parameter variations.

## Scope

- Two initial features:
    - Data layer: store and retrieve standard x-ray qualities and their x-ray tube parameters.
    - Simulation layer: compute spectra and integral quantities (some of them using SpekPy), perform sensitivity
      analysis.
- Future: more metrology features (spectrometry, calibrations, etc.).

## High-level architecture (Modules, major components, and responsibilities)

- metpyx/ — package code
- metpyx/data/ — data model and persistence?
- metpyx/sim/ — SpekPy integration and simulation wrappers
- examples/notebooks/ — user notebooks

## Data model (conceptual)

- XRayQuality
    - series (N, L, W, H)
    - qualities in each series (N-60, N-80, etc.)
    - filtration parameters (inherent and additional filtration)
    - derived properties: high voltage (from name)
- OperationalQuantity
    - name (e.g., H*(10), H'(0.07))
    - irradiation angles per quality
    - mono-energetic conversion coefficients per energy and angle
    - provenance/source for coefficients

## Simulation layer

### Integration with SpekPy

- Use SpekPy for spectral simulation and basic integral quantities (mean energy, air kerma, HVL).
- MetPyX responsibilities:
    - Manage/serve standard quality parameter sets to SpekPy.
    - Compute operational quantities not provided by SpekPy (mean conversion coefficient, full operational quantity
      pipeline).
    - Provide an API to select transfer coefficient set (NIST vs Penelope) and CMI/ISO sources for conversion
      coefficients.
- Investigate SpekPy internals to locate mono\-energetic transfer coefficients and integration points.
- Compute mean conversion coefficients by folding mono\-energetic coefficients with simulated spectra.
- Compute operational quantities using mean conversion coefficients and air kerma from SpekPy?

### Sensitivity analysis

- Provide sensitivity analysis:
    - Vary one parameter at a time (kVp, additional filtration thickness, additional filtration purity).
    - Report sensitivity of spectra and derived integral quantities.
- Implement a routine to compute maximum allowable parameter deviation to meet a tolerance (e.g., 2\% variation in mean
  conversion coefficient).

## Public API (Key classes/functions and intended usage patterns)

## Dependencies & rationale (Major third-party choices and why)

- SpekPy: established and widely used x-ray spectrum simulation library.

## Testing strategy

- testpy and pytest-cov.
- Integration test using one quality, verify numerical values.

## Acceptance criteria

- CRUD API for standard qualities and operational quantities?
- Integration tests that run SpekPy simulations using stored quality parameters.
- Implementation of mean conversion coefficient calculation and sensitivity analysis.
- Ability to select coefficient source (NIST or Penelope) at runtime.

## Open questions / next steps

- Locate and document where SpekPy stores mono-energetic transfer coefficients and whether they are exportable.
- Decide on default persistence format for qualities (YAML/JSON/SQLite).
- Implement a small prototype: store one series (N-) qualities, simulate with SpekPy, compute one operational quantity.