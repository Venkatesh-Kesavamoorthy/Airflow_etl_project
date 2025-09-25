# X (Twitter) ETL Pipeline with Apache Airflow

## Introduction

This project implements an automated ETL (Extract, Transform, Load) pipeline using Apache Airflow to fetch Elon Musk's recent tweets from the X (formerly Twitter) API and store them in Amazon S3. The pipeline is designed to handle rate limiting gracefully and provides a robust data collection system for social media analytics.

## Features

- **Automated Tweet Collection**: Fetches the latest 10 tweets from Elon Musk's account
- **Rate Limit Handling**: Implements proper retry logic with exponential backoff
- **Data Transformation**: Cleans and structures tweet data with engagement metrics
- **Cloud Storage**: Saves processed data directly to Amazon S3
- **Airflow Integration**: Uses Apache Airflow for workflow orchestration and monitoring
- **Manual Triggering**: Designed for on-demand execution rather than scheduled runs

## Project Structure

```
Airflow_project/
├── x_dag.py              # Airflow DAG definition
├── x_etl.py              # ETL logic for tweet extraction
├── elon_musk_tweets.csv  # Sample output data
└── README.md             # Project documentation
```

## Prerequisites

- Python 3.7+
- Apache Airflow 2.0+
- Twitter API v2 access (Bearer Token)
- Amazon S3 bucket access
- Required Python packages:
  - `tweepy` - Twitter API client
  - `pandas` - Data manipulation
  - `apache-airflow` - Workflow orchestration

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Airflow_project
   ```

2. **Install dependencies**:
   ```bash
   pip install tweepy pandas apache-airflow
   ```

3. **Set up Airflow**:
   ```bash
   # Initialize Airflow database
   airflow db init
   
   # Create admin user
   airflow users create \
       --username admin \
       --firstname Admin \
       --lastname User \
       --role Admin \
       --email admin@example.com
   ```

4. **Configure Airflow connections**:
   - Set up S3 connection in Airflow UI (Admin > Connections)
   - Configure AWS credentials for S3 access

## Configuration

### Twitter API Setup

1. Obtain a Bearer Token from Twitter Developer Portal
2. Update the `bearer_token` in `x_etl.py` (line 8)

### S3 Configuration

1. Create an S3 bucket named `airflow-s3-x-bucket`
2. Configure AWS credentials in Airflow connections
3. Ensure proper IAM permissions for S3 read/write access

## Usage

### Running the Pipeline

1. **Start Airflow webserver**:
   ```bash
   airflow webserver --port 8080
   ```

2. **Start Airflow scheduler**:
   ```bash
   airflow scheduler
   ```

3. **Access Airflow UI**:
   - Open `http://localhost:8080` in your browser
   - Login with your admin credentials

4. **Trigger the DAG**:
   - Navigate to the DAGs page
   - Find the `x_dag` DAG
   - Click the "Trigger DAG" button to run manually

### Data Output

The pipeline generates a CSV file with the following structure:

| Column | Description |
|--------|-------------|
| `user` | Twitter username (elonmusk) |
| `date` | Tweet creation timestamp |
| `text` | Tweet content |
| `retweet_count` | Number of retweets |
| `like_count` | Number of likes |
| `reply_count` | Number of replies |
| `quote_count` | Number of quote tweets |

## DAG Configuration

The Airflow DAG (`x_dag.py`) is configured with:

- **Manual triggering only** (no automatic scheduling)
- **4 retries** with 16-minute delay between attempts
- **Rate limit handling** for Twitter API constraints
- **Error handling** for various API exceptions

## Error Handling

The pipeline includes comprehensive error handling:

- **Rate Limiting**: Automatically retries after rate limit windows
- **API Errors**: Graceful handling of Twitter API exceptions
- **Network Issues**: Retry logic for temporary connectivity problems
- **Data Validation**: Ensures data integrity before S3 upload

## Monitoring

Monitor your pipeline through the Airflow UI:

- **DAG Runs**: View execution history and status
- **Task Logs**: Detailed logs for debugging
- **Metrics**: Performance and success rate tracking
- **Alerts**: Email notifications for failures (if configured)

## Security Considerations

- **API Keys**: Store sensitive credentials in Airflow connections
- **S3 Access**: Use IAM roles with minimal required permissions
- **Network Security**: Ensure secure connections to external APIs

## Troubleshooting

### Common Issues

1. **Rate Limit Errors**: The pipeline will automatically retry after the rate limit window
2. **S3 Access Denied**: Verify AWS credentials and bucket permissions
3. **Twitter API Errors**: Check Bearer Token validity and API access

### Debugging

- Check Airflow task logs for detailed error messages
- Verify all connections are properly configured
- Ensure all dependencies are installed correctly

## Future Enhancements

- **Scheduled Execution**: Add cron-based scheduling for regular data collection
- **Data Processing**: Add data transformation and analysis steps
- **Multiple Users**: Extend to collect tweets from multiple accounts
- **Real-time Processing**: Implement streaming data collection
- **Data Visualization**: Add dashboard for tweet analytics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please:
1. Check the troubleshooting section
2. Review Airflow and Twitter API documentation
3. Open an issue in the repository

---

**Note**: This project is for educational and research purposes. Please ensure compliance with Twitter's Terms of Service and API usage policies.