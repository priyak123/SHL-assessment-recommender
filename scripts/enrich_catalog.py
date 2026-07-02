import json
import os
import sys

# Add data folder to path to import test_mappings
sys.path.append('data')
try:
    import test_mappings
    KEY_MAP = test_mappings.KEY_MAP
    trace_recs = test_mappings.trace_recs
except ImportError:
    # Fallback mappings if import fails
    KEY_MAP = {
        'Ability & Aptitude': 'A',
        'Assessment Exercises': 'E',
        'Biodata & Situational Judgment': 'B',
        'Competencies': 'C',
        'Development & 360': 'D',
        'Knowledge & Skills': 'K',
        'Personality & Behavior': 'P',
        'Simulations': 'S'
    }
    trace_recs = {}

with open("data/catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f, strict=False)

# Enrich catalog items
enriched_catalog = []
for item in catalog:
    # Set URL field matching schema
    item['url'] = item.get('link', '')
    
    # Try to find test_type in trace_recs by URL matching
    test_type = None
    for name, rec in trace_recs.items():
        if rec['url'] == item['url']:
            test_type = rec['test_type']
            break
            
    if test_type is None:
        mapped = [KEY_MAP[k] for k in item.get('keys', []) if k in KEY_MAP]
        test_type = ", ".join(mapped)
        
    item['test_type'] = test_type
    enriched_catalog.append(item)

with open("data/catalog.json", "w", encoding="utf-8") as f:
    json.dump(enriched_catalog, f, indent=2, ensure_ascii=False)

print("Catalog enriched successfully with test_type and url!")
