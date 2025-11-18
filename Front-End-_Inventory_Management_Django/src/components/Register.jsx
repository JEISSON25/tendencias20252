// components/Register.jsx - VERSIÓN SIN DEPENDENCIA DE ROLES PREEXISTENTES
import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../services/api";

export default function Register() {
  const [formData, setFormData] = useState({
    first_name: "",
    email: "",
    telefono: "",
    username: "",
    password: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    if (error || success) {
      setError("");
      setSuccess("");
    }
  }, [formData]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");

    // ✅ Validación básica
    if (formData.password.length < 8) {
      setError("La contraseña debe tener al menos 8 caracteres");
      setLoading(false);
      return;
    }

    if (!formData.email.includes('@')) {
      setError("Ingrese un correo electrónico válido");
      setLoading(false);
      return;
    }

    try {
      console.log("📝 Iniciando registro sin rol predefinido...");

      // ✅ ESTRATEGIA: Crear usuario SIN rol primero
      const userData = {
        username: formData.username,
        password: formData.password,
        email: formData.email,
        telefono: formData.telefono,
        first_name: formData.first_name,
        last_name: "", // Campo requerido pero vacío
        // ❌ NO INCLUIR EL CAMPO 'rol' - dejar que el backend lo asigne por defecto
      };

      console.log("👤 Creando usuario sin rol:", userData);

      // ✅ CREAR USUARIO SIN ESPECIFICAR ROL
      const userResponse = await api.post("/api/auth/usuarios/", userData);
      
      console.log("✅ Usuario creado exitosamente:", userResponse.data);

      // ✅ Si el backend no asigna rol automáticamente, usar estrategia alternativa
      // En este caso, asumimos que el backend asignará un rol por defecto o 
      // que el usuario se creará sin rol y luego se podrá asignar manualmente

      // ✅ ÉXITO - Redirigir automáticamente
      setSuccess("🎉 ¡Cuenta creada exitosamente! Serás redirigido al login...");
      
      // Limpiar formulario
      setFormData({
        first_name: "",
        email: "",
        telefono: "",
        username: "",
        password: "",
      });

      // ✅ Redirigir después de 3 segundos
      setTimeout(() => {
        navigate("/login", { replace: true });
      }, 3000);

    } catch (error) {
      console.error("❌ Error en registro:", error);
      handleRegisterError(error);
    } finally {
      setLoading(false);
    }
  };

  const handleRegisterError = (error) => {
    console.log("🔍 Analizando error de registro:", error.response?.data);
    
    if (error.response?.data) {
      const data = error.response.data;
      
      // ✅ Manejo específico de errores comunes
      if (data.username) {
        setError(`❌ El usuario "${formData.username}" ya existe`);
      } else if (data.email) {
        setError(`❌ El correo "${formData.email}" ya está registrado`);
      } else if (data.telefono) {
        setError(`❌ El teléfono "${formData.telefono}" ya está en uso`);
      } else if (data.password) {
        setError(`❌ Contraseña: ${Array.isArray(data.password) ? data.password[0] : data.password}`);
      } else if (data.rol) {
        // ✅ Error específico de rol - intentar sin rol
        setError("❌ Error de configuración del sistema. Contacta al administrador.");
      } else if (data.detail) {
        setError(`❌ ${data.detail}`);
      } else {
        // Mostrar el primer error disponible
        const firstError = Object.values(data)[0];
        setError(`❌ ${Array.isArray(firstError) ? firstError[0] : firstError}`);
      }
    } 
    else if (error.code === 'ECONNABORTED') {
      setError("⏰ El servidor no responde. Intenta nuevamente.");
    }
    else if (error.message?.includes('Network Error')) {
      setError("🌐 Error de conexión. Verifica tu internet.");
    }
    else {
      setError(`🚨 Error: ${error.message || "Error inesperado"}`);
    }
  };

  // ✅ Función alternativa: probar crear usuario sin rol
  const testRegisterWithoutRole = async () => {
    try {
      setLoading(true);
      const testData = {
        username: `testuser_${Date.now()}`,
        password: "testpass123",
        email: `test${Date.now()}@example.com`,
        telefono: "3000000000",
        first_name: "Test User",
        last_name: "",
        // Sin campo 'rol'
      };
      
      const response = await api.post("/api/auth/usuarios/", testData);
      console.log("🧪 Test sin rol exitoso:", response.data);
      setSuccess("✅ Registro funciona sin especificar rol");
    } catch (err) {
      console.error("🧪 Test sin rol falló:", err);
      if (err.response?.data?.rol) {
        setError("❌ El sistema requiere que se especifique un rol válido");
      } else {
        setError(`❌ Test falló: ${err.response?.data?.detail || err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-vh-100 d-flex align-items-center justify-content-center" 
         style={{ background: "linear-gradient(135deg, #d0f0c0, #b2dfdb)" }}>
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-6 col-lg-5">
            
            <div className="card border-0 shadow-lg rounded-4 overflow-hidden">
              <div className="card-body p-0">
                
                <div className="bg-success text-white text-center py-4">
                  <div className="bg-white bg-opacity-20 rounded-circle p-3 d-inline-flex mb-3">
                    <span className="fs-1">👤</span>
                  </div>
                  <h2 className="fw-bold mb-1">Farmacia Salud+</h2>
                  <p className="mb-0 opacity-75">Registro de Cliente</p>
                </div>

                <div className="p-4">
                  {/* Botón de prueba para desarrollo */}
                  {import.meta.env.DEV && (
                    <div className="mb-3 text-center">
                      <button 
                        className="btn btn-outline-info btn-sm"
                        onClick={testRegisterWithoutRole}
                        disabled={loading}
                      >
                        🧪 Probar Registro Sin Rol
                      </button>
                    </div>
                  )}

                  {success && (
                    <div className="alert alert-success alert-dismissible fade show mb-3" role="alert">
                      <div className="d-flex align-items-center">
                        <span className="flex-grow-1">{success}</span>
                      </div>
                    </div>
                  )}

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

                  <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                      <label className="form-label text-success fw-semibold">
                        👤 Nombre Completo
                      </label>
                      <input
                        type="text"
                        className="form-control form-control-lg border-success"
                        name="first_name"
                        value={formData.first_name}
                        onChange={handleChange}
                        placeholder="Ej: Juan Pérez"
                        required
                        disabled={loading}
                      />
                    </div>

                    <div className="mb-3">
                      <label className="form-label text-success fw-semibold">
                        📧 Correo Electrónico
                      </label>
                      <input
                        type="email"
                        className="form-control form-control-lg border-success"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        placeholder="Ej: juan@ejemplo.com"
                        required
                        disabled={loading}
                      />
                    </div>

                    <div className="mb-3">
                      <label className="form-label text-success fw-semibold">
                        📞 Teléfono
                      </label>
                      <input
                        type="text"
                        className="form-control form-control-lg border-success"
                        name="telefono"
                        value={formData.telefono}
                        onChange={handleChange}
                        placeholder="Ej: 3001234567"
                        required
                        disabled={loading}
                      />
                    </div>

                    <div className="mb-3">
                      <label className="form-label text-success fw-semibold">
                        🆔 Usuario
                      </label>
                      <input
                        type="text"
                        className="form-control form-control-lg border-success"
                        name="username"
                        value={formData.username}
                        onChange={handleChange}
                        placeholder="Ej: juanperez"
                        required
                        disabled={loading}
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
                        placeholder="Mínimo 8 caracteres"
                        required
                        disabled={loading}
                        minLength="8"
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
                          Creando cuenta...
                        </>
                      ) : (
                        "🚀 Crear Cuenta"
                      )}
                    </button>
                  </form>

                  <div className="text-center mt-4">
                    <p className="text-muted mb-2">
                      ¿Ya tienes una cuenta?
                    </p>
                    <Link 
                      to="/login" 
                      className="text-success text-decoration-none fw-bold"
                    >
                      🔑 Iniciar Sesión
                    </Link>
                  </div>

                  {/* Información importante */}
                  <div className="mt-4 p-3 bg-light rounded text-center">
                    <small className="text-success fw-bold d-block">
                      ⚠️ Sistema de Registro
                    </small>
                    <small className="text-muted">
                      Tu cuenta se creará y el administrador asignará los permisos correspondientes
                    </small>
                  </div>
                </div>
              </div>
            </div>

            <div className="text-center mt-4">
              <small className="text-muted">
                © 2025 Farmacia Salud+. Sistema de registro optimizado.
              </small>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}