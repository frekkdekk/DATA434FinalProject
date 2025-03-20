# Goal: Median home price by County.
import csv
import datetime

def csv_to_list(path: str) -> list:
    """Takes the CSV file name/path and returns a list of the data."""
    if not path.endswith(".csv"):
        raise ValueError("csv_to_list(path): file must be of type CSV.")

    try:
        with open(path, "r") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    except Exception as e:
        raise Exception(f"Error reading CSV file: {e}")
    
def get_avg_index(listing: dict) -> float:
    print(listing)
    total_index = 0
    for key, value in listing.items():
        try:
            if not key or key in ["CountyName", "RegionID", "SizeRank", "RegionName", "RegionType", "StateName", "State", "City", "Metro"]:
                continue
            if value != "":
                date_key = datetime.datetime.strptime(key, "%Y-%m-%d").date()
                target_date = datetime.date(2025, 1, 31)
                if date_key == target_date:
                    total_index += float(value)
        except (ValueError, TypeError):
            # Skip keys that can't be parsed as dates
            continue
    
    return total_index

def get_county_indexes(dict_list: list) -> dict:
    if type(dict_list) != list:
        raise TypeError("Input must be of type list.")
    
    # County: Average Index
    counties = {}
    county_count = {}
    
    for listing in dict_list:
        # pull out the county name
        county_name = listing.get("CountyName", "Unknown")
        
        # split the "county" from "marion county"
        county_name_list = county_name.split(" ")
        
        # turn it into "MARION"
        county_normalized = county_name_list[0].upper()
        
        # check if we've already seen a marion listing
        if county_normalized not in counties:
            # if not, we add the new county
            county_count[county_normalized] = 0
            counties[county_normalized] = 0
            
        # get the average index for the listing
        average_index = get_avg_index(listing)
        
        # increment respective counties index
        counties[county_normalized] += average_index
        county_count[county_normalized] += 1
        
    # average each county using the count dictionary
    for county, index in counties.items():
        counties[county] = index / county_count[county]
        
    return counties

def write_county_indexes_to_file(county_indexes: dict, output_path: str) -> None:
    if not output_path.endswith(".csv"):
        output_path += ".csv"
        
    try:
        with open(output_path, "w", newline="") as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(["County", "Average Home Value Index"])
            
            # Write data sorted by county name
            for county, avg_index in sorted(county_indexes.items()):
                writer.writerow([county, f"{avg_index:.2f}"])
                
        print(f"Successfully wrote county indexes to {output_path}")
    except Exception as e:
        raise Exception(f"Error writing to CSV file: {e}")
    

if __name__ == "__main__":
    path = "oregon_zillow_homes.csv"
    data_list = csv_to_list(path)
    county_averages = get_county_indexes(data_list)
    print(county_averages)
    output_file = "oregon_county_home_values.csv"
    write_county_indexes_to_file(county_averages, output_file)
    