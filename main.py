import sys
import json
import endpointparser as epp


class Parser:
    def __init__(self):
        self.in_file_name = "urls"
        self.target_name = "realself.com"

    def parseURLS(self):
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
                self.writeData(data, api_out_file, subdomain_out_file, all_out_file)  # todo print to word files
            line_number += 1

        in_file.close()
        api_out_file.close()
        subdomain_out_file.close()
        all_out_file.close()

    def writeData(self, data, api_out, subdomain_out, all_out):
        subdomains = data.get("subdomains")
        directories = data.get("directories")
        # subdomain_out.writelines(subdomains)
        # all_out.writelines(subdomains)
        for item in subdomains:
            if len(item) >= 1:
                subdomain_out.write(item+"\n")
                all_out.write(item+"\n")
        # subdomain_out.writelines(directories)
        # all_out.writelines(directories)
        for item in directories:
            if len(item) >= 1:
                subdomain_out.write(item)
                all_out.write(item)
        api_dict = data.get("apis")
        api_resource = api_dict.get("resource")  # TODO do something with this
        api_parameters = api_dict.get("parameters")
        api_values = api_dict.get("values")
        if not api_parameters is None:
            # api_out.writelines(api_parameters)
            # all_out.writelines(api_parameters)
            for item in api_parameters:
                if len(item) >= 1:
                    api_out.write(item+"\n")
                    all_out.write(item+"\n")
        if not api_values is None:
            # api_out.writelines(api_values)
            # all_out.writelines(api_values)
            for item in api_values:
                if len(item) >= 1:
                    api_out.write(item+"\n")
                    all_out.write(item+"\n")

    def parseLine(self, line, data):
        datafound = False
        subdomains = list()
        directories = list()
        api_dict = dict()

        data_in = line.split(self.target_name)  # e.g. ["http://www.customer.help.", "/index.php"]
        data_left = list()
        try:  # process left side of record (the subdomains)
            data_left = data_in[0].split("//")[1].split(".")  # e.g. ['customer', 'help'] or ['admin']
        except IndexError:
            pass  # TODO we will skip this line in this case, print out error with line for posterity
        for sub_domain in data_left:
            datafound = True
            subdomains.append(sub_domain)  # update subdomains

        data_right = list()
        try:  # process right (the directories and api's)
            data_right = data_in[1].split(
                "/")  # e.g. for "en/portal/form.php?name=x&y" => ["en", "portal", "form.php?name=x&y"]
        except IndexError:
            pass  # TODO we will skip this line in this case, print out error with line for posterity
        for item in data_right:
            datafound = True

            if "?" in item:  # process api side
                endpointparser = epp.EndpointParser(item)
                api_dict["resource"] = endpointparser.get_resource()
                api_dict["parameters"] = endpointparser.get_parameters()
                api_dict["values"] = endpointparser.get_values()
            else:
                subdomains.append(item)  # record the subdirectories

        data["subdomains"] = subdomains
        data["apis"] = api_dict
        data["directories"] = directories
        return datafound


# TODO:
# make sure everything that writes is set to append!!!
# do a max number of lines at a time to avoid taking up to much memory???
if __name__ == '__main__':
    urlparser = Parser()
    urlparser.parseURLS()
    print("Hello world")

# TODO check length of arguments, if too few then error and exit len(sys.argv)
# self.in_file_name = sys.argv[1]
# self.target_name = sys.argv[2]
