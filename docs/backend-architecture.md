# Backend Architecture

The backend architecture processes the time-series usage and global ranking snapshots from Pokémon Showdown.

# Table of Contents

TODO

# Tech Stack

-   Go
-   AWS Lambda
-   AWS DynamoDB
-   AWS API Gateway
-   AWS Cloudwatch
-   AWS Serverless Application Model
-   Redis

# Database Schema

Document tables are separated by formats.

## Pokémon Team Snapshots

Document for individual team snapshots and ranking metadata.

```javascript
{
    date: datetime,                 // mm/dd/yy
    format: str,
    pokemon_list: [str],
    rating: int,
    replay_upload_date: datetime    // mm/dd/yy
}
```

## Pokémon Usage Snapshots

Document for individual Pokémon usage data out of all ranked teams.

```javascript
{
    date: datetime,
    format: str,
    pokemon_usage: {        // List of Pokémon usage as a percentage to all teams
        [
            str: float
        ]
    },
    average_rating: {       // Denotes Pokémon's average rating between all appearances
        [
            str: float
        ]
    }
}
```

# Endpoints

# Infrastructure
