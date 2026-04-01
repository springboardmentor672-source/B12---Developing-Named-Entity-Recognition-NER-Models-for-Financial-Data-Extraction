import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const convertPDF = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);
  const res = await API.post("/convert-pdf", formData);
  return res.data;
};

export const nerAPI = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);
  const res = await API.post("/ner", formData);
  return res.data;
};

export const sentimentAPI = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);
  const res = await API.post("/sentiment", formData);
  return res.data;
};

export const langextractAPI = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);
  const res = await API.post("/langextract", formData);
  return res.data;
};

export const analyzePDF = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);
  const res = await API.post("/analyze-all", formData);
  return res.data;
};