# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations

import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCharts import QChart, QChartView, QPieSeries


class TestChart(QMainWindow):

    def __init__(self):
        super().__init__()

        self.series = QPieSeries()

        self.series.append('Ready', 3)
        self.series.append('High Priority', 1)
        self.series.append('Non-essential', 1)

        self.slice = self.series.slices()[0]
        # self.slice.setExploded()
        self.slice.setLabelVisible()
        self.slice.setBrush(QColor(0, 255, 0))

        self.slice = self.series.slices()[1]
        self.slice.setLabelVisible()
        self.slice.setBrush(QColor(255, 85, 0))

        self.slice = self.series.slices()[2]
        self.slice.setLabelVisible()
        self.slice.setBrush(QColor(255, 255, 0))

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle('Simple piechart example')
        self.chart.legend().hide()

        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.setCentralWidget(self._chart_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = TestChart()
    window.show()
    window.resize(440, 300)

    sys.exit(app.exec())