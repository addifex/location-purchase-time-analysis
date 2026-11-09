# Purchase Time Heatmaps
A python script for taking location based venues purchase and entry data and generates heatmaps
that show when visors purchase by day of the week and month. Produces a PNG image for each location
of two heatmaps: by day of week and by month. 

## Usage
The script expects a csv with the headers:
TransactionDate, TransactionTime, EntryDate, EntryTime, and Location.
Location is used for separating heatmaps by different venues.

### Parameters
- --filePath (required): The path to the csv file.
- --leadTime: Filter data where the customer purchased less than x hours from their entry.
- --startDate: Filter data that comes before a start date.
- --outputDir: The directory path to output heatmap images.

## License
[MIT](https://choosealicense.com/licenses/mit/)