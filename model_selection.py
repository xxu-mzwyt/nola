import json

def model_selection():
    mod_front = "models_data_front.json"

    print("   Please input the model year of the car.")
    message = input("   > ")
    print("   Please input the make of the car.")
    maker = input("   > ")
    print("   Please input the model of the car.")
    mod = input("   > ")

    id = iterate_helper(mod_front, message, maker, mod)
    return id

def iterate_helper(mod_front, message, maker, mod):
    with open(mod_front, 'r') as g:
        gg = json.load(g)
        for i in gg:
            if i["year"].casefold().replace(' ', '') == message.casefold().replace(' ', ''):
                if i["make"].casefold().replace(' ', '') == maker.casefold().replace(' ', ''):
                    if i["model"].casefold().replace(' ', '') == mod.casefold().replace(' ', ''):
                        options = i["option"][0] + ", " + i["option"][1] + "cyl, " + i["option"][2] + "L"
                        print("   Confirm? (y/n)", i["year"], i["make"], i["model"]+",", options)
                        answer = input("   > ")
                        if(answer.casefold() == "y".casefold()): return int(i["id"])
        # else:
        #   print("Please enter a valid input.")
        #   return model_selection();
    print("   Invalid input. Please try again.")
    return model_selection()
