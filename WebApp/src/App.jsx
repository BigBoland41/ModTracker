import { useState } from 'react';
import axios from 'axios';

import ModTable from './modTable';
import TextInputBox from './textInputBox';

function App() {
    const [mods, setMods] = useState([]);
    const [input, setInput] = useState('');
    const [output, setOutput] = useState('');
    const [tempMod, setTempMod] = useState()

    const handlePriorityChange = (tablePos, newPriority) => {
        setMods(mods.map(mod =>
            mod.tablePos === tablePos ? { ...mod, priority: newPriority } : mod
        ));
    };

    const handleDelete = (tablePosition) => {
        setMods(mods.filter(mod => mod.tablePos !== tablePosition));
    };

    const addMod = async () => {
        try {
            const response = await axios.post('http://localhost:8000/run-test', {
                url: input,
            });

            if (response.data.name == "Untitled Mod") {
                setOutput('Could not find this mod. Check that the URL you provided is valid.')
            }
            else {
                setOutput('Added ' + response.data.name)

                const newMod = {
                    tablePos: mods.length > 0 ? Math.max(...mods.map(mod => mod.tablePos)) + 1 : 1,
                    name: "" + response.data.name,
                    version: "" + response.data.version,
                    priority: "" + response.data.priority
                };
                setMods([...mods, newMod]);
            }
        } catch (error) {
            console.error('Error:', error);
            setOutput('Error calling API:\n' + error);
        }
    };

    return (
        <>
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
