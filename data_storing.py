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
        with open(self.file_path, "w", newline="") as file:
            writer = csv.writer(file)

            for key in kwargs:
                if key == "town_hall":
                    pass
                elif key == "rocks_removed":
                    pass
                elif key == "total_gold":
                    pass
                elif key == "total_elixir":
                    pass
                elif key == "bases_searched":
                    pass
                else:
                    raise KeyError("Parameter does not exist")

    def get_account_info(self, account_number: int) -> list:
        """
        Returns the stored data about an account given its number in the list
        [town hall level, if the rocks have been removed, total gold read, total elixir read, total bases searched]
        :param account_number: The number corresponding to where the account is in the Supercell ID account menu
        :return: A list containing the corresponding data for the account number
        """
        with open(self.file_path, "r") as file:
            reader = csv.reader(file)
            i = 0
            for row in reader:
                if i == account_number:
                    return row
                i += 1

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
