# backend

The backend uses FastAPI to set up a simple API that can get, update, and delete flow for a station. It can also get the total flow of all stations.

Currently, it is hard-coded to handle two stations with IDs `station1` and `station2`.

## endpoints

The base URL for the API is `https://8ndi1e.deta.dev`. So, for example, to initialize the database for station 1, you would call `GET https://8ndi1e.deta.dev/initialize/station1`.

`GET /initialize/{station_id}` -- initializes the database entry for a particular station and sets the station's flow to 0 -- **this needs to be called once at start or after deleting flow**

`GET /flow/{station_id}` -- gets flow for a particular station (specified by the `station_id`)

`GET /total_flow` -- gets total flow of both stations combined

`POST /flow/{station_id}/{more_flow}` -- updates a particular station's (`station_id`) flow count by adding (`more_flow`) to it

`DELETE /flow/{station_id}` -- resets a station's flow count (**must run initialize for the station after this**)