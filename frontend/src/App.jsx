import { useState } from "react";

export default function App() {
  const [brewMethod, setBrewMethod] = useState("drip");
  const [roastLevel, setRoastLevel] = useState("medium");
  const [result, setResult] = useState(null);

  const handleRecommend = async () => {
    // 실제로는 API 호출
    setResult({
      flavor: "밸런스 좋은 산미와 초콜릿 향",
      bean: "에티오피아 예가체프",
      reason: "중배전 + 드립 추출에서 꽃향과 과일 산미가 잘 살아남",
    });
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>☕ 초기 구동 버전 음하하하하하하하하하 가보자고 해보자고</h1>
      <p style={styles.subtitle}>
        추출 조건에 맞는 원두와 맛을 추천해드립니다
        
      </p>

      <div style={styles.card}>
        <label>추출 방식</label>
        <select value={brewMethod} onChange={(e) => setBrewMethod(e.target.value)}>
          <option value="drip">드립</option>
          <option value="espresso">에스프레소</option>
          <option value="french">프렌치프레스</option>
        </select>

        <label>로스팅 정도</label>
        <select value={roastLevel} onChange={(e) => setRoastLevel(e.target.value)}>
          <option value="light">라이트</option>
          <option value="medium">미디엄</option>
          <option value="dark">다크</option>
        </select>

        <button onClick={handleRecommend} style={styles.button}>
          추천 받기
        </button>
      </div>

      {result && (
        <div style={styles.result}>
          <h3>추천 결과</h3>
          <p><strong>원두:</strong> {result.bean}</p>
          <p><strong>맛:</strong> {result.flavor}</p>
          <p style={{ color: "#666" }}>{result.reason}</p>
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: 500,
    margin: "2rem auto",
    fontFamily: "Arial, sans-serif",
  },
  title: {
    textAlign: "center",
  },
  subtitle: {
    textAlign: "center",
    color: "#666",
  },
  card: {
    display: "flex",
    flexDirection: "column",
    gap: "0.5rem",
    padding: "1rem",
    border: "1px solid #ddd",
    borderRadius: "8px",
  },
  button: {
    marginTop: "1rem",
    padding: "0.5rem",
    background: "#6f4e37",
    color: "white",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
  },
  result: {
    marginTop: "1.5rem",
    padding: "1rem",
    background: "#fafafa",
    borderRadius: "8px",
    border: "1px solid #eee",
  },
};
