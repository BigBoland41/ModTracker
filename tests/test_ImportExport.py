import sys, os, unittest
from PyQt6 import QtWidgets

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import windows, mod, json
from testData import TestData

_testAPICalls = True

class TestImportExport(unittest.TestCase):
    def setUp(self):
        self._window = QtWidgets.QMainWindow()
        self._detailsView = windows.DetailsWindow()
        self._selectView = windows.ProfileSelectWindow(self._openDetailsView, allowWriteToFile=False)
        self._data = TestData()

        self._fileName = "tests\\testProfile.json" 

        global _testAPICalls
        _testAPICalls = self._data.testAPICalls

    def _openDetailsView(self, profile:mod.ModProfile):
        self._detailsView = windows.DetailsWindow(profile.modList, profile.priorityList, profile.selectedVersion, self._closeDetailsView, self._selectView.saveJson)

    def _closeDetailsView(self):
        self._detailsView.deleteLater()

    def testExport(self):
        profile = mod.ModProfile(self._data.constructModList(), self._data.priorityList, self._data.selectedVersion, "Test Profile")
        profileDict = profile.createDict()  # dictionary to test against

        self._detailsView.loadNewData(profile.modList, profile.priorityList, profile.selectedVersion)
        self._detailsView.simulate_export(self._fileName)

        try:
            with open(self._fileName, "r") as f:
                outputDict = json.load(f)  # dictionary from output file.
                self.assertEqual(profileDict, outputDict)  # test if before and after dictionaries match
        except FileNotFoundError:
            self.fail("Output file could not be found.")

    def testImport(self):
        profile = mod.ModProfile(self._data.constructModList(), self._data.priorityList, self._data.selectedVersion, "Test Profile")
        
        self._selectView.simulate_import(f"{parent_dir}\\{self._fileName}", requireValidModURL=False)
        importedProfile = self._selectView.getProfileList()[0]

        self.assertEqual(profile.modList[0], importedProfile.modList[0])
        
    def tearDown(self):
        self._window.deleteLater()
        self._detailsView.getModList().clear()
        self._detailsView.getModTable()._dropdownBtnList.clear()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    unittest.main(verbosity=2,failfast=True)