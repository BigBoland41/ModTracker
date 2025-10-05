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
                        <td>{mod.version}</td>
                        <td>
                            <select
                                value={mod.priority}
                                onChange={(e) => onPriorityChange(mod.tablePos, e.target.value)}
                                className="priority-dropdown"
                            >
                                <option value="Low">Low</option>
                                <option value="Medium">Medium</option>
                                <option value="High">High</option>
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
