#step 1 : clean and store data from input file into dictionaries for easy access later on in the algorithm
def read_input(filename):
    hospital_slots = {}
    hospital_preferences = {}
    resident_preferences = {}

    file = open(filename, "r")
    lines = file.readlines()
    file.close()

    hospital_section = True

    for line in lines:
        line = line.strip()

        if line == "":
            hospital_section = False
            continue

        parts = line.split(",")

        for i in range(len(parts)):
            parts[i] = parts[i].strip()

        if hospital_section:
            hospital_name = parts[0]
            slots = int(parts[1])
            residents = parts[2:]

            hospital_slots[hospital_name] = slots
            hospital_preferences[hospital_name] = residents

        else:
            resident_name = parts[0]
            hospitals = parts[1:]

            resident_preferences[resident_name] = hospitals

    return hospital_slots, hospital_preferences, resident_preferences


hospital_slots, hospital_preferences, resident_preferences = read_input("INPUT.TXT")

print("Hospital Slots:")
print(hospital_slots)

print("\nHospital Preferences:")
print(hospital_preferences)

print("\nResident Preferences:")
print(resident_preferences)
















#step 2 : create a cheat sheet for the algorithm to quickly access the rank of a student for a hospital without having to loop through the preference list each time














#step 3 : implement Gale-Shapley Algorithm
