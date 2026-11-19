from paho.mqtt import client as mqtt_client
from random import randint
from decouple import config

# Reading broker credentials
BROKER = config("BROKER")
PORT = int(config("PORT"))
TOPIC = config("TOPIC")
USER = config("USER")
PASS = config("PASS")

# Create a randdom id for login in MQTT
CLIENT_ID = f"id-mqtt-{randint(0,100)}"


# Create a client to interact with MQTT
def connectMqtt() -> mqtt_client:#注释return的量是mqtt_client的对象
    def on_connect(client, userdata, flags, rc):#参数为mqtt库触发回调时自动传入（MQTT 库提供了一个这个接口，我可以在on_connect处赋一个函数，表示链接成功的反应）
                                                #回调函数就是：你先定义一个函数，把它交给别人，等某个条件满足时，由别人来调用它
        if rc == 0:
            print("[MQTT] Connected to server.")
        else:
            print("[MQTT] Failure to connect.")

    client = mqtt_client.Client(CLIENT_ID)
    client.username_pw_set(USER, PASS)
    client.on_connect = on_connect
    client.connect(BROKER, PORT)

    return client


# Receiving messages sendings with MQTT
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(
            f"[MQTT] Received message from {msg.topic} topic:",
            f"\n{msg.payload.decode()}",  #msg.payload 获取的是消息的数据内容。但它通常是字节类型（bytes），而不是普通字符串
              )

    client.subscribe(TOPIC)
    client.on_message = on_message


# Publishing messages with MQTT
def publish(client, msg="Hello MQTT"):
    result = client.publish(TOPIC, msg)   #client.publish(TOPIC, msg)这个相当于调用了publish这个函数是吧，然后这个函数的返回值传给了result


if __name__ == "__main__":                #该文件作为主函数运行时才会执行主程序
    client = connectMqtt()
    subscribe(client)
    publish(client)
    publish(client, msg="Custom Messages Working!")
    client.loop_forever()
