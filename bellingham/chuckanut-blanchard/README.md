# Chuckanut Mountain & Blanchard State Forest

A geospatial dataset and regulatory inventory of the seaside mountain bike singletracks across **Chuckanut Mountain** and **Blanchard State Forest** (Whatcom & Skagit Counties, WA).

---

## Land Management & Regulatory Context

Rising directly from the saltwater shoreline of Samish Bay, Chuckanut and Blanchard Mountains feature some of the steepest, most rugged sandstone terrain in Western Washington:
* **Larrabee State Park:** Managed by the **Washington State Parks and Recreation Commission**. Features strict enforcement against mountain bikes on pedestrian-only conservation footpaths.
* **Blanchard State Forest:** Managed by the **Washington State Department of Natural Resources (WA DNR)**. A working state forest that hosts officially sanctioned technical gravity descents (*Double Black Diamond, Double Down*).
* **Chuckanut Mountain Park:** Managed by **Whatcom County Parks & Recreation**.

---

## Data Sources & Provenance

This dataset was compiled from four primary sources:
1. **OpenStreetMap (OSM) Core API 0.6:** High-resolution extraction covering bounding coordinates `48.600°N to 48.700°N` and `-122.520°W to -122.420°W`.
2. **WA DNR Recreation Geodatabase:** Blanchard State Forest authorized non-motorized trail corridors.
3. **Washington State Parks GIS:** Larrabee State Park boundary and trail inventory.
4. **Trailforks Regions 1686 & 1687:** Regional ground truth for Chuckanut and Blanchard gravity lines.

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

## File Manifest

| Filename | Format | Description |
| :--- | :--- | :--- |
| `chuckanut_sanctioned.geojson` | GeoJSON | Complete WGS84 feature collection of the 60 sanctioned singletracks with IMBA ratings, lengths, and tags. |
| `chuckanut_sanctioned.kml` | KML 2.2 | Styled KML vector placemarks for CalTopo, Gaia GPS, and Google Earth. |
| `chuckanut_sanctioned.gpx` | GPX 1.1 | Vector tracks enriched with `<tf:difficulty>` and `<gpxx:DisplayColor>` tags. |
| `chuckanut_unsanctioned.geojson` | GeoJSON | Vector feature collection of the 24 unsanctioned and pirate singletracks. |
| `chuckanut_unsanctioned.kml` | KML 2.2 | Styled KML placemarks in Blaze Orange (`#ea580c`). |
| `chuckanut_unsanctioned.gpx` | GPX 1.1 | Unsanctioned tracks for offline GPS navigation. |
