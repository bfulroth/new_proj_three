from .hash_str import get_csci_salt, get_user_id, hash_str
from .io import atomic_write
import pandas as pd


def get_user_hash(username, salt=None):
    salt = salt or get_csci_salt()
    return hash_str(username, salt=salt)


if __name__ == "__main__":

    for user in ["gorlins", "bfulroth"]:
        print("Id for {}: {}".format(user, get_user_id(user)))

    data_source = "data/hashed.xlsx"

    # Read in the data from Amazon S3 into a DataFrame
    df = pd.read_excel(data_source)

    # Transform data in DataFrame to Parquet. Use my atomic_write context manager.
    with atomic_write("data/excel_data_to_parquet.parquet", mode="w+b") as file:
        df.to_parquet(file, engine="pyarrow")

    # Store the 'hashed_id column from the written parquet file.
    result = pd.read_parquet(
        "data/excel_data_to_parquet.parquet", engine="pyarrow", columns=["hashed_id"]
    )

    # Print the hashed_id column.
    print(result)
