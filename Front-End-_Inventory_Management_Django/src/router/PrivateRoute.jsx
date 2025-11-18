// router/PrivateRoute.jsx - VERSIÓN MEJORADA CON REDIRECCIÓN FORZADA
import { Navigate } from "react-router-dom";

const PrivateRoute = ({ children, rolPermitido }) => {
  const token = localStorage.getItem("access");
  const rol = localStorage.getItem("rol")?.toLowerCase()?.trim();

  console.log("🔐 PrivateRoute - Verificación detallada:", {
    token: !!token,
    rolUsuario: `"${rol}"`,
    rolRequerido: rolPermitido,
    pathActual: window.location.pathname
  });

  // Si no hay token, redirigir a login
  if (!token) {
    console.log("❌ No hay token, redirigiendo a login");
    return <Navigate to="/login" replace />;
  }

  // Verificar expiración del token
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const exp = payload.exp * 1000;
    
    if (Date.now() >= exp) {
      console.log("❌ Token expirado");
      localStorage.clear();
      return <Navigate to="/login" replace />;
    }
  } catch (error) {
    console.error("Error verificando token:", error);
    localStorage.clear();
    return <Navigate to="/login" replace />;
  }

  // Si no hay rol, redirigir a login
  if (!rol) {
    console.log("❌ No hay rol definido en localStorage");
    localStorage.clear();
    return <Navigate to="/login" replace />;
  }

  // Convertir rolPermitido a array para facilitar la verificación
  const rolesPermitidos = Array.isArray(rolPermitido) 
    ? rolPermitido 
    : [rolPermitido];
  
  // Verificar si el rol del usuario está permitido
  const tienePermiso = rolesPermitidos.some(r => r.toLowerCase() === rol);
  
  console.log("📊 Resultado verificación de permisos:", {
    rolesPermitidos,
    rolUsuario: rol,
    tienePermiso
  });

  if (!tienePermiso) {
    console.log("🚫 Acceso denegado - Redirigiendo según rol del usuario");
    
    // FORZAR REDIRECCIÓN SEGÚN ROL - ESTO ES CLAVE
    if (rol === "administrador") {
      console.log("🔄 FORZANDO redirección de administrador a /admin");
      return <Navigate to="/admin" replace />;
    } else if (rol === "empleado") {
      console.log("🔄 FORZANDO redirección de empleado a /empleado");
      return <Navigate to="/empleado" replace />;
    } else if (rol === "cliente") {
      console.log("🔄 FORZANDO redirección de cliente a /cliente");
      return <Navigate to="/cliente" replace />;
    } else {
      console.log("🔄 Rol desconocido, redirigiendo a login");
      localStorage.clear();
      return <Navigate to="/login" replace />;
    }
  }

  console.log("✅ Acceso permitido a:", window.location.pathname);
  return children;
};

export default PrivateRoute;