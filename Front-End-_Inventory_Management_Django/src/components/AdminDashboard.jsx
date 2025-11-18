import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Package, Users, TrendingUp, LogOut, BarChart3, ShoppingCart, User } from "lucide-react";
import "bootstrap/dist/css/bootstrap.min.css";

export default function AdminDashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    totalProductos: 0,
    totalVentas: 0,
    stockBajo: 0,
    totalMovimientos: 0
  });
  const [userName, setUserName] = useState("Administrador");
  const [loading, setLoading] = useState(true);

  // Función para verificar permisos y cargar datos del usuario
  const verificarPermisosYCargarUsuario = () => {
    const rol = localStorage.getItem("rol")?.trim().toLowerCase();
    const userStorage = localStorage.getItem("user");
    
    console.log("🔐 Verificando permisos - Rol:", rol);
    
    if (rol !== "administrador") {
      console.log("❌ Rol no autorizado, redirigiendo a login");
      navigate("/login");
      return false;
    }

    // ✅ Cargar información del usuario administrador
    if (userStorage) {
      try {
        const userParsed = JSON.parse(userStorage);
        
        // Establecer nombre para mostrar
        if (userParsed.nombre) {
          setUserName(userParsed.nombre);
        } else if (userParsed.username) {
          // Capitalizar el username para mejor presentación
          const formattedName = userParsed.username
            .split('.')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
          setUserName(formattedName);
        }
      } catch (parseError) {
        console.error("Error parseando user data:", parseError);
      }
    }

    return true;
  };

  useEffect(() => {
    const cargarEstadisticas = async () => {
      // Verificar permisos antes de cargar datos
      if (!verificarPermisosYCargarUsuario()) return;

      try {
        const token = localStorage.getItem("access");

        // Cargar estadísticas en paralelo
        const [productosRes, ventasRes, movimientosRes] = await Promise.all([
          fetch(
            "https://prueba-de-despliegue-wyj1.onrender.com/farmacia/productos/",
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          ),
          fetch(
            "https://prueba-de-despliegue-wyj1.onrender.com/farmacia/facturasventa/",
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          ),
          fetch(
            "https://prueba-de-despliegue-wyj1.onrender.com/farmacia/movimientos/",
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          ),
        ]);

        // Verificar respuestas
        if (!productosRes.ok) throw new Error("Error al cargar productos");
        if (!ventasRes.ok) throw new Error("Error al cargar ventas");
        if (!movimientosRes.ok) throw new Error("Error al cargar movimientos");

        const productos = await productosRes.json();
        const ventas = await ventasRes.json();
        const movimientos = await movimientosRes.json();

        const stockBajo = productos.filter((p) => p.stock < 10).length;

        setStats({
          totalProductos: productos.length,
          totalVentas: ventas.length,
          stockBajo: stockBajo,
          totalMovimientos: movimientos.length,
        });
      } catch (error) {
        console.error("Error cargando estadísticas:", error);
        // En caso de error, redirigir a login
        localStorage.clear();
        navigate("/login");
      } finally {
        setLoading(false);
      }
    };

    cargarEstadisticas();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center vh-100" 
           style={{ background: "linear-gradient(135deg, #d0f0c0, #b2dfdb)" }}>
        <div className="spinner-border text-success" role="status">
          <span className="visually-hidden">Cargando...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-vh-100" style={{ background: "linear-gradient(135deg, #d0f0c0, #b2dfdb)" }}>
      {/* Navbar Mejorada con Información del Usuario */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-success shadow-sm">
        <div className="container">
          <span className="navbar-brand fw-bold fs-4 d-flex align-items-center">
            💊 Farmacia Salud+
          </span>
          
          <div className="d-flex align-items-center">
            {/* Información del Usuario Administrador */}
            <div className="text-white me-3 text-end">
              <div className="fw-bold d-flex align-items-center">
                <User size={16} className="me-1" />
                {userName}
              </div>
              <small className="opacity-75">Administrador</small>
            </div>
            
            <button onClick={handleLogout} className="btn btn-outline-light btn-sm">
              <LogOut size={16} className="me-1" />
              Cerrar sesión
            </button>
          </div>
        </div>
      </nav>

      {/* Contenido Principal */}
      <div className="container py-5">
        
        {/* Header con Bienvenida Personalizada */}
        <div className="text-center mb-5">
          <h1 className="fw-bold text-success mb-3">Panel de Administración</h1>
          <p className="text-muted fs-5">
            ¡Bienvenido, {userName}! 👋 - Gestión integral del sistema
          </p>
        </div>

        {/* Estadísticas Rápidas */}
        <div className="row g-4 mb-5">
          <div className="col-md-3">
            <div className="card border-0 shadow-sm hover-lift bg-white rounded-4">
              <div className="card-body text-center p-4">
                <div className="bg-success bg-opacity-10 rounded-circle p-3 d-inline-flex mb-3">
                  <Package size={24} className="text-success" />
                </div>
                <h3 className="fw-bold text-success">{stats.totalProductos}</h3>
                <p className="text-muted mb-0">Productos</p>
              </div>
            </div>
          </div>
          
          <div className="col-md-3">
            <div className="card border-0 shadow-sm hover-lift bg-white rounded-4">
              <div className="card-body text-center p-4">
                <div className="bg-primary bg-opacity-10 rounded-circle p-3 d-inline-flex mb-3">
                  <ShoppingCart size={24} className="text-primary" />
                </div>
                <h3 className="fw-bold text-primary">{stats.totalVentas}</h3>
                <p className="text-muted mb-0">Ventas</p>
              </div>
            </div>
          </div>
          
          <div className="col-md-3">
            <div className="card border-0 shadow-sm hover-lift bg-white rounded-4">
              <div className="card-body text-center p-4">
                <div className="bg-warning bg-opacity-10 rounded-circle p-3 d-inline-flex mb-3">
                  <TrendingUp size={24} className="text-warning" />
                </div>
                <h3 className="fw-bold text-warning">{stats.stockBajo}</h3>
                <p className="text-muted mb-0">Stock Bajo</p>
              </div>
            </div>
          </div>
          
          <div className="col-md-3">
            <div className="card border-0 shadow-sm hover-lift bg-white rounded-4">
              <div className="card-body text-center p-4">
                <div className="bg-info bg-opacity-10 rounded-circle p-3 d-inline-flex mb-3">
                  <BarChart3 size={24} className="text-info" />
                </div>
                <h3 className="fw-bold text-info">{stats.totalMovimientos}</h3>
                <p className="text-muted mb-0">Movimientos</p>
              </div>
            </div>
          </div>
        </div>

        {/* Módulos Principales */}
        <div className="row g-4">
          {/* Gestión de Productos */}
          <div className="col-md-6 col-lg-4">
            <div className="card border-0 shadow-sm hover-lift h-100 rounded-4">
              <div className="card-body p-4 text-center">
                <div className="bg-success text-white rounded-circle p-3 d-inline-flex mb-3">
                  <Package size={28} />
                </div>
                <h5 className="card-title fw-bold text-success">Gestión de Productos</h5>
                <p className="card-text text-muted mb-3">
                  Administra productos, categorías y control de stock
                </p>
                <button
                  onClick={() => navigate("/admin/productos")}
                  className="btn btn-success w-100 fw-semibold"
                >
                  Gestionar Productos
                </button>
              </div>
            </div>
          </div>

          {/* Gestión de Movimientos */}
          <div className="col-md-6 col-lg-4">
            <div className="card border-0 shadow-sm hover-lift h-100 rounded-4">
              <div className="card-body p-4 text-center">
                <div className="bg-primary text-white rounded-circle p-3 d-inline-flex mb-3">
                  <TrendingUp size={28} />
                </div>
                <h5 className="card-title fw-bold text-primary">Movimientos</h5>
                <p className="card-text text-muted mb-3">
                  Registra entradas, salidas y control de inventario
                </p>
                <button
                  onClick={() => navigate("/admin/movimientos")}
                  className="btn btn-primary w-100 fw-semibold"
                >
                  Ver Movimientos
                </button>
              </div>
            </div>
          </div>

          {/* Gestión de Usuarios */}
          <div className="col-md-6 col-lg-4">
            <div className="card border-0 shadow-sm hover-lift h-100 rounded-4">
              <div className="card-body p-4 text-center">
                <div className="bg-warning text-white rounded-circle p-3 d-inline-flex mb-3">
                  <Users size={28} />
                </div>
                <h5 className="card-title fw-bold text-warning">Usuarios</h5>
                <p className="card-text text-muted mb-3">
                  Gestiona empleados, clientes y permisos del sistema
                </p>
                <button
                  onClick={() => navigate("/usuarios")}
                  className="btn btn-warning text-white w-100 fw-semibold"
                >
                  Gestionar Usuarios
                </button>
              </div>
            </div>
          </div>

          {/* Reportes y Análisis */}
          <div className="col-md-6 col-lg-4">
            <div className="card border-0 shadow-sm hover-lift h-100 rounded-4">
              <div className="card-body p-4 text-center">
                <div className="bg-secondary text-white rounded-circle p-3 d-inline-flex mb-3">
                  <BarChart3 size={28} />
                </div>
                <h5 className="card-title fw-bold text-secondary">Reportes</h5>
                <p className="card-text text-muted mb-3">
                  Genera reportes de ventas, inventario y estadísticas
                </p>
                <button
                  onClick={() => navigate("/reportes")}
                  className="btn btn-secondary w-100 fw-semibold"
                >
                  Ver Reportes
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-success text-white text-center py-3 mt-5">
        <small>© 2025 Farmacia Salud+. Sistema de Gestión de Inventario</small>
      </footer>

      <style jsx>{`
        .hover-lift {
          transition: all 0.3s ease;
        }
        .hover-lift:hover {
          transform: translateY(-5px);
          box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important;
        }
      `}</style>
    </div>
  );
}