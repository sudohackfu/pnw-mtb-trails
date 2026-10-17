# Chuckanut Mountain & Blanchard State Forest

A geospatial dataset and regulatory inventory of the seaside mountain bike singletracks across **Chuckanut Mountain** and **Blanchard State Forest** (Whatcom & Skagit Counties, WA).

---

## Datasets & Exact API Specifications

| Dataset / Source | Exact API Endpoint / Spatial Identifier | Purpose in Analysis |
| :--- | :--- | :--- |
| **OpenStreetMap Core API 0.6** | Bounding box: `(-122.520, 48.600, -122.420, 48.700)` | Way geometry, node elevations, surface materials, and trail tags. |
| **WA DNR Blanchard Recreation Plan** | WA DNR Forest Practices GIS Portal | Blanchard State Forest authorized non-motorized trail network. |
| **Washington State Parks GIS** | Larrabee State Park Boundary & Facility Inventory | Auditing pedestrian-only conservation restrictions (`bicycle=no`). |
| **Trailforks Regions 1686 & 1687** | Chuckanut & Blanchard Directories | Community ground truth for seaside gravity descents and pirate lines. |

---

## Land Management & Regulatory Context

Rising directly from the saltwater shoreline of Samish Bay, Chuckanut and Blanchard Mountains feature some of the steepest, most rugged sandstone terrain in Western Washington:
* **Larrabee State Park:** Managed by the **Washington State Parks and Recreation Commission**. Features strict enforcement against mountain bikes on pedestrian-only conservation footpaths.
* **Blanchard State Forest:** Managed by the **Washington State Department of Natural Resources (WA DNR)**. A working state forest that hosts officially sanctioned technical gravity descents (*Double Black Diamond, Double Down*).
* **Chuckanut Mountain Park:** Managed by **Whatcom County Parks & Recreation**.

---

## Trail Naming Derivation Methodology

1. **Official Ground-Truth Gravity Lines:**
   * *Double Black Diamond (DBD)*: The classic 1,500-ft technical descent over steep sandstone rock faces and root drops.
   * *Double Down*: The expert-tier lower extension featuring high-speed rock steps and steep transitions.
   * *Hush Hush Trail*: Steep technical black-diamond descent dropping off Chuckanut Ridge.
   * *Dan's Traverse Trail, Hemlock Trail, Cinco, Quattro, Raptor Ridge, Salal Trail, Fern Trail*.
2. **Community-Maintained Pirate Singletracks:**
   * *Fiona Ridge*: Exposed, technical pirate ridgeline singletrack cut along the cliff crests.
   * *Rooty Ridge & Rooty Ridge Lower*: Raw, hand-cut loam and root chutes dropping toward Samish Bay.
   * *21 Unnamed Informal Lines*: Hand-cut bandit chutes and bypass singletracks referenced by their OSM Way ID (e.g., *Unnamed Trail (1138172036)*).
3. **Excluded Pedestrian-Only Footpaths:**
   * In strict accordance with our methodology, sanctioned walking trails where bikes are legally prohibited (`bicycle=no`) are excluded: *Fragrance Lake Trail*, *Fragrance Lake Cliff Trail*, *Rock Trail*, *Chinscraper*, and *(PNT) Samish Bay Connector*.

---

## Trail Inventory & Difficulty Breakdown

* **Total Singletrack Segments:** 84
* **Sanctioned MTB Singletracks:** 60 segments (36 unique trail names)
* **Unsanctioned MTB Singletracks:** 24 segments (24 unique lines)
* **Gravel Fire Roads / Logging Spurs:** 9 segments filtered out (`BL-1616`, `DNR B-1600`, `Lost Lake Road`, `Pacific Rim Drive`).

### Sanctioned Singletrack Difficulty Distribution

| Rating Tier | IMBA Scale | Hex Color | Count | Key Trails |
| :--- | :--- | :--- | :--- | :--- |
| **Double Black** | Level 4 | `#000000` | 2 segments | *Double Down* (High-consequence rock steps and technical drops) |
| **Black Diamond** | Level 3 | `#dc2626` | 7 segments | *Double Black Diamond (DBD), Hush Hush Trail, Madrone Crest Trail, Ridge Trail* |
| **Blue Square** | Level 2 | `#0284c7` | 46 segments | *Dan's Traverse Trail, Hemlock Trail, Cinco, Quattro, Raptor Ridge, Salal Trail, Fern Trail, Lost Lake Singletrack links* |
| **Green Circle** | Level 1 | `#22c55e` | 5 segments | *Clayton Beach Trail, Interurban connector spurs* |

### Unsanctioned Singletrack Roster (`#ea580c` Blaze Orange)
* *Fiona Ridge* (Exposed rocky cliffline singletrack; Level 3 Black Diamond)
* *Rooty Ridge* (Dense root-carpet technical descent; Level 3 Black Diamond)
* *Rooty Ridge Lower* (Steep fall-line loam chute; Level 3 Black Diamond)
* *21 Unnamed Informal Singletrack Lines* (Active underground pirate descents)

---

## Reproducible Build Script

The complete pipeline to re-query the OSM data, strip fire roads, isolate singletracks, apply ratings, and export all vector formats is provided in the local `scripts/` directory:

```bash
# From within this directory:
python scripts/build_chuckanut.py
```

### Script Manifest:
* **[`scripts/build_chuckanut.py`](./scripts/build_chuckanut.py):** Standalone Python script that queries the Chuckanut bounding box, applies the pedestrian filter, resolves ratings and names, and generates `chuckanut_sanctioned` and `chuckanut_unsanctioned` (GeoJSON, KML 2.2, GPX 1.1).

---

## File Manifest

| Filename | Format | Description |
| :--- | :--- | :--- |
| `chuckanut_sanctioned.geojson` | GeoJSON | Complete WGS84 feature collection of the 60 sanctioned singletracks with IMBA ratings, lengths, and tags. |
| `chuckanut_sanctioned.kml` | KML 2.2 | Styled KML vector placemarks for CalTopo, Gaia GPS, and Google Earth. |
| `chuckanut_sanctioned.gpx` | GPX 1.1 | Vector tracks enriched with `<tf:difficulty>` and `<gpxx:DisplayColor>` tags. |
| `chuckanut_unsanctioned.geojson` | GeoJSON | Vector feature collection of the 24 unsanctioned and pirate singletracks. |
| `chuckanut_unsanctioned.kml` | KML 2.2 | Styled KML placemarks in Blaze Orange (`#ea580c`). |
| `chuckanut_unsanctioned.gpx` | GPX 1.1 | Unsanctioned tracks for offline GPS navigation. |
