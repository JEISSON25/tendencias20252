// services/api.js - VERSIÓN CON MÁS DIAGNÓSTICO
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "https://prueba-de-despliegue-wyj1.onrender.com";

console.log("🔗 URL Base del Backend:", API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // ✅ Aumentado a 30 segundos
});

// Interceptor para requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    console.log(`🚀 Request: ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`, config.data);
    return config;
  },
  (error) => {
    console.error("❌ Error en request INTERCEPTOR:", error);
    return Promise.reject(error);
  }
);

// Interceptor para responses
api.interceptors.response.use(
  (response) => {
    console.log(`✅ Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error("❌ Error DETAILED en response:", {
      url: error.config?.url,
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      code: error.code,
      message: error.message,
      config: error.config
    });
    
    // ✅ Manejo específico para errores de CORS/red
    if (error.code === 'ECONNABORTED') {
      console.warn("⚠️ Timeout - El servidor puede estar iniciando");
      error.response = { data: { detail: "Timeout: El servidor no respondió a tiempo" } };
    }
    
    if (!error.response && error.message) {
      console.error("🔌 Error de red/CORS:", error.message);
      error.response = { data: { detail: `Error de conexión: ${error.message}` } };
    }
    
    return Promise.reject(error);
  }
);

export default api;