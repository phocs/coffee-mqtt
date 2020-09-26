import paho.mqtt.client as PahoMqtt
from .topic import Topic

class Client(PahoMqtt.Client):
    def __init__(self, client_id="", clean_session=None, userdata=None,
                 protocol=PahoMqtt.MQTTv311, transport="tcp"):
        super().__init__(client_id, clean_session, userdata, protocol, transport)
        self._routes = []

    def reinitialise(self, client_id="", clean_session=True, userdata=None):
        routes = self._routes
        for r in routes: r["subscribed"] = False
        super().reinitialise(client_id, clean_session, userdata)
        self._routes = routes

    def addroute(self, pattern, qos=0, handler=None):
        def decorator(handler):
            new = Topic(pattern)
            self._routes.append({
                "topic":    new,
                "qos":      qos,
                "handler":  handler,
                "subscribed": self.is_connected(),
            })
            if self.is_connected():
                self.subscribe(new.topic, qos)
        return decorator

    def _handle_on_message(self, message):
        route = None
        for r in self._routes:
            if r["topic"].match(message.topic):
                route = r;
                break;

        if route and route["handler"]:
            try:
                params = route["topic"].extract(message.topic);
                route["handler"](message, **params)
            except Exception as err:
                super()._easy_log(PahoMqtt.MQTT_LOG_DEBUG, "Route handler error", err)
        else:
            super()._handle_on_message(message)

    def _handle_connack(self):
        res = super()._handle_connack()
        if res == 0:
            for r in self._routes:
                if not r["subscribed"]:
                    r["subscribed"] = True
                    self.subscribe(r["topic"].topic, r["qos"])
        return res
