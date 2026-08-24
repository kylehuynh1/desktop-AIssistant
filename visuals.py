import sys
import math
import visualState
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt, QTimer, QRectF, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QFont


# ============================================================
# FRIDAY ANIMATED CORE
# ============================================================

class FridayCore(QWidget):

    def __init__(self):
        super().__init__()

        # ----------------------------------------------------
        # ROTATION
        # ----------------------------------------------------

        self.outerAngle = 0.0
        self.middleAngle = 0.0
        self.innerAngle = 0.0

        # ----------------------------------------------------
        # IDLE BREATHING
        # ----------------------------------------------------

        self.pulse = 0.0
        self.pulseDirection = 1

        # ----------------------------------------------------
        # AUDIO INPUTS
        # ----------------------------------------------------

        # OUTER spectrum:
        # microphone + computer/system audio
        self.environmentLevel = 0.0

        # INNER core:
        # Friday/Piper voice ONLY
        self.fridayVoiceLevel = 0.0

        # Individual radial spectrum bars
        self.audioBars = [0.0 for _ in range(64)]

        # ----------------------------------------------------
        # ANIMATION TIMER
        # ----------------------------------------------------

        # Roughly 60 FPS
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateAnimation)
        self.timer.start(16)


    # ========================================================
    # RECEIVE ENVIRONMENT AUDIO
    # ========================================================

    def setEnvironmentLevel(self, level):

        self.environmentLevel = max(
            0.0,
            min(float(level), 1.0)
        )


    # ========================================================
    # RECEIVE FRIDAY VOICE AUDIO
    # ========================================================

    def setFridayVoiceLevel(self, level):

        self.fridayVoiceLevel = max(
            0.0,
            min(float(level), 1.0)
        )


    # ========================================================
    # ANIMATION UPDATE
    # ========================================================

    def updateAnimation(self):

        # ----------------------------------------------------
        # CONSTANT HUD ROTATION
        # ----------------------------------------------------

        self.outerAngle += 0.20
        self.middleAngle -= 0.35
        self.innerAngle += 0.55

        # Prevent numbers from growing forever
        self.outerAngle %= 360
        self.middleAngle %= 360
        self.innerAngle %= 360


        # ----------------------------------------------------
        # SUBTLE IDLE BREATHING
        # ----------------------------------------------------

        self.pulse += 0.12 * self.pulseDirection

        if self.pulse >= 3:
            self.pulseDirection = -1

        elif self.pulse <= 0:
            self.pulseDirection = 1

        micLevel = visualState.getEnvironmentLevel()
        systemLevel = visualState.getSystemAudioLevel()

        self.environmentLevel = max(
            micLevel,
            systemLevel
        )

        self.fridayVoiceLevel = (
            visualState.getFridayVoiceLevel()
        )

        # ----------------------------------------------------
        # OUTER AUDIO SPECTRUM
        # ----------------------------------------------------

        for i in range(len(self.audioBars)):

            # Gives each radial bar slightly different
            # movement while still being driven by
            # the SAME real audio level.
            variation = (
                math.sin(
                    (i * 0.72)
                    + (self.outerAngle * 0.12)
                ) + 1
            ) / 2

            target = (
                self.environmentLevel
                * 55
                * (0.35 + variation * 0.65)
            )

            # Smooth movement toward target
            self.audioBars[i] += (
                target - self.audioBars[i]
            ) * 0.30


        # ----------------------------------------------------
        # AUDIO DECAY
        # ----------------------------------------------------

        # If the audio system stops sending values,
        # the visualizer smoothly returns to zero.

        self.update()


    # ========================================================
    # OUTER AUDIO SPECTRUM
    # ========================================================

    def drawSpectrum(self, painter, center, radius):

        barCount = len(self.audioBars)

        pen = QPen(
            QColor(
                80,
                220,
                255,
                190
            )
        )

        pen.setWidth(2)

        painter.setPen(pen)

        for i, level in enumerate(self.audioBars):

            angle = (
                360 / barCount
            ) * i

            radians = math.radians(angle)

            innerRadius = radius

            outerRadius = (
                radius + level
            )

            x1 = (
                center.x()
                + math.cos(radians)
                * innerRadius
            )

            y1 = (
                center.y()
                + math.sin(radians)
                * innerRadius
            )

            x2 = (
                center.x()
                + math.cos(radians)
                * outerRadius
            )

            y2 = (
                center.y()
                + math.sin(radians)
                * outerRadius
            )

            painter.drawLine(
                QPointF(x1, y1),
                QPointF(x2, y2)
            )


    # ========================================================
    # SEGMENTED ROTATING RING
    # ========================================================

    def drawSegmentedRing(
        self,
        painter,
        center,
        radius,
        angleOffset,
        segmentCount,
        segmentLength,
        opacity=210,
        width=3
    ):

        pen = QPen(
            QColor(
                100,
                220,
                255,
                opacity
            )
        )

        pen.setWidth(width)

        painter.setPen(pen)

        rect = QRectF(
            center.x() - radius,
            center.y() - radius,
            radius * 2,
            radius * 2
        )

        spacing = (
            360 / segmentCount
        )

        for i in range(segmentCount):

            angle = (
                angleOffset
                + (i * spacing)
            )

            painter.drawArc(
                rect,
                int(angle * 16),
                int(segmentLength * 16)
            )


    # ========================================================
    # HUD TICK MARKS
    # ========================================================

    def drawTicks(
        self,
        painter,
        center,
        radius
    ):

        pen = QPen(
            QColor(
                70,
                180,
                220,
                130
            )
        )

        pen.setWidth(1)

        painter.setPen(pen)

        for angle in range(
            0,
            360,
            5
        ):

            radians = math.radians(
                angle
            )

            if angle % 30 == 0:
                tickLength = 12

            elif angle % 10 == 0:
                tickLength = 8

            else:
                tickLength = 4


            x1 = (
                center.x()
                + math.cos(radians)
                * radius
            )

            y1 = (
                center.y()
                + math.sin(radians)
                * radius
            )


            x2 = (
                center.x()
                + math.cos(radians)
                * (
                    radius
                    + tickLength
                )
            )

            y2 = (
                center.y()
                + math.sin(radians)
                * (
                    radius
                    + tickLength
                )
            )


            painter.drawLine(
                QPointF(x1, y1),
                QPointF(x2, y2)
            )


    # ========================================================
    # CROSSHAIR / TARGET LINES
    # ========================================================

    def drawCrosshair(
        self,
        painter,
        center
    ):

        painter.setPen(
            QPen(
                QColor(
                    60,
                    170,
                    210,
                    80
                ),
                1
            )
        )

        length = 250
        gap = 220

        # Left
        painter.drawLine(
            QPointF(
                center.x() - length,
                center.y()
            ),
            QPointF(
                center.x() - gap,
                center.y()
            )
        )

        # Right
        painter.drawLine(
            QPointF(
                center.x() + gap,
                center.y()
            ),
            QPointF(
                center.x() + length,
                center.y()
            )
        )

        # Top
        painter.drawLine(
            QPointF(
                center.x(),
                center.y() - length
            ),
            QPointF(
                center.x(),
                center.y() - gap
            )
        )

        # Bottom
        painter.drawLine(
            QPointF(
                center.x(),
                center.y() + gap
            ),
            QPointF(
                center.x(),
                center.y() + length
            )
        )


    # ========================================================
    # FRIDAY VOICE CORE
    # ========================================================

    def drawCenter(
        self,
        painter,
        center
    ):

        # ----------------------------------------------------
        # FRIDAY VOICE EXPANSION
        # ----------------------------------------------------

        # This value should ONLY increase when Piper
        # is actually producing Friday's speech.

        voiceExpansion = (
            self.fridayVoiceLevel
            * 42
        )

        size = (
            27
            + self.pulse
            + voiceExpansion
        )


        # ----------------------------------------------------
        # OUTER VOICE GLOW
        # ----------------------------------------------------

        glowSize = (
            size
            + 12
            + (
                self.fridayVoiceLevel
                * 18
            )
        )

        glowAlpha = int(
            25
            + (
                self.fridayVoiceLevel
                * 110
            )
        )

        painter.setPen(
            QPen(
                QColor(
                    70,
                    210,
                    255,
                    min(
                        glowAlpha + 30,
                        180
                    )
                ),
                1
            )
        )

        painter.setBrush(
            QColor(
                50,
                190,
                255,
                min(
                    glowAlpha,
                    140
                )
            )
        )

        painter.drawEllipse(
            center,
            glowSize,
            glowSize
        )


        # ----------------------------------------------------
        # MAIN CORE
        # ----------------------------------------------------

        coreAlpha = int(
            70
            + (
                self.fridayVoiceLevel
                * 150
            )
        )

        painter.setPen(
            QPen(
                QColor(
                    150,
                    240,
                    255,
                    230
                ),
                2
            )
        )

        painter.setBrush(
            QColor(
                80,
                220,
                255,
                min(
                    coreAlpha,
                    220
                )
            )
        )

        painter.drawEllipse(
            center,
            size,
            size
        )


        # ----------------------------------------------------
        # INNER CORE RING
        # ----------------------------------------------------

        innerSize = (
            16
            + (
                self.fridayVoiceLevel
                * 10
            )
        )

        painter.setBrush(
            QColor(
                20,
                80,
                100,
                180
            )
        )

        painter.setPen(
            QPen(
                QColor(
                    180,
                    250,
                    255,
                    230
                ),
                2
            )
        )

        painter.drawEllipse(
            center,
            innerSize,
            innerSize
        )


        # ----------------------------------------------------
        # CENTER LIGHT
        # ----------------------------------------------------

        centerSize = (
            5
            + (
                self.fridayVoiceLevel
                * 5
            )
        )

        painter.setPen(
            Qt.NoPen
        )

        painter.setBrush(
            QColor(
                220,
                255,
                255,
                245
            )
        )

        painter.drawEllipse(
            center,
            centerSize,
            centerSize
        )


        # ========================================================
    # DRAW COMPLETE CORE
    # ========================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        try:
            painter.setRenderHint(
                QPainter.Antialiasing
            )

            center = QPointF(
                self.width() / 2,
                self.height() / 2
            )

            # ----------------------------------------------------
            # CROSSHAIRS
            # ----------------------------------------------------

            self.drawCrosshair(
                painter,
                center
            )

            # ----------------------------------------------------
            # OUTER AUDIO SPECTRUM
            # ----------------------------------------------------

            self.drawSpectrum(
                painter,
                center,
                185
            )

            # ----------------------------------------------------
            # OUTER ROTATING RING
            # ----------------------------------------------------

            self.drawSegmentedRing(
                painter,
                center,
                165,
                self.outerAngle,
                24,
                8,
                opacity=200,
                width=3
            )

            # ----------------------------------------------------
            # MIDDLE COUNTER-ROTATING RING
            # ----------------------------------------------------

            self.drawSegmentedRing(
                painter,
                center,
                130,
                self.middleAngle,
                12,
                18,
                opacity=180,
                width=2
            )

            # ----------------------------------------------------
            # INNER ROTATING RING
            # ----------------------------------------------------

            self.drawSegmentedRing(
                painter,
                center,
                95,
                self.innerAngle,
                8,
                25,
                opacity=220,
                width=3
            )

            # ----------------------------------------------------
            # EXTRA INNER DETAIL RING
            # ----------------------------------------------------

            self.drawSegmentedRing(
                painter,
                center,
                68,
                -self.middleAngle,
                6,
                32,
                opacity=120,
                width=1
            )

            # ----------------------------------------------------
            # HUD TICKS
            # ----------------------------------------------------

            self.drawTicks(
                painter,
                center,
                210
            )

            # ----------------------------------------------------
            # FRIDAY VOICE CORE
            # ----------------------------------------------------

            self.drawCenter(
                painter,
                center
            )

        finally:
            painter.end()


# ============================================================
# FRIDAY DASHBOARD WINDOW
# ============================================================

class FridayWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "F.R.I.D.A.Y. // Desktop Intelligence"
        )

        self.resize(
            1200,
            750
        )

        # Pure black for eventual projector use
        self.setStyleSheet(
            "background-color: black;"
        )

        self.state = "IDLE"

        self.lastCommand = (
            "SYSTEM READY"
        )

        self.activeTool = (
            "NONE"
        )


        # ----------------------------------------------------
        # ANIMATED CORE
        # ----------------------------------------------------

        self.core = FridayCore()

        self.core.setParent(
            self
        )


        # ----------------------------------------------------
        # DASHBOARD REFRESH
        # ----------------------------------------------------

        self.dashboardTimer = QTimer(
            self
        )

        self.dashboardTimer.timeout.connect(
            self.update
        )

        self.dashboardTimer.start(
            1000
        )


    # ========================================================
    # EXTERNAL AUDIO CONTROLS
    # ========================================================

    def setEnvironmentLevel(
        self,
        level
    ):

        self.core.setEnvironmentLevel(
            level
        )


    def setFridayVoiceLevel(
        self,
        level
    ):

        self.core.setFridayVoiceLevel(
            level
        )


    # ========================================================
    # FRIDAY STATE
    # ========================================================

    def setState(
        self,
        state
    ):

        self.state = (
            str(state).upper()
        )

        self.update()


    # ========================================================
    # COMMAND DISPLAY
    # ========================================================

    def setLastCommand(
        self,
        command
    ):

        self.lastCommand = str(
            command
        )

        self.update()


    # ========================================================
    # ACTIVE TOOL DISPLAY
    # ========================================================

    def setActiveTool(
        self,
        tool
    ):

        self.activeTool = str(
            tool
        )

        self.update()


    # ========================================================
    # DASHBOARD DRAWING
    # ========================================================

        # ========================================================
    # DASHBOARD DRAWING
    # ========================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        try:
            painter.setRenderHint(
                QPainter.Antialiasing
            )

            # ----------------------------------------------------
            # COLORS
            # ----------------------------------------------------

            cyan = QColor(
                90,
                220,
                255
            )

            dimCyan = QColor(
                60,
                150,
                180
            )

            faintCyan = QColor(
                40,
                100,
                120
            )

            # ----------------------------------------------------
            # HEADER
            # ----------------------------------------------------

            painter.setPen(
                QPen(
                    cyan,
                    1
                )
            )

            painter.setFont(
                QFont(
                    "Consolas",
                    18
                )
            )

            painter.drawText(
                40,
                45,
                "F.R.I.D.A.Y."
            )

            painter.setFont(
                QFont(
                    "Consolas",
                    9
                )
            )

            painter.drawText(
                42,
                65,
                "DESKTOP INTELLIGENCE SYSTEM"
            )

            painter.drawLine(
                40,
                80,
                self.width() - 40,
                80
            )

            # ----------------------------------------------------
            # DECORATIVE HEADER SEGMENTS
            # ----------------------------------------------------

            painter.setPen(
                QPen(
                    faintCyan,
                    1
                )
            )

            painter.drawLine(
                self.width() - 300,
                45,
                self.width() - 200,
                45
            )

            painter.drawLine(
                self.width() - 180,
                45,
                self.width() - 40,
                45
            )

            # ----------------------------------------------------
            # LEFT TELEMETRY
            # ----------------------------------------------------

            painter.setPen(
                dimCyan
            )

            painter.setFont(
                QFont(
                    "Consolas",
                    9
                )
            )

            painter.drawText(
                45,
                130,
                "SYSTEM // LOCAL"
            )

            painter.drawText(
                45,
                165,
                "WAKE ENGINE     ONLINE"
            )

            painter.drawText(
                45,
                190,
                "SPEECH          ONLINE"
            )

            painter.drawText(
                45,
                215,
                "LOCAL AI        QWEN 2.5"
            )

            painter.drawText(
                45,
                240,
                "VOICE           CORI"
            )

            # ----------------------------------------------------
            # LEFT DECORATIVE BARS
            # ----------------------------------------------------

            painter.setPen(
                QPen(
                    faintCyan,
                    2
                )
            )

            for i in range(5):

                painter.drawLine(
                    45,
                    280 + (i * 12),
                    100 + (i * 14),
                    280 + (i * 12)
                )

            # ----------------------------------------------------
            # RIGHT TELEMETRY
            # ----------------------------------------------------

            right = (
                self.width() - 275
            )

            painter.setPen(
                dimCyan
            )

            painter.drawText(
                right,
                130,
                "ACTIVE PROCESS"
            )

            painter.setPen(
                cyan
            )

            painter.setFont(
                QFont(
                    "Consolas",
                    13
                )
            )

            painter.drawText(
                right,
                160,
                self.state
            )

            painter.setFont(
                QFont(
                    "Consolas",
                    9
                )
            )

            painter.setPen(
                dimCyan
            )

            painter.drawText(
                right,
                210,
                "ACTIVE TOOL"
            )

            painter.setPen(
                cyan
            )

            painter.drawText(
                right,
                235,
                self.activeTool
            )

            painter.setPen(
                dimCyan
            )

            painter.drawText(
                right,
                285,
                "CONTROL SYSTEM"
            )

            painter.drawText(
                right,
                315,
                "WINDOWS       READY"
            )

            painter.drawText(
                right,
                340,
                "MEDIA         READY"
            )

            painter.drawText(
                right,
                365,
                "AUDIO         READY"
            )

            # ----------------------------------------------------
            # RIGHT DECORATIVE BARS
            # ----------------------------------------------------

            painter.setPen(
                QPen(
                    faintCyan,
                    2
                )
            )

            for i in range(5):

                painter.drawLine(
                    right,
                    405 + (i * 12),
                    right + 55 + (i * 14),
                    405 + (i * 12)
                )

            # ----------------------------------------------------
            # BOTTOM COMMAND PANEL
            # ----------------------------------------------------

            painter.setPen(
                QPen(
                    dimCyan,
                    1
                )
            )

            painter.drawLine(
                40,
                self.height() - 120,
                self.width() - 40,
                self.height() - 120
            )

            painter.drawText(
                45,
                self.height() - 85,
                "LAST COMMAND"
            )

            painter.setPen(
                cyan
            )

            commandText = (
                "> "
                + self.lastCommand
            )

            # Prevent giant commands from going
            # all the way across the dashboard.
            if len(commandText) > 90:

                commandText = (
                    commandText[:87]
                    + "..."
                )

            painter.drawText(
                45,
                self.height() - 58,
                commandText
            )

            painter.setPen(
                dimCyan
            )

            painter.drawText(
                self.width() - 250,
                self.height() - 85,
                "STATUS"
            )

            painter.setPen(
                cyan
            )

            painter.drawText(
                self.width() - 250,
                self.height() - 58,
                self.state
            )

            # ----------------------------------------------------
            # SMALL FOOTER
            # ----------------------------------------------------

            painter.setPen(
                faintCyan
            )

            painter.setFont(
                QFont(
                    "Consolas",
                    7
                )
            )

            painter.drawText(
                45,
                self.height() - 25,
                "LOCAL SYSTEM // PROJECT FRIDAY"
            )

        finally:
            painter.end()


    # ========================================================
    # POSITION ANIMATED CORE
    # ========================================================

    def resizeEvent(
        self,
        event
    ):

        coreWidth = 600
        coreHeight = 550

        x = (
            self.width()
            - coreWidth
        ) // 2

        y = (
            self.height()
            - coreHeight
        ) // 2

        self.core.setGeometry(
            x,
            y,
            coreWidth,
            coreHeight
        )


    # ========================================================
    # FULLSCREEN CONTROLS
    # ========================================================

    def keyPressEvent(
        self,
        event
    ):

        # F11
        if (
            event.key()
            == Qt.Key_F11
        ):

            if self.isFullScreen():

                self.showNormal()

            else:

                self.showFullScreen()


        # ESC
        elif (
            event.key()
            == Qt.Key_Escape
        ):

            self.showNormal()


# ============================================================
# START VISUAL APPLICATION
# ============================================================

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    friday = FridayWindow()

    friday.show()

    sys.exit(
        app.exec()
    )