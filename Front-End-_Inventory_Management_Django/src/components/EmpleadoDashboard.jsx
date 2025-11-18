// EmpleadoDashboard.jsx - VERSIÓN OPTIMIZADA
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  Package,
  TrendingUp,
  LogOut,
  ClipboardList,
  BarChart3,
  ShoppingBag,
  User
} from "lucide-react";
import api from "../services/api";

export default function EmpleadoDashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    totalProductos: 0,
    stockBajo: 0,
    ventasHoy: 0,
    movimientosHoy: 0,
  });
  const [userName, setUserName] = useState("Empleado");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const cargarDatosDashboard = async () => {
      try {
        setLoading(true);
        setError(null);

        // Verificar autenticación y obtener datos del usuario
        const token = localStorage.getItem("access");
        const rol = localStorage.getItem("rol")?.toLowerCase();
        const userStorage = localStorage.getItem("user");

        if (!token || rol !== "empleado") {
          console.log("❌ No autenticado como empleado, redirigiendo...");
          navigate("/login");
          return;
        }

        // ✅ Obtener información del usuario desde localStorage
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

        // ✅ Cargar estadísticas con endpoints corregidos
        let productos = [];
        let ventas = [];
        let movimientos = [];

        try {
          console.log("📦 Cargando productos...");
          const productosRes = await api.get("/farmacia/productos/");
          productos = productosRes.data;
          console.log("✅ Productos cargados:", productos.length);
        } catch (error) {
          console.error("❌ Error cargando productos:", error);
          setError("No se pudieron cargar los productos");
        }

        try {
          console.log("🛒 Cargando ventas...");
          const ventasRes = await api.get("/farmacia/facturasventa/");
          ventas = ventasRes.data;
          console.log("✅ Ventas cargadas:", ventas.length);
        } catch (error) {
          console.error("❌ Error cargando ventas:", error);
        }

        try {
          console.log("📋 Cargando movimientos...");
          const movimientosRes = await api.get("/farmacia/movimientos/");
          movimientos = movimientosRes.data;
          console.log("✅ Movimientos cargados:", movimientos.length);
        } catch (error) {
          console.error("❌ Error cargando movimientos:", error);
        }

        const hoy = new Date().toISOString().split("T")[0];

        // Filtrar ventas del día
        const ventasHoy = Array.isArray(ventas) 
          ? ventas.filter((v) => {
              const fechaVenta = v.fecha || v.fecha_creacion || v.created_at;
              return fechaVenta && fechaVenta.startsWith(hoy);
            }).length 
          : 0;

        // Filtrar movimientos del día
        const movimientosHoy = Array.isArray(movimientos)
          ? movimientos.filter((m) => {
              const fechaMov = m.fecha || m.fecha_creacion || m.created_at;
              return fechaMov && fechaMov.startsWith(hoy);
            }).length
          : 0;

        // Contar productos con stock bajo
        const stockBajo = Array.isArray(productos)
          ? productos.filter((p) => p.stock !== undefined && p.stock < 10).length
          : 0;

        setStats({
          totalProductos: Array.isArray(productos) ? productos.length : 0,
          stockBajo,
          ventasHoy,
          movimientosHoy,
        });

      } catch (error) {
        console.error("❌ Error general cargando dashboard:", error);
        setError("Error al cargar los datos del dashboard");
        
        if (error.response?.status === 401 || error.response?.status === 403) {
          localStorage.clear();
          navigate("/login");
        }
      } finally {
        setLoading(false);
      }
    };

    cargarDatosDashboard();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  const handleNavegarRegistrarVenta = () => {
    console.log("🔄 Navegando a /registrar-venta");
    navigate("/registrar-venta");
  };

  if (loading) {
    return (
      <div
        className="d-flex justify-content-center align-items-center vh-100"
        style={{ background: "linear-gradient(135deg, #d0f0c0, #b2dfdb)" }}
      >
        <div
          className="spinner-border text-success"
          style={{ width: "3rem", height: "3rem" }}
        >
          <span className="visually-hidden">Cargando...</span>
        </div>
      </div>
    );
  }

  return (
    <div
      className="min-vh-100"
      style={{ background: "linear-gradient(135deg, #d0f0c0, #b2dfdb)" }}
    >
      {/* Navbar Mejorada con Información del Usuario */}
      <nav className="navbar navbar-dark bg-success shadow-lg">
        <div className="container-fluid">
          <span className="navbar-brand fw-bold fs-4">
            💊 Farmacia Salud+ 
          </span>
          
          <div className="d-flex align-items-center">
            {/* Información del Usuario */}
            <div className="text-white me-3 text-end">
              <div className="fw-bold d-flex align-items-center">
                <User size={16} className="me-1" />
                {userName}
              </div>
              <small className="opacity-75">Empleado</small>
            </div>
            
            <button onClick={handleLogout} className="btn btn-outline-light btn-sm">
              <LogOut size={16} /> Cerrar Sesión
            </button>
          </div>
        </div>
      </nav>

      {/* Contenido Principal */}
      <div className="container py-4">
        {/* Mensaje de error */}
        {error && (
          <div className="alert alert-warning alert-dismissible fade show" role="alert">
            <strong>Advertencia:</strong> {error}
            <button 
              type="button" 
              className="btn-close" 
              onClick={() => setError(null)}
            ></button>
          </div>
        )}

        {/* Bienvenida Personalizada */}
        <div className="text-center mb-4">
          <h2 className="text-success fw-bold">¡Bienvenido, {userName}! 👋</h2>
          <p className="text-muted">Panel de control - Módulo de Empleado</p>
        </div>

        {/* Resto del código permanece igual... */}
        {/* Estadísticas */}
        <div className="row g-4 mb-5">
          <div className="col-md-3">
            <div className="card border-0 shadow-sm h-100 bg-white rounded-4">
              <div className="card-body text-center p-4">
                <Package size={40} className="text-primary mb-3" />
                <h3 className="fw-bold text-primary">{stats.totalProductos}</h3>
                <p className="text-muted mb-0">Productos Totales</p>
              </div>
            </div>
          </div>

          <div className="col-md-3">
            <div className="card border-0 shadow-sm h-100 bg-white rounded-4">
              <div className="card-body text-center p-4">
                <TrendingUp size={40} className="text-warning mb-3" />
                <h3 className="fw-bold text-warning">{stats.stockBajo}</h3>
                <p className="text-muted mb-0">Stock Bajo</p>
              </div>
            </div>
          </div>

          <div className="col-md-3">
            <div className="card border-0 shadow-sm h-100 bg-white rounded-4">
              <div className="card-body text-center p-4">
                <ShoppingBag size={40} className="text-success mb-3" />
                <h3 className="fw-bold text-success">{stats.ventasHoy}</h3>
                <p className="text-muted mb-0">Ventas Hoy</p>
              </div>
            </div>
          </div>

          <div className="col-md-3">
            <div className="card border-0 shadow-sm h-100 bg-white rounded-4">
              <div className="card-body text-center p-4">
                <ClipboardList size={40} className="text-info mb-3" />
                <h3 className="fw-bold text-info">{stats.movimientosHoy}</h3>
                <p className="text-muted mb-0">Movimientos Hoy</p>
              </div>
            </div>
          </div>
        </div>

        {/* Módulos del Empleado */}
        <div className="row g-4">
          {/* Registrar Venta */}
          <div className="col-md-6 col-lg-4">
            <div className="card border-0 shadow hover-lift h-100 rounded-4">
              <div className="card-body p-4 text-center">
                <div className="bg-primary text-white rounded-circle p-3 d-inline-flex mb-3">
                  <ShoppingBag size={32} />
                </div>
                <h5 className="fw-bold text-primary">Registrar Venta</h5>
                <p className="text-muted mb-4">
                  Crear nueva venta con múltiples productos
                </p>
                <button
                  onClick={handleNavegarRegistrarVenta}
                  className="btn btn-primary w-100 fw-semibold"
                >
                  Ir a Ventas
                </button>
              </div>
            </div>
          </div>

          {/* Consultar Productos */}
          <div className="col-md-6 col-lg-4">
            <div className="card border-0 shadow hover-lift h-100 rounded-4">
              <div className="card-body p-4 text-center">
                <div className="bg-success text-white rounded-circle p-3 d-inline-flex mb-3">
                  <Package size={32} />
                </div>
                <h5 className="fw-bold text-success">Consultar Productos</h5>
                <p className="text-muted mb-4">
                  Ver stock actual y detalles de productos
                </p>
                <button
                  onClick={() => navigate("/empleado/productos")}
                  className="btn btn-success w-100 fw-semibold"
                >
                  Ver Productos
                </button>
              </div>
            </div>
          </div>

          {/* Registrar Salida */}
          <div className="col-md-6 col-lg-4">
            <div className="card border-0 shadow hover-lift h-100 rounded-4">
              <div className="card-body p-4 text-center">
                <div className="bg-warning text-white rounded-circle p-3 d-inline-flex mb-3">
                  <TrendingUp size={32} />
                </div>
                <h5 className="fw-bold text-warning">Registrar Salida</h5>
                <p className="text-muted mb-4">
                  Registrar salida de productos del inventario
                </p>
                <button
                  onClick={() => navigate("/empleado/registrar-salida")}
                  className="btn btn-warning text-white w-100 fw-semibold"
                >
                  Registrar Salida
                </button>
              </div>
            </div>
          </div>

          {/* Mis Ventas */}
          <div className="col-md-6 col-lg-4">
            <div className="card border-0 shadow hover-lift h-100 rounded-4">
              <div className="card-body p-4 text-center">
                <div className="bg-info text-white rounded-circle p-3 d-inline-flex mb-3">
                  <BarChart3 size={32} />
                </div>
                <h5 className="fw-bold text-info">Mis Ventas</h5>
                <p className="text-muted mb-4">
                  Historial personal de ventas registradas
                </p>
                <button
                  onClick={() => navigate("/mis-ventas")}
                  className="btn btn-info text-white w-100 fw-semibold"
                >
                  Ver Mis Ventas
                </button>
              </div>
            </div>
          </div>

          {/* Movimientos */}
          <div className="col-md-6 col-lg-4">
            <div className="card border-0 shadow hover-lift h-100 rounded-4">
              <div className="card-body p-4 text-center">
                <div className="bg-secondary text-white rounded-circle p-3 d-inline-flex mb-3">
                  <ClipboardList size={32} />
                </div>
                <h5 className="fw-bold text-secondary">Movimientos</h5>
                <p className="text-muted mb-4">
                  Ver entradas y salidas de inventario
                </p>
                <button
                  onClick={() => navigate("/empleado/movimientos")}
                  className="btn btn-secondary text-white w-100 fw-semibold"
                >
                  Ver Movimientos
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}