import sys, os, unittest
from PyQt6 import QtWidgets, QtTest, QtCore, QtGui

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import windows, mod
from testData import TestData

class TestDetailsView(unittest.TestCase):
    def setUp(self):
        self._window = QtWidgets.QMainWindow()
        self._detailsView = None
        self._selectView = windows.ProfileSelectWindow(self._openDetailsView, allowWriteToFile=False)
        self._data = TestData()

    def tearDown(self):
        self._window.deleteLater()

        if self._detailsView is not None:
            self._detailsView.getModList().clear()
            self._detailsView.getModTable()._dropdownBtnList.clear()

        self._selectView._profileList.clear()
        self._selectView._priorityList.clear()
        self._selectView._profileWidgets.clear()

    def _openDetailsView(self, profile:mod.ModProfile):
        self._detailsView = windows.DetailsWindow(profile.modList, profile.priorityList, profile.selectedVersion, self._closeDetailsView, self._selectView.saveJson)

    def _closeDetailsView(self):
        self._detailsView.deleteLater()
    
    def testCreateWindow(self):
        self.assertIsNotNone(self._selectView)

    def testAddProfile(self):
        testDataProfile = mod.ModProfile(self._data.constructModList())
        manualProfile = mod.ModProfile(
            [mod.Mod("Mod 1", -1, ["1.19.2", "1.21.1"], mod.ModPriority("custom priority level 1")),
            mod.Mod("Mod 2", -1, ["1.21.1", "1.21.3"], mod.ModPriority("custom priority level 2")),
            mod.Mod("Mod 3", -1, ["1.16.4", "1.19.2"], mod.ModPriority("custom priority level 3"))]
        )
        emptyProfile = mod.ModProfile()

        self._selectView.addProfile(testDataProfile, promptProfileName=False)
        self._selectView.addProfile(manualProfile, promptProfileName=False)
        self._selectView.addProfile(emptyProfile, promptProfileName=False)
        
        profileList = self._selectView.getProfileList()
        priorityList = self._selectView.getPriorityList()

        self.assertEqual(len(profileList), 3)
        self.assertEqual(len(priorityList), 5)

        self.assertEqual(profileList[0], testDataProfile)
        self.assertEqual(profileList[1], manualProfile)
        self.assertEqual(profileList[2], emptyProfile)

    def testOpenDetailsView(self):
        testDataProfile = mod.ModProfile(self._data.constructModList())
        self._selectView.addProfile(testDataProfile, promptProfileName=False)

        QtTest.QTest.mouseClick(self._selectView._profileWidgets[0], QtCore.Qt.MouseButton.LeftButton)

        self.assertIsNotNone(self._detailsView)

        modTable = self._detailsView.getModTable()
        modList = self._data.modNames

        for i in range(len(self._data.modNames)):
            self.assertEqual(modTable.getRowNameText(i), modList[i], f"Element #{i} of {len(modList)} (0 indexed)")

    def testAddPriorityLevel(self):
        newPriorityName = "New Priority"
        newPriorityColor = QtGui.QColor(255, 255, 255)
        
        testDataProfile = mod.ModProfile(self._data.constructModList())
        self._selectView.addProfile(testDataProfile, promptProfileName=False)
        QtTest.QTest.mouseClick(self._selectView._profileWidgets[0], QtCore.Qt.MouseButton.LeftButton)

        priorityList = self._selectView.getPriorityList()
        self.assertEqual(len(priorityList), 2)
        
        modTable = self._detailsView.getModTable()
        dropdownBtn = modTable.getRowDropdownBtn(0)
        dropdownBtn.clickDropdownOption(2, newPriorityName, newPriorityColor)

        priorityList = self._selectView.getPriorityList()
        self.assertEqual(len(priorityList), 3)
        self.assertEqual(priorityList[2].name, newPriorityName)

    def testAddTooManyProfiles(self):
        # max amount of profiles is 8. There should only be 8 widgets, even if there's 9 profiles.
        profileList = [mod.ModProfile(), mod.ModProfile(), mod.ModProfile(), mod.ModProfile(),
                       mod.ModProfile(), mod.ModProfile(), mod.ModProfile(), mod.ModProfile(), mod.ModProfile()]

        for profile in profileList:
            self._selectView.addProfile(profile, promptProfileName=False)

        self.assertEqual(len(self._selectView._profileWidgets), 8)
        self.assertFalse(self._selectView._addProfileWidget.isHidden())

    def testDeleteProfile(self):
        profile1 = mod.ModProfile()
        profile2 = mod.ModProfile()

        self._selectView.addProfile(profile1, promptProfileName=False)
        self._selectView.addProfile(profile2, promptProfileName=False)

        self._selectView.deleteProfile(0)

        profileList = self._selectView.getProfileList()
        widgetList = self._selectView._profileWidgets

        self.assertEqual(profileList[0], profile2)
        self.assertNotIn(profile1, profileList)
        self.assertEqual(len(widgetList), 1)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    unittest.main(verbosity=2,failfast=True)