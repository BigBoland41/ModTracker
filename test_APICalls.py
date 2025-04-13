import mod, unittest, json

class TestAPICalls(unittest.TestCase):
    def testAPICalls(self):
        modObj = mod.Mod(url ="https://modrinth.com/mod/sodium")
        modObj2 = mod.Mod(url = "https://modrinth.com/mod/fabric-api")
        modObj3 = mod.Mod(url = "https://modrinth.com/mod/cloth-config")
        modObj4 = mod.Mod(url = "https://www.curseforge.com/minecraft/mc-mods/sodium")
        modObj5 = mod.Mod(url = "https://www.curseforge.com/minecrafods/sodium")
        self.assertNotEqual(modObj.getModrinthData(), False)
        self.assertEqual(modObj.getCurrentVersion(), "1.21.5")
        self.assertNotEqual(modObj.getCurseforgeData(), False)
        self.assertEqual(modObj.getID(), "AANobbMI")
        self.assertNotEqual(modObj2.getModrinthData(), False)
        self.assertEqual(modObj2.getCurrentVersion(), "25w15a")
        self.assertNotEqual(modObj3.getModrinthData(), False)
        self.assertEqual(modObj3.getCurrentVersion(), "1.21.5")
        with open("mod_info.json", "w") as json_file:
            json.dump(modObj.getCurseforgeData(), json_file, indent=4)
        self.assertNotEqual(modObj4.getModrinthData(), False)
        self.assertEqual(modObj4.getCurrentVersion(), "1.21.5")
        self.assertNotEqual(modObj4.getCurseforgeData(), False)
        self.assertEqual(modObj4.getID(), "AANobbMI")
        self.assertEqual(modObj.getName(), "Sodium")
        self.assertEqual(modObj2.getName(), "Fabric API")
        self.assertEqual(modObj3.getName(), "Cloth Config API")
        self.assertEqual(modObj4.getName(), "Sodium")
        self.assertEqual(modObj.getCurrentVersion(), "1.21.5")
        self.assertEqual(modObj2.getCurrentVersion(), "25w15a")
        self.assertEqual(modObj3.getCurrentVersion(), "1.21.5")
        self.assertEqual(modObj4.getCurrentVersion(), "1.21.5")
        self.assertEqual(modObj.getURL(), "https://modrinth.com/mod/sodium")
        self.assertEqual(modObj2.getURL(), "https://modrinth.com/mod/fabric-api")
        self.assertEqual(modObj3.getURL(), "https://modrinth.com/mod/cloth-config")
        self.assertEqual(modObj4.getURL(), "https://www.curseforge.com/minecraft/mc-mods/sodium")
        self.assertTrue(modObj.verifyURL())
        self.assertTrue(modObj2.verifyURL())
        self.assertTrue(modObj3.verifyURL())
        self.assertTrue(modObj4.verifyURL())
        self.assertFalse(modObj5.verifyURL())


if __name__ == "__main__":
    unittest.main()