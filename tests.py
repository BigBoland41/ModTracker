import data
import unittest
class testAPICalls(unittest.TestCase):

    def testUrlSearch(self):
        self.assertEqual(data.mod_lookup("https://www.curseforge.com/minecraft/mc-mods/worldedit"), 225608)
        self.assertEqual(data.mod_lookup("https://www.curseforge.com/minecraft/mc-mods/sodium"), 394468)
        #self.assertEqual(data.mod_lookup("https://www.curseforge.com/minecraft/mc-mods/lithium"), 360438)
        self.assertEqual(data.mod_lookup("https://www.curseforge.com/minecraft/mc-mods/old-combat"), 317035)
        self.assertEqual(data.mod_lookup("https://www.curseforge.com/minecraft/mc-mods/litematica"), 308892)


if __name__ == "__main__":
    unittest.main()