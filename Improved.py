from csv import DictReader
from glob import glob
from calendar import month_name
import argparse

months = {'1': 'Jan', '2': 'Feb', '3': 'Mar',  # All month names
          '4': 'Apr', '5': 'May', '6': 'Jun',
          '7': 'Jul', '8': 'Aug', '9': 'Sep',
          '10': 'Oct', '11': 'Nov', '12': 'Dec'}
italic_start, italic_end, red, blue = '\x1b[3m', '\x1b[0m', '\u001b[31m', '\u001b[34m'  # Escape Sequebces


class TemperatureStats:
    def __init__(self, arg):
        year, month = "", ""
        if arg.e is not None:
            year = arg.e
            month = "*"
        else:
            for line in arg.__dict__:
                if arg.__dict__.get(line) is not None:
                    year, month = arg.__dict__.get(line).split('/')
                    break
            month = months[month]
        path = f"{arg.path_to_file}/Murree_weather_{year}_{month}.txt"
        file_names = glob(path)
        if not file_names:
            raise Exception("File not Found")
        self.files_data = []
        self.__get_files_data(file_names)

    def __get_files_data(self, names):
        for file_name in names:
            with open(file_name, 'r') as file:
                file_data = DictReader(file)
                for row in file_data:
                    self.files_data.append(row)

    def max_number(self, key):
        max_num, date = 0, ""
        for row in self.files_data:
            if row[key] != "":
                number = int(row[key])
                if number > max_num:
                    max_num = number
                    date = row['PKT']
        date = self.__numerical_month_to_alphabetical(date)
        return max_num, date

    def min_number(self, key):
        min_num, date = 1000, ""
        for row in self.files_data:
            if row[key] != "":
                number = int(row[key])
                if number < min_num:
                    min_num = number
                    date = row['PKT']
        date = self.__numerical_month_to_alphabetical(date)
        return min_num, date

    @staticmethod
    def __numerical_month_to_alphabetical(temp_date):  # changing num month to alpha month
        year, month, date = temp_date.split('-')
        month = month_name[int(month)]
        return f"{month} {date}"

    def calc_average(self, key):
        data = []
        for row in self.files_data:
            if row[key] != '':
                num = int(row[key])
                data.append(num)
        return int(sum(data) / len(data))

    def horizontal_bar(self, key1, key2, num_bars):
        num1, num2 = 0, 0
        for index, row in enumerate(self.files_data):
            if row[key1] != '' and row[key2] != '':
                num1 = int(row[key1])
                num2 = int(row[key2])
            if num_bars == 1:
                self.__one_horizontal_bar(index + 1, num1, num2)
            if num_bars == 2:
                self.__two_horizontal_bars(index + 1, num1, num2)

    @staticmethod
    def __two_horizontal_bars(value, number1, number2):  # 2 line bar first is for max temp and second for min temp
        print(f"{italic_start}{value}{italic_end}", end=" ")
        for counter in range(number1):
            print(f'{red}{italic_start}+{italic_end}', end="")
        print(f"{italic_start} {number1}C{italic_end}")
        print(f"{italic_start}{value}{italic_end}", end=" ")
        for counter in range(number2):
            print(f'{blue}{italic_start}+{italic_end}', end="")
        print(f"{italic_start} {number2}C{italic_end}")

    @staticmethod
    def __one_horizontal_bar(value, number1, number2):  # 1 line bar first is for max temp and second for min temp
        print(f"{italic_start}{value}{italic_end}", end=" ")
        for counter in range(number1):
            print(f'{red}{italic_start}+{italic_end}', end="")
        for counter in range(number2):
            print(f'{blue}{italic_start}+{italic_end}', end="")
        print(f"{italic_start}{number1}C-{number2}C{italic_end}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', help="Enter Year to get max and min temperature")
    parser.add_argument('-a', help="Enter year and month to get average of temperatures")
    parser.add_argument('-u', help="Enter year and month for two bar graphical representation")
    parser.add_argument('-b', help="Enter year and month for one bar graphical representation")
    parser.add_argument('path_to_file', help="Enter the path where files are located")  # path to file
    args = parser.parse_args()
    obj = TemperatureStats(args)
    if args.e:
        max_temperature, date1 = obj.max_number('Max TemperatureC')
        min_temperature, date2 = obj.min_number('Min TemperatureC')
        max_humidity, date3 = obj.max_number('Max Humidity')
        print(f"Highest: {max_temperature}C on {date1}")
        print(f"Lowest: {min_temperature}C on {date2}")
        print(f"Humid: {max_humidity}% on {date3}")
    elif args.a:
        avg_max_temp = obj.calc_average('Max TemperatureC')
        avg_min_temp = obj.calc_average('Min TemperatureC')
        avg_humidity = obj.calc_average('Max Humidity')
        print(f"Highest Average: {avg_max_temp}C")
        print(f"Lowest Average: {avg_min_temp}C")
        print(f"Humidity Average: {avg_humidity}%")
    elif args.u:
        year, month = args.u.split('/')
        month = month_name[int(month)]
        print(f"{month} {year}")
        obj.horizontal_bar('Max TemperatureC', 'Min TemperatureC', 2)
    elif args.b:
        year, month = args.b.split('/')
        month = month_name[int(month)]
        print(f"{month} {year}")
        obj.horizontal_bar('Max TemperatureC', 'Min TemperatureC', 1)
    else:
        raise Exception("Invalid Argument")

if __name__ == '__main__':
    main()
