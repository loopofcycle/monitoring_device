import os, time, pprint
import paho.mqtt.client as mqtt

class mqtt_client(mqtt.Client):

    def __init__(self, client_id="", clean_session=True,
                userdata=None, protocol=mqtt.MQTTv311, transport="tcp",
                host='broker.hivemq.com'):
                #host='broker.emqx.io'):
        self.host = host
        super().__init__(client_id="", clean_session=True,
                        userdata=None, protocol=mqtt.MQTTv311, transport="tcp")

    def on_log(self, client, userdata, level, buf):
        client.enable_logger()
        pprint.pprint({'*log time -': time.localtime()[:6],
                        'buf': buf}, width=65)

    def execute(self, topic, msg=''):
        self.msg = msg
        self.topic = topic
        self.connect(self.host)
        self.loop_forever()
        return msg

class Subscriber(mqtt_client):

    def on_connect(self, client, userdata, flags, rc):
        self.connected_time = time.perf_counter()
        client.subscribe(self.topic, qos=2)

    def on_message(self, client, userdata, msg):
        self.msg = msg.payload
        pprint.pprint({'*message received':str(time.localtime()[:6]),
                    'client_id': client._client_id,
                    'userdata': userdata,
                    'msg.payload': msg.payload,
                    'msg.topic': msg.topic,
                    'is_connected': client.is_connected()})
        client.disconnect()

    def on_subscribe(self, client, userdata, mid, granted_qos):
        pprint.pprint({'*subscribed':str(time.localtime()[:6]),
                    'is_connected': client.is_connected()})
        while int(time.perf_counter() - self.connected_time) < 5:
            print('waiting for message')
            time.sleep(1)
        client.disconnect()

class Publisher(mqtt_client):

    def on_connect(self, client, userdata, flags, rc):
        client.publish(self.topic, payload=self.msg, retain=True)
    
    def on_publish(self, client, userdata, mid):
        pprint.pprint({'message published':str(time.localtime()[:6]),
                    'client_id': client._client_id,
                    'userdata': userdata,
                    'mid': mid,
                    'is_connected': client.is_connected()})
        client.disconnect()

if __name__ == '__main__':
    topic = 'alfascan_kazan\rem_zone\temperature'
    #pub = Publisher()
    #pub.execute(topic=topic, msg=str(time.localtime()[:6]))
    sub = Subscriber()
    sub.execute(topic=topic)