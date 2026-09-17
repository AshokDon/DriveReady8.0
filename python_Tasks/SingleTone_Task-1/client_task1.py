from singleton_config_manager import FileBasedConfigurationManager


def main():

    # TODO 1:
    # Get the first Configuration Manager instance.
    config1 = FileBasedConfigurationManager.get_instance()

    # TODO 2:
    # Store configuration values
    #
     config1.set_configuration("app.name", "MyApplication")
     config1.set_configuration("max.connections", 100)
     config1.set_configuration("timeout", 30.5)

    # TODO 3:
    # Read the configuration values.
    #
     print("App Name:", config.get_configuration("app.name"))
     print("Max Connections:", config.get_configuration("max.connections"))
     print("Timeout:",config.get_configuration("timeout"))

    # TODO 4:
    # Get the Singleton instance again.
    config2 = FileBasedConfigurationManager.get_instance()

    # TODO 5:
    # Verify that config1 and config2 are the same object.
    #
     print("Same instance:", config1 is config2)

    # TODO 6:
    # Remove the timeout configuration.
    #
    # config1.remove_configuration("timeout")
     print("Timeout after removal:",config.get_configuration("timeout"))

    # TODO 7:
    # Clear all configurations.
    #
    # config1.clear()
     print("App Name after clear:", config.get_configuration("app.name"))

    # TODO 8:
    # Reset the Singleton.
    #
     config1 = FileBasedConfigurationManager.get_instance()
     FileBasedConfigurationManager.reset_instance()
     config2 = FileBasedConfigurationManager.get_instance()

    # TODO 9:
    # Get the Configuration Manager again.
    config3 =  FileBasedConfigurationManager.get_instance()

    # TODO 10:
    # Verify that config1 and config3 are different objects.
    #
     print("New instance after reset:",config1 is config2 )


if __name__ == "__main__":
    main()
