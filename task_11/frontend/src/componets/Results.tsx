type Props = {
  data: any;
};

const Results = ({ data }: Props) => {
  if (!data) return null;

  return (
    <div style={{ marginTop: "30px" }}>
      <h2>📊 Analysis Results</h2>

      {/* ---------------- FILE INFO ---------------- */}
      <div style={cardStyle}>
        <h3>📄 File Info</h3>
        <p><b>Filename:</b> {data.filename}</p>
        <p><b>Status:</b> {data.status}</p>
      </div>

      {/* ---------------- NER ---------------- */}
      {data.ner && (
        <div style={cardStyle}>
          <h3>🏷 Named Entities</h3>
          <p>Total: {data.ner.total}</p>

          <table style={tableStyle}>
            <thead>
              <tr>
                <th>Text</th>
                <th>Type</th>
              </tr>
            </thead>
            <tbody>
              {data.ner.entities?.map((e: any, i: number) => (
                <tr key={i}>
                  <td>{e.word || e.text}</td>
                  <td>{e.entity_group || e.entity || e.type}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* ---------------- SENTIMENT ---------------- */}
      {data.sentiment && (
        <div style={cardStyle}>
          <h3>💬 Sentiment Analysis</h3>

          <p><b>Dominant:</b> {data.sentiment.summary?.dominant_sentiment}</p>
          <p><b>Total Sentences:</b> {data.sentiment.summary?.total_sentences}</p>

          <ul>
            {Object.entries(data.sentiment.summary?.counts || {}).map(
              ([key, value]: any) => (
                <li key={key}>
                  {key}: {value}
                </li>
              )
            )}
          </ul>
        </div>
      )}

      {/* ---------------- LANGEXTRACT ---------------- */}
      {data.langextract && (
        <div style={cardStyle}>
          <h3>💰 Financial Entities</h3>
          <p>Total: {data.langextract.total}</p>

          <table style={tableStyle}>
            <thead>
              <tr>
                <th>Text</th>
                <th>Type</th>
              </tr>
            </thead>
            <tbody>
              {data.langextract.entities?.map((e: any, i: number) => (
                <tr key={i}>
                  <td>{e.text}</td>
                  <td>{e.type}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Results;

/* ---------------- STYLES ---------------- */

const cardStyle = {
  border: "1px solid #ddd",
  borderRadius: "10px",
  padding: "20px",
  marginTop: "20px",
  boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
};

const tableStyle = {
  width: "100%",
  borderCollapse: "collapse" as const,
  marginTop: "10px",
};