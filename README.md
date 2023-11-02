# dsw2seek

## Project overview

dsw2seek is a python web application that uses Data Management Plans (DMPs) from DSW to create projects in FAIRDOM-SEEK.

## Important resources

DSW test environment: https://dsw-test.elixir.no/ \
DSW SDK: https://github.com/ds-wizard/dsw-sdk

Seek API documentation: https://docs.seek4science.org/tech/api/ \
Examples using the Seek API: https://docs.seek4science.org/help/user-guide/api.html \
Seek for Docker: https://docs.seek4science.org/tech/docker

## Project setup

### Python packages

Navigate to the project directory and run:

```
pip install -r requirements.txt
```

### Docker

First, create the following 4 volumes in Docker:

```
docker volume create --name=seek-filestore
docker volume create --name=seek-mysql-db
docker volume create --name=seek-solr-data
docker volume create --name=seek-cache
```

Then run `docker-compose` in the root directory of this project:

```
docker-compose -f docker/docker-compose.seek.yml -p seek up -d
docker-compose -f docker/docker-compose.dsw.yml -p dsw up -d
```

### Connect DSW

In DSW, add a new document submission service with the following parameters:
| Parameter           | Value                       |
|---------------------|-----------------------------|
| ID                  | dsw2seek                    |
| Name                | Seek                        |
| Supported formats   | dsw:rda-madmp, 1.14.0, JSON |
| Request method      | POST                        |
| Request URL         | <dsw2seek url>/upload       |
| Multipart           | Enabled                     |
| Multipart File Name | jsonFile                    |

Substitute `<dsw2seek url>` with the URL to your instance of dsw2seek.
Users can now submit their DMPs to Seek.

## Seek API

Example request to the Seek API:

```
GET http://localhost:3000/projects/1 HTTP/1.1
Accept: application/vnd.api+json
Accept-Charset: ISO-8859-1
Authorization: Basic <credentials>
Content-Type: application/vnd.api+json
```

The authorization credentials are the base64-encoding of the string `<username>:<password>`.
