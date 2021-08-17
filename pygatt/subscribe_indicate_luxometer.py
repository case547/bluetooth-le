import pygatt


def data_handler_cb(handle, value):
    """
        Indication and notification come asynchronously, we use this function to
        handle them either one at the time as they come.
    :param handle:
    :param value:
    :return:
    """
    print("Data: {}".format(value.hex()))
    print("Handle: {}".format(handle))


def main():
    """
        Main function. The comments below try to explain what each section of
        the code does.
    """

    # pygatt uses pexpect and if your device has a long list of characteristics,
    # pexpect will not catch them all. We increase the search window to
    # 2048 bytes for the this example. By default, it is 200.
    # Note: We need an instance of GATToolBackend per each device connection
    adapter = pygatt.GATTToolBackend(search_window_size=2048)

    try:
        # Start the adapter
        adapter.start()
        # Connect to the device with that given parameter.
        # For scanning, use adapter.scan()
        device = adapter.connect("80:6F:B0:F0:2B:95")
        # Set the security level to medium
        device.bond()
        # Observes the given characteristics for indications.
        # When a response is available, calls data_handle_cb
        device.subscribe("f000aa71-0451-4000-b000-000000000000",
                         callback=data_handler_cb,
                         indication=True)

        input("Press enter to stop program...\n")

    finally:
        # Stop the adapter session
        adapter.stop()

    return 0


if __name__ == '__main__':
    exit(main())