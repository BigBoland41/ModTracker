import sys, os, unittest, testData
from PyQt6 import QtWidgets


class TestFileDownloads(testData.TestCase):
    def testModrinthDownload(self):
        if self._testAPICalls is False:
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

    def testCurseforgeDownload(self):
        if self._testAPICalls is False:
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