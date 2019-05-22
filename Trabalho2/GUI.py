import threading
from queue import Queue
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from NeuralNetwork import NeuralNetwork
from KNearestNeighbor import knn_main
from SVM import svm_main
from tkinter import Tk, Label, Button, Entry, StringVar, DISABLED, NORMAL, END, W, E, LEFT, filedialog, Toplevel, Text
import random
import matplotlib
matplotlib.use('TkAgg')


class MainWindow:
    def __init__(self):
        self.master = Tk()
        self.master.protocol("WM_DELETE_WINDOW", self.quit)
        self.master.geometry("500x300")
        self.master.resizable(0, 0)

        self.master.title("Deep Learning")
        self.title_label = Label(
            self.master, text="Dota2 Victory prevision App")
        self.title_label.grid(row=0, column=1)

        self.train_file_label = Label(
            self.master, text="Train File Path", justify=LEFT)
        self.train_file_label.grid(row=1)

        self.train_file_path = Entry(self.master)
        self.train_file_path.grid(row=2, column=0)

        self.train_file_browse = Button(
            self.master, text="Browser", command=self.browseTrain)

        self.train_file_browse.grid(row=2, column=1)

        self.test_file_label = Label(
            self.master, text="Test File Path", justify=LEFT)
        self.test_file_label.grid(row=3)

        self.test_file_path = Entry(self.master)
        self.test_file_path.grid(row=4, column=0)

        self.test_file_browse = Button(
            self.master, text="Browser", command=self.browseTest)

        self.test_file_browse.grid(row=4, column=1)

        self.NeuralNetworkButton = Button(
            self.master, text="Neural Network", command=self.startNeuralNetwork)
        self.NeuralNetworkButton.grid(row=5, column=1)

        self.KNNButton = Button(
            self.master, text="KNN", command=self.KNN)
        self.KNNButton.grid(row=6, column=1)

        self.SVMButton = Button(
            self.master, text="SVM", command=self.KNN)
        self.SVMButton.grid(row=7, column=1)

        self.C4dot5Button = Button(
            self.master, text="C4.5", command=self.C4dot5)
        self.C4dot5Button.grid(row=8, column=1)

    def run(self):
        self.master.mainloop()

    def startNeuralNetwork(self):
        win = AlgorithmWindow(self)
        win.startTask(threading.Thread(target=NeuralNetwork, args=(win, self.train_file_path.get(),
                                                                   self.test_file_path.get())))

    def KNN(self):
        win = AlgorithmWindow(self)
        win.startTask(threading.Thread(target=knn_main, args=(win, self.train_file_path.get(),
                                                              self.test_file_path.get())))

    def SVM(self):
        win = AlgorithmWindow(self)
        win.startTask(threading.Thread(target=svm_main, args=(win, self.train_file_path.get(),
                                                              self.test_file_path.get())))

    def C4dot5(self):
        print("c4.5")

    def browseTrain(self):
        filename = filedialog.askopenfilename()
        self.train_file_path.insert(0, filename)

    def browseTest(self):
        filename = filedialog.askopenfilename()
        self.test_file_path.insert(0, filename)

    def hide(self):
        self.master.withdraw()

    def show(self):
        self.master.update()
        self.master.deiconify()

    def quit(self):
        self.master.quit()
        self.master.destroy()


class AlgorithmWindow:
    def __init__(self, parent):
        self.STOP_THREAD = False
        self.plots = Queue()
        self.task = threading.Event()
        self.master = Toplevel()
        self.parent = parent
        self.parent.hide()
        self.master.protocol("WM_DELETE_WINDOW", self.returnMain)
        self.master.geometry("600x680")
        self.master.resizable(0, 0)

        self.master.title("Deep Learning")

        self.textarea = Text(self.master, height=10, width=60)
        self.textarea.config(state=DISABLED)
        self.textarea.grid(row=0, column=0)
        self.setCanvas()

    def print(self, text):
        self.textarea.config(state=NORMAL)
        self.textarea.insert(END, text+"\n")
        self.textarea.config(state=DISABLED)

    def startTask(self, task):
        self.task = task
        self.task.start()
        self.STOP_THREAD = False

    def returnMain(self):
        self.STOP_THREAD = True
        self.task.join()
        self.parent.show()
        self.parent.master.after_cancel(self._afterJob)
        self.master.destroy()

    def setCanvas(self):
        fig, axes = plt.subplots(2, sharex=True, figsize=(5, 5))
        self.axes = axes
        # Tell Tkinter to display matplotlib figure
        self.canvas = FigureCanvasTkAgg(fig, master=self.master)
        self.canvas.get_tk_widget().grid(row=1, column=0)

        fig.suptitle('Training Metrics')

        axes[0].set_ylabel("Loss", fontsize=14)
        axes[0].plot([])

        axes[1].set_ylabel("Accuracy", fontsize=14)
        axes[1].set_xlabel("Epoch", fontsize=14)
        axes[1].plot([])
        self.canvas.draw()
        self.updatePlot()

    def plot(self, train_loss_results, train_accuracy_results):
        self.plots.put([train_loss_results, train_accuracy_results])

    def updatePlot(self):
        try:  # Try to check if there is data in the queue
            result = self.plots.get_nowait()
            self.axes[0].plot(result[0])
            self.axes[1].plot(result[1])
            self.canvas.draw()
            self._afterJob = self.parent.master.after(500, self.updatePlot)
        except:
            self._afterJob = self.parent.master.after(500, self.updatePlot)


def runApp():
    app = MainWindow()
    app.run()
