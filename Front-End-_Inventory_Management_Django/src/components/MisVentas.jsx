// components/MisVentas.jsx - VERSIÓN CORREGIDA
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import {
  ArrowLeft,
  ShoppingCart,
  Download,
  Search,
  Calendar,
} from "lucide-react";

export default function MisVentas() {
  const navigate = useNavigate();
  const [ventas, setVentas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [filterDate, setFilterDate] = useState("");

  useEffect(() => {
    const cargarVentas = async () => {
      try {
        // Obtener ID del empleado actual
        const token = localStorage.getItem("access");
        let empleadoId = null;

        if (token) {
          const payload = JSON.parse(atob(token.split(".")[1]));
          const empleadosRes = await api.get("/farmacia/empleados/");
          const empleado = empleadosRes.data.find(
            (emp) => emp.usuario === payload.user_id
          );
          empleadoId = empleado?.id;
        }

        // Cargar todas las ventas y filtrar por empleado
        const response = await api.get("/farmacia/facturasventa/");
        let ventasFiltradas = response.data;

        if (empleadoId) {
          ventasFiltradas = ventasFiltradas.filter(
            (v) => v.id_empleado === empleadoId
          );
        }

        console.log("📦 Ventas cargadas:", ventasFiltradas);
        setVentas(ventasFiltradas);
      } catch (error) {
        console.error("❌ Error cargando ventas:", error);
        alert("Error al cargar las ventas");
      } finally {
        setLoading(false);
      }
    };

    cargarVentas();
  }, []);

  // CORRECCIÓN: Ahora SÍ usamos ventasFiltradas en el render
  const ventasFiltradas = ventas.filter((venta) => {
    const matchesSearch =
      venta.id_cliente?.nombre
        ?.toLowerCase()
        .includes(searchTerm.toLowerCase()) ||
      venta.id.toString().includes(searchTerm);

    const matchesDate = !filterDate || venta.fecha === filterDate;

    return matchesSearch && matchesDate;
  });

  const descargarPDF = async () => {
    try {
      // Aquí puedes implementar la descarga de PDF si el backend lo soporta
      alert("Funcionalidad de descarga PDF en desarrollo");
    } catch (error) {
      console.error("Error al descargar PDF:", error);
      alert("Error al descargar el PDF");
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
    <div className="min-vh-100" style={{ background: "linear-gradient(135deg, #d0f0c0, #b2dfdb)" }}>
      <div className="container py-4">
        {/* Header */}
        <div className="d-flex justify-content-between align-items-center mb-4">
          <button
            onClick={() => navigate("/empleado")}
            className="btn btn-outline-success"
          >
            <ArrowLeft size={18} /> Volver al Dashboard
          </button>
          <h1 className="text-success d-flex align-items-center">
            <ShoppingCart className="me-2" /> Mis Ventas
          </h1>
          <button 
            onClick={descargarPDF} 
            className="btn btn-outline-success"
          >
            <Download size={18} /> Descargar PDF
          </button>
        </div>

        {/* Filtros y Búsqueda */}
        <div className="card shadow-sm border-0 mb-4">
          <div className="card-body">
            <div className="row g-3">
              <div className="col-md-6">
                <div className="input-group">
                  <span className="input-group-text bg-light">
                    <Search size={16} />
                  </span>
                  <input
                    type="text"
                    className="form-control"
                    placeholder="Buscar por cliente o ID de factura..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
              </div>
              <div className="col-md-4">
                <div className="input-group">
                  <span className="input-group-text bg-light">
                    <Calendar size={16} />
                  </span>
                  <input
                    type="date"
                    className="form-control"
                    value={filterDate}
                    onChange={(e) => setFilterDate(e.target.value)}
                  />
                </div>
              </div>
              <div className="col-md-2 text-center">
                <span className="badge bg-success fs-6">
                  {ventasFiltradas.length} ventas
                </span>
              </div>
            </div>
            {(searchTerm || filterDate) && (
              <div className="mt-2">
                <small className="text-muted">
                  Filtros activos: 
                  {searchTerm && ` Cliente/ID: "${searchTerm}"`}
                  {filterDate && ` Fecha: ${filterDate}`}
                  <button 
                    className="btn btn-sm btn-outline-secondary ms-2"
                    onClick={() => {
                      setSearchTerm("");
                      setFilterDate("");
                    }}
                  >
                    Limpiar filtros
                  </button>
                </small>
              </div>
            )}
          </div>
        </div>

        {/* Tabla de Ventas */}
        <div className="card shadow-lg border-0">
          <div className="card-header bg-success text-white py-3">
            <h4 className="mb-0">Historial de Ventas</h4>
          </div>
          <div className="card-body">
            {ventasFiltradas.length === 0 ? (
              <div className="text-center py-5">
                <ShoppingCart size={64} className="text-muted mb-3" />
                <h5 className="text-muted">
                  {ventas.length === 0 ? "No hay ventas registradas" : "No hay ventas que coincidan con los filtros"}
                </h5>
                <p className="text-muted">
                  {ventas.length === 0 
                    ? "Las ventas que registres aparecerán aquí" 
                    : "Intenta con otros términos de búsqueda"}
                </p>
                {(searchTerm || filterDate) && ventas.length > 0 && (
                  <button 
                    className="btn btn-success"
                    onClick={() => {
                      setSearchTerm("");
                      setFilterDate("");
                    }}
                  >
                    Mostrar todas las ventas
                  </button>
                )}
              </div>
            ) : (
              <div className="table-responsive">
                <table className="table table-striped table-hover">
                  <thead className="table-success">
                    <tr>
                      <th>ID Factura</th>
                      <th>Fecha</th>
                      <th>Cliente</th>
                      <th>Total</th>
                      <th>Estado</th>
                    </tr>
                  </thead>
                  <tbody>
                    {ventasFiltradas.map((venta) => (
                      <tr key={venta.id}>
                        <td className="fw-bold">#{venta.id}</td>
                        <td>
                          <div className="d-flex align-items-center">
                            <Calendar size={14} className="text-muted me-1" />
                            {new Date(venta.fecha).toLocaleDateString('es-ES')}
                          </div>
                        </td>
                        <td>{venta.id_cliente?.nombre || "Cliente general"}</td>
                        <td className="fw-bold text-success">
                          ${parseFloat(venta.total || 0).toFixed(2)}
                        </td>
                        <td>
                          <span className="badge bg-success">Completada</span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>

        {/* Resumen Estadístico */}
        {ventasFiltradas.length > 0 && (
          <div className="row mt-4">
            <div className="col-md-4">
              <div className="card border-0 bg-success text-white">
                <div className="card-body text-center">
                  <h4 className="fw-bold">{ventasFiltradas.length}</h4>
                  <p className="mb-0">Ventas Totales</p>
                </div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="card border-0 bg-warning text-white">
                <div className="card-body text-center">
                  <h4 className="fw-bold">
                    ${ventasFiltradas.reduce((sum, venta) => sum + parseFloat(venta.total || 0), 0).toFixed(2)}
                  </h4>
                  <p className="mb-0">Ingresos Totales</p>
                </div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="card border-0 bg-info text-white">
                <div className="card-body text-center">
                  <h4 className="fw-bold">
                    {new Set(ventasFiltradas.map(v => v.id_cliente?.id)).size}
                  </h4>
                  <p className="mb-0">Clientes Únicos</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}