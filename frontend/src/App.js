import { useState, useEffect, useRef } from 'react';

function App() {
  const videoRef = useRef(null);
  const [note, setNote] = useState('');
  const [showGif, setShowGif] = useState(false);
  const [stats, setStats] = useState({
    totalWords: 0,
    swearWords: 0,
    lettersTyped: 0,
    uselessClicks: 0,
  });

  const swearWords = ['хуй', 'пизда', 'еблан', 'бля', 'сука', 'пиздец', 'нах', 'гондон', 'хуесос', 'ебал'];

  const cursorStyle = {
    cursor: 'url("data:image/x-icon;base64,AAACAAEAICAAAAAAAACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAABAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADAAAABgAAAAgAAAAGAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwAAAAwAAAAVAAAAHAAAABUAAAAMAAAAAwAAAAAAAAAAAAAAAAAA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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABYajP9tcvP/bXLz/21y8/8WGoz/Zsz//0Rzt/8AAAAfAAAADAAAAAMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFhqM/21y8/8ABXr/bXLz/xYajP9Ec7f/AAAAHwAAAAwAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWGoz/AAV6/21y8/9tcvP/FhqM/wAAABUAAAAMAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWGoz/FhqM/xYajP8AAAAIAAAABgAAAAMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//////////////////////////////////////////////////////////////////////////////////////8f///+D////g////4P////Af///gD///wA///4AP//8BH//+A////Af///gP///wH///8D////B////4////8="), auto'
  };

  useEffect(() => {
    const words = note.split(/\s+/).filter(word => word.length > 0);
    const swearCount = words.filter(word => 
      swearWords.some(swear => word.toLowerCase().includes(swear)))
    .length;

    setStats({
      totalWords: words.length,
      swearWords: swearCount,
      lettersTyped: note.length,
      uselessClicks: stats.uselessClicks,
    });
  }, [note]);

  const sendNote = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/офигетькакойкрутойэндпоинтвсенанемработает', {
        method: "DELETE",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "something": "pizdez" }),
      });
      const json = await response.json();
      return json;
    } catch (e) {
      console.error("Ошибка? Ну анлак, иди поплачь.");
    } finally {
      setStats(prev => ({
        ...prev,
        uselessClicks: prev.uselessClicks + 1,
      }));
    }
  };

  const uselessGif = showGif ? (
    <img 
      src="https://media1.tenor.com/m/MiHWwXIS7S0AAAAC/dota2day.gif" 
      style={{
        position: 'absolute',
        top: '50%',
        left: '10%',
        width: '300px',
        height: '300px',
        transform: 'rotate(15deg)',
        border: '10px dashed red',
        zIndex: 9999,
      }} 
      alt="Бесполезная гифка"
    />
  ) : null;

  const mirrorStats = (
    <div style={{
      position: 'absolute',
      top: '20px',
      right: '20px',
      width: '300px',
      height: '200px',
      backgroundColor: 'rgba(0, 0, 0, 0.7)',
      color: 'lime',
      fontFamily: 'Courier New',
      padding: '10px',
      transform: 'scaleX(-1)',
      border: '5px dotted yellow',
      overflow: 'hidden',
      zIndex: 1,
    }}>
      <h3 style={{ 
        textAlign: 'center', 
        margin: '0 0 10px 0',
        textDecoration: 'underline wavy red',
      }}>
        СТАТИСТИКА
      </h3>
      <p>Всего слов: {stats.totalWords}</p>
      <p>Матерных: {stats.swearWords}</p>
      <p>Символов: {stats.lettersTyped}</p>
      <p>Бесполезных кликов: {stats.uselessClicks}</p>
      <p style={{ 
        fontSize: '10px',
        color: 'cyan',
        marginTop: '10px',
      }}>
        Данные обновляются в реальном времени (но никому не нужны)
      </p>
    </div>
  );

  return (
    <div style={{
      height: '100vh',
      overflow: 'hidden',
      position: 'relative',
    }}>
      {/* YouTube видео как фон */}
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        zIndex: -1,
        overflow: 'hidden'
      }}>
        <iframe
          ref={videoRef}
          width="100%"
          height="100%"
          src="https://www.youtube.com/embed/sIrCv3TDwqw?autoplay=1&mute=1&controls=0&loop=1&playlist=sIrCv3TDwqw"
          title="YouTube video player"
          frameBorder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
          style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            minWidth: '100%',
            minHeight: '100%',
            width: 'auto',
            height: 'auto'
          }}
        ></iframe>
      </div>

      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        backgroundColor: 'rgba(0,0,0,0.5)',
        zIndex: -1
      }}></div>


      <div style={{
        position: 'relative',
        zIndex: 1,
        height: '100%',
        ...cursorStyle,
      }}>

        <div style={{
          fontSize: "100px",
          color: "yellow",
          marginLeft: "253px",
          textShadow: "0 0 5px blue, 0 0 5px blue, 0 0 5px blue, 0 0 5px blue",
          fontFamily: "Comic Sans MS",
          transform: 'skewX(-15deg)',
          paddingTop: '20px',
        }}>
          <i><p>Заметки</p></i>
        </div>

        <div style={{ display: "flex" }}>
          <textarea 
            style={{
              borderColor: "yellow",
              borderWidth: 10,
              width: "500px",
              height: "700px",
              marginLeft: "200px",
              backgroundColor: 'rgba(255, 255, 0, 0.2)',
              fontFamily: 'Wingdings',
              fontSize: '24px',
            }}
            onChange={(e) => setNote(e.target.value)}
          />
          
          <button 
            style={{
              color: "white",
              backgroundColor: "yellow",
              fontSize: 70,
              borderWidth: 10,
              width: "200px",
              height: "400px",
              marginLeft: "200px",
              textShadow: "0 0 5px yellow, 0 0 5px yellow, 0 0 5px yellow, 0 0 5px yellow",
            }}
            onClick={() => {
              sendNote();
              setShowGif(!showGif);
            }}
          >
            Принять
          </button>
        </div>

        {uselessGif}
        {mirrorStats}

      </div>
    </div>
  );
}

export default App;