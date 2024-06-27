class Factory:
    # Create an instance of the class from the plugin files. Save the instance in the dictionary.

    def __init__(self):
        # Dictionary to store the commands and the instances command -> str : instance
        self.command_instance_references = {}


    def return_class_instance(self, command):
        # Return a class instance by passing a command
        try:
            class_object = self.command_instance_references[command]
            instance = class_object()
            return instance
        except KeyError:
            raise KeyError(f'No class instance found for keyword {command}')


    def add_to_references(self, keyword, instance):
        # Register a plugin - Add a command and instance to the dictionary
        self.command_instance_references[keyword] = instance
    
    def remove_from_references(self, keyword):
        # Unregister a plugin - Remove a command and instance from the dictionary
        try:
            self.command_instance_references.pop(keyword)
        except KeyError:
            raise KeyError(f'No class instance found for keyword {keyword}')