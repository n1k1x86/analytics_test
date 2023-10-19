from mixpanel import Mixpanel
from ua_parser import user_agent_parser

mp = Mixpanel("03cb555225d67cfaff6e4e327f0dcb7b")

user_dist = {
    "admin": ("London", "England"),
    "john": ("NoCity", "NoCountry"),
    "lilpip": ("London", "England"),
    "lol": ("London", "England"),
    "nik": ("London", "England"),
    "nikita": ("Moscow", "Russia"),
    "root": ("Sidney", "Australia"),
    "anonymous": ("NoCity", "NoCountry"),
}


def event_to_track(request, event, properties):
    parsed_ua = user_agent_parser.Parse(request.headers["User-Agent"])
    username = request.user.username if request.user.username != "" else "anonymous"

    city = user_dist[username][0]
    country = user_dist[username][1]

    properties.update({
        "$browser": parsed_ua["user_agent"]["family"],
        "$device": parsed_ua["device"]["family"],
        "$os": parsed_ua["os"]["family"],
        "$city": city,
        "mp_country_code": country
    })

    mp.track(username, event, properties)
