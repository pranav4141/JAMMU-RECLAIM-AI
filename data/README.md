# Data
- `jammu_district_boundary.geojson` — Jammu District polygon, Census of India 2011 (DataMeet `Districts/Census_2011`, DT_CEN_CD 21), simplified. Rebuild: `python3 data/build_data.py <2011_Dist shapefile prefix>`.
- `sites.json`, `changes.json` — **simulated prototype data**, sampled inside the boundary (≥~1.3 km from its edge) and validated.
- `validation_report.json` — audit of the earlier dataset (8 of 42 outside) and of the regenerated one.
- `test_geo.py` — geographic test (`python3 data/test_geo.py`); frontend equivalent: `cd frontend && npm test`.
After rebuilding, copy the three JSON files to `frontend/public/` (boundary as `boundary.json`).
