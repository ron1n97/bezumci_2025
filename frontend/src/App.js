
import backgroundImg from "./phone.jpg";
function App() {
  return (
    <div style={{
      backgroundImage:`url(${backgroundImg})`,
    }}
    >
      <div style={{
        fontSize: "100px",
        color: "yellow",
        marginLeft: "253px",
        textShadow: "0 0 5px blue, 0 0 5px blue, 0 0 5px blue, 0 0 5px blue",
      }}><i><p>Заметки</p></i></div>
      <div
      style={{
        display: "flex"
      }}>
        <textarea style={{
        borderColor: "yellow",
        borderWidth: 10,
        width: "500px",
        height: "700px",
        marginLeft: "200px"
      }}></textarea>
      <button style={{
      color: "white",
      backgroundColor: "yellow",
      fontSize: 70,
      borderWidth: 10,
      width: "200px",
      height: "400px",
      marginLeft: "200px",
      textShadow: "0 0 5px yellow, 0 0 5px yellow, 0 0 5px yellow, 0 0 5px yellow",
    }}>Принять</button>
      </div>
    </div>
  );
}

export default App;
