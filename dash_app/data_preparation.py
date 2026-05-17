import polars as pl
import pandas as pd


####
## Dataset loading
## Here we load from the parquet files the tpg data, and we do some pre-processing to be able to use it in the app
####
initial_dataset_df = pl.read_parquet("./data/line_aggregated_tpg_and_meteo.parquet")

# Save some of the date info in case
min_date_dataset = initial_dataset_df["Date"].min()
max_date_dataset = initial_dataset_df["Date"].max()

# Remove the columns that we won't use for the analysis
columns_to_drop = ["total_number_of_disembarking_passengers"]

dataset_df = initial_dataset_df.drop(columns_to_drop)

# Aggregate by line and sum daily ridership for all lines
daily_ridership_all_lines_pdf = dataset_df.group_by("Date").agg(pl.sum("total_number_of_boarding_passengers"),
                                  pl.first("day_week"),
                                  pl.first("is_autumn_vacation"),
                                  pl.first("is_winter_vacation"),
                                  pl.first("is_february_vacation"),
                                  pl.first("is_easter_vacation"),
                                  pl.first("is_summer_vacation"),
                                  pl.first("is_public_holiday")).sort("Date").to_pandas()

# Create individual dataframes for the vacation periods, keeping only the dates,
# to be able to easily add shading in the graph for the selected vacation periods
autumn_vacation_df = daily_ridership_all_lines_pdf[daily_ridership_all_lines_pdf["is_autumn_vacation"] == True]["Date"]
winter_vacation_df = daily_ridership_all_lines_pdf[daily_ridership_all_lines_pdf["is_winter_vacation"] == True]["Date"]
february_vacation_df = daily_ridership_all_lines_pdf[daily_ridership_all_lines_pdf["is_february_vacation"] == True]["Date"]
easter_vacation_df = daily_ridership_all_lines_pdf[daily_ridership_all_lines_pdf["is_easter_vacation"] == True]["Date"]
summer_vacation_df = daily_ridership_all_lines_pdf[daily_ridership_all_lines_pdf["is_summer_vacation"] == True]["Date"]

# In each dataframe, identify the start and end of each vacation period, to be able to add a single rectangle for each vacation period in the graph instead of one for each day
def get_vacation_periods(vacation_dates):
    vacation_periods = []
    current_vacation_start = None

    for date in vacation_dates:
        if current_vacation_start is None:
            current_vacation_start = date
        elif (date - previous_date).days > 1:
            vacation_periods.append((current_vacation_start, previous_date))
            current_vacation_start = date
        previous_date = date

    if current_vacation_start is not None:
        vacation_periods.append((current_vacation_start, previous_date))

    return vacation_periods

autumn_vacation_periods = get_vacation_periods(autumn_vacation_df)
winter_vacation_periods = get_vacation_periods(winter_vacation_df)
february_vacation_periods = get_vacation_periods(february_vacation_df)
easter_vacation_periods = get_vacation_periods(easter_vacation_df)
summer_vacation_periods = get_vacation_periods(summer_vacation_df)

# Put them in a dictionary to be able to easily access them in the graph function
vacation_periods_df_dict = {
    "is_autumn_vacation": autumn_vacation_periods,
    "is_winter_vacation": winter_vacation_periods,
    "is_february_vacation": february_vacation_periods,
    "is_easter_vacation": easter_vacation_periods,
    "is_summer_vacation": summer_vacation_periods
}


####
## Put together some info about the current (May 2026) tpg lines. This will be useful for the data selection and graphing
####

# We create list of lines for different type of transportation, with their color code.
tramway_lines = [12, 14, 15, 17, 18]
tramway_lines_color = ["#F5A300", "#5A1E82", "#84471C", "#00ACE7", "#B82F89"]

trolleybus_lines = [2, 3, 6, 7, 10, 19]
trolleybus_lines_color = ["#D2DB4A", "#B82F89", "#008CBE", "#00A828", "#006E3D", "#A05909"]

bus_lines = [1, 5, 8, 9,
             11,
             20, 21, 22, 23, 25, 28,
             31, 32, 33, 34, 37, 38, 39,
             40, 41, 42, 43, 44, 45, 46, 47, 48,
             50, 51, 52, 53, 54, 55, 57, 58, 59,
             60, 61, 64, 66, 67, 68, 69,
             70, 71, 72, 73, 74, 75, 78,
             80, 82, 83,
             91, 92,
             "A", "E", "G", "L"]
bus_lines_color = ["#5E5E5E" for _ in bus_lines] # We use a default grey color, and we add specific color for a few lines
bus_lines_color[bus_lines.index(1)] = "#5A1E82" # Line 1
bus_lines_color[bus_lines.index(5)] = "#00ACE7" # Line 5
bus_lines_color[bus_lines.index(8)] = "#84471C" # Line 8
bus_lines_color[bus_lines.index(9)] = "#E2001D" # Line 9
bus_lines_color[bus_lines.index(11)] = "#82419E" # Line 11
bus_lines_color[bus_lines.index(20)] = "#00A828" # Line 20
bus_lines_color[bus_lines.index(21)] = "#78003C" # Line 21
bus_lines_color[bus_lines.index(22)] = "#5A1E82" # Line 22
bus_lines_color[bus_lines.index(23)] = "#B82F89" # Line 23
bus_lines_color[bus_lines.index(25)] = "#A05909" # Line 25
bus_lines_color[bus_lines.index(28)] = "#82419E" # Line 28

express_lines = ["E+", "G+"]
express_lines_color = ["#000000", "#000000"]

school_lines = ["C1", "C3", "C4", "C5", "C6", "C7", "C8", "C9"]
school_lines_color = ["#000000" for _ in school_lines]

crossborder_lines = [271, 272, 274, "M", "N"]
crossborder_lines_color = ["#5E5E5E" for _ in crossborder_lines]

# Create a dictionary with the line properties (color, name, etc.)
line_info_dict = {
    "tramway": (tramway_lines, tramway_lines_color),
    "trolleybus": (trolleybus_lines, trolleybus_lines_color),
    "bus": (bus_lines, bus_lines_color),
    "express": (express_lines, express_lines_color),
    "school": (school_lines, school_lines_color),
    "crossborder": (crossborder_lines, crossborder_lines_color)
}

# Add the line type and the line color to the main pandas dataframe, by merging it with the line_info_dict

line_number_and_color_df = pd.DataFrame({
    "Line": line_info_dict["tramway"][0] + line_info_dict["trolleybus"][0] + line_info_dict["bus"][0] + line_info_dict["express"][0] + line_info_dict["school"][0] + line_info_dict["crossborder"][0],
    "line_color": line_info_dict["tramway"][1] + line_info_dict["trolleybus"][1] + line_info_dict["bus"][1] + line_info_dict["express"][1] + line_info_dict["school"][1] + line_info_dict["crossborder"][1],
    "line_transport_type": ["tramway"] * len(line_info_dict["tramway"][0]) + ["trolleybus"] * len(line_info_dict["trolleybus"][0]) + ["bus"] * len(line_info_dict["bus"][0]) + ["express"] * len(line_info_dict["express"][0]) + ["school"] * len(line_info_dict["school"][0]) + ["crossborder"] * len(line_info_dict["crossborder"][0])
})
# Convert the Line column to the same type as in the main dataframe (string)
line_number_and_color_df["Line"] = line_number_and_color_df["Line"].astype(str)

daily_ridership_all_lines_with_line_info_pdf = dataset_df.to_pandas().merge(line_number_and_color_df, on="Line", how="left")

daily_ridership_per_line_transport_type_pdf = daily_ridership_all_lines_with_line_info_pdf.groupby(["Date", "line_transport_type"]).agg({"total_number_of_boarding_passengers": "sum"}).reset_index().sort_values("Date")
