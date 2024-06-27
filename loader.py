import importlib.util
from instance_factory import *
import json


class Loader:
    
    def __init__(self):
        # Instance of the Factory class
        self.factory = Factory()


    def load_plugins(self):
        with open('configuration.json') as file:
            # Load the config data from the file
            self.data = json.load(file)

            for command, plugin in self.data.items():
                # Create the module location for the plugin
                location = self.create_module_location(plugin=plugin)
                # Create the module specification
                specification = self.create_module_specification(location)
                # Create an instance from the plugin name and specifivation
                # Register the plugin - Add the class instance to the factory
                self.factory.add_to_references(command, self.create_class_from_module(plugin, specification))


    def create_module_location(self, plugin):
        # Create the path for the pluguin
        module_name = plugin
        module_location = './' + module_name.replace('.', '/') + '.py'

        return module_name, module_location


    def create_module_specification(self, module_info):
        # Create the specification for the plugin
        module_name, module_location = module_info
        try:
            specification = importlib.util.spec_from_file_location(module_name, module_location)
            return specification
        except FileNotFoundError as e:
            raise e


    def convert_to_class_name(self, plugin):
        # Convert the plugin name to the name of the class: plugin.oepn_program -> OpenProgram
        parts = plugin.split('.')
        class_name = ''.join(part.capitalize() for part in parts[-1].split('_'))
        return class_name


    def create_class_from_module(self, module_name: str, specification):
        # Create a class instance from the plugin
        class_name = self.convert_to_class_name(module_name)

        module = importlib.util.module_from_spec(specification)
        try:
            # Execute the plugin
            specification.loader.exec_module(module)
            # Get the class instance of the plugin
            instance = getattr(module, class_name)
            return instance
        except (AttributeError, ImportError) as e:
            raise e