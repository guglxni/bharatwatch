# Graph Report - bharatwatch  (2026-08-20)

## Corpus Check
- 44 files · ~10,336 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 111 nodes · 96 edges · 8 communities detected
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 10 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 10|Community 10]]

## God Nodes (most connected - your core abstractions)
1. `run_source()` - 11 edges
2. `CLI` - 6 edges
3. `compute_diff()` - 5 edges
4. `Handler` - 4 edges
5. `Snapshot` - 3 edges
6. `Change` - 3 edges
7. `HealEvent` - 3 edges
8. `validate_items()` - 3 edges
9. `heal_source()` - 3 edges
10. `item_key()` - 2 edges

## Surprising Connections (you probably didn't know these)
- `test_diff_created()` --calls--> `compute_diff()`  [INFERRED]
  tests/test_diff.py → bharatwatch/core/diff_engine.py
- `test_diff_updated()` --calls--> `compute_diff()`  [INFERRED]
  tests/test_diff.py → bharatwatch/core/diff_engine.py
- `run_source()` --calls--> `compute_hash()`  [INFERRED]
  bharatwatch/core/orchestrator.py → bharatwatch/core/diff_engine.py
- `run_source()` --calls--> `compute_diff()`  [INFERRED]
  bharatwatch/core/orchestrator.py → bharatwatch/core/diff_engine.py
- `run_source()` --calls--> `Snapshot`  [INFERRED]
  bharatwatch/core/orchestrator.py → bharatwatch/core/models.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.18
Nodes (6): BaseModel, CollegecutoffItem, MandiwatchItem, NauktrialertItem, StartuppulseItem, TendersentryItem

### Community 1 - "Community 1"
Cohesion: 0.33
Nodes (8): load_module_schema(), parse_output(), run_all(), run_module(), run_source(), trigger_collector(), build_validator(), validate_items()

### Community 2 - "Community 2"
Cohesion: 0.33
Nodes (7): Base, heal_monitor(), heal_source(), Change, HealEvent, Snapshot, Source

### Community 4 - "Community 4"
Cohesion: 0.25
Nodes (2): fetchHealEvents(), HealLog()

### Community 5 - "Community 5"
Cohesion: 0.48
Nodes (1): CLI

### Community 6 - "Community 6"
Cohesion: 0.38
Nodes (5): compute_diff(), compute_hash(), item_key(), test_diff_created(), test_diff_updated()

### Community 8 - "Community 8"
Cohesion: 0.4
Nodes (2): Handler, SimpleHTTPRequestHandler

### Community 10 - "Community 10"
Cohesion: 0.5
Nodes (2): Badge(), cn()

## Knowledge Gaps
- **Thin community `Community 4`** (8 nodes): `fetchChanges()`, `fetchHealEvents()`, `fetchHealth()`, `fetchModules()`, `fetchSources()`, `page.tsx`, `api.ts`, `HealLog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 5`** (7 nodes): `__main__.py`, `CLI`, `.heal_monitor()`, `.init_db()`, `.run_all()`, `.run_module()`, `.serve()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 8`** (5 nodes): `Handler`, `.end_headers()`, `.translate_path()`, `SimpleHTTPRequestHandler`, `server.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 10`** (4 nodes): `Badge()`, `badge.tsx`, `utils.ts`, `cn()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_source()` connect `Community 1` to `Community 2`, `Community 6`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `compute_diff()` connect `Community 6` to `Community 1`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `run_source()` (e.g. with `validate_items()` and `compute_hash()`) actually correct?**
  _`run_source()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `compute_diff()` (e.g. with `run_source()` and `test_diff_created()`) actually correct?**
  _`compute_diff()` has 3 INFERRED edges - model-reasoned connections that need verification._