from coffee.mqtt.client import Client

def test_property(capsys):
    with capsys.disabled():
        pass
        #
        # client = Client();
        #
        # @client.addroute("test/+who", 0)
        # def handler(message, who):
        #     print(who + "send me: %s" % message.payload)
        #
        # client.connect(host="localhost")
        #
        # rc = 0
        # i = 0
        # while rc == 0:
        #     client.publish("test/first", "Hello World")
        #     time.sleep(1)
        #     print(client._routes)
        #     rc = client.loop()
        #     i = i + 1
        #     if i == 5:
        #         client.reinitialise()
        #         client.connect(host="localhost")
        #         i = 0
