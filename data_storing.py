from os.path import exists
import csv


class DataStorer:
    """
    Stores data for each account including Town hall level, if the rocks have been removed, and attacking resource
    averages
    """

    file_path = "account_data.csv"
    number_of_accounts = 1

    def __init__(self, number_of_accounts: int):
        self.number_of_accounts = number_of_accounts

    def update_account_info(self, account_number: int, **kwargs):
        """
        Updates the stored data about an account given its number and a value
        :param account_number: The number corresponding to where the account is in the Supercell ID account menu
        :param kwargs: updates the stored value with the given value
        town_hall: int
        rocks_removed: bool
        total_gold: int
        total_elixir: int
        bases_searched: int
        :return:
        """
        # Reads all the rows
        rows = []
        with open(self.file_path, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                rows.append(row)

        # Updates the value in the row based on the key
        for key, value in kwargs.items():
            with open(self.file_path, "w", newline="") as file:
                writer = csv.writer(file)
                # Gets the writer to the correct row without changing the previous rows
                writer.writerows(rows[:account_number])

                new_row = rows[account_number]

                if key == "town_hall":
                    new_row[0] = value
                elif key == "rocks_removed":
                    new_row[1] = value
                elif key == "total_gold":
                    new_row[2] = value
                elif key == "total_elixir":
                    new_row[3] = value
                elif key == "bases_searched":
                    new_row[4] = value
                else:
                    writer.writerows(rows[account_number:])  # Saves the rest of the data before raising the error
                    raise KeyError("Parameter does not exist")

                # Writes the rest of the file
                writer.writerow(new_row)
                writer.writerows(rows[account_number + 1:])

    def get_account_info(self, account_number: int) -> list:
        """
        Returns the stored data about an account given its number in the list
        [town hall level, if the rocks have been removed, total gold read, total elixir read, total bases searched]
        :param account_number: The number corresponding to where the account is in the Supercell ID account menu
        :return: A list containing the corresponding data for the account number
        """
        with open(self.file_path, "r") as file:
            reader = csv.reader(file)
            # Gets the specific row, then returns it
            for i, row in enumerate(reader):
                if i == account_number:
                    return row

    def add_new_accounts(self):
        """
        Adds rows for newly added accounts or creates the file for data storage if it doesn't exist
        :param number_of_accounts: The number of Supercell ID accounts connected to the device
        :return:
        """
        if not exists(self.file_path):
            # Makes the csv file rows to the csv file assuming each newly added account is a Town hall 2 with no rocks removed
            with open(self.file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows([[2, False, 0, 0, 0]] * self.number_of_accounts)
        else:
            # Reads all the rows
            rows = []
            with open(self.file_path, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    rows.append(row)

            # Adds new rows to the csv file for newly added Supercell ID accounts
            if len(rows) < self.number_of_accounts:
                with open(self.file_path, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
                    writer.writerows([[2, False, 0, 0, 0]] * (self.number_of_accounts - len(rows)))
