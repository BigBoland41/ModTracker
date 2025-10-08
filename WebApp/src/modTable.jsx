import './styles/modTable.css';

const ModTable = ({ mods, onPriorityChange, onDelete }) => {
    return (
        <table className="mod-table">
            <thead>
                <tr>
                    <th>Mod Name</th>
                    <th>Latest Version</th>
                    <th>Ready/Priority</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                {mods.map((mod) => (
                    <tr key={mod.tablePos}>
                        <td>{mod.name}</td>
                        <td>{mod.versions.at(-1)}</td>
                        <td>
                            <select
                                value={mod.priority.name}
                                onChange={(e) => onPriorityChange(mod.tablePos, e.target.value)}
                                className="priority-dropdown"
                            >
                                <option value="Low Priority">Low Priority</option>
                                <option value="Medium Priority">Medium Priority</option>
                                <option value="High Priority">High Priority</option>
                                <option value={mod.priority.name}>{mod.priority.name}</option>
                            </select>
                        </td>
                        <td>
                            <button
                                onClick={() => onDelete(mod.tablePos)}
                                className="delete-button"
                            >
                                X
                            </button>
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default ModTable;
