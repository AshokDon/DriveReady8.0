from singleton_connection_pool import ConnectionPoolImpl


def main():

    # TODO 1:
    # Get a Connection Pool with a maximum of 5 connections.
    pool1 = None

    # TODO 2:
    # Initialize the pool.
    #
    # pool1.initialize_pool()

    # TODO 3:
    # Check the initial counts.
    #
    # print("Total connections:", ...)
    # print("Available connections:", ...)

    # TODO 4:
    # Get one connection.
    #
    # connection = pool1.get_connection()

    # TODO 5:
    # Check available connections after acquiring one.
    #
    # print("Available connections after get:", ...)

    # TODO 6:
    # Release the connection.
    #
    # pool1.release_connection(connection)

    # TODO 7:
    # Check available connections after releasing it.
    #
    # print("Available connections after release:", ...)

    # TODO 8:
    # Get the Singleton again.
    pool2 = None

    # TODO 9:
    # Verify that pool1 and pool2 are the same object.
    #
    # print("Same instance:", pool1 is pool2)

    # TODO 10:
    # Reset the Singleton.
    #
    # ConnectionPoolImpl.reset_instance()

    # TODO 11:
    # Get a new pool.
    pool3 = None

    # TODO 12:
    # Verify that a new object was created.
    #
    # print("New instance after reset:", pool1 is pool3)


if __name__ == "__main__":
    main()
