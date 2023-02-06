import glob
import argparse

months = ['January', 'February', 'March',  # All month names
          'April', 'May', 'June',
          'July', 'August', 'September',
          'October', 'November', 'December']


class FilesNames:  # handling file names with this class
    @staticmethod
    def file_names_whole_year(path, year):  # Getting the names of all file names with specific year
        path_to_file = f"{path}/Murree_weather_{year}_{'*'}.txt"
        names_of_files = glob.glob(path_to_file)  # returns list of files names which matches
        if not names_of_files:  # raising exception if file not found
            raise Exception("Files not found")
        return names_of_files

    @staticmethod
    def file_name(path, year, month):  # getting the name of file with year and month
        mon = months[month - 1]
        path_to_file = f"{path}/Murree_weather_{year}_{mon[:3]}.txt"
        name_of_file = glob.glob(path_to_file)
        if not name_of_file:
            raise Exception("File not found")
        return name_of_file


class TemperatureStats:  # to find average, max and min values of dataset
    @staticmethod
    def max_temperature(data1, max_num, date):
        for indx in range(1, len(data1)):
            if data1[indx][1] == '':  # it skips the iteration if this condition is true
                continue
            number = int(data1[indx][1])
            if number > max_num:
                max_num = number
                date = data1[indx][0]

        return max_num, date  # returning max and date

    @staticmethod
    def min_temperature(data1, min_num, date):  # minimum Temperature
        for indx in range(1, len(data1)):
            if data1[indx][3] == '':
                continue
            number = int(data1[indx][3])
            if number < min_num:
                min_num = number
                date = data1[indx][0]

        return min_num, date

    @staticmethod
    def max_humidity(data1, max_humid, date):  # Maximum Humidity
        for indx in range(1, len(data1)):
            if data1[indx][7] == '':
                continue
            num3 = int(data1[indx][7])
            if num3 > max_humid:
                max_humid = num3
                date = data1[indx][0]

        return max_humid, date

    @staticmethod
    def numerical_month_to_alphabetical(date):  # changing num month to alpha month
        date = date.split('-')
        return f"{months[int(date[1]) - 1]} {date[2]}"

    @staticmethod
    def max_temp_average(data1):  # calculating the max temperature avg
        sum1 = 0
        count = 0
        for indx in range(1, len(data1)):
            if data1[indx][1] == "":
                continue
            num = int(data1[indx][1])
            sum1 += num
            count += 1
        return sum1 / count

    @staticmethod
    def min_temp_average(data1):
        sum1 = 0
        count = 0
        for indx in range(1, len(data1)):
            if data1[indx][3] == "":
                continue
            num = int(data1[indx][3])
            sum1 += num
            count += 1
        return sum1 / count

    @staticmethod
    def humidity_average(data1):
        sum1 = 0
        count = 0
        for indx in range(1, len(data1)):
            if data1[indx][7] == "":
                continue
            num = int(data1[indx][7])
            sum1 += num
            count += 1
        return sum1 / count

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
# Task 1
if args.e:  # -e 2004 path_to_file
    names = FilesNames()  # creating object for getting multiple names
    files_names = names.file_names_whole_year(args.path_to_file, int(args.e))
    obj = TemperatureStats()
    max_temp, min_temp, max_humidity = 0, 1000, 0
    date1, date2, date3 = 0, 0, 0
    for names in files_names:
        data_set = []
        with open(names, 'r') as file:
            for content in file:  #
                temp = (content.strip()).split(',')  # separating the row from commas and leading spaces
                data_set.append(temp)  # making 2D list of a file
        max_temp, date1 = obj.max_temperature(data_set, max_temp, date1)
        min_temp, date2 = obj.min_temperature(data_set, min_temp, date2)
        max_humidity, date3 = obj.max_humidity(data_set, max_humidity, date3)

    date1 = obj.numerical_month_to_alphabetical(date1)
    date2 = obj.numerical_month_to_alphabetical(date2)
    date3 = obj.numerical_month_to_alphabetical(date3)
    print(f"Highest: {max_temp}C on {date1}")
    print(f"Lowest: {min_temp}C on {date2}")
    print(f"Humid: {max_humidity}% on {date3}")

# Task 2
elif args.a:  # average of max temp,  min temp, humidity
    avg_max_temp, avg_min_temp, avg_humidity = 0, 0, 0
    name = FilesNames()
    file_name = name.file_name(args.path_to_file,
                               args.a[:4], int(args.a[5:]))  # name of file with year and month
    name = ""
    name = name.join(file_name)  # file_name is list to convert to str
    data = []  # to store the data of file
    with open(name, 'r') as file:
        for row in file:
            temp = (row.strip()).split(',')
            data.append(temp)
    obj = TemperatureStats()
    avg_max_temp = obj.max_temp_average(data)
    avg_min_temp = obj.min_temp_average(data)
    avg_humidity = obj.humidity_average(data)
    print(f"Highest Average: {round(avg_max_temp)}C")
    print(f"Lowest Average: {round(avg_min_temp)}C")
    print(f"Average Humidity: {round(avg_humidity)}%")

# Task 3
elif args.u:  # min and max temperature in 2 line bars
    name = FilesNames()
    file_name = name.file_name(args.path_to_file, args.u[:4], int(args.u[5:]))
    name = ""
    name = name.join(file_name)
    data = []
    with open(name, 'r') as file:
        for row in file:
            temp = (row.strip()).split(',')
            data.append(temp)
    entered_month = months[int(args.u[5:]) - 1]
    print(f"{entered_month} {args.u[:4]}")
    for index in range(1, len(data)):
        if data[index][1] == "" and data[index][3] == "":
            continue
        num1 = int(data[index][1])
        num2 = int(data[index][3])
        obj = TemperatureStats()
        obj.two_horizontal_bars(index, num1, num2)

elif args.b:  # max min temperature in single line horizontal bar
    name = FilesNames()
    file_name = name.file_name(args.path_to_file, args.b[:4], int(args.b[5:]))
    name = ""
    name = name.join(file_name)
    data = []
    with open(name, 'r') as file:
        for row in file:
            temp = (row.strip()).split(',')
            data.append(temp)
    entered_month = months[int(args.b[5:]) - 1]
    print(f"{entered_month} {args.b[:4]}")
    for index in range(1, len(data)):
        num1 = int(data[index][1])
        num2 = int(data[index][3])
        obj = TemperatureStats()
        obj.one_horizontal_bar(index, num1, num2)

else:
    raise Exception("Argument is incorrect")
