# Instructions for Data Import

For large files, it's necessary to use the JQ library for compressing and standardizing the GeoJSON. Specifically, the provided command selects the "features" field typical of GeoJSON files and processes it:

```shell
jq --compact-output ".features" input.geojson > output.geojson
```

The output is an array of JSON objects.

At this point, it would have been nice to use the following command "mongoimport --db dbname -c collectionname --file "output.geojson" --jsonArray", but the problem is that the input file "output.geojson" is 350MB in size. Therefore, mongoimport is practically useless...

[IDEA] The idea was to read the input file line by line and then insert into the database for each individual object read.

[Issues Encountered]:

- Input encoding type "utf16" -> "utf-8"
- Issues with the Decimal type due to Python's BSON and JSON objects
- Issues with the JSON library caused by the excessively large size of individual lines of the array objects

[SOLUTION]:

- Convert the output3 file with utf8 encoding to the file --> output3_utf8 ("cmd: iconv -f UTF-16 -t UTF-8 output3.geojson > output3_utf8.geojson")
- Recursively convert all Decimal type elements to Float present within a single object
- Change the JSON handling library to "ijson", which is more suitable for reading large JSON files
