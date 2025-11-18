// PerfilClienteCRUD.jsx - VERSIÓN MEJORADA CON DATOS REALES Y ESTILO PROFESIONAL
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { ArrowLeft, User, Mail, Phone, Edit, Save, X, Trash2, Shield, AlertCircle, CheckCircle, Info } from "lucide-react";

export default function PerfilClienteCRUD() {
  const navigate = useNavigate();
  const [perfil, setPerfil] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // Cargar perfil desde múltiples fuentes
  useEffect(() => {
    cargarPerfil();
  }, []);

  const cargarPerfil = async () => {
    try {
      const userData = JSON.parse(localStorage.getItem("user") || "{}");
      const userId = userData.id;

      if (!userId) {
        throw new Error("No se pudo obtener la información del usuario");
      }

      console.log("🔍 Cargando perfil para usuario:", userId);

      let perfilCargado = null;

      // ✅ ESTRATEGIA 1: Intentar cargar desde el backend
      try {
        // Cargar datos actualizados del usuario
        const usuarioRes = await api.get(`/api/auth/usuarios/${userId}/`);
        const usuarioData = usuarioRes.data;
        
        console.log("✅ Datos de usuario desde backend:", usuarioData);

        perfilCargado = {
          id: usuarioData.id,
          nombre: usuarioData.first_name || usuarioData.username || "No especificado",
          correo: usuarioData.email || "No especificado",
          telefono: usuarioData.telefono || "No especificado",
          username: usuarioData.username,
          fecha_registro: usuarioData.date_joined
        };

      } catch (backendError) {
        console.warn("⚠️ No se pudieron cargar datos del backend:", backendError);
        
        // ✅ ESTRATEGIA 2: Usar datos del localStorage como respaldo
        perfilCargado = {
          id: userData.id,
          nombre: userData.first_name || userData.username || "No especificado",
          correo: userData.email || "No especificado",
          telefono: userData.telefono || "No especificado",
          username: userData.username,
          fecha_registro: "No disponible"
        };
      }

      setPerfil(perfilCargado);
      setFormData({
        nombre: perfilCargado.nombre,
        correo: perfilCargado.correo,
        telefono: perfilCargado.telefono
      });

      console.log("✅ Perfil final cargado:", perfilCargado);

    } catch (error) {
      console.error("❌ Error al cargar perfil:", error);
      setError("No se pudo cargar la información del perfil");
    } finally {
      setLoading(false);
    }
  };

  // ✅ Función para actualizar datos en localStorage
  const actualizarLocalStorage = (nuevosDatos) => {
    try {
      const userData = JSON.parse(localStorage.getItem("user") || "{}");
      const datosActualizados = {
        ...userData,
        ...nuevosDatos
      };
      localStorage.setItem("user", JSON.stringify(datosActualizados));
      console.log("✅ localStorage actualizado:", datosActualizados);
    } catch (error) {
      console.error("Error actualizando localStorage:", error);
    }
  };

  // Guardar cambios con animación
  const guardarCambios = async () => {
    setSaving(true);
    setError("");
    setSuccess("");

    try {
      const userData = JSON.parse(localStorage.getItem("user") || "{}");
      const updateData = {
        first_name: formData.nombre,
        email: formData.correo,
        telefono: formData.telefono
      };

      // ✅ Actualizar en el backend
      try {
        await api.patch(`/api/auth/usuarios/${userData.id}/`, updateData);
        console.log("✅ Perfil actualizado en backend");
      } catch (backendError) {
        console.warn("⚠️ No se pudo actualizar en backend:", backendError);
        throw new Error("No se pudo conectar con el servidor para guardar los cambios");
      }

      // ✅ Actualizar en localStorage
      actualizarLocalStorage(updateData);

      // ✅ Actualizar estado local
      setPerfil({ ...perfil, ...formData });
      setEditMode(false);
      setSuccess("✅ Perfil actualizado exitosamente");

      // Limpiar mensaje de éxito después de 3 segundos
      setTimeout(() => setSuccess(""), 3000);

    } catch (error) {
      console.error("Error al actualizar:", error);
      setError(error.message || "❌ Error al actualizar el perfil");
    } finally {
      setSaving(false);
    }
  };

  // Cerrar sesión
  const cerrarSesion = () => {
    localStorage.clear();
    
    // Animación de despedida
    document.querySelector('.card')?.classList.add('fade-out');
    setTimeout(() => {
      navigate("/login");
    }, 500);
  };

  // Cancelar edición
  const cancelarEdicion = () => {
    setFormData({
      nombre: perfil.nombre,
      correo: perfil.correo,
      telefono: perfil.telefono
    });
    setEditMode(false);
    setError("");
    setSuccess("");
  };

  if (loading) {
    return (
      <div className="min-vh-100 d-flex justify-content-center align-items-center" 
           style={{ background: "linear-gradient(135deg, #d0f0c0, #b2dfdb)" }}>
        <div className="text-center">
          <div className="spinner-border text-success mb-3" role="status">
            <span className="visually-hidden">Cargando...</span>
          </div>
          <p className="text-success fw-semibold">Cargando tu perfil...</p>
        </div>
      </div>
    );
  }

  if (!perfil) {
    return (
      <div className="min-vh-100 d-flex justify-content-center align-items-center" 
           style={{ background: "linear-gradient(135deg, #d0f0c0, #b2dfdb)" }}>
        <div className="card shadow-lg border-0 rounded-4 text-center p-4" style={{ maxWidth: "500px" }}>
          <AlertCircle size={64} className="text-warning mb-3" />
          <h4 className="text-warning fw-bold mb-3">Error al cargar</h4>
          <p className="text-muted mb-4">{error || "No se pudo cargar el perfil"}</p>
          <button
            onClick={() => navigate("/cliente")}
            className="btn btn-success"
          >
            Volver al Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-vh-100 py-4" 
         style={{ background: "linear-gradient(135deg, #d0f0c0, #b2dfdb)" }}>
      <div className="container" style={{ maxWidth: "700px" }}>
        
        {/* Header con animación */}
        <div className="d-flex justify-content-between align-items-center mb-4 animate-slide-down">
          <button 
            onClick={() => navigate("/cliente")} 
            className="btn btn-outline-success d-flex align-items-center gap-2 shadow-sm hover-lift"
          >
            <ArrowLeft size={18} />
            Volver al Dashboard
          </button>
          
          {!editMode ? (
            <button 
              onClick={() => setEditMode(true)} 
              className="btn btn-success d-flex align-items-center gap-2 shadow-sm hover-lift pulse-on-hover"
            >
              <Edit size={18} />
              Editar Perfil
            </button>
          ) : (
            <div className="d-flex gap-2">
              <button 
                onClick={cancelarEdicion} 
                className="btn btn-outline-secondary d-flex align-items-center gap-2 shadow-sm hover-lift"
              >
                <X size={18} />
                Cancelar
              </button>
              <button 
                onClick={guardarCambios} 
                disabled={saving} 
                className="btn btn-success d-flex align-items-center gap-2 shadow-sm hover-lift"
              >
                {saving ? (
                  <>
                    <div className="spinner-border spinner-border-sm me-2" />
                    Guardando...
                  </>
                ) : (
                  <>
                    <Save size={18} />
                    Guardar Cambios
                  </>
                )}
              </button>
            </div>
          )}
        </div>

        {/* Mensajes de estado */}
        {success && (
          <div className="alert alert-success alert-dismissible fade show mb-4 d-flex align-items-center" role="alert">
            <CheckCircle size={20} className="me-2" />
            <span className="flex-grow-1">{success}</span>
            <button type="button" className="btn-close" onClick={() => setSuccess("")}></button>
          </div>
        )}

        {error && (
          <div className="alert alert-danger alert-dismissible fade show mb-4 d-flex align-items-center" role="alert">
            <AlertCircle size={20} className="me-2" />
            <span className="flex-grow-1">{error}</span>
            <button type="button" className="btn-close" onClick={() => setError("")}></button>
          </div>
        )}

        {/* Tarjeta principal con efectos */}
        <div className="card shadow-lg border-0 rounded-4 overflow-hidden hover-lift transition-all">
          <div className="bg-success text-white p-5 text-center position-relative overflow-hidden">
            <div className="position-absolute top-0 start-0 w-100 h-100 bg-white opacity-10 wave-animation"></div>
            <div className="position-relative">
              <div className="bg-white text-success rounded-circle mx-auto mb-3 d-flex align-items-center justify-content-center shadow-lg icon-bounce"
                   style={{ width: '80px', height: '80px' }}>
                <User size={36} />
              </div>
              <h3 className="fw-bold fs-4 mb-1">Mi Perfil</h3>
              <p className="opacity-90 mb-0">Gestiona tu información personal</p>
            </div>
          </div>

          <div className="card-body p-5">
            {/* Información del sistema */}
            <div className="alert alert-info mb-4 d-flex align-items-center">
              <Info size={20} className="me-2 flex-shrink-0" />
              <small>
                <strong>💡 Información:</strong> Los cambios se sincronizan con tu cuenta.
              </small>
            </div>

            <div className="space-y-4">
              {/* Campo Nombre */}
              <div className="d-flex align-items-center gap-3 p-3 rounded-3 bg-light hover-glow transition-all">
                <div className="bg-success text-white rounded-circle d-flex align-items-center justify-content-center shadow-sm flex-shrink-0"
                     style={{ width: '45px', height: '45px' }}>
                  <User size={20} />
                </div>
                <div className="flex-grow-1">
                  <small className="text-muted fw-semibold">Nombre completo</small>
                  {editMode ? (
                    <input
                      type="text"
                      className="form-control mt-1 border-success shadow-sm focus-glow"
                      value={formData.nombre}
                      onChange={(e) => setFormData({...formData, nombre: e.target.value})}
                      placeholder="Ingresa tu nombre completo"
                    />
                  ) : (
                    <p className="fw-bold text-dark mb-0 fs-5">{perfil.nombre}</p>
                  )}
                </div>
              </div>

              {/* Campo Email */}
              <div className="d-flex align-items-center gap-3 p-3 rounded-3 bg-light hover-glow transition-all">
                <div className="bg-success text-white rounded-circle d-flex align-items-center justify-content-center shadow-sm flex-shrink-0"
                     style={{ width: '45px', height: '45px' }}>
                  <Mail size={20} />
                </div>
                <div className="flex-grow-1">
                  <small className="text-muted fw-semibold">Correo electrónico</small>
                  {editMode ? (
                    <input
                      type="email"
                      className="form-control mt-1 border-success shadow-sm focus-glow"
                      value={formData.correo}
                      onChange={(e) => setFormData({...formData, correo: e.target.value})}
                      placeholder="Ingresa tu correo electrónico"
                    />
                  ) : (
                    <p className="fw-bold text-dark mb-0 fs-5">{perfil.correo}</p>
                  )}
                </div>
              </div>

              {/* Campo Teléfono */}
              <div className="d-flex align-items-center gap-3 p-3 rounded-3 bg-light hover-glow transition-all">
                <div className="bg-success text-white rounded-circle d-flex align-items-center justify-content-center shadow-sm flex-shrink-0"
                     style={{ width: '45px', height: '45px' }}>
                  <Phone size={20} />
                </div>
                <div className="flex-grow-1">
                  <small className="text-muted fw-semibold">Teléfono</small>
                  {editMode ? (
                    <input
                      type="text"
                      className="form-control mt-1 border-success shadow-sm focus-glow"
                      value={formData.telefono}
                      onChange={(e) => setFormData({...formData, telefono: e.target.value})}
                      placeholder="Ingresa tu número de teléfono"
                    />
                  ) : (
                    <p className="fw-bold text-dark mb-0 fs-5">{perfil.telefono}</p>
                  )}
                </div>
              </div>

              {/* Información adicional (solo lectura) */}
              {!editMode && (
                <>
                  <div className="d-flex align-items-center gap-3 p-3 rounded-3 bg-light">
                    <div className="bg-secondary text-white rounded-circle d-flex align-items-center justify-content-center shadow-sm flex-shrink-0"
                         style={{ width: '45px', height: '45px' }}>
                      <User size={20} />
                    </div>
                    <div className="flex-grow-1">
                      <small className="text-muted fw-semibold">Usuario</small>
                      <p className="fw-bold text-dark mb-0">{perfil.username}</p>
                    </div>
                  </div>
                </>
              )}
            </div>

            {/* Sección de acciones */}
            {!editMode && (
              <div className="text-center mt-5 pt-4 border-top">
                <button 
                  onClick={() => setShowDeleteConfirm(true)} 
                  className="btn btn-outline-danger d-flex align-items-center gap-2 mx-auto hover-shake"
                >
                  <Trash2 size={16} />
                  Cerrar Sesión
                </button>
                <small className="text-muted d-block mt-2">
                  Esta acción cerrará tu sesión actual
                </small>
              </div>
            )}
          </div>
        </div>

        {/* Modal de confirmación para cerrar sesión */}
        {showDeleteConfirm && (
          <div className="modal fade show d-block" style={{backgroundColor: 'rgba(0,0,0,0.5)'}}>
            <div className="modal-dialog modal-dialog-centered">
              <div className="modal-content border-0 shadow-lg rounded-4">
                <div className="modal-header bg-warning text-dark">
                  <h5 className="modal-title d-flex align-items-center gap-2">
                    <Shield size={20} />
                    Confirmar Cierre de Sesión
                  </h5>
                </div>
                <div className="modal-body text-center p-4">
                  <div className="text-warning mb-3">
                    <AlertCircle size={48} />
                  </div>
                  <h6 className="fw-bold">¿Estás seguro de cerrar tu sesión?</h6>
                  <p className="text-muted mb-0">
                    Serás redirigido al login y deberás iniciar sesión nuevamente para acceder.
                  </p>
                </div>
                <div className="modal-footer justify-content-center border-0">
                  <button 
                    onClick={() => setShowDeleteConfirm(false)} 
                    className="btn btn-outline-secondary px-4"
                  >
                    Cancelar
                  </button>
                  <button 
                    onClick={cerrarSesion} 
                    className="btn btn-warning px-4 d-flex align-items-center gap-2 text-white"
                  >
                    <Trash2 size={16} />
                    Sí, Cerrar Sesión
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Estilos CSS para animaciones */}
      <style jsx>{`
        .hover-lift:hover {
          transform: translateY(-2px);
          transition: all 0.3s ease;
        }
        
        .hover-glow:hover {
          box-shadow: 0 4px 15px rgba(40, 167, 69, 0.2);
        }
        
        .focus-glow:focus {
          box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.25);
          border-color: #28a745;
        }
        
        .pulse-on-hover:hover {
          animation: pulse 1s infinite;
        }
        
        .hover-shake:hover {
          animation: shake 0.5s;
        }
        
        .fade-out {
          animation: fadeOut 0.5s forwards;
        }
        
        .wave-animation {
          background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
          animation: wave 6s infinite linear;
        }
        
        .icon-bounce {
          animation: bounce 2s infinite;
        }
        
        .animate-slide-down {
           animation: slideDown 0.6s ease-out;
        }
        
        .transition-all {
          transition: all 0.3s ease;
        }
        
        @keyframes pulse {
          0% { transform: scale(1); }
          50% { transform: scale(1.05); }
          100% { transform: scale(1); }
        }
        
        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          25% { transform: translateX(-5px); }
          75% { transform: translateX(5px); }
        }
        
        @keyframes fadeOut {
          to { opacity: 0; transform: scale(0.95); }
        }
        
        @keyframes wave {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(100%); }
        }
        
        @keyframes bounce {
          0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
          40% { transform: translateY(-10px); }
          60% { transform: translateY(-5px); }
        }
        
        @keyframes slideDown {
          from { opacity: 0; transform: translateY(-20px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  );
}