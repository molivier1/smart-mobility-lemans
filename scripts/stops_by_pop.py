import pandas as pd


def main():
    stops = pd.read_csv("data/gtfs_static/stops_frequency.csv")
    communes = pd.read_csv("data/reference/communes.csv")

    # Sum stop visits by commune
    supply = stops.groupby("nearest_commune")["daily_trip_count"].sum().reset_index()

    # Keep all communes, including those without stops
    result = communes[["commune", "population"]].merge(
        supply, left_on="commune", right_on="nearest_commune", how="left"
    )
    result["daily_trip_count"] = result["daily_trip_count"].fillna(0)

    # Daily stop visits per 1,000 residents
    result["passages_per_1000_residents"] = (
        result["daily_trip_count"] / result["population"] * 1000
    )

    result = result.sort_values("passages_per_1000_residents")
    result = result[["commune", "population", "daily_trip_count", "passages_per_1000_residents"]]

    result.to_csv("data/gtfs_static/stops_by_pop.csv", index=False)
    print(result.to_string(index=False))


if __name__ == "__main__":
    main()
