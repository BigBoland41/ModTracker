import mod, unittest, json

class TestAPICalls(unittest.TestCase):
    def testModrinthData(self):
        modObj = mod.Mod(url ="https://modrinth.com/mod/sodium")
        modObj2 = mod.Mod(url = "https://modrinth.com/mod/fabric-api")
        modObj3 = mod.Mod(url = "https://modrinth.com/mod/cloth-config")
        modObj4 = mod.Mod(url = "https://www.curseforge.com/minecraft/mc-mods/sodium")
        self.assertNotEqual(modObj.getModrinthData(), False)
        self.assertNotEqual(modObj2.getModrinthData(), False)
        self.assertNotEqual(modObj3.getModrinthData(), False)
        self.assertNotEqual(modObj4.getModrinthData(), False)


         
    def testVersion(self):
        modObj = mod.Mod(url ="https://modrinth.com/mod/sodium")
        modObj2 = mod.Mod(url = "https://modrinth.com/mod/fabric-api")
        modObj3 = mod.Mod(url = "https://modrinth.com/mod/cloth-config")
        modObj4 = mod.Mod(url = "https://www.curseforge.com/minecraft/mc-mods/sodium")
        self.assertEqual(modObj.getCurrentVersion(), "1.21.5")
        self.assertEqual(modObj2.getCurrentVersion(), "25w17a")
        self.assertEqual(modObj3.getCurrentVersion(), "1.21.5")
        self.assertEqual(modObj4.getCurrentVersion(), "1.21.5")

    def testName(self):
        modObj = mod.Mod(url ="https://modrinth.com/mod/sodium")
        modObj2 = mod.Mod(url = "https://modrinth.com/mod/fabric-api")
        modObj3 = mod.Mod(url = "https://modrinth.com/mod/cloth-config")
        modObj4 = mod.Mod(url = "https://www.curseforge.com/minecraft/mc-mods/sodium")
        self.assertEqual(modObj.getName(), "Sodium")
        self.assertEqual(modObj2.getName(), "Fabric API")
        self.assertEqual(modObj3.getName(), "Cloth Config API")
        self.assertEqual(modObj4.getName(), "Sodium")

    def testUrl(self):
        modObj = mod.Mod(url ="https://modrinth.com/mod/sodium")
        modObj2 = mod.Mod(url = "https://modrinth.com/mod/fabric-api")
        modObj3 = mod.Mod(url = "https://modrinth.com/mod/cloth-config")
        modObj4 = mod.Mod(url = "https://www.curseforge.com/minecraft/mc-mods/sodium")
        self.assertEqual(modObj.getURL(), "https://modrinth.com/mod/sodium")
        self.assertEqual(modObj2.getURL(), "https://modrinth.com/mod/fabric-api")
        self.assertEqual(modObj3.getURL(), "https://modrinth.com/mod/cloth-config")
        self.assertEqual(modObj4.getURL(), "https://www.curseforge.com/minecraft/mc-mods/sodium")

    def testValidUrl(self):
        modObj = mod.Mod(url ="https://modrinth.com/mod/sodium")
        modObj2 = mod.Mod(url = "https://modrinth.com/mod/fabric-api")
        modObj3 = mod.Mod(url = "https://modrinth.com/mod/cloth-config")
        modObj4 = mod.Mod(url = "https://www.curseforge.com/minecraft/mc-mods/sodium")
        modObj5 = mod.Mod(url = "https://www.curseforge.com/minecrafods/sodium")
        self.assertTrue(modObj.verifyURL())
        self.assertTrue(modObj2.verifyURL())
        self.assertTrue(modObj3.verifyURL())
        self.assertTrue(modObj4.verifyURL())
        self.assertFalse(modObj5.verifyURL())

    def testModSave(self):
        modObj = mod.Mod(url ="https://modrinth.com/mod/sodium")
        modObj2 = mod.Mod(url = "https://modrinth.com/mod/fabric-api")
        modObj3 = mod.Mod(url = "https://modrinth.com/mod/cloth-config")
        modObj4 = mod.Mod(url = "https://www.curseforge.com/minecraft/mc-mods/sodium")
        dict1 = modObj.createDict()
        dict2 = modObj2.createDict()
        dict3 = modObj3.createDict()
        dict4 = modObj4.createDict()
        self.assertEqual(dict1["name"], modObj.getName())
        self.assertEqual(dict1["id"], modObj.getID())
        self.assertEqual(dict1["url"], modObj.getURL())
        self.assertEqual(dict1["versions"], modObj.getVersions())
        self.assertEqual(dict2["name"], modObj2.getName())
        self.assertEqual(dict2["id"], modObj2.getID())
        self.assertEqual(dict2["url"], modObj2.getURL())
        self.assertEqual(dict2["versions"], modObj2.getVersions())
        self.assertEqual(dict3["name"], modObj3.getName())
        self.assertEqual(dict3["id"], modObj3.getID())
        self.assertEqual(dict3["url"], modObj3.getURL())
        self.assertEqual(dict3["versions"], modObj3.getVersions())
        self.assertEqual(dict4["name"], modObj4.getName())
        self.assertEqual(dict4["id"], modObj4.getID())
        self.assertEqual(dict4["url"], modObj4.getURL())
        self.assertEqual(dict4["versions"], modObj4.getVersions())




if __name__ == "__main__":
    unittest.main(verbosity=2,failfast=True)