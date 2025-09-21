import axios from "axios";

// Axios 인스턴스 생성
const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  withCredentials: false, // 파일 업로드에는 credentials 불필요
  headers: {
    "Content-Type": "application/json",
  },
});

// 요청 인터셉터 - FormData일 때 Content-Type 제거
axiosInstance.interceptors.request.use((config) => {
  if (config.data instanceof FormData) {
    delete config.headers["Content-Type"];
  }
  return config;
});

export default axiosInstance;
