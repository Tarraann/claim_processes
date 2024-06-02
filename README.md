# Project Setup and Running Instructions

## Prerequisites
- Ensure you have Docker installed on your machine. If not, download and install it from Docker's official site.

## Getting Started
Follow these steps to set up and run the project:

1. Clone the Git Repository - First, clone the repository to your local machine using the following command.       
```git clone https://github.com/Tarraann/claims```
2. Setup Environment Variables - Navigate into the project directory, Copy the dev.env file and create a new .env file   
```cp dev.env .env```
3. Configure the Environment Variables - Open the newly created .env file in your preferred text editor and update the PAYMENT_SERVICE_URL to match your payment service URL.
4. Build and Run the Docker Containers ```docker compose up --build```

## API Usage

1. CREATE CLAIMS API - ```POST - \claim\create```
This endpoint allows the creation of multiple claims in a single request. Each claim in the request body must adhere to the defined schema, and the API will validate the data before inserting it into the database.
The request body should be a JSON array of objects, each representing a single claim. The keys are case-insensitive and can contain spaces, which will be normalized by the server. Here is the schema for a single claim.
```[
    {
        "Service Date": "3/28/2018 0:00:00",
        "Submitted Procedure": "D0180",
        "Quadrant": "UR",
        "Plan Group": "GRP-1000",
        "Subscriber": 3730189502,
        "Provider NPI": 1497775530,
        "Provider Fees": 100.00,
        "Allowed Fees": 100.00,
        "Member Coinsurance": 0.00,
        "Member Copay": 0.00
    },
    {
        "Service Date": "3/28/2018 0:00:00",
        "Submitted Procedure": "D0210",
        "Quadrant": "LR",
        "Plan Group": "GRP-2000",
        "Subscriber": 3730189503,
        "Provider NPI": 1497775531,
        "Provider Fees": 108.00,
        "Allowed Fees": 108.00,
        "Member Coinsurance": 0.00,
        "Member Copay": 0.00
    }
]
```
```angular2html
curl -X POST "http://localhost:8001/claims/" -H "Content-Type: application/json" -d '[
    {
        "Service Date": "3/28/2018 0:00:00",
        "Submitted Procedure": "D0180",
        "Quadrant": "UR",
        "Plan Group": "GRP-1000",
        "Subscriber": 3730189502,
        "Provider NPI": 1497775530,
        "Provider Fees": 100.00,
        "Allowed Fees": 100.00,
        "Member Coinsurance": 0.00,
        "Member Copay": 0.00
    },
    {
        "Service Date": "3/28/2018 0:00:00",
        "Submitted Procedure": "D0210",
        "Quadrant": "LR",
        "Plan Group": "GRP-2000",
        "Subscriber": 3730189503,
        "Provider NPI": 1497775531,
        "Provider Fees": 108.00,
        "Allowed Fees": 108.00,
        "Member Coinsurance": 0.00,
        "Member Copay": 0.00
    }
]'

```
Validation Rules - 
- submitted_procedure: Must start with the letter 'D'.
- provider_npi: Must be a 10-digit integer.
- service_date: Must be in the format 'MM/DD/YYYY HH:MM

2. GET TOP PROVIDERS API - ```GET - \claim\top\providers```
- This API endpoint retrieves the top providers based on net fees generated.
- The response body will contain a list of objects, each representing a top provider along with their net fees.
```angular2html
RESPONSE BODY
- provider_id (int): The unique identifier of the provider.
- provider_npi (int): The National Provider Identifier (NPI) of the provider.
- net_fee (float): The net fee generated by the provider.
```
```angular2html
EXAMPLE - 
[
    {
        "provider_id": 1,
        "provider_npi": 1234567890,
        "net_fee": 1000.00
    },
    {
        "provider_id": 2,
        "provider_npi": 0987654321,
        "net_fee": 800.50
    }
]

```

## Retry Mechanism for Notifying Payment Service

If notifying the payment service fails, the system will automatically retry after 2 hours. A Celery job is responsible for retrying the notification for all failed net fees with their corresponding claim IDs. This job runs every two hours.


## Slack Notifier for Debugging
For better debugging, a Slack notifier can also be integrated into the system. It will notify developers every time notifying the payment service fails. This will further help in promptly identifying and resolving any issues with the payment service integration.



