const TextInputBox = ({ onTextChange }) => {
    return (
        <input
            type='text'
            placeholder='Mod URL'
            size='75'
            onChange={(event) => {
                onTextChange(event.target.value)
            }}
        />
    )
}

export default TextInputBox