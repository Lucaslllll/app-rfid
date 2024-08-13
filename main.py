from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
import time
import os
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass
    UsbManager = autoclass('android.hardware.usb.UsbManager')
    File = autoclass('java.io.File')
else:
    UsbManager = None
    File = None

KV = '''
ScreenManager:
    MainScreen:

<MainScreen>:
    name: "main"
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20

        MDLabel:
            text: "RFID Reader"
            halign: "center"
            font_style: "H4"

        MDTextField:
            id: output
            hint_text: "Output"
            readonly: True
            multiline: True

        MDRaisedButton:
            text: "Start Reading"
            on_release: app.start_reading()

        MDRaisedButton:
            text: "Stop Reading"
            on_release: app.stop_reading()

        MDRaisedButton:
            text: "Send via WhatsApp"
            on_release: app.send_via_whatsapp()
'''

class MainScreen(Screen):
    pass

class RFIDApp(MDApp):
    reading = False
    rfid_data = []

    def build(self):
        self.title = "RFID Reader"
        self.icon = "icon.png"  # Opcional
        Window.size = (360, 640)
        return Builder.load_string(KV)

    def start_reading(self):
        self.reading = True
        Clock.schedule_interval(self.read_rfid, 1)

    def stop_reading(self):
        self.reading = False
        Clock.unschedule(self.read_rfid)

    def read_rfid(self, dt):
        if self.reading:
            # Simulação da leitura RFID
            tag_id = "TAG" + str(int(time.time()))
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            data = f"Tag: {tag_id}, Time: {timestamp}\n"
            self.root.ids.output.text += data
            self.rfid_data.append(data)

    def send_via_whatsapp(self):
        file_path = os.path.join(os.getenv('HOME'), 'rfid_log.txt')
        with open(file_path, 'w') as f:
            f.writelines(self.rfid_data)

        # Aqui você precisa usar uma solução como PyWhatKit ou Automação do Android
        # para enviar o arquivo via WhatsApp. Este é um placeholder.
        print(f"Sending {file_path} via WhatsApp...")

if __name__ == "__main__":
    RFIDApp().run()
