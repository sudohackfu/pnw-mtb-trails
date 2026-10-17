# PNW Mountain Bike Trails Geospatial Repository

A curated geospatial repository and toolset for mapping, auditing, and analyzing mountain bike networks across the Pacific Northwest (Western Washington).

## Systems Covered

### 1. Exit 27 / Rattlesnake Mountain / Raging River
* **Focus:** Unsanctioned and pirate freeride downhill network.
* **Geospatial Audits:** Cross-referenced against King County Cadastral parcel records (`PIN 1423089001` - Rattlesnake Mountain NRCA under RCW 79.71) and WA DNR Public Forest Practices transportation baselines.
* **Layers:**
  - Active Freeride Singletracks
  - DNR Active Decommissioning Targets
  - Physically Demolished Historical Lines

### 2. Bellingham Mountain Systems
* **Galbraith Mountain:** 240+ named trails (~65 miles) spanning north and south sectors, including world-famous jump progression complexes (*Blue Steel, Unemployment Line, Mohawk, Cedar Dust*) and technical ridge descents (*Evolution, SST, Scorpion*).
* **Chuckanut & Blanchard Mountain:** 47 named trails covering seaside sandstone slabs and high-consequence gravity descents (*Double Black Diamond, Double Down, Hush Hush, Chinscraper*).
* **Lookout Mountain Forest Preserve:** 33 named trails on the eastern flank of Lake Whatcom featuring sustained, forested descents (*Cougar Ridge, Floam, Rufus Creek, El Diablo*).

## Data Formats & Specifications

* **GeoJSON:** Full WGS84 feature collections preserving raw OpenStreetMap tags, surface data, difficulty ratings, and land management metadata.
* **KML 2.2:** Vector line placemarks styled with custom hex color palettes for immediate import into Google Earth, CalTopo, and Gaia GPS.
* **GPX 1.1:** Vector tracks enriched with Trailforks (`<tf:...>`) and Garmin (`<gpxx:...>`) schema extensions for GPS units and offline bike computers.
