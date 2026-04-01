import { useState } from "react";
import FileUpload from "./componets/FileUpload";
import Results from "./componets/Results";
import "./App.css";

import {
  convertPDF,
  nerAPI,
  sentimentAPI,
  langextractAPI,
  analyzePDF,
} from "./services/api";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const callAPI = async (apiFunc: any) => {
    if (!file) return alert("Upload a PDF first!");

    setLoading(true);
    try {
      const res = await apiFunc(file);
      setData(res);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>📊 Finance AI Analyzer</h1>

      <FileUpload onFileSelect={setFile} />

      {/* BUTTONS */}
      <div style={{ marginTop: "20px", display: "flex", gap: "10px", flexWrap: "wrap" }}>
        <button onClick={() => callAPI(convertPDF)}>Convert</button>
        <button onClick={() => callAPI(nerAPI)}>NER</button>
        <button onClick={() => callAPI(sentimentAPI)}>Sentiment</button>
        <button onClick={() => callAPI(langextractAPI)}>LangExtract</button>
        <button onClick={() => callAPI(analyzePDF)}>Analyze All</button>
      </div>

      {loading && <p>⏳ Processing...</p>}

      <Results data={data} />
    </div>
  );
}

export default App;