from config_manager import ConfigManager


class FileBasedConfigurationManager(ConfigManager):

    # TODO:
    # Store the Singleton instance here.
    _instance = None

    def __new__(cls):
        # TODO:
        # Control object creation so that only one
        # FileBasedConfigurationManager object exists.
        pass

    def __init__(self):
        # TODO:
        # Initialize the parent class.
        # Be careful: __init__ can run more than once
        # when using a Singleton with __new__.
        pass

    @classmethod
    def get_instance(cls):
        # TODO:
        # Return the Singleton instance.
        pass

    @classmethod
    def reset_instance(cls):
        # TODO:
        # Reset the Singleton instance.
        pass

    def get_configuration(self, key, value_type=None):
        # TODO:
        # 1. Get the value using key.
        # 2. If it does not exist, return None.
        # 3. If value_type is None, return the value.
        # 4. Otherwise convert it to the requested type.
        pass

    def set_configuration(self, key, value):
        # TODO:
        # Store the configuration.
        pass

    def remove_configuration(self, key):
        # TODO:
        # Remove the configuration if it exists.
        pass

    def clear(self):
        # TODO:
        # Remove all configurations.
        pass
