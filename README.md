# TVP Pipeline

The TVP Pipeline is a modular data processing pipeline designed to extract, transform, load, and analyze Total Value Processed (TVP) data from Dune. The pipeline leverages Apache Spark for distributed processing, supports scalable data storage, and includes functionality for Top K analysis.

## Features

### Class TVPExtractor

Extract data from Dune API.

### Class TVPTransformer
Transform data into weekly summaries by verticals and protocols.

### Class TVPLoader
Store transformed data in Parquet files for efficient querying.

### Class TVPAnalyzer
Perform Top K analysis for TVP verticals and protocols using Apache Spark.

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/duartevieira10/tvp_pipeline.git
cd tvp_pipeline
```

### 2. Install Docker
Ensure Docker is installed on your machine.

### 3. Set Environment Variables
Edit the config/app.env file to include your Dune API key and query IDs:

```plaintext
DUNE_API_KEY=your_dune_api_key
VERTICAL_AND PROTOCOL_QUERY_ID=123456  # Replace with actual query ID for query with vertical and protocol data
OUTPUT_DIRECTORY=/app/output
```


### 4. Build the Docker Image
Run the following command to build the Docker image:

```bash
make build
```

### 5. Run the Pipeline
To execute the pipeline:

```bash
make run
```

This will:
1. Extract data from Dune.
2. Transform the data into weekly summaries.
3. Save the summaries as Parquet files in the output/ directory or upload data to Dune if specified.
4. Perform Top K analysis and display results.


### 6. Debugging and Logs

View Logs:
```bash
make logs
```

### 7. Clean Up

Stop and remove any running containers:
```bash
make clean
```

### Testing
Validate the Output

1. Parquet Files:
Check the output/ directory for weekly_vertical_summary.parquet and weekly_protocol_summary.parquet.

2. Dune Tables:
Verify data in the target tables on Dune.

3. Top K Results:
Confirm the Top K verticals and protocols are displayed correctly in the console.


## Contributors
Nuno Vieira 
