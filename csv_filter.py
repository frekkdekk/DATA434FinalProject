import csv

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


def oregon_filter(data: list) -> list:
    """Takes a list of dicts and returns only records from Oregon."""
    if not isinstance(data, list):
        raise TypeError("oregon_filter(data): parameter must be of type list.")

    # Use list comprehension to filter records
    return [record for record in data if record.get("StateName") == "OR"]


def write_oregon_csv(data: list, path: str) -> None:
    """Takes a list of dicts and writes them to a CSV file."""
    if not path.endswith(".csv"):
        raise ValueError("write_oregon_csv(data, path): file must be of type CSV.")

    if not data:
        raise ValueError("write_oregon_csv(data, path): data list is empty.")

    # Extract field names (headers) from the first dictionary
    fieldnames = data[0].keys()

    try:
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        raise Exception(f"Error writing to CSV file: {e}")


if __name__ == "__main__":
    # the file to be read
    reading_path = "zillow_home_values.csv"
    
    # the location to write results to
    writing_path = "oregon_zillow_homes.csv"
    
    try:
        csv_list = csv_to_list(reading_path)
        oregon_csv_list = oregon_filter(csv_list)
        write_oregon_csv(oregon_csv_list, writing_path)
        print(f"Filtered data written to {writing_path}")
        
    except Exception as e:
        print(f"An error occurred: {e}")