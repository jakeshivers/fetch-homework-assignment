### Writing Sample

Hey team!

I just got done with the analysis you asked for; I was able to process the data up to ~ 3/1/2021.  While I do have answers to your questions, I don't trust them enough to give to you for your presentation. A couple of things:
* It seems we're missing some data from 2021 forward.  
* Our pipelines indicated that there is quite a bit of duplicate or missing data from various files. 

I can elaborate better in person as the QA files formats are not really intended for stakeholders. With the vast amount of dupes and missing field data, I would be hesitant to give you the query results without a huge asterisk. Would it be possible for us to delay your presentation until I can get with my team to better understand why the data is the way it is? It is quite possible that there was just an outage or a failed DAG, and we can get your data reprocessed.

Thank you for understanding.


Thanks,

Jake



### 1. What questions do you have about the data?
* The data appears to contain many duplicate `users`. I would like to know why this is the case. 
* There are duplicate barcode values in the `brands` file as well. How would we distinguish one `barcode` type from another if they have the same value?
* Category has missing data for many records. Perhaps this is a product that Fetch does not work with, which would explain that. Same with `barcode`.
* The ER diagram I created is a bit too normalized for a data warehouse. It answers the data questions, but another step could be taken to create a star schema. This would speed up querying for large data sets. I would use a tool like [`dbt`](https://github.com/jakeshivers/airbnb-dbt) to help build out a reliable model.

### 2. How did you discover the data quality issues?
* I knew right away there were issues when I tried loading the data. Once I got the data loaded into my database, I installed `Great Expectations` and had it run analysis on some of the fields. I did not QA the quality in each field, but wanted to showcase my knowledge of `GA`.

### 3. What do you need to know to resolve the data quality issues?
* I would need to have a holistic understanding of the business, how these files are generated, and some business logic. I can't perscribe a definite solution unless I had a better business understanding. 

### 4. What other information would you need to help you optimize the data assets you're trying to create?
* I would like to know why there are duplicats. Up above I suggested we were missing data. I realize that this is a mockup, with static data. However, that would be a real issue in production. I would need to know immediately if there was an actual outage, and would then need to backfill the data as quickly as possible.

### 5. What performance and scaling concerns do you anticipate in production and how do you plan to address them?
* The first thing I would do is setup the files to be partitioned by day. Each file would have a timestamp appended to the end (`users_2024-12-22.json`). These files would live in S3 or similar. Partitioning does a few things for us:
    1. In the event of an outage, only the necessary files would need to be reprocessed. I would build out a checkpoint table that stored successful runs. If the data was bad, but flagged as successful, we could investingate and solve DQ issue, rebuild the file, and then delete the checkpoint value. This would have the pipeline reprocess the new data.
    2. Unnesting JSON files. I would advocate to get the json files in an unnested structure. Processing nested files is a nightmare and leads to a lot of extra development downstream (just look at my python scripts :D). Unnested files, would speed up the pipeline development and execution of pipelines for the DE team. Since those files seem to be internal to Fetch, I feel that it is a reasonable ask compared to asking an external vendor. 
    3. Daily file partitions set us up for success if we're using a distributed system like Spark. Spark likes partitioned files, so we would be one step ahead of the curve if that was ever implemented.
#### Duplicate data. 
As the company scales, I would like to mitigate duplicates. We can fix it downstream, but that's unnecessary processing/compute time which adds up monetarily.

#### Apache Iceberg
This suggestion is a bit of a reach but I would try to get this same data in a parquet file. Parquet files are optimized for columnar storage. Depending on the tech stack, we would be able to use Apache Iceberg right in S3 buckets (something that was recently announced at AWS conference). Regardless of the implementation of Iceberg, parquet files are a much smaller file format and an industry standard for storing and processing data. 