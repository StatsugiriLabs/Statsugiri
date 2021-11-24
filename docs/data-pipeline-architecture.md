# Data Pipeline Architecture

The data pipeline (known as [Drilbur](<https://bulbapedia.bulbagarden.net/wiki/Drilbur_(Pok%C3%A9mon)>)) extracts and processes ranking and replay data from [Pokémon Showdown](https://pokemonshowdown.com/).

# Architecture

#### Architecture Overview Diagram

![High Level Architecture Diagram](images/svg/Data_Pipeline_Architecture.svg)

The core components of the data pipeline are the [DataExtractor](#DataExtractor), [ReplayParser](#ReplayParser), and [ModelTransformer](#ModelTransformer). The `DataExtractor` is responsible for retrieving replay logs from ranked users. The `ReplayParser` is responsible for cleaning and processing the replay logs. The `ModelTransformer` creates database models from the processed logs.

The Data Extraction [Lambda](https://aws.amazon.com/lambda/) is scheduled to run every 24 hours using [CloudWatch](https://aws.amazon.com/cloudwatch/). CloudWatch is also responsible for monitoring errors from the Data Extraction Lamba logs. [Simple Notification Service](https://aws.amazon.com/sns/?whats-new-cards.sort-by=item.additionalFields.postDateTime&whats-new-cards.sort-order=desc) (SNS) will notify the user via email. The Data Extraction Lambda builds are updated through [Elastic Container Registry](https://aws.amazon.com/ecr/) (ECR) deploying the Docker image.

## DataExtractor

## ReplayParser

## ModelTransformer
