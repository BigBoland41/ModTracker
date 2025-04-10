import testAPICalls, testDetailsWindow, testModTable, testDropdownBtn, testPieChart
import mod, unittest

'''
# applies to any test making an API call, not just the testAPICalls class
# it's recommended you turn this off if you plan to run tests multiple
# times in a row, in order to not get our API calls denied.
_testAPICalls = True

# applies only to specific classes. These should generally be left on unless testing the tests
_testDetailsWindow = True
_testModTable = True
_testDropdownBtn = False
_testPieChart = True

_selectedVersion = "1.21.5"
_highPriority = mod.ModPriority("High Priority", 255, 85, 0)
_lowPriority = mod.ModPriority("Low Priority", 255, 255, 0)
_priorityList = [_highPriority, _lowPriority]

_modNames = [
    "Sodium",
    "Lithium",
    "Entity Culling",
    "Dynamic FPS",
    "Enhanced Block Entities",
    "Entity Model Features",
    "Entity Texture Features",
    "CIT Resewn",
    "Animatica",
    "Continuity",
    "Iris Shaders",
    "WI Zoom",
    "LambDynamicLights",
    "MaLiLib",
    "Litematica",
    "MiniHUD",
    "WorldEdit",
    "Flashback",
    "Shulker Box Tooltip",
    "CraftPresence",
    "Command Keys",
    "Advancements Reloaded",
    "Mod Menu"
]

_modVersions = [
    ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"],
    ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
    ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
    ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"],
    ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
    ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
    ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
    ["1.21", "1.21.1"],
    ["1.21"],
    ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
    ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"],
    ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"],
    ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"],
    ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
    ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
    ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
    ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
    ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
    ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
    ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
    ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"],
    ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
    ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"]
]

_modPriorities = [0,0,1,1,0,0,0,1,1,0,1,0,0,0,0,0,0,1,1,1,1,1,1]

_modCurrentVersions = [
            "1.21.5",
            "1.21.4",
            "1.21.4",
            "1.21.5",
            "1.21.4",
            "1.21.4",
            "1.21.4",
            "1.21.1",
            "1.21",
            "1.21.4",
            "1.21.5",
            "1.21.5",
            "1.21.5",
            "1.21.4",
            "1.21.4",
            "1.21.4",
            "1.21.4",
            "1.21.4",
            "1.21.4",
            "1.21.4",
            "1.21.5",
            "1.21.4",
            "1.21.5"
        ]
'''

if __name__ == "__main__":
    testSuite = unittest.TestSuite()

    testSuite.addTest(unittest.TestLoader().loadTestsFromTestCase(testAPICalls.testAPICalls))
    testSuite.addTest(unittest.TestLoader().loadTestsFromTestCase(testDropdownBtn.testDropdownBtn))
    testSuite.addTest(unittest.TestLoader().loadTestsFromTestCase(testPieChart.testPieChart))
    testSuite.addTest(unittest.TestLoader().loadTestsFromTestCase(testDetailsWindow.testdetailsView))
    testSuite.addTest(unittest.TestLoader().loadTestsFromTestCase(testModTable.testModTable))

    unittest.TextTestRunner(failfast=True).run(testSuite)