# Dam-Level-Data-Scraper
Scrape weekly dam water level data from the South African Department of Water and Sanitation using the Internet Archive for use in modeling. 

Data source: http://www.dwa.gov.za/Hydrology/Weekly/Province.aspx

The script scraper.py will put the data gathered for each province into its own CSV ordered by date. It will not normalize the data. The functions in normalize.py will squeeze the FSC (Full Storage Capacity) between 0.0 and 1.0 and the percentage values will be converted into corresponding decimal values for the percentages.

```
usage: scraper.py [-h] [--output OUTPUT] [--provinces PROVINCES [PROVINCES ...]] [--no_override]

Scrape South African dam water level data from the Internet Archive

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        directory where the CSVs will go
  --provinces PROVINCES [PROVINCES ...], -p PROVINCES [PROVINCES ...]
                        ids of the specific provinces to download
  --no_override, -n     will not redownload data that is already present
  ```
