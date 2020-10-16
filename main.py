import sys
import json

class Parser:
    def __init__(self):
        # TODO check length of arguments, if too few then error and exit len(sys.argv)
        self.in_file_name = sys.argv[1]
        self.target_name = sys.argv[2]


    def parseURLS(self):
        # TODO maybe make a directory and put files into that
        in_file = open(self.in_file_name, "r")
        api_out_file = open("api_wordlist.txt", "w+")
        subdomain_out_file = open("subdomain_wordlist.txt", "w+")
        all_out_file = open("all_wordlist.txt", "w+")

        line_number = 1
        input_lines = in_file.readlines()
        for line in input_lines:
            print(line)
            data = dict()
            success = self.parseLine(line, data)
            if not success:
                print("Error on line", line_number)
            else:
                print("adding line one to wordlists and json data")
            line_number += 1

        in_file.close()
        api_out_file.close()
        subdomain_out_file.close()
        all_out_file.close()

    def parseLine(self, line, data):
        subdomains = list()
        directories = list()
        api_dict = dict()
        api_dict["endpoints_to_param"] = dict()
        api_dict["parameters_to_values"] = dict()

        data_in = line.split(self.target_name)
        data_left = list()
        try:  # process left side of record (the subdirectories)
            data_left = data_in[0].split("//")[1].split(".") # e.g. ['customer', 'help', 'admin']
        except IndexError:
            pass # TODO we will skip this line in this case, print out error with line for posterity
        for sub_domain in data_left:
            subdomains.append(sub_domain)
        data_right = list()
        try:  # process right
            data_right = data_in[1].split("/") # e.g. ["en", "portal", "form.php?fname=poop&lname=face"]
        except IndexError:
            pass # TODO we will skip this line in this case, print out error with line for posterity
        for item in data_right:
            param_list = list()
            if "?" in item:
                x = item.index("?")
                endpoint_name = item[:x]
                # if api_dict["endpoints_to_param"].keys().count(api_call[0])# check if endpoint in api.keys(), if not then set it up
                if api_dict["endpoints_to_param"].keys().count(endpoint_name) > 0:
                    param_list = api_dict["endpoints_to_param"][endpoint_name]
                if x < len(item) - 2:
                    param_value = item[x+1:]
                    new_data = param_list.split("&")
                    current_param = new_data[0]
                    for pair in new_data:
                        if "=" in pair:
                            pass

                pass # process api side
            else:
                subdomains.append(item) # record the subdirectories


        data["subdomains"] = subdomains
        data["apis"] = api_dict
        data["directories"] = directories
        return False #fixme return true if anything good is collected




# TODO:
    # make sure everything that writes is set to append!!!
    # do a max number of lines at a time to avoid taking up to much memory???
if __name__ == '__main__':
    print("Hello world")

