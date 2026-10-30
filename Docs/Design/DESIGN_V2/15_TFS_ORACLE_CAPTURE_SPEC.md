# 15 — CANONICAL TFS ORACLE CAPTURE SPEC

## Why this file exists
This ChatGPT session has the handoff snapshot but not executable access to the local `C:/Users/handl/Downloads/tfs-budtender` source. Exact expected recommendations must therefore be captured locally rather than invented.

## Authority
Use shipped/local-matching **v7.11.4** only:
- source: `dev/v7114/tool.html`
- baked site: `deploy/2026-10-30-v7114/site/`

Do not snapshot unreleased v7.11.5 behavior into canonical tests.

## Fixture capture process
For every QA case with TFS involvement:
1. construct deterministic inventory fixture from real current/canonical test data;
2. construct exact `KnownCustomerProfile` fixture;
3. build TFS input through the same production adapter used by the game;
4. execute v7.11.4;
5. serialize only deterministic, PII-free output fields needed for parity;
6. hash input and output;
7. store fixture under game test data;
8. run the same fixture through Unity port/RecommendationService;
9. assert semantic parity.

## Snapshot schema

```yaml
TfsOracleFixture:
  oracle_version: v7.11.4
  fixture_id: string
  input_hash: sha256
  inventory_fixture_hash: sha256
  mode: SEARCH | FLOOR | SIMILAR | COMPARE
  normalized_output:
    ordered_result_ids: []
    exposed_scores_if_any: []
    effect_labels: []
    anxiety_risk_if_exposed: []
    time_of_use_if_exposed: []
    dominant_category_if_exposed: []
    flavor_profile_if_exposed: []
  output_hash: sha256
```

Only fields actually exposed/owned by canonical TFS are captured. Do not add invented test-only chemistry fields.

## Parity tolerances
- ordered IDs: exact unless canonical implementation documents a stable tie rule requiring set-equivalence;
- numeric values: exact or documented serialization tolerance only;
- labels/categories: exact normalized text;
- inventory eligibility: exact.

## Difficulty parity matrix
Every core TFS fixture executes under Beginner, Standard and Expert game configurations with identical known profile/inventory. Expected oracle hash is identical.

## Known-input refinement test
For ambiguity tests, capture **two** fixtures:
- before legitimate question answer;
- after answer is appended to KnownCustomerProfile.

A changed result is valid only because the input hash changed.

## Similar/repeat tests
Repeat memory is translated into legitimate current input/reference context, then canonical Similar is executed. History never writes directly into result ordering.

## Failure output
On parity failure log:
- fixture ID;
- oracle version;
- input hash;
- expected output hash;
- actual output hash;
- first differing normalized field.

Do not silently update snapshots. Any oracle refresh requires an explicit canonical TFS version decision.
