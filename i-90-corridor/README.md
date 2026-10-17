# I-90 Corridor Mountain Bike Networks

The Interstate 90 (I-90) corridor through the Cascade foothills of King County represents one of the premier mountain biking regions in the Pacific Northwest. Running from Issaquah east toward Snoqualmie Pass, the corridor spans diverse land jurisdictions including Washington State Department of Natural Resources (WA DNR) working forests, Natural Resources Conservation Areas (NRCAs), King County Parks, and private commercial timberlands.

## Sub-Networks & Areas

* **[Exit 27 (Rattlesnake Mountain / Raging River Ridge)](./exit-27/)**: The historic unsanctioned and pirate freeride downhill network. Features steep, high-consequence loam chutes, wooden gap jumps, and drop-ins on the western shoulder of Rattlesnake Mountain.
* **Raging River State Forest (Sanctioned)**: The officially developed multi-use trail system managed by WA DNR and Evergreen Mountain Bike Alliance (EMBA), featuring *Poppin' Tops, CCDH, Invictus, Physical Therapy, and the Raging Tiger connector*.
* **Tiger Mountain State Forest**: The cornerstone state forest trail system featuring sanctioned classics (*Predator, Not-On-Tour-Guy, Preston RR, Side Hustle*).
* **Grand Ridge & Duthie Hill**: The low-elevation, all-weather progression parks and cross-country links connecting Issaquah and Sammamish.

## Directory Structure

```text
i-90-corridor/
├── README.md               # Corridor overview and jurisdiction reference
└── exit-27/                # Unsanctioned freeride network datasets & audit layers
    ├── README.md           # Trail inventory, status guide, and layer manifest
    ├── exit27_unsanctioned_trails.kml
    ├── exit27_unsanctioned_network.geojson
    ├── exit27_unsanctioned_network.gpx
    ├── exit27_active_freeride.gpx
    ├── exit27_WILL_BE_decommissioned.gpx
    ├── exit27_ALREADY_decommissioned.gpx
    ├── decommission_targets.geojson
    ├── dnr_authorized.geojson
    ├── nrca_boundary.geojson
    ├── exit27_raging_river_master.geojson
    └── exit27_raging_river_master.gpx
```
