import sys, os, unittest
from PyQt6 import QtWidgets, QtTest, QtCore

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import windows
from testData import TestData

_testAPICalls = True

class TestFileDownloads(unittest.TestCase):
    def setUp(self):
        # self._app = QtWidgets.QApplication(sys.argv)
        self._window = QtWidgets.QMainWindow()
        self._detailsView = windows.DetailsWindow()
        self._data = TestData()

        global _testAPICalls
        _testAPICalls = self._data.testAPICalls

    def tearDown(self):
        self._window.deleteLater()
        self._detailsView.getModList().clear()
        self._detailsView.getModTable()._dropdownBtnList.clear()
        # self._app.quit()
    
    @unittest.skipIf(not _testAPICalls, "API tests are off")
    def testModrinthDownload(self):
        if _testAPICalls is False:
            self.skipTest("API tests are off")

        self._detailsView.simulate_enterAndAddMod("https://modrinth.com/mod/entityculling")
        self._detailsView.simulate_enterAndAddMod("https://modrinth.com/mod/nether-height-expansion-mod")

        self._detailsView._selectedVersion = "1.21.6"

        self.assertEqual(self._detailsView.simulate_downloadMod(0), [True, False])
        self.assertEqual(self._detailsView.simulate_downloadMod(1), [True, False])
        self.assertEqual(self._detailsView.simulate_downloadMod(2), [True, False])
        self.assertEqual(self._detailsView.simulate_downloadMod(3), [False, False])

        self._detailsView._selectedVersion = "1.21"

        self.assertEqual(self._detailsView.simulate_downloadMod(0), [True, False])
        self.assertEqual(self._detailsView.simulate_downloadMod(1), [True, True])
        self.assertEqual(self._detailsView.simulate_downloadMod(2), [True, False])
        self.assertEqual(self._detailsView.simulate_downloadMod(3), [False, False])

    @unittest.skipIf(not _testAPICalls, "API tests are off")
    def testCurseforgeDownload(self):
        if _testAPICalls is False:
            self.skipTest("API tests are off")

        self._detailsView.simulate_enterAndAddMod("https://www.curseforge.com/minecraft/mc-mods/entityculling")
        self._detailsView.simulate_enterAndAddMod("https://www.curseforge.com/minecraft/mc-mods/ice-cream-mini-sword-and-new-trades")

        self._detailsView._selectedVersion = "1.21.6"

        self.assertEqual(self._detailsView.simulate_downloadMod(0), [True, False])
        self.assertEqual(self._detailsView.simulate_downloadMod(1), [True, False])
        self.assertEqual(self._detailsView.simulate_downloadMod(2), [True, False])
        self.assertEqual(self._detailsView.simulate_downloadMod(3), [False, False])

        self._detailsView._selectedVersion = "1.20.1"

        self.assertEqual(self._detailsView.simulate_downloadMod(0), [True, True])
        self.assertEqual(self._detailsView.simulate_downloadMod(1), [True, False])
        self.assertEqual(self._detailsView.simulate_downloadMod(2), [False, False])
        self.assertEqual(self._detailsView.simulate_downloadMod(3), [False, False])

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    unittest.main(verbosity=2,failfast=True)