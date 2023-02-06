import glob
import argparse

months = ['January', 'February', 'March',  # All month names
          'April', 'May', 'June',
          'July', 'August', 'September',
          'October', 'November', 'December']


class FilesNames:  # handling file names with this class
    @staticmethod
    def file_names_of_whole_year(path, year):  # Getting the names of all file names with specific year
        path_to_file = f"{path}/Murree_weather_{year}_{'*'}.txt"
        names_of_files = glob.glob(path_to_file)  # returns list of files names which matches
        if not names_of_files:  # raising exception if file not found
            raise Exception("Files not found")
        return names_of_files

    @staticmethod
    def get_data_of_single_file(path, year, month):  # getting the name of file with year and month
        mon = months[month - 1]
        path_to_file = f"{path}/Murree_weather_{year}_{mon[:3]}.txt"
        name_of_file = glob.glob(path_to_file)
        if not name_of_file:
            raise Exception("File not found")
        name1 = ""
        name1 = name1.join(name_of_file)  # file_name is list to convert to str
        data1 = []  # to store the data of file
        with open(name1, 'r') as file1:
            for row in file1:
                temp1 = (row.strip()).split(',')
                data1.append(temp1)
        return data1


class TemperatureStats(FilesNames):  # to find average, max and min values of dataset
    @staticmethod
    def maximum_num(data1, max_num, date, idx):
        for indx in range(1, len(data1)):
            if data1[indx][idx] != '':  # it skips the iteration if this condition is true
                number = int(data1[indx][idx])
                if number > max_num:
                    max_num = number
                    date = data1[indx][0]
        return max_num, date  # returning max and date

    @staticmethod
    def minimum_num(data1, min_num, date):  # minimum Temperature
        for indx in range(1, len(data1)):
            if data1[indx][3] != '':
                number = int(data1[indx][3])
                if number < min_num:
                    min_num = number
                    date = data1[indx][0]
        return min_num, date

    @staticmethod
    def numerical_month_to_alphabetical(date):  # changing num month to alpha month
        date = date.split('-')
        return f"{months[int(date[1]) - 1]} {date[2]}"

    @staticmethod
    def average(data1, idx):  # Calculating the Average
        _list = []
        for indx in range(1, len(data1)):
            if data1[indx][idx] != '':
                num = int(data1[indx][idx])
                _list.append(num)
        return sum(_list) / len(_list)

    @staticmethod
    def two_horizontal_bars(value, number1, number2):  # 2 line bar first is for max temp and second for min temp
        print(f"\x1b[3m{value}\x1b[0m", end=" ")  # these are escape sequence making text italic
        for counter in range(number1):
            print("\u001b[31m" + '\x1b[3m+\x1b[0m', end="")  # \u001b[31m = Red
        print(f"\x1b[3m {number1}C\x1b[0m")
        print(f"\x1b[3m{value}\x1b[0m", end=" ")
        for counter in range(number2):
            print("\u001b[34m" + '\x1b[3m+\x1b[0m', end="")  # \u001b[34m = Blue
        print(f"\x1b[3m {number2}C\x1b[0m")

    @staticmethod
    def one_horizontal_bar(value, number1, number2):
        print(f"\x1b[3m{value}\x1b[0m", end=" ")
        for counter in range(number1):
            print("\u001b[34m" + '\x1b[3m+\x1b[0m', end="")
        for counter in range(number2):
            print("\u001b[31m" + '\x1b[3m+\x1b[0m', end="")
        print(f"\x1b[3m{number1}C-{number2}C\x1b[0m")


parser = argparse.ArgumentParser()  # parsing arguments for Tasks
parser.add_argument('-e', help="Enter Year to get max and min temperature")  # Task 1 handling all files of year
parser.add_argument('-a', help="Enter year and month to get average of temperatures")  # Task 2 handling a single file
parser.add_argument('-u', help="Enter year and month for two bar graphical representation")  # 2 line horizontal bars
parser.add_argument('-b', help="Enter year and month for one bar graphical representation")  # 1 line horizontal bar
parser.add_argument('path_to_file', help="Enter the path where files are located")  # path to file
args = parser.parse_args()
if args.e:  # -e 2004 path_to_file
    obj = TemperatureStats()  # creating object for getting multiple names
    files_names = obj.file_names_of_whole_year(args.path_to_file, int(args.e))
    max_temp, min_temp, max_humidity = 0, 1000, 0
    date1, date2, date3 = 0, 0, 0
    for names in files_names:
        data_set = []
        with open(names, 'r') as file:
            for content in file:  #
                temp = (content.strip()).split(',')  # separating the row from commas and leading spaces
                data_set.append(temp)  # making 2D list of a file
        max_temp, date1 = obj.maximum_num(data_set, max_temp, date1, 1)  # file data, max_value,
        min_temp, date2 = obj.minimum_num(data_set, min_temp, date2)
        max_humidity, date3 = obj.maximum_num(data_set, max_humidity, date3, 7)
    date1 = obj.numerical_month_to_alphabetical(date1)
    date2 = obj.numerical_month_to_alphabetical(date2)
    date3 = obj.numerical_month_to_alphabetical(date3)
    print(f"Highest: {max_temp}C on {date1}")
    print(f"Lowest: {min_temp}C on {date2}")
    print(f"Humid: {max_humidity}% on {date3}")
elif args.a:  # average of max temp,  min temp, humidity
    obj = TemperatureStats()
    data = obj.get_data_of_single_file(args.path_to_file,
                                       args.a[:4], int(args.a[5:]))  # name of file with year and month
    avg_max_temp = obj.average(data, 1)
    avg_min_temp = obj.average(data, 3)
    avg_humidity = obj.average(data, 7)
    print(f"Highest Average: {round(avg_max_temp)}C")
    print(f"Lowest Average: {round(avg_min_temp)}C")
    print(f"Average Humidity: {round(avg_humidity)}%")
elif args.u:  # min and max temperature in 2 line bars
    obj = TemperatureStats()
    data = obj.get_data_of_single_file(args.path_to_file, args.u[:4], int(args.u[5:]))
    entered_month = months[int(args.u[5:]) - 1]
    print(f"{entered_month} {args.u[:4]}")
    for index in range(1, len(data)):
        if data[index][1].isnumeric() != '' and data[index][3] != '':
            num1 = int(data[index][1])
            num2 = int(data[index][3])
            obj.two_horizontal_bars(index, num1, num2)
elif args.b:  # max min temperature in single line horizontal bar
    obj = TemperatureStats()
    data = obj.get_data_of_single_file(args.path_to_file, args.b[:4], int(args.b[5:]))
    entered_month = months[int(args.b[5:]) - 1]
    print(f"{entered_month} {args.b[:4]}")
    for index in range(1, len(data)):
        if data[index][1].isnumeric() != '' and data[index][3] != '':
            num1 = int(data[index][1])
            num2 = int(data[index][3])
            obj.one_horizontal_bar(index, num1, num2)
else:
    raise Exception("Argument is incorrect")
