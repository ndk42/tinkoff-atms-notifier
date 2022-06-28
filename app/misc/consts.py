TINKOFF_URL = 'https://api.tinkoff.ru/geo/withdraw/clusters'
NSK_REQUEST_JSON = {
    "bounds": {
        "bottomLeft": {
            "lat": 54.79369468788256, "lng": 82.3319082435153
        },
        "topRight": {
            "lat": 55.15784133040111, "lng": 83.99633695445284
        }
    },
    "filters": {
        "banks": ["tcs"],
        "showUnavailable": True,
        "currencies": ["USD"]
    },
    "zoom": 10
}

MAIN_LOGGER_NAME = 'tink_notify'
