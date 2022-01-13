from math import cos, asin, sqrt

# helper method to calculate aproximate distance between two coordinates
def coordinateDistance(lat1, lon1, lat2, lon2):

    p = 0.017453292519943295
    c = cos
    a = (
        0.5
        - c((lat2 - lat1) * p) / 2
        + c(lat1 * p) * c(lat2 * p) * (1 - c((lon2 - lon1) * p)) / 2
    )
    return 12742 * asin(sqrt(a))
