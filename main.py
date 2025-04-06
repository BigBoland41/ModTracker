import sys, detailsWindow, mod
from PyQt6 import QtWidgets

def initMockData(window):
    highPriority = mod.ModPriority("High Priority", 255, 85, 0)
    lowPriority = mod.ModPriority("Low Priority", 255, 255, 0)
    priorityList = [highPriority, lowPriority]
    
    modList = [
        mod.Mod("Sodium", 1, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], highPriority),
        mod.Mod("Lithium", 2, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
        mod.Mod("Entity Culling", 3, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], lowPriority),
        mod.Mod("Dynamic FPS", 4, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], lowPriority),
        mod.Mod("Enhanced Block Entities", 5, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
        mod.Mod("Entity Model Features", 6, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
        mod.Mod("Entity Texture Features", 7, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
        mod.Mod("CIT Resewn", 8, ["1.21", "1.21.1"], lowPriority),
        mod.Mod("Animatica", 9, ["1.21"], lowPriority),
        mod.Mod("Continuity", 10, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
        mod.Mod("Iris Shaders", 11, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], lowPriority),
        mod.Mod("WI Zoom", 12, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], highPriority),
        mod.Mod("LambDynamicLights", 13, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], highPriority),
        mod.Mod("MaLiLib", 14, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
        mod.Mod("Litematica", 15, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
        mod.Mod("MniHUD", 16, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
        mod.Mod("WorldEdit", 17, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
        mod.Mod("Flashback", 18, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], lowPriority),
        mod.Mod("Shulker Box Tooltip", 19, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], lowPriority),
        mod.Mod("CraftPresence", 20, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], lowPriority),
        mod.Mod("Command Keys", 21, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], lowPriority),
        mod.Mod("Advancements Reloaded", 22, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], lowPriority),
        mod.Mod("Mod Menu", 23, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], lowPriority)
    ]

    return detailsWindow.DetailsWindow(window, modList, priorityList, "1.21.5")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    profileView = initMockData(mainWindow)
    mainWindow.showMaximized()
    sys.exit(app.exec())