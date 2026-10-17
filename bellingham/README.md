# Bellingham & Whatcom County Mountain Bike Networks

Bellingham and Whatcom County represent the premier mountain biking hub in Washington State. Spanning glacial ridges, coastal sandstone bluffs, and active working forests, the region features an interconnected ecosystem of legally sanctioned trail networks coexisting with historic underground freeride lines.

---

## Regional Geography & Mountain Systems

The Bellingham library is divided into three distinct mountain systems:

```text
bellingham/
├── README.md                           # Regional overview, sources & easement guide
│
├── galbraith-mountain/                 # Galbraith Mountain (North & South)
│   ├── README.md                       # Easement history, jump complexes & trail roster
│   ├── galbraith_sanctioned.geojson / .kml / .gpx
│   └── galbraith_unsanctioned.geojson / .kml / .gpx
│
├── chuckanut-blanchard/                # Chuckanut Mountain & Blanchard State Forest
│   ├── README.md                       # Larrabee State Park & DNR seaside gravity lines
│   ├── chuckanut_sanctioned.geojson / .kml / .gpx
│   └── chuckanut_unsanctioned.geojson / .kml / .gpx
│
└── lookout-mountain/                   # Lookout Mountain, Lake Whatcom & Stewart Mountain
    ├── README.md                       # County forest preserve & Stewart Mountain lines
    ├── lookout_sanctioned.geojson / .kml / .gpx
    └── lookout_unsanctioned.geojson / .kml / .gpx
```

---

## Regional Land Governance & Legal Baselines

1. **The Galbraith Mountain Recreation Use Easement (2,182 Acres):**
   * **Parties:** City of Bellingham, Whatcom Land Trust, and *Galbraith Tree Farm, LLC* (Whatcom County Auditor File Nos. 2018-0803004 / 2018-0807005).
   * **Stewardship:** Whatcom Mountain Bike Coalition (WMBC).
   * **Legal Effect:** Permanently secured non-motorized public recreation across the entire commercial tree farm. All WMBC-adopted trails inside this boundary are fully legal and sanctioned.
2. **Chuckanut Mountain & Larrabee State Park:**
   * **Jurisdiction:** Washington State Parks and Recreation Commission (Larrabee) and Washington State Department of Natural Resources (Blanchard State Forest).
   * **Regulatory Dynamic:** Steep sandstone bluffs dropping into Samish Bay. Strict enforcement against bicycle access on pedestrian-only conservation trails (*Fragrance Lake, Rock Trail*), alongside officially adopted double-black descents (*Double Black Diamond, Double Down*).
3. **Lookout Mountain Forest Preserve & Lake Whatcom:**
   * **Jurisdiction:** Whatcom County Parks & Recreation Department and WA DNR.
   * **Focus:** Deep forested ridges featuring sustained downhill flow (*Cougar Ridge, Floam*) and long-standing community-built singletracks on Stewart Mountain (*Brown Pow, Chanterelle*).

---

## Data Provenance & Methodology Summary

All datasets in this directory strictly adhere to the master methodology defined in the root [`README.md`](../README.md):
* **Sources Queried:** OpenStreetMap Core API 0.6, WMBC official trail directory, WA DNR recreation GIS, Whatcom County Parks master plans, and Trailforks regional databases.
* **Singletrack Isolation:** All gravel logging roads (`RD 2000` series, `Tower Road`, `BL-1616`, `OC-17`) were stripped out, preserving 100% pure singletrack trails.
* **Pedestrian Exclusion:** Sanctioned footpaths that prohibit bicycles (`bicycle=no`) are excluded.
* **Rating Resolution:** Every trail carries an IMBA rating (1–5) and Trailforks hex color (`#22c55e` Green, `#0284c7` Blue, `#dc2626` Black, `#000000` Double Black, `#8b5cf6` Pro-Line).
