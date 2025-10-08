import { useEffect, useState } from 'react';
import axios from 'axios';

import ModTable from './modTable';
import TextInputBox from './textInputBox';

function App() {
    const blankProfileData = {
        profile: {
            "name": "No Data",
            "version": "No Data",
            "modlist": []
        },
        modListLength: 0,
        errorMessage: "None"
    }

    const [profileData, setProfileData] = useState(blankProfileData)
    const [mods, setMods] = useState([]);
    const [input, setInput] = useState('');
    const [output, setOutput] = useState('');

    useEffect(() => { updateProfileData() }, [])

    useEffect(() => {
        let modList = []
        for (let i = 0; i < profileData.modListLength; i++) {
            const modData = profileData.profile.modlist[i]
            const newMod = {
                name: modData.name,
                id: modData.id,
                url: modData.url,
                versions: modData.versions,
                priority: modData.priority,
                tablePos: i
            };
            modList = [...modList, newMod]
        }
        setMods(modList);
    }, [profileData])

    const genericCall = async (callName, params) => {
        try {
            const url = `http://localhost:8000/${callName}`
            console.log('Making post to ' + url + ' with data ' + JSON.stringify(params))
            const response = await axios.post(url, params);
            // console.log('Post successful!')
            return response.data
        } catch (error) {
            console.error('Error:\n', error);
            setOutput('Error calling API:\n' + error);
        }
    }

    const handlePriorityChange = (tablePos, newPriority) => {
        console.log("Changing priority functionality coming soon!")
        setMods(mods.map(mod =>
            mod.tablePos === tablePos ? { ...mod, priority: newPriority } : mod
        ));
    };

    const handleDelete = (tablePosition) => {
        console.log("Delete functionality coming soon!")
        // setMods(mods.filter(mod => mod.tablePos !== tablePosition));
    };

    const updateProfileData = async () => {
        const data = await genericCall("get-profile", { profileIndex: 0 })
        setProfileData(data)

        if (profileData.errorMessage != "None") {
            console.log("ERROR:\n" + profileData.errorMessage)
            setOutput("ERROR:\n" + profileData.errorMessage)
        }
    }

    const addMod = async () => {
        const data = await genericCall("add-mod", { url: input, profileIndex: 0 })

        if (data.errorMessage != "None")
            setOutput("ERROR:\n" + data.errorMessage)
        else
            setOutput('Mod successfully added')

        updateProfileData()
    }

    return (
        <>
            <div>
                <h2>{profileData.profile.name}</h2>
                <pre>Selected Version: {profileData.profile.version}</pre>
                <pre>{profileData.modListLength} mods</pre>
            </div>
            <div>
                <ModTable
                    mods={mods}
                    onPriorityChange={handlePriorityChange}
                    onDelete={handleDelete}
                />
            </div>
            <div>
                <TextInputBox
                    onTextChange={(newInput) => { setInput(newInput) }}
                />
                <button onClick={addMod} className="add-mod-button">Add Mod</button>
                <pre>{output}</pre>
            </div>
        </>
    );
}

export default App;
