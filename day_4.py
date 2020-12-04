"""
--- Day 4: Passport Processing ---
You arrive at the airport only to realize that you grabbed your North Pole Credentials instead of your passport.
While these documents are extremely similar, North Pole Credentials aren't issued by a country and therefore aren't
actually valid documentation for travel in most of the world.

It seems like you're not the only one having problems, though; a very long line has formed for the automatic passport
scanners, and the delay could upset your travel itinerary.

Due to some questionable network security, you realize you might be able to solve both of these problems at the same
 time.

The automatic passport scanners are slow because they're having trouble detecting which passports have all required
fields. The expected fields are as follows:

byr (Birth Year)
iyr (Issue Year)
eyr (Expiration Year)
hgt (Height)
hcl (Hair Color)
ecl (Eye Color)
pid (Passport ID)
cid (Country ID)
Passport data is validated in batch files (your puzzle input). Each passport is represented as a sequence of
 key:value pairs separated by spaces or newlines. Passports are separated by blank lines.

Here is an example batch file containing four passports:

ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
The first passport is valid - all eight fields are present. The second passport is invalid - it is missing hgt
 (the Height field).

The third passport is interesting; the only missing field is cid, so it looks like data from North Pole Credentials,
 not a passport at all! Surely, nobody would mind if you made the system temporarily ignore missing cid fields. Treat
 this "passport" as valid.

The fourth passport is missing two fields, cid and byr. Missing cid is fine, but missing any other field is not, so
 this passport is invalid.

According to the above rules, your improved system would report 2 valid passports.

Count the number of valid passports - those that have all required fields. Treat cid as optional. In your batch file,
 how many passports are valid?

Part 2.

byr (Birth Year) - four digits; at least 1920 and at most 2002.
iyr (Issue Year) - four digits; at least 2010 and at most 2020.
eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
hgt (Height) - a number followed by either cm or in:
If cm, the number must be at least 150 and at most 193.
If in, the number must be at least 59 and at most 76.
hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
pid (Passport ID) - a nine-digit number, including leading zeroes.
cid (Country ID) - ignored, missing or not.

"""
import numpy as np
import re


def read_passports_data(filepath):
    with open(filepath) as fp:
        data = ""
        passports_data = []
        count = 0
        for line in fp:
            line = line.strip("\n")
            if line == "":
                passports_data.append(data)
                data = ""
                count += 1
            else:
                if data == "":
                    data += line
                else:
                    data += (" " + line)
        # last one:
        passports_data.append(data)
    return passports_data


class Passport:
    def __init__(self, string=None):
        self.data = {}
        if string:
            self.read(string)

    def read(self, string):
        for item in string.split(" "):
            self.data[item.split(":")[0]] = item.split(":")[1]

    def has_required_keys(self):
        return set(self.data.keys()) >= {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}

    def byr_valid(self):
        return ("byr" in self.data.keys()) and \
               (re.search(r"^\d{4}$", self.data["byr"]) is not None) and \
               (int(self.data["byr"]) >= 1920) and \
               (int(self.data["byr"]) <= 2002)

    def iyr_valid(self):
        return ("iyr" in self.data.keys()) and \
               (re.search(r"^\d{4}$", self.data["iyr"]) is not None) and \
               (int(self.data["iyr"]) >= 2010) and \
               (int(self.data["iyr"]) <= 2020)

    def eyr_valid(self):
        return ("eyr" in self.data.keys()) and \
               (re.search(r"^\d{4}$", self.data["eyr"]) is not None) and \
               (int(self.data["eyr"]) >= 2020) and \
               (int(self.data["eyr"]) <= 2030)

    def hgt_valid(self):
        within_bounds = lambda hgt: ((int(hgt[:-2]) >= 150) and (int(hgt[:-2]) <= 193)) if hgt[-2:] == "cm" \
            else ((int(hgt[:-2]) >= 59) and (int(hgt[:-2]) <= 76))
        return ("hgt" in self.data.keys()) and \
               (re.search(r"^\d+(cm|in)$", self.data["hgt"]) is not None) and \
               within_bounds(self.data["hgt"])

    def hcl_valid(self):
        return ("hcl" in self.data.keys()) and \
               (re.search(r"^#[a-z0-9]{6}$", self.data["hcl"]) is not None)

    def ecl_valid(self):
        return ("ecl" in self.data.keys()) and \
               (re.search(r"^(amb|blu|brn|gry|grn|hzl|oth)$", self.data["ecl"]) is not None)

    def pid_valid(self):
        return ("pid" in self.data.keys()) and \
               (re.search(r"^[0-9]{9}$", self.data["pid"]) is not None)

    def all_valid(self):
        return np.array([
            self.byr_valid(),
            self.iyr_valid(),
            self.eyr_valid(),
            self.hgt_valid(),
            self.hcl_valid(),
            self.ecl_valid(),
            self.pid_valid()]
        ).all()


def part1():
    filepath = 'data/input_4.txt'
    passports_data = read_passports_data(filepath)
    passports = []
    for data_string in passports_data:
        passports.append(Passport(string=data_string))
    valid_status = [p.has_required_keys() for p in passports]
    print("Number of valid passports %d" % np.array(valid_status).sum())


def part2():
    filepath = 'data/input_4.txt'
    passports_data = read_passports_data(filepath)
    passports = []
    for data_string in passports_data:
        passports.append(Passport(string=data_string))
    valid_status = [p.all_valid() for p in passports]
    print("Number of valid passports %d" % np.array(valid_status).sum())


if __name__ == '__main__':
    part1()
    print("*************")
    part2()
