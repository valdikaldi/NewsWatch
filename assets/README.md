
# Assets

Static resources shipped with NewsWatch.

## locales.csv

A lookup table of Google News locale parameters.

**Columns:**
- `ceid` — Country Edition ID (e.g. `US:en`, `DE:de`)
- `hl` — Interface language (e.g. `en-US`, `de`)
- `gl` — Geographic region (e.g. `US`, `DE`)

**Sources:**
- CEID codes: https://www.searchapi.io/docs/parameters/google-news-portal/ceid
- HL/GL codes: https://developers.google.com/custom-search/docs/xml_results_appendices

**Notes:**
- Not all country/language combinations are supported by Google News.
- Only the CEID values listed in the SearchAPI table are valid.