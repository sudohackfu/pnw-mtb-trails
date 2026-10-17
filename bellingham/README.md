# Bellingham & Whatcom County Mountain Bike Networks

Bellingham and Whatcom County represent the premier mountain biking hub in Washington State. Spanning glacial ridges, coastal sandstone bluffs, and active working forests, the region features an interconnected ecosystem of legally sanctioned trail networks coexisting with historic underground freeride lines.

---

## Regional Geography & Mountain Systems

The Bellingham library is divided into three distinct mountain systems:

`	ext
bellingham/
??? README.md                           # Regional overview, sources & easement guide
?
??? galbraith-mountain/                 # Galbraith Mountain (North & South)
?   ??? README.md                       # Easement history, jump complexes & trail roster
?   ??? galbraith_sanctioned.geojson / .kml / .gpx
?   ??? galbraith_unsanctioned.geojson / .kml / .gpx
?   ??? scripts/
?       ??? build_galbraith.py          # Standalone OSM builder & vector generator
?       ??? community_index.json        # Community trail index with overrides & sources
?
??? chuckanut-blanchard/                # Chuckanut Mountain & Blanchard State Forest
?   ??? README.md                       # Larrabee State Park & DNR seaside gravity lines
?   ??? chuckanut_sanctioned.geojson / .kml / .gpx
?   ??? chuckanut_unsanctioned.geojson / .kml / .gpx
?   ??? scripts/
?       ??? build_chuckanut.py          # Standalone OSM builder & vector generator
?       ??? community_index.json        # Community trail index with overrides & sources
?
??? lookout-mountain/                   # Lookout Mountain, Lake Whatcom & Stewart Mountain
    ??? README.md                       # County forest preserve & Stewart Mountain lines
    ??? lookout_sanctioned.geojson / .kml / .gpx
    ??? lookout_unsanctioned.geojson / .kml / .gpx
    ??? scripts/
        ??? build_lookout.py            # Standalone OSM builder & vector generator
        ??? community_index.json        # Community trail index with overrides & sources
`

---

## Regional Land Governance & Legal Baselines

1. **The Galbraith Mountain Recreation Use Easement (2,182 Acres):**
   * **Parties:** City of Bellingham, Whatcom Land Trust, and *Galbraith Tree Farm, LLC* (Whatcom County Auditor File Nos. 2018-0803004 / 2018-0807005).
   * **Stewardship:** Whatcom Mountain Bike Coalition (WMBC).
   * **Legal Effect:** Permanently secured non-motorized public recreation across the entire commercial tree farm. All WMBC-adopted trails inside this boundary are fully legal and sanctioned (399 sanctioned singletrack segments).
2. **Chuckanut Mountain & Larrabee State Park:**
   * **Jurisdiction:** Washington State Parks and Recreation Commission (Larrabee) and Washington State Department of Natural Resources (Blanchard State Forest).
   * **Regulatory Dynamic:** Steep sandstone bluffs dropping into Samish Bay. Strict enforcement against bicycle access on pedestrian-only conservation trails (*Fragrance Lake, Rock Trail*), alongside officially adopted double-black descents (*Double Black Diamond, Double Down*).
3. **Lookout Mountain Forest Preserve & Lake Whatcom:**
   * **Jurisdiction:** Whatcom County Parks & Recreation Department and WA DNR.
   * **Focus:** Deep forested ridges featuring sustained downhill flow (*Cougar Ridge, Floam*) and long-standing community-built singletracks on Stewart Mountain (*#5, #8, Brown Pow, Chanterelle*).

---

## Data Provenance & Methodology Summary

All datasets in this directory strictly adhere to the master methodology defined in the root [README.md](../README.md):
* **Programmatic First -> Community Index Override:** Official park singletracks are parsed dynamically from live APIs. Community research (builder lore, Strava segment leaderboards) lives cleanly in external community_index.json files with "override": true flags, preventing brittle hardcoded dictionaries in Python scripts.
* **Zero Generic Placeholders:** Candidate spurs under review ("override": false) that lack verified names are excluded from vector exports. 100% of exported trails carry authentic official or community names.
* **Singletrack Isolation:** All gravel logging roads (RD 2000 series, Tower Road, BL-1616, OC-17) were stripped out, preserving 100% pure singletrack trails.
* **Pedestrian Exclusion:** Sanctioned footpaths that prohibit bicycles (icycle=no) are excluded.
* **Rating Resolution:** Every trail carries an IMBA rating (1?5) and Trailforks hex color (#22c55e Green, #0284c7 Blue, #dc2626 Black, #000000 Double Black, #8b5cf6 Pro-Line).

---

## Regional Singletrack Inventory

| Mountain System | Sanctioned Segments | Unsanctioned Segments | Excluded Candidate Spurs | Key Lines |
| :--- | :--- | :--- | :--- | :--- |
| **Galbraith Mountain** | 399 | 12 | 119 | *Blue Steel, Evolution, U-Line, Mohawk, Old Keystone, Scorpion (old)* |
| **Chuckanut & Blanchard** | 96 | 13 | 70 | *Double Down, DBD, Hush Hush, Fiona Ridge, Rooty Ridge* |
| **Lookout & Stewart Mtn** | 61 | 13 | 63 | *Cougar Ridge, Floam, Brown Pow, #5, #8, BR* |
| **Total Bellingham** | **556** | **38** | **252** | **100% Authentic Names Across All Systems** |
