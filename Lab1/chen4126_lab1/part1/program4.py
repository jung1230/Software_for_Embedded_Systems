lib = {
    #  keys              values
    "Albert Einstein": "01/17/1706",
    "Benjamin Franklin": "04/21/1049",
    "Ada Lovelace": "12/18/2020",
    "Albert Franklin": "12/17/2020",
    "Benjamin Lovelace": "04/18/1049",
}

print("Welcome to the birthday dictionary. We know the birthdays of:")
for name in lib.keys():
    print(name)
name = input("Whose birthday do you want to look up?\n")

if name in lib:
    birthday = lib[name]
    print(name + "\'s birthday is", birthday)
