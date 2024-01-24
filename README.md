# First round of requirements.

```
Create a PostgreSQL database in AWS with the fields outlined separately.
The DB should have a Web UI using Python and Django and on that UI the user should be able to:

1. Search and view records
2. Update records
   a. Moves adds and changes via a web form.
   b. Upload a csv to add records. Note: Create a template for upload.
3. Download/export records to a csv.
   a. The exporter should be able to choose which records to download. For example, all records for customer xyz corp.
   b. The export fields should be selectable.
4. Some DB Fields must align with Method CRM. For example, the Customer name and service types must match,
   a. So, on the Web UI there should be option for an API query to Method to obtain those fields. This may also be something to be done automatically on a daily basis. Note: I will get you set up in Method so you can see the API docs and test.
   b. Also, on the Web UI there should be an option to update YakChat via API. This will be on a customer specific basis. Note e will get the API info for you.
5. We will have to work together to harmonize and move our existing Master DIDs file into the DB.

```

## Screen Shots

[![SB Admin Preview](https://github.com/JohnGDalrymple/NumberDB/blob/develop/number_db/screen_shots/workflow.jpg)](https://github.com/JohnGDalrymple/NumberDB/tree/develop)
