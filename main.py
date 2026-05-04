import sys
import vlc
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QHBoxLayout, QPushButton, QLabel, QFileDialog,
                              QSlider, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from face_detector import FaceDetector


class LookBasedPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Look Based Media Player")
        self.resize(960, 620)
        self.setStyleSheet("background-color: #141414; color: white;")

        self.instance = vlc.Instance('--no-xlib', '--quiet')
        self.media_player = self.instance.media_player_new()
        self.detector = FaceDetector()
        self.file_loaded = False
        self.user_seeking = False

        self._build_ui()

        # Face check timer
        self.face_timer = QTimer()
        self.face_timer.timeout.connect(self._check_face)
        self.face_timer.start(400)

        # Progress timer
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self._update_progress)
        self.progress_timer.start(500)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main = QVBoxLayout(central)
        main.setSpacing(0)
        main.setContentsMargins(0, 0, 0, 0)

        # ── TOP BAR ──
        top = QWidget()
        top.setFixedHeight(40)
        top.setStyleSheet("background-color: #1f1f1f; border-bottom: 1px solid #333;")
        top_layout = QHBoxLayout(top)
        top_layout.setContentsMargins(12, 0, 12, 0)

        self.face_label = QLabel("👤 Face: Not Detected ❌")
        self.face_label.setStyleSheet("color: #ff6b6b; font-size: 12px;")
        top_layout.addWidget(self.face_label)

        top_layout.addStretch()

        self.file_label = QLabel("No file loaded")
        self.file_label.setStyleSheet("color: #888; font-size: 11px;")
        top_layout.addWidget(self.file_label)

        main.addWidget(top)

        # ── VIDEO AREA ──
        self.video_widget = QWidget()
        self.video_widget.setStyleSheet("background-color: #000000;")
        self.video_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main.addWidget(self.video_widget, stretch=1)

        # ── BOTTOM CONTROLS ──
        controls = QWidget()
        controls.setFixedHeight(120)
        controls.setStyleSheet("background-color: #1a1a1a; border-top: 1px solid #333;")
        ctrl_layout = QVBoxLayout(controls)
        ctrl_layout.setContentsMargins(16, 8, 16, 8)
        ctrl_layout.setSpacing(6)

        # Progress row
        prog_row = QHBoxLayout()

        self.time_label = QLabel("0:00")
        self.time_label.setStyleSheet("color: #aaa; font-size: 11px; min-width: 36px;")
        prog_row.addWidget(self.time_label)

        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setRange(0, 1000)
        self.progress_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 5px;
                background: #3a3a3a;
                border-radius: 2px;
            }
            QSlider::sub-page:horizontal {
                background: #e50914;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: white;
                width: 13px;
                height: 13px;
                margin: -4px 0;
                border-radius: 6px;
            }
        """)
        self.progress_slider.sliderPressed.connect(lambda: setattr(self, 'user_seeking', True))
        self.progress_slider.sliderReleased.connect(self._seek)
        prog_row.addWidget(self.progress_slider)

        self.duration_label = QLabel("0:00")
        self.duration_label.setStyleSheet("color: #aaa; font-size: 11px; min-width: 36px;")
        self.duration_label.setAlignment(Qt.AlignRight)
        prog_row.addWidget(self.duration_label)

        ctrl_layout.addLayout(prog_row)

        # Buttons row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.open_btn = self._make_btn("📂 Open",  "#2979ff")
        self.back_btn = self._make_btn("⏮ -10s",  "#444444")
        self.play_btn = self._make_btn("▶  Play",  "#e50914", width=110)
        self.fwd_btn  = self._make_btn("⏭ +10s",  "#444444")
        self.stop_btn = self._make_btn("⏹ Stop",  "#444444")

        self.open_btn.clicked.connect(self.open_file)
        self.back_btn.clicked.connect(lambda: self._skip(-10))
        self.play_btn.clicked.connect(self.toggle_play_pause)
        self.fwd_btn.clicked.connect(lambda: self._skip(10))
        self.stop_btn.clicked.connect(self.stop)

        btn_row.addWidget(self.open_btn)
        btn_row.addStretch()
        btn_row.addWidget(self.back_btn)
        btn_row.addWidget(self.play_btn)
        btn_row.addWidget(self.fwd_btn)
        btn_row.addStretch()
        btn_row.addWidget(self.stop_btn)

        ctrl_layout.addLayout(btn_row)

        # Info label
        info = QLabel("👁  Auto-pauses when you look away  ·  Resumes when you look back")
        info.setStyleSheet("color: #444; font-size: 9px;")
        info.setAlignment(Qt.AlignCenter)
        ctrl_layout.addWidget(info)

        main.addWidget(controls)

    def _make_btn(self, text, color, width=90):
        btn = QPushButton(text)
        btn.setFixedHeight(36)
        btn.setFixedWidth(width)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #ffffff33;
            }}
        """)
        return btn

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Media File", "",
            "Media Files (*.mp4 *.avi *.mkv *.mp3 *.wav *.flac *.mov *.wmv)"
        )
        if not path:
            return
        media = self.instance.media_new(path)
        self.media_player.set_media(media)
        self.media_player.set_xwindow(int(self.video_widget.winId()))
        self.media_player.play()
        self.file_loaded = True
        self.play_btn.setText("⏸  Pause")
        self.file_label.setText(path.split('/')[-1])
        self.file_label.setStyleSheet("color: #ccc; font-size: 11px;")

    def toggle_play_pause(self):
        if not self.file_loaded:
            return
        state = self.media_player.get_state()
        if state == vlc.State.Playing:
            self.media_player.pause()
            self.play_btn.setText("▶  Play")
        elif state in (vlc.State.Paused, vlc.State.Stopped):
            self.media_player.play()
            self.play_btn.setText("⏸  Pause")

    def stop(self):
        if not self.file_loaded:
            return
        self.media_player.stop()
        self.file_loaded = False
        self.progress_slider.setValue(0)
        self.time_label.setText("0:00")
        self.duration_label.setText("0:00")
        self.play_btn.setText("▶  Play")
        self.file_label.setText("No file loaded")
        self.file_label.setStyleSheet("color: #888; font-size: 11px;")

    def _skip(self, seconds):
        if not self.file_loaded:
            return
        t = self.media_player.get_time()
        self.media_player.set_time(max(0, t + seconds * 1000))

    def _check_face(self):
        if not self.file_loaded:
            return
        looking = self.detector.is_looking()
        state = self.media_player.get_state()
        if looking:
            self.face_label.setText("👤 Face: Detected ✅")
            self.face_label.setStyleSheet("color: #51cf66; font-size: 12px;")
            if state == vlc.State.Paused:
                self.media_player.play()
                self.play_btn.setText("⏸  Pause")
        else:
            self.face_label.setText("👤 Face: Not Detected ❌")
            self.face_label.setStyleSheet("color: #ff6b6b; font-size: 12px;")
            if state == vlc.State.Playing:
                self.media_player.pause()
                self.play_btn.setText("▶  Play")

    def _update_progress(self):
        if not self.file_loaded or self.user_seeking:
            return
        pos = self.media_player.get_position()
        if pos >= 0:
            self.progress_slider.setValue(int(pos * 1000))
        cur = self.media_player.get_time()
        total = self.media_player.get_length()
        if cur >= 0:
            self.time_label.setText(self._fmt(cur))
        if total > 0:
            self.duration_label.setText(self._fmt(total))

    def _seek(self):
        self.media_player.set_position(self.progress_slider.value() / 1000.0)
        self.user_seeking = False

    def _fmt(self, ms):
        s = max(0, ms) // 1000
        return f"{s // 60}:{s % 60:02d}"

    def closeEvent(self, event):
        self.face_timer.stop()
        self.progress_timer.stop()
        self.media_player.stop()
        self.detector.release()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LookBasedPlayer()
    window.show()
    sys.exit(app.exec_())