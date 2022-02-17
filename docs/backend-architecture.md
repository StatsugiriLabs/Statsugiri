# Backend Architecture

The backend architecture processes the time-series usage and global ranking snapshots from Pokémon Showdown.

# Tech Stack

-   Go 1.17
-   Python 3.9
-   MongoDB
-   AWS Lambda
-   AWS Elastic Container Registry
-   AWS Cloudwatch
-   AWS EventBridge

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

Get all recorded team snapshots for every available format.
Add `limit` and `offset` query params for pagination. Maximum limit of 10.
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

Get all recorded team snapshots for a specific format.
Add `limit` and `offset` query params for pagination. Maximum limit of 10.
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

Get all recorded team snapshots for a specific format and date.
Add `limit` and `offset` query params for pagination. Maximum limit of 10.
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

## `GET /api/usage`

Get all recorded usage snapshots for every available format.
Add `limit` and `offset` query params for pagination. Maximum limit of 10.

### Request

```console
curl /api/usage
```

### Response

```console
[
    {
        "Date": "2022-01-22",
        "FormatId": "gen8ou",
        "PokemonUsage": {
            "Aegislash": 2,
            "Blacephalon": 1,
            "Blissey": 1,
            "Chansey": 1,
            ...
        }
    },
    {
        ...
    }
]
```

## `GET /api/usage/{format}`

Get all recorded usage snapshots for a specific format.
Add `limit` and `offset` query params for pagination. Maximum limit of 10.

### Request

```console
curl /api/usage/gen8ou
```

### Response

```console
[
    {
        "Date": "2022-01-27",
        "FormatId": "gen8ou",
        "PokemonUsage": {
            "Arctozolt": 1,
            "Barraskewda": 1,
            "Bisharp": 1,
            "Blacephalon": 1,
            "Blissey": 2,
            ...
        }
    },
    {
        "Date": "2022-01-26",
        "FormatId": "gen8ou",
        "PokemonUsage": {
            "Arctovish": 1,
            "Arctozolt": 2,
            "Aurorus": 1,
            "Barraskewda": 1,
            "Bisharp": 1,
            ...
        }
    },
    {
        ...
    }
]
```

## `GET /api/usage/{format}/{date}`

Get all recorded usage snapshots for a specific format and date.
Add `limit` and `offset` query params for pagination. Maximum limit of 10.

### Request

```console
curl /api/usage/gen8ou/2022-01-27
```

### Response

```console
[
    {
        "Date": "2022-01-27",
        "FormatId": "gen8ou",
        "PokemonUsage": {
            "Arctozolt": 1,
            "Barraskewda": 1,
            "Bisharp": 1,
            "Blacephalon": 1,
            "Blissey": 2,
            ...
        }
    }
]
```

## `GET /api/rating-usage`

Get all recorded rating-to-usage snapshots for every available format.
Add `limit` and `offset` query params for pagination. Maximum limit of 10.

### Request

```console
curl /api/rating-usage
```

### Response

```console
[
    {
        "Date": "2022-01-26",
        "FormatId": "gen8ou",
        "PokemonAverageRatingUsage": {
            "Arctovish": 1900,
            "Arctozolt": 1889,
            "Aurorus": 1900,
            "Barraskewda": 1958,
            "Bisharp": 1860,
            ...
        }
    },
    {
        ...
    }
]
```

## `GET /api/rating-usage/{format}`

Get all recorded rating-to-usage snapshots for a specific format.
Add `limit` and `offset` query params for pagination. Maximum limit of 10.

### Request

```console
curl /api/rating-usage/gen8ou
```

### Response

```console
[
    {
        "Date": "2022-01-25",
        "FormatId": "gen8ou",
        "PokemonAverageRatingUsage": {
            "Arctovish": 1911,
            "Arctozolt": 1900,
            "Aurorus": 1911,
            "Barraskewda": 1957,
            "Blacephalon": 1980,
            ...
        }
    },
    {
        "Date": "2022-01-24",
        "FormatId": "gen8ou",
        "PokemonAverageRatingUsage": {
            "Aegislash": 1906,
            "Arctovish": 1891,
            "Arctozolt": 1895,
            "Aurorus": 1891,
            "Azumarill": 1938,
            ...
        }
    },
    {
        ...
    }
]
```

## `GET /api/rating-usage/{format}/{date}`

Get all recorded rating-to-usage snapshots for a specific format and date.
Add `limit` and `offset` query params for pagination. Maximum limit of 10.

### Request

```console
curl /api/rating-usage/gen8ou/2022-01-27
```

### Response

```console
[
    {
        "Date": "2022-01-27",
        "FormatId": "gen8ou",
        "PokemonAverageRatingUsage": {
            "Arctozolt": 1869,
            "Barraskewda": 1965,
            "Bisharp": 1891,
            "Blacephalon": 1940,
            "Blissey": 1884,
            ...
        }
    }
]
```

## `GET /api/partner-usage`

Get all recorded partner usage snapshots for every available format.
Add `limit` and `offset` query params for pagination. Maximum limit of 10.

### Request

```console
curl /api/partner-usage
```

### Response

```console
[
    {
        "Date": "2022-01-24",
        "FormatId": "gen8vgc2021series11",
        "PokemonPartnerUsage": {
        "Calyrex-Ice": {
            "Incineroar": 1,
            "Kyogre": 1,
            "Mimikyu": 1,
            "Regieleki": 1,
            "Venusaur": 1
        },
        "Calyrex-Shadow": {
            "Chandelure": 1,
            "Tapu Lele": 1,
            "Thundurus": 1,
            "Urshifu": 1,
            "Whimsicott": 1
        },
        ...
    },
    {
        ...
    }
]
```

## `GET /api/partner-usage/{format}`

Get all recorded partner usage snapshots for a specific format.
Add `limit` and `offset` query params for pagination. Maximum limit of 10.

### Request

```console
curl /api/partner-usage/gen8vgc2021series11
```

### Response

```console
[
    {
        "Date": "2022-01-23",
        "FormatId": "gen8vgc2021series11",
        "PokemonPartnerUsage": {
            "Calyrex-Ice": {
                "Incineroar": 1,
                "Kyogre": 1,
                "Mimikyu": 1,
                "Regieleki": 1,
                "Venusaur": 1
            },
            "Calyrex-Shadow": {
                "Chandelure": 1,
                "Tapu Lele": 1,
                "Thundurus": 1,
                "Urshifu": 1,
                "Whimsicott": 1
            },
            ...
        }
    },
    {
        "Date": "2022-01-22",
        "FormatId": "gen8vgc2021series11",
        "PokemonPartnerUsage": {
            "Araquanid": {
                "Bronzong": 1,
                "Incineroar": 1,
                "Kyogre": 1,
                "Porygon2": 1,
                "Tapu Koko": 1
            },
            "Bronzong": {
                "Araquanid": 1,
                "Incineroar": 1,
                "Kyogre": 1,
                "Porygon2": 1,
                "Tapu Koko": 1
            },
            ...
        }
    },
    {
        ...
    }
]
```

## `GET /api/partner-usage/{format}/{date}`

Get all recorded partner usage snapshots for a specific format and date.
Add `limit` and `offset` query params for pagination. Maximum limit of 10.

### Request

```console
curl /api/rating-usage/gen8vgc2021series11/2022-01-27
```

### Response

```console
[
    {
        "Date": "2022-01-27",
        "FormatId": "gen8vgc2021series11",
        "PokemonPartnerUsage": {
            "Araquanid": {
                "Bronzong": 1,
                "Incineroar": 1,
                "Kyogre": 1,
                "Porygon2": 1,
                "Tapu Koko": 1
            },
            "Bronzong": {
                "Araquanid": 1,
                "Incineroar": 1,
                "Kyogre": 1,
                "Porygon2": 1,
                "Tapu Koko": 1
            },
            ...
        }
    }
]
```

## `GET /api/time-usage/{pokemon}`

Get Pokémon's time-series usage to most recent date for all formats.
Add `start` and `end` query params to filter by window.

### Request

```console
curl /api/time-usage/Landorus-Therian
```

### Response

```console
{
  "Pokemon": "Landorus-Therian",
  "FormatUsageSnapshots": [
    {
      "FormatId": "gen8ou",
      "TimeSeriesUsageSnapshots": [
        {
          "Date": "2022-01-27",
          "Usage": 7
        },
        {
          "Date": "2022-01-26",
          "Usage": 6
        },
        {
          "Date": "2022-01-25",
          "Usage": 7
        },
        {
          "Date": "2022-01-24",
          "Usage": 6
        },
        {
          "Date": "2022-01-22",
          "Usage": 7
        }
      ]
    },
    {
      "FormatId": "gen8vgc2021series11",
      "TimeSeriesUsageSnapshots": [
        {
          "Date": "2022-01-27",
          "Usage": 2
        },
        {
          "Date": "2022-01-26",
          "Usage": 4
        },
        {
          "Date": "2022-01-25",
          "Usage": 4
        },
        {
          "Date": "2022-01-24",
          "Usage": 4
        },
        {
          "Date": "2022-01-23",
          "Usage": 4
        },
        {
          "Date": "2022-01-22",
          "Usage": 3
        }
      ]
    },
    ...
  ]
}
```

## `GET /api/time-usage/{pokemon}/{format}`

Get Pokémon's time-series usage to most recent date for a specific format.
Add `start` and `end` query params to filter by window.

### Request

```console
curl /api/time-usage/Landorus-Therian/gen8ou?end=2022-01-26
```

### Response

```console
{
  "Pokemon": "Landorus-Therian",
  "FormatUsageSnapshots": [
    {
      "FormatId": "gen8ou",
      "TimeSeriesUsageSnapshots": [
        {
          "Date": "2022-01-26",
          "Usage": 6
        },
        {
          "Date": "2022-01-25",
          "Usage": 7
        },
        {
          "Date": "2022-01-24",
          "Usage": 6
        },
        {
          "Date": "2022-01-22",
          "Usage": 7
        }
      ]
    }
  ]
}
```
