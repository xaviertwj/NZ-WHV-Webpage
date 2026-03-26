def load_gpx_data(base_folder="data/gpx"):
    import os
    import gpxpy
    import pandas as pd

    all_data = []

    for island in ["north", "south"]:
        folder = os.path.join(base_folder, island)

        for file in os.listdir(folder):
            if file.endswith(".gpx"):
                with open(os.path.join(folder, file), "r") as f:
                    gpx = gpxpy.parse(f)

                    for track in gpx.tracks:
                        for segment in track.segments:
                            for point in segment.points:
                                all_data.append({
                                    "lat": point.latitude,
                                    "lon": point.longitude,
                                    "activity": file.replace(".gpx", "").replace("_", " ").title(),
                                    "island": "North Island" if island == "north" else "South Island"
                                })

    return pd.DataFrame(all_data)
