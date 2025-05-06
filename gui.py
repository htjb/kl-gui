import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QSlider, QLabel, QHBoxLayout
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class LinePlotWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.mean = 0
        self.std = 1

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Set up matplotlib figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Sliders layout
        sliders_layout = QVBoxLayout()

        self.ndims = 2
        self.mean_prior = [-3, 3]
        self.std_prior = [0.01, 10]
        self.mean_slider = self.create_slider(self.update_plot, 3*100/6)
        self.std_slider = self.create_slider(self.update_plot, 1.01*100/9.99)

        sliders_layout.addLayout(
            self.labeled_slider(r"Mean", self.mean_slider,
                                self.mean_prior))
        sliders_layout.addLayout(
            self.labeled_slider(r"Sigma", self.std_slider,
                                self.std_prior))

        layout.addLayout(sliders_layout)

        self.setLayout(layout)
        self.update_plot()

    def create_slider(self, slot, value):
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 100)  # for decimal steps
        slider.setSingleStep(1)
        slider.setValue(int(value))
        slider.valueChanged.connect(slot)
        return slider

    def labeled_slider(self, label_text, slider, prior):
        layout = QHBoxLayout()
        value = slider.value() / 100* (prior[1] - prior[0]) + prior[0]
        label = QLabel(f"{label_text} = {value:.3f}")
        slider.valueChanged.connect(
            lambda val: label.setText(f"{label_text} = {(val/100* (prior[1] - prior[0]) + prior[0]):.3f}"))
        layout.addWidget(label)
        layout.addWidget(slider)
        return layout

    def update_plot(self):

        def gaussian(x, mean, std):
            return np.exp(-0.5 * ((x - mean) / std) ** 2) / (std * np.sqrt(2 * np.pi))

        x = np.linspace(-5, 5, 100)

        self.mean = self.mean_slider.value() / 100 * (self.mean_prior[1] - self.mean_prior[0]) + self.mean_prior[0]
        self.std = self.std_slider.value() / 100 * (self.std_prior[1] - self.std_prior[0]) + self.std_prior[0]

        kl = np.log(self.std / 1) + (1 ** 2 + (self.mean - 0) ** 2) / (2 * self.std ** 2) - 0.5

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, gaussian(x, 0, 1), marker='x')
        ax.plot(x, gaussian(x, self.mean, self.std), marker='o', label="KL={kl:.3f}".format(kl=kl))
        ax.set_ylim(0, 1)
        ax.legend()
        ax.set_xlabel("x")
        ax.set_ylabel("Probability Density")
        ax.grid(True)

        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LinePlotWidget()
    window.setWindowTitle("Sigma MS")
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec())
