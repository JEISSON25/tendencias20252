// components/Login.jsx - VERSIÓN CORREGIDA SIN ERRORES
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../services/api";

export default function Login() {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      console.log("🔐 Iniciando sesión...", { username: formData.username });

      // ✅ 1. Autenticación con el backend
      const authResponse = await api.post("/api/token/", {
        username: formData.username,
        password: formData.password
      });

      console.log("✅ Login exitoso, respuesta:", authResponse.data);

      const { access, refresh } = authResponse.data;

      if (!access) {
        throw new Error("No se recibió token de acceso");
      }

      // ✅ 2. Obtener información del usuario autenticado usando el token
      const userResponse = await api.get("/api/auth/usuarios/", {
        headers: { Authorization: `Bearer ${access}` }
      });

      console.log("👤 Usuarios disponibles:", userResponse.data);

      // ✅ 3. Encontrar el usuario actual por username
      const currentUser = userResponse.data.find(
        user => user.username === formData.username
      );

      if (!currentUser) {
        throw new Error("No se pudo encontrar la información del usuario");
      }

      console.log("🎯 Usuario autenticado:", currentUser);

      // ✅ 4. ESTRATEGIA NUEVA: Determinar el tipo de usuario por funcionalidad
      const userType = await determineUserType(currentUser, access);
      
      // ✅ 5. Guardar datos en localStorage
      const userData = {
        id: currentUser.id,
        username: currentUser.username,
        email: currentUser.email,
        telefono: currentUser.telefono,
        rol: userType,
        rol_id: currentUser.rol
      };

      localStorage.setItem("access", access);
      localStorage.setItem("refresh", refresh || "");
      localStorage.setItem("user", JSON.stringify(userData));
      localStorage.setItem("rol", userType);
      localStorage.setItem("username", currentUser.username);
      localStorage.setItem("user_id", currentUser.id);

      console.log("💾 Datos guardados:", userData);

      // ✅ 6. Redirigir según el tipo de usuario determinado
      redirectUser(userType);

    } catch (error) {
      console.error("❌ Error en login:", error);
      handleLoginError(error);
    } finally {
      setLoading(false);
    }
  };

  // ✅ NUEVA ESTRATEGIA: Determinar tipo de usuario por funcionalidad
  const determineUserType = async (user, accessToken) => {
    try {
      console.log("🔍 Determinando tipo de usuario para:", user.username);

      // ✅ ESTRATEGIA 1: Verificar si tiene perfil de cliente
      try {
        const clientesRes = await api.get("/farmacia/clientes/", {
          headers: { Authorization: `Bearer ${accessToken}` }
        });
        
        const clienteData = clientesRes.data.find(cliente => cliente.usuario === user.id);
        if (clienteData) {
          console.log("✅ Usuario identificado como: cliente");
          return "cliente";
        }
      } catch (error) {
        console.warn("⚠️ No se pudo verificar perfil de cliente:", error);
      }

      // ✅ ESTRATEGIA 2: Verificar si tiene perfil de empleado
      try {
        const empleadosRes = await api.get("/farmacia/empleados/", {
          headers: { Authorization: `Bearer ${accessToken}` }
        });
        
        const empleadoData = empleadosRes.data.find(empleado => empleado.usuario === user.id);
        if (empleadoData) {
          console.log("✅ Usuario identificado como: empleado");
          return "empleado";
        }
      } catch (error) {
        console.warn("⚠️ No se pudo verificar perfil de empleado:", error);
      }

      // ✅ ESTRATEGIA 3: Verificar si tiene perfil de proveedor
      try {
        const proveedoresRes = await api.get("/farmacia/proveedores/", {
          headers: { Authorization: `Bearer ${accessToken}` }
        });
        
        const proveedorData = proveedoresRes.data.find(proveedor => proveedor.usuario === user.id);
        if (proveedorData) {
          console.log("✅ Usuario identificado como: proveedor");
          return "proveedor";
        }
      } catch (error) {
        console.warn("⚠️ No se pudo verificar perfil de proveedor:", error);
      }

      // ✅ ESTRATEGIA 4: Verificar si es administrador por permisos
      try {
        // Intentar acceder a endpoint de administración (sin guardar en variable)
        await api.get("/farmacia/categorias/", {
          headers: { Authorization: `Bearer ${accessToken}` }
        });
        
        // Si puede acceder a categorías (solo admin/empleado), verificar más permisos
        const usuariosRes = await api.get("/api/auth/usuarios/", {
          headers: { Authorization: `Bearer ${accessToken}` }
        });
        
        // Si puede ver todos los usuarios, probablemente es admin
        if (usuariosRes.data && usuariosRes.data.length > 0) {
          console.log("✅ Usuario identificado como: administrador");
          return "administrador";
        }
      } catch (error) {
        console.warn("⚠️ No se pudo verificar permisos de administrador:", error);
      }

      // ✅ ESTRATEGIA 5: Usar rol del usuario si está disponible
      if (user.rol) {
        console.log("🎯 Usando rol del usuario:", user.rol);
        // Si el usuario tiene rol, intentar obtener el nombre
        try {
          const rolesRes = await api.get("/api/auth/roles/", {
            headers: { Authorization: `Bearer ${accessToken}` }
          });
          const role = rolesRes.data.find(r => r.id === user.rol);
          if (role) {
            return role.name.toLowerCase();
          }
        } catch (error) {
          console.warn("⚠️ No se pudieron cargar los roles:", error);
        }
      }

      // ✅ ESTRATEGIA 6: Por defecto, asumir que es cliente
      console.log("🔧 Usuario sin rol específico, asignando como: cliente");
      return "cliente";

    } catch (error) {
      console.error("❌ Error determinando tipo de usuario:", error);
      
      // ✅ ESTRATEGIA DE RESPUESTA: Asignar como cliente por defecto
      console.log("🔄 Asignando tipo de usuario por defecto: cliente");
      return "cliente";
    }
  };

  // ✅ Función de redirección optimizada
  const redirectUser = (userType) => {
    const normalizedType = userType.toLowerCase().trim();
    
    console.log(`🔄 Redirigiendo usuario tipo: ${normalizedType}`);

    const redirectPaths = {
      administrador: "/admin",
      empleado: "/empleado",
      cliente: "/cliente",
      proveedor: "/proveedor"
    };

    const path = redirectPaths[normalizedType];
    
    if (path) {
      console.log(`📍 Navegando a: ${path}`);
      navigate(path, { replace: true });
    } else {
      console.warn(`⚠️ Tipo de usuario no reconocido: ${normalizedType}`);
      // Por defecto, redirigir a cliente
      console.log("🔄 Redirigiendo por defecto a: /cliente");
      navigate("/cliente", { replace: true });
    }
  };

  // ✅ Manejo mejorado de errores
  const handleLoginError = (error) => {
    // Limpiar datos de sesión en caso de error
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("user");
    localStorage.removeItem("rol");
    
    if (error.response) {
      const { status, data } = error.response;
      
      switch (status) {
        case 401:
          setError("❌ Usuario o contraseña incorrectos");
          break;
        case 400:
          setError("📝 Datos de login inválidos. Verifique el formato.");
          break;
        case 403:
          setError("🚫 Acceso denegado. No tiene permisos para acceder.");
          break;
        case 500:
          setError("⚙️ Error interno del servidor. Intente más tarde.");
          break;
        default:
          setError(`⚠️ Error ${status}: ${data.detail || 'Error de autenticación'}`);
      }
    } 
    else if (error.code === 'ECONNABORTED') {
      setError("⏰ El servidor no responde. Verifique su conexión.");
    }
    else if (error.message.includes('Network Error')) {
      setError("🌐 Error de conexión. Verifique su internet y que el servidor esté activo.");
    }
    else {
      setError(`🚨 ${error.message || "Error inesperado durante el login"}`);
    }
  };

  // ✅ Función para acceso rápido en desarrollo
  const quickLogin = (username, password) => {
    setFormData({ username, password });
    // Auto-submit después de un breve delay
    setTimeout(() => {
      const submitEvent = new Event('submit', { cancelable: true });
      document.querySelector('form').dispatchEvent(submitEvent);
    }, 100);
  };

  return (
    <div className="min-vh-100 d-flex align-items-center justify-content-center" 
         style={{ background: "linear-gradient(135deg, #d0f0c0, #b2dfdb)" }}>
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-6 col-lg-5">
            
            {/* Tarjeta Principal */}
            <div className="card border-0 shadow-lg rounded-4 overflow-hidden">
              <div className="card-body p-0">
                
                {/* Header con Gradiente */}
                <div className="bg-success text-white text-center py-4">
                  <div className="bg-white bg-opacity-20 rounded-circle p-3 d-inline-flex mb-3">
                    <span className="fs-1">💊</span>
                  </div>
                  <h2 className="fw-bold mb-1">Farmacia Salud+</h2>
                  <p className="mb-0 opacity-75">Sistema de Gestión Integral</p>
                </div>

                {/* Contenido del Formulario */}
                <div className="p-4">
                  {/* Quick Login para desarrollo */}
                  {import.meta.env.DEV && (
                    <div className="mb-3">
                      <small className="text-muted d-block mb-2">🔧 Acceso Rápido (Desarrollo):</small>
                      <div className="d-flex gap-2 flex-wrap">
                        <button 
                          className="btn btn-outline-success btn-sm"
                          onClick={() => quickLogin("admin45", "password123")}
                        >
                          👑 Admin
                        </button>
                        <button 
                          className="btn btn-outline-primary btn-sm"
                          onClick={() => quickLogin("empleado25", "password123")}
                        >
                          👨‍💼 Empleado
                        </button>
                        <button 
                          className="btn btn-outline-warning btn-sm"
                          onClick={() => quickLogin("cliente25", "password123")}
                        >
                          👤 Cliente
                        </button>
                        <button 
                          className="btn btn-outline-info btn-sm"
                          onClick={() => quickLogin("proveedor23", "password123")}
                        >
                          🚚 Proveedor
                        </button>
                      </div>
                    </div>
                  )}

                  {/* Mensaje de Error */}
                  {error && (
                    <div className="alert alert-warning alert-dismissible fade show mb-3" role="alert">
                      <div className="d-flex align-items-center">
                        <span className="flex-grow-1">{error}</span>
                        <button 
                          type="button" 
                          className="btn-close btn-close-sm ms-2" 
                          onClick={() => setError("")}
                        ></button>
                      </div>
                    </div>
                  )}

                  {/* Formulario */}
                  <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                      <label className="form-label text-success fw-semibold">
                        👤 Usuario
                      </label>
                      <input
                        type="text"
                        className="form-control form-control-lg border-success"
                        name="username"
                        value={formData.username}
                        onChange={handleChange}
                        placeholder="Ingrese su usuario"
                        required
                        disabled={loading}
                        autoComplete="username"
                      />
                    </div>

                    <div className="mb-4">
                      <label className="form-label text-success fw-semibold">
                        🔒 Contraseña
                      </label>
                      <input
                        type="password"
                        className="form-control form-control-lg border-success"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        placeholder="Ingrese su contraseña"
                        required
                        disabled={loading}
                        autoComplete="current-password"
                      />
                    </div>

                    <button
                      type="submit"
                      className="btn btn-success btn-lg w-100 fw-bold py-3 shadow-sm"
                      disabled={loading}
                    >
                      {loading ? (
                        <>
                          <span className="spinner-border spinner-border-sm me-2" />
                          Verificando...
                        </>
                      ) : (
                        "🚀 Iniciar Sesión"
                      )}
                    </button>
                  </form>

                  {/* Enlaces Adicionales */}
                  <div className="text-center mt-4">
                    <p className="text-muted mb-2">
                      ¿No tienes una cuenta?
                    </p>
                    <Link 
                      to="/register" 
                      className="text-success text-decoration-none fw-bold"
                    >
                      📝 Regístrate aquí
                    </Link>
                  </div>

                  {/* Info del Sistema */}
                  <div className="mt-4 p-3 bg-light rounded">
                    <small className="text-muted d-block">
                      <strong>🔗 Servidor:</strong> {api.defaults.baseURL}
                    </small>
                    <small className="text-muted">
                      <strong>🎯 Sistema:</strong> Detección automática de permisos
                    </small>
                  </div>
                </div>
              </div>
            </div>

            {/* Footer */}
            <div className="text-center mt-4">
              <small className="text-muted">
                © 2025 Farmacia Salud+. Sistema adaptativo de permisos.
              </small>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}