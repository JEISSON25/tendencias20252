import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { ArrowLeft, BarChart3, Download, TrendingUp, Package, Users, DollarSign } from "lucide-react";

export default function Reportes() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [estadisticas, setEstadisticas] = useState({
    totalVentas: 0,
    totalProductos: 0,
    stockBajo: 0,
    movimientosMes: 0
  });

  useEffect(() => {
    const cargarEstadisticas = async () => {
      try {
        const rol = localStorage.getItem("rol");
        if (rol !== "administrador") {
          navigate("/login");
          return;
        }

        // Usar la API para cargar datos reales
        const [ventasRes, productosRes, movimientosRes] = await Promise.all([
          api.get("/farmacia/facturasventa/"),
          api.get("/farmacia/productos/"),
          api.get("/farmacia/movimientos/")
        ]);

        const productos = productosRes.data;
        const stockBajo = productos.filter(p => p.low_stock).length;

        setEstadisticas({
          totalVentas: ventasRes.data.length,
          totalProductos: productos.length,
          stockBajo: stockBajo,
          movimientosMes: movimientosRes.data.length
        });

      } catch (error) {
        console.error("Error cargando reportes:", error);
        alert("Error al cargar los reportes");
      } finally {
        setLoading(false);
      }
    };

    cargarEstadisticas();
  }, [navigate]);

  const descargarReporte = async (tipo) => {
    try {
      let endpoint = "";
      let filename = "";

      switch(tipo) {
        case "productos":
          endpoint = "/farmacia/productos/all_pdf/";
          filename = "reporte_productos.pdf";
          break;
        case "movimientos":
          endpoint = "/farmacia/movimientos/all_pdf/";
          filename = "reporte_movimientos.pdf";
          break;
        case "ventas":
          endpoint = "/farmacia/detallesventa/all_pdf/";
          filename = "reporte_ventas.pdf";
          break;
        default:
          return;
      }

      const response = await api.get(endpoint, {
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      alert(`✅ Reporte ${tipo} descargado exitosamente`);
    } catch (error) {
      console.error("Error al descargar reporte:", error);
      alert("Error al generar el reporte PDF");
    }
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
    <div className="min-vh-100 py-5" style={{ background: "linear-gradient(135deg, #d0f0c0, #b2dfdb)" }}>
      <div className="container">
        {/* Header */}
        <div className="d-flex justify-content-between align-items-center mb-4">
          <button onClick={() => navigate(-1)} className="btn btn-outline-success">
            <ArrowLeft size={18} /> Volver
          </button>
          <h1 className="text-success fw-bold d-flex align-items-center">
            <BarChart3 size={30} className="me-2" /> Reportes y Estadísticas
          </h1>
        </div>

        {/* Estadísticas Rápidas */}
        <div className="row g-4 mb-5">
          <div className="col-md-3">
            <div className="card border-0 shadow-sm bg-white rounded-4">
              <div className="card-body text-center p-4">
                <div className="bg-success bg-opacity-10 rounded-circle p-3 d-inline-flex mb-3">
                  <DollarSign size={24} className="text-success" />
                </div>
                <h3 className="fw-bold text-success">{estadisticas.totalVentas}</h3>
                <p className="text-muted mb-0">Total Ventas</p>
              </div>
            </div>
          </div>
          
          <div className="col-md-3">
            <div className="card border-0 shadow-sm bg-white rounded-4">
              <div className="card-body text-center p-4">
                <div className="bg-primary bg-opacity-10 rounded-circle p-3 d-inline-flex mb-3">
                  <Package size={24} className="text-primary" />
                </div>
                <h3 className="fw-bold text-primary">{estadisticas.totalProductos}</h3>
                <p className="text-muted mb-0">Productos</p>
              </div>
            </div>
          </div>
          
          <div className="col-md-3">
            <div className="card border-0 shadow-sm bg-white rounded-4">
              <div className="card-body text-center p-4">
                <div className="bg-warning bg-opacity-10 rounded-circle p-3 d-inline-flex mb-3">
                  <TrendingUp size={24} className="text-warning" />
                </div>
                <h3 className="fw-bold text-warning">{estadisticas.stockBajo}</h3>
                <p className="text-muted mb-0">Stock Bajo</p>
              </div>
            </div>
          </div>
          
          <div className="col-md-3">
            <div className="card border-0 shadow-sm bg-white rounded-4">
              <div className="card-body text-center p-4">
                <div className="bg-info bg-opacity-10 rounded-circle p-3 d-inline-flex mb-3">
                  <Users size={24} className="text-info" />
                </div>
                <h3 className="fw-bold text-info">{estadisticas.movimientosMes}</h3>
                <p className="text-muted mb-0">Movimientos</p>
              </div>
            </div>
          </div>
        </div>

        {/* Reportes Disponibles */}
        <div className="card shadow-lg border-0 rounded-4">
          <div className="card-header bg-success text-white py-3">
            <h4 className="mb-0">Reportes Disponibles</h4>
          </div>
          <div className="card-body p-4">
            <div className="row g-4">
              
              {/* Reporte de Productos */}
              <div className="col-md-6">
                <div className="card border-0 shadow-sm h-100">
                  <div className="card-body text-center p-4">
                    <div className="bg-success text-white rounded-circle p-3 d-inline-flex mb-3">
                      <Package size={28} />
                    </div>
                    <h5 className="card-title fw-bold text-success">Reporte de Productos</h5>
                    <p className="card-text text-muted mb-3">
                      Lista completa de productos con stock y precios
                    </p>
                    <button
                      onClick={() => descargarReporte("productos")}
                      className="btn btn-success w-100 d-flex align-items-center justify-content-center gap-2"
                    >
                      <Download size={18} />
                      Descargar PDF
                    </button>
                  </div>
                </div>
              </div>

              {/* Reporte de Movimientos */}
              <div className="col-md-6">
                <div className="card border-0 shadow-sm h-100">
                  <div className="card-body text-center p-4">
                    <div className="bg-primary text-white rounded-circle p-3 d-inline-flex mb-3">
                      <TrendingUp size={28} />
                    </div>
                    <h5 className="card-title fw-bold text-primary">Reporte de Movimientos</h5>
                    <p className="card-text text-muted mb-3">
                      Historial completo de entradas y salidas
                    </p>
                    <button
                      onClick={() => descargarReporte("movimientos")}
                      className="btn btn-primary w-100 d-flex align-items-center justify-content-center gap-2"
                    >
                      <Download size={18} />
                      Descargar PDF
                    </button>
                  </div>
                </div>
              </div>

              {/* Reporte de Ventas */}
              <div className="col-md-6">
                <div className="card border-0 shadow-sm h-100">
                  <div className="card-body text-center p-4">
                    <div className="bg-warning text-white rounded-circle p-3 d-inline-flex mb-3">
                      <DollarSign size={28} />
                    </div>
                    <h5 className="card-title fw-bold text-warning">Reporte de Ventas</h5>
                    <p className="card-text text-muted mb-3">
                      Detalles de ventas y facturas del sistema
                    </p>
                    <button
                      onClick={() => descargarReporte("ventas")}
                      className="btn btn-warning text-white w-100 d-flex align-items-center justify-content-center gap-2"
                    >
                      <Download size={18} />
                      Descargar PDF
                    </button>
                  </div>
                </div>
              </div>

              {/* Próximamente */}
              <div className="col-md-6">
                <div className="card border-0 shadow-sm h-100">
                  <div className="card-body text-center p-4">
                    <div className="bg-secondary text-white rounded-circle p-3 d-inline-flex mb-3">
                      <BarChart3 size={28} />
                    </div>
                    <h5 className="card-title fw-bold text-secondary">Reportes Avanzados</h5>
                    <p className="card-text text-muted mb-3">
                      Gráficos y análisis detallados (Próximamente)
                    </p>
                    <button className="btn btn-secondary w-100" disabled>
                      En Desarrollo
                    </button>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
  );
}