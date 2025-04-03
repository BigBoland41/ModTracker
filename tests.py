import data
import mod
import unittest
import json
class testAPICalls(unittest.TestCase):

    #


    def testMod(self):
        modObj = mod.Mod(url ="https://modrinth.com/mod/sodium")
        modObj2 = mod.Mod(url = "https://modrinth.com/mod/fabric-api")
        modObj3 = mod.Mod(url = "https://modrinth.com/mod/cloth-config")
        modObj4 = mod.Mod(url = "https://www.curseforge.com/minecraft/mc-mods/sodium")
        self.assertNotEqual(modObj.modrinth, False)
        self.assertEqual(modObj.getCurrentVersion(), "1.21.5")
        self.assertNotEqual(modObj.curseforge, False)
        self.assertEqual(modObj.getID(), "AANobbMI")
        self.assertNotEqual(modObj2.modrinth, False)
        self.assertEqual(modObj2.getCurrentVersion(), "1.21.5")
        self.assertNotEqual(modObj3.modrinth, False)
        self.assertEqual(modObj3.getCurrentVersion(), "1.21.5")
        with open("mod_info.json", "w") as json_file:
            json.dump(modObj.curseforge, json_file, indent=4)
        self.assertNotEqual(modObj4.modrinth, False)
        self.assertEqual(modObj4.getCurrentVersion(), "1.21.5")
        self.assertNotEqual(modObj4.curseforge, False)
        self.assertEqual(modObj4.getID(), "AANobbMI")
        self.assertEqual(modObj.getName(), "Sodium")
        self.assertEqual(modObj2.getName(), "Fabric API")
        self.assertEqual(modObj3.getName(), "Cloth Config API")
        self.assertEqual(modObj4.getName(), "Sodium")
        self.assertEqual(modObj.getCurrentVersion(), "1.21.5")
        self.assertEqual(modObj2.getCurrentVersion(), "1.21.5")
        self.assertEqual(modObj3.getCurrentVersion(), "1.21.5")
        self.assertEqual(modObj4.getCurrentVersion(), "1.21.5")
        self.assertEqual(modObj.getURL(), "https://modrinth.com/mod/sodium")
        self.assertEqual(modObj2.getURL(), "https://modrinth.com/mod/fabric-api")
        self.assertEqual(modObj3.getURL(), "https://modrinth.com/mod/cloth-config")
        self.assertEqual(modObj4.getURL(), "https://www.curseforge.com/minecraft/mc-mods/sodium")




if __name__ == "__main__":
    unittest.main()