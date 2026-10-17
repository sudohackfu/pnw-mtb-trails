# Lookout Mountain & Lake Whatcom Networks

A comprehensive geospatial dataset of the mountain bike singletrack trails across **Lookout Mountain Forest Preserve**, **Lake Whatcom Park**, and **Stewart Mountain** (Whatcom County, WA).

---

## Land Management & Historical Context

Situated along the eastern flank of Lake Whatcom, this network spans county park preserve lands and state timber:
* **Lookout Mountain Forest Preserve:** Managed by **Whatcom County Parks & Recreation**. Features modern, machine-built and hand-finished gravity descents (*Cougar Ridge, Floam*) built to relieve trail pressure on Galbraith.
* **Lake Whatcom Park & Stewart Mountain:** Features long sustained climbs and descents (*Chanterelle, Brown Pow*). Historically, Stewart Mountain hosted underground rogue freeride tracks (*Surfin' Turf, Brown Pow*), some of which were adopted by the county while others were decommissioned.
* **Stimpson Family Nature Reserve (Conservation Boundary):** Directly adjacent to Lookout Mountain, this 350-acre reserve is strictly preserved for wildlife habitat; **all bicycle access is prohibited by county code**.

---

## Data Sources & Provenance

This dataset was compiled from four primary sources:
1. **OpenStreetMap (OSM) Core API 0.6:** Multi-tile extraction covering bounding coordinates `48.690°N to 48.780°N` and `-122.380°W to -122.240°W`.
2. **Whatcom County Parks & Recreation Department Master Plan:** Official trail alignment and conservation boundary geodatabase.
3. **WA DNR Olsen Creek Block GIS:** Public forest practices recreation corridors.
4. **Trailforks Region 17820 & Lake Whatcom Records:** Ground-truth confirmation of rideable descents and condition reports.

---

## Trail Naming Derivation Methodology

1. **Official Ground-Truth Singletracks:**
   * *Cougar Ridge Trail*: The premier 1,400-ft descent on Lookout Mountain (fast berms, natural timber flow, technical root carpets).
   * *Floam*: Steep, deep-loam technical descent dropping off the upper ridgeline.
   * *Brown Pow*: The famous descent in Lake Whatcom Park (bermed turns, tabletop jumps, and steep loamy switchbacks).
   * *Rufus Creek Trail (Rufous Creek)*: Sustained technical descent linking the upper logging benches.
   * *Chanterelle Trail, El Diablo, Moto's Run, Bottoms Up, Hooty Hoot, Waterfall Trail (Gnargus), Baneberry Trail, Creekside Trail, Earth Star, Turkey Tail*.
2. **Community-Maintained Pirate Singletracks:**
   * *#5 & #8*: Active, user-maintained dirt singletracks cut through the timber on Stewart Mountain above Lake Whatcom.
   * *BR*: Historical abandoned/unauthorized singletrack line (`#475569`).
   * *18 Unnamed Informal Singletrack Lines*: Rogue cuts and bandit chutes referenced cleanly by their topological OSM Way ID (e.g., *Unnamed Trail (1470422399)*).
3. **Excluded Pedestrian-Only Footpaths:**
   * Official walking trails in the Stimpson Family Nature Reserve where bikes are prohibited (`bicycle=no`) are excluded: *Stimpson Main Loop*, *Strawberry Falls Trail*, *Leila June Trail*, and *Geneva Pond Loop*.

---

## Trail Inventory & Difficulty Breakdown

* **Total Singletrack Segments:** 71
* **Sanctioned MTB Singletracks:** 50 segments (30 unique trail names)
* **Unsanctioned MTB Singletracks:** 21 segments (21 unique lines)
* **Gravel Fire Roads / Service Doubletracks:** 3 segments filtered out (`OC-ML`, `OC-17`, `Seed Orchard Trail`).

### Sanctioned Singletrack Difficulty Distribution

| Rating Tier | IMBA Scale | Hex Color | Count | Key Trails |
| :--- | :--- | :--- | :--- | :--- |
| **Black Diamond** | Level 3 | `#dc2626` | 4 segments | *Cougar Ridge Trail, Floam, Brown Pow* |
| **Blue Square** | Level 2 | `#0284c7` | 38 segments | *Rufus Creek Trail, Chanterelle Trail, El Diablo, Moto's Run, Bottoms Up, Hooty Hoot, Waterfall Trail (Gnargus), Earth Star, Turkey Tail, Baneberry Trail* |
| **Green Circle** | Level 1 | `#22c55e` | 8 segments | *Creekside Trail, Lake Louise Road Connector, Backside Trail links* |

### Unsanctioned Singletrack Roster (`#ea580c` Orange / `#475569` Slate)
* *#5* (Stewart Mountain user-maintained singletrack; Level 3 Black Diamond; `#ea580c`)
* *#8* (Stewart Mountain user-maintained singletrack; Level 3 Black Diamond; `#ea580c`)
* *BR* (Abandoned / decommissioned singletrack; Level 3 Black Diamond; `#475569`)
* *18 Unnamed Informal Singletrack Lines* (Hand-cut timber chutes and bandit bypasses; `#ea580c`)

---

## File Manifest

| Filename | Format | Description |
| :--- | :--- | :--- |
| `lookout_sanctioned.geojson` | GeoJSON | Complete WGS84 feature collection of the 50 sanctioned singletracks with IMBA ratings, lengths, and tags. |
| `lookout_sanctioned.kml` | KML 2.2 | Styled KML vector placemarks for CalTopo, Gaia GPS, and Google Earth. |
| `lookout_sanctioned.gpx` | GPX 1.1 | Vector tracks enriched with `<tf:difficulty>` and `<gpxx:DisplayColor>` tags. |
| `lookout_unsanctioned.geojson` | GeoJSON | Vector feature collection of the 21 unsanctioned and user-maintained singletracks. |
| `lookout_unsanctioned.kml` | KML 2.2 | Styled KML placemarks in Blaze Orange (`#ea580c`) and Ghost Slate (`#475569`). |
| `lookout_unsanctioned.gpx` | GPX 1.1 | Unsanctioned tracks for offline GPS navigation. |
