import data
import mod
import unittest
class testAPICalls(unittest.TestCase):

    #


    def testMod(self):
        modObj = mod.Mod(url ="https://modrinth.com/mod/sodium")
        self.assertNotEqual(modObj.modrinth, False)
        self.assertEqual(modObj.getCurrentVersion(), "1.21.5")
        self.assertEqual(modObj.getID(), "AANobbMI")


if __name__ == "__main__":
    unittest.main()