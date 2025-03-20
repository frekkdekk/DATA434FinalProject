# Goal: get average index from each date columns. a time series of all county home value indexes in Oregon.

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
    
def get_average_by_date(data_list: list) -> dict:
    """Computes the average home value index for each date column."""
    
    if not data_list:
        return {}

    # Identify date columns
    first_row = data_list[0]
    exclude_set = ("RegionID","SizeRank","RegionName","RegionType","StateName","State","City","Metro","CountyName")
    date_columns = [col for col in first_row if col not in exclude_set]

    # Dictionary to store total values and counts for each date
    date_totals = {date: [0, 0] for date in date_columns}  # {date: [total_index, count]}

    # Sum up values for each date column
    for record in data_list:
        for date in date_columns:
            try:
                value = float(record[date])  # Convert to float
                date_totals[date][0] += value  # Add to total
                date_totals[date][1] += 1  # Increment count
            except ValueError:
                continue  # Skip if value is missing or invalid

    # Compute averages
    date_averages = {date: total / count if count > 0 else None for date, (total, count) in date_totals.items()}

    return date_averages

def write_date_indexes_to_file(date_indexes: dict, output_path: str) -> None:
    """Writes the average home value index per date to a CSV file."""
    
    if not output_path.endswith(".csv"):
        output_path += ".csv"
        
    try:
        with open(output_path, "w", newline="") as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(["Date", "Average Home Value Index"])
            
            # Write data sorted by date
            for date, avg_index in sorted(date_indexes.items()):
                writer.writerow([date, f"{avg_index:.2f}" if avg_index is not None else "N/A"])
                
        print(f"Successfully wrote date indexes to {output_path}")
    except Exception as e:
        raise Exception(f"Error writing to CSV file: {e}")


def main():
    path = "oregon_zillow_homes.csv"
    data_list = csv_to_list(path)
    date_indexes = get_average_by_date(data_list)
    write_path = "average_oregon_home_value_timeseries.csv"
    write_date_indexes_to_file(date_indexes, write_path)
    
if __name__ == "__main__":
    main()