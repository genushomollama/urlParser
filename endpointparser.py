class EndpointParser:
    def __init__(self, endpoint):
        self.data = endpoint
        self.resource = ""  # endpoint, name of resource, string
        self.parameters = list()  # query parameters, list
        self.values = list() # values given for parameters, list
        # call method to populate those necessary values

    def populate(self):
        # set resource
        len_resource = self.data.index("?")
        if len_resource > 0:
            self.resource = self.data[:len_resource]
        param_values = self.data[len_resource+1:].split("&")
        current_param = None # use this TODO
        if len(param_values) > 0:
            for current in param_values:
                if "=" in current:
                    equals = current.index("=")
                    self.parameters.append(current[:equals])
                    current_param = current[:equals] # for when we map params to values TODO
                    if equals+1 < len(current):
                        self.values.append(current[equals+1:])
                else:
                    # for when we map params to values we should use current param TODO
                    self.parameters.append(current)

        # loop through the parameters/values
        print(self.data) # FIXME remove testing
        print(self.resource)
        print(self.parameters)
        print(self.values)
        return

    # provide getter methods to those resources
    def get_parameters(self):
        return self.parameters

    def get_resource(self):
        return self.resource

    def get_values(self):
        return self.values


if __name__ == '__main__':
    url = "https://trends.realself.com/2018/01/18/botox-new-alternative/?utm_content=buffercdb74&utm_medium=social&utm_source=twitter.com&utm_campaign=buffer"
    parser = EndpointParser(url)
    parser.populate()