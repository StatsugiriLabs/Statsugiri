# Backend Architecture

The backend architecture processes the time-series usage and global ranking snapshots from Pokémon Showdown.

# Tech Stack

-   Go
-   Python
-   MongoDB
-   AWS Lambda
-   AWS Elastic Container Registry
-   AWS Cloudwatch
-   AWS EventBridge
-   Redis

# Database Models

Document tables are separated by team and usage snapshots.

## Pokémon Team Snapshots

Document for daily team snapshots and ranking metadata.

```javascript
{
    Date: str,                  // Primary Key: yyyy-mm-dd
    FormatId: str,              // Secondary Key
    Teams: [
        {
            PokemonRoster: [str],
            Rating: int,
            ReplayUploadDate: str //yyyy-mm-dd
        }
    ]
}
```

## Pokémon Usage Snapshots

Document for individual Pokémon usage data out of all ranked teams.

```javascript
{
    Date: str,                  // Primary Key: yyyy-mm-dd
    FormatId: str,              // Secondary Key
    PokemonUsage: {             // List of Pokémon usage as number of appearances
        str: int
    },
    PokemonPartnerUsage: {
        str: {              // List of Pokémon recorded
            str: int        // Denotes Pokémon's partners as number of appearances
        }
    },
    PokemonAverageRatingUsage: {     // Denotes Pokémon's average rating normalized by number of appearances
        str: int
    }
}
```

# Endpoints

## `GET api/health`

Get API health status.

### Request

```console
curl /api/health
```

### Response

```console
{
    "status": "up and running"
}
```

## `GET api/formats`

Get supported formats.

### Request

```console
curl /api/formats
```

### Response

```console
{
    formats: ["gen8vgc2021", "gen8ou", "gen8uu", "gen8ru", "gen8nu"]
}
```

## `GET /api/teams`

Get all recorded teams for every available format.
Add `limit` and `offset` query params for pagination.
Add `pokemon` query param to filter for teams featuring the specified Pokémon.

### Request

```console
curl /api/teams
```

### Response

```console
[
    {
        "Date": "2022-01-23",
        "FormatId": "gen8vgc2021series11",
        "Teams": {
        "PokemonRoster": [
            "Calyrex-Shadow",
            "Whimsicott",
            "Urshifu",
            "Tapu Lele",
            "Thundurus",
            "Chandelure"
        ],
        "Rating": 1725,
        "ReplayUploadDate": "2022-01-09"
        },
    },
    {
        "Date": "2022-01-22",
        "FormatId": "gen8ou",
        "Teams": {
        "PokemonRoster": [
            "Skarmory",
            "Clefable",
            "Hippowdon",
            "Tornadus-Therian",
            "Blissey",
            "Slowbro"
        ],
        "Rating": 1976,
        "ReplayUploadDate": "2021-07-17"
        },
    },
    {
        ...
    }
]
```

## `GET /api/teams/{format}`

Get all recorded teams for a specific format.
Add `limit` and `offset` query params for pagination.
Add `pokemon` query param to filter for teams featuring the specified Pokémon.

### Request

```console
curl /api/teams/gen8vgc2021series11
```

### Response

```console
[
    {
        "Date": "2022-01-23",
        "FormatId": "gen8vgc2021series11",
        "Teams": {
        "PokemonRoster": [
            "Calyrex-Shadow",
            "Whimsicott",
            "Urshifu",
            "Tapu Lele",
            "Thundurus",
            "Chandelure"
        ],
        "Rating": 1725,
        "ReplayUploadDate": "2022-01-09"
        },
    },
    {
        "Date": "2022-01-22",
        "FormatId": "gen8vgc2021series11",
        "Teams": {
        "PokemonRoster": [
            "Naganadel",
            "Tornadus",
            "Dracovish",
            "Mienshao",
            "Chandelure",
            "Tsareena"
        ],
        "Rating": 1708,
        "ReplayUploadDate": "2022-01-16"
        },
    },
    {
        ...
    }
]
```

## `GET /api/teams/{format}/{date}`

Get all recorded teams for a specific format and date.
Add `limit` and `offset` query params for pagination.
Add `pokemon` query param to filter for teams featuring the specified Pokémon.

### Request

```console
curl /api/teams/gen8vgc2021series11/2022-01-22?pokemon=Urshifu
```

### Response

```console
[
    {
        "Date": "2022-01-22",
        "FormatId": "gen8vgc2021series11",
        "Teams": {
        "PokemonRoster": [
            "Calyrex-Shadow",
            "Whimsicott",
            "Urshifu",
            "Tapu Lele",
            "Thundurus",
            "Chandelure"
        ],
        "Rating": 1730,
        "ReplayUploadDate": "2022-01-09"
    },
    {
        "Date": "2022-01-22",
        "FormatId": "gen8vgc2021series11",
        "Teams": {
        "PokemonRoster": [
            "Rillaboom",
            "Urshifu",
            "Coalossal",
            "Thundurus",
            "Zacian",
            "Incineroar"
        ],
        "Rating": 1695,
        "ReplayUploadDate": "2021-12-01"
    },
    {
        ...
    }
]
```

## `GET /api/usage/{format}/{date}`

Get most recent recorded individual Pokémon usage for specific format.
Defaults to recent VGC format if format not provided (eg. `gen8vgc2021`).
Defaults to most recent if date is not given.

### Request

```console
curl /api/usage/gen8vgc2021/2021-12-15
```

### Response

```console
{
    date: 2021-12-15,
    format: gen8vgc2021,
    pokemon_usage: {
        {
            "incineroar": 47.0,
            "rillaboom": 37.0,
            "regieleki": 22.0,
            ...
        },
    }
}
```

## `GET /api/rating-usage/{format}/{date}`

Get most recent recorded Pokémon rating to usage ratio for specific format.
Filter by Pokémon using `-F pokemon[]={pokemon}`.
Defaults to recent VGC format if format not provided (eg. `gen8vgc2021`).
Defaults to most recent if date is not given.

### Request

```console
curl /api/rating-usage/gen8vgc2021/2021-12-15
```

### Response

```console
{
    date: 2021-12-15,
    format: gen8vgc2021,
    rating_usage_ratio: {
        {
            "incineroar": 35.4,
            "rillaboom": 21.3,
            ...
        },
    }
}
```

## `GET /api/core-usage/{date}`

Get most recent recorded Pokémon core combinations of 3. Exclusive to current VGC format.
Filter by Pokémon using `-F pokemon[]={pokemon}`.
Defaults to most recent if date is not given.

Add `limit` and `offset` query params for pagination.

### Request

```console
curl /api/core-usage/2021-12-15
```

### Response

```console
{
    date: 2021-12-15,
    format: gen8vgc2021,
    core_usage: {
        {
            ["incineroar", "rillaboom", "regieleki"]: 11,
            ["torkoal", "venusaur", "incineroar"]: 8,
            ...
        },
    }
}
```

## `GET /api/partners/{pokemon}/{date}`

Get Pokémon's top 5 partners. Exclusive to current VGC format.
Defaults to most recent if date is not given.

### Request

```console
curl /api/core-usage/2021-12-15
```

### Response

```console
{
    date: 2021-12-15,
    format: gen8vgc2021,
    pokemon: "togekiss",
    partners: {
        {
            incineroar: 27,
            rillaboom: 25,
            whimsicott: 16,
            regieleki: 15,
            amoonguss: 11,
        },
    }
}
```

## `GET /api/timeseries-usage/{format}/{pokemon}`

Get Pokémon's time-series usage to present.

Add `limit` and `offset` query params for pagination.

### Request

```console
curl /api/timeseries-usage/gen8vgc2021/incineroar
```

### Response

```console
{
    format: gen8vgc2021,
    pokemon: togekiss,
    time-usage: {
        "2021-12-15": 25,
        "2021-12-14": 21,
        "2021-12-13": 23,
        "2021-12-12": 13,
        ...
    }
}
```
