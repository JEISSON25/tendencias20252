// src/components/ConsultarProductos.jsx - VERSIÓN PARA EMPLEADO
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  Package,
  ArrowLeft,
  Download,
  Search,
  AlertTriangle,
  BarChart3
} from "lucide-react";
import api from "../services/api";

export default function ConsultarProductos() {
  const navigate = useNavigate();
  const [productos, setProductos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [filterCategoria, setFilterCategoria] = useState("");
  const [filterStock, setFilterStock] = useState("");
  const [stats, setStats] = useState({
    total: 0,
    stockBajo: 0,
    sinStock: 0,
    disponible: 0
  });

  useEffect(() => {
    cargarProductos();
  }, []);

  const cargarProductos = async () => {
    try {
      const response = await api.get("/farmacia/productos/");
      setProductos(response.data);
      calcularEstadisticas(response.data);
    } catch (error) {
      console.error("Error cargando productos:", error);
      alert("Error al cargar productos");
    } finally {
      setLoading(false);
    }
  };

  const calcularEstadisticas = (productosData) => {
    const total = productosData.length;
    const stockBajo = productosData.filter(p => p.stock < 10 && p.stock > 0).length;
    const sinStock = productosData.filter(p => p.stock === 0).length;
    const disponible = productosData.filter(p => p.stock >= 10).length;

    setStats({ total, stockBajo, sinStock, disponible });
  };

  const descargarPDF = async () => {
    try {
      const response = await api.get("/farmacia/productos/all_pdf/", {
        responseType: "blob",
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "inventario_productos.pdf");
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error("Error al descargar PDF:", error);
      alert("Error al descargar el PDF");
    }
  };

  const productosFiltrados = productos.filter((producto) => {
    const nombreProducto = producto.nombre?.toLowerCase() || "";
    const nombreCategoria = producto.id_categoria?.nombre?.toLowerCase() || "";
    const terminoBusqueda = searchTerm.toLowerCase();

    const matchesSearch =
      nombreProducto.includes(terminoBusqueda) ||
      nombreCategoria.includes(terminoBusqueda);

    const matchesCategoria =
      !filterCategoria || producto.id_categoria?.nombre === filterCategoria;

    const matchesStock =
      !filterStock ||
      (filterStock === "bajo"
        ? (producto.stock || 0) < 10 && (producto.stock || 0) > 0
        : filterStock === "sin"
        ? (producto.stock || 0) === 0
        : filterStock === "disponible"
        ? (producto.stock || 0) >= 10
        : true);

    return matchesSearch && matchesCategoria && matchesStock;
  });

  const categoriasUnicas = [
    ...new Set(productos.map((p) => p.id_categoria?.nombre).filter(Boolean)),
  ];

  // Determinar a dónde volver según el rol
  const getBackPath = () => {
    const rol = localStorage.getItem("rol");
    return rol === "administrador" ? "/admin" : "/empleado";
  };

  if (loading) {
    return (
      <div
        className="d-flex justify-content-center align-items-center vh-100"
        style={{ background: "linear-gradient(135deg, #d0f0c0, #b2dfdb)" }}
      >
        <div className="spinner-border text-success" role="status">
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
      <div className="container py-4">
        {/* Header */}
        <div className="d-flex justify-content-between align-items-center mb-4">
          <button
            onClick={() => navigate(getBackPath())}
            className="btn btn-outline-success"
          >
            <ArrowLeft size={18} /> Volver al Dashboard
          </button>
          <h1 className="text-success d-flex align-items-center">
            <Package className="me-2" /> Consulta de Productos
          </h1>
          <button onClick={descargarPDF} className="btn btn-success">
            <Download size={18} /> Descargar PDF
          </button>
        </div>

        {/* Tarjetas de Estadísticas */}
        <div className="row mb-4">
          <div className="col-md-3">
            <div className="card bg-success text-white shadow-sm border-0">
              <div className="card-body text-center py-3">
                <BarChart3 size={24} className="mb-2" />
                <h4 className="mb-1">{stats.total}</h4>
                <small>Total Productos</small>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card bg-warning text-dark shadow-sm border-0">
              <div className="card-body text-center py-3">
                <AlertTriangle size={24} className="mb-2" />
                <h4 className="mb-1">{stats.stockBajo}</h4>
                <small>Stock Bajo</small>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card bg-danger text-white shadow-sm border-0">
              <div className="card-body text-center py-3">
                <Package size={24} className="mb-2" />
                <h4 className="mb-1">{stats.sinStock}</h4>
                <small>Sin Stock</small>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card bg-primary text-white shadow-sm border-0">
              <div className="card-body text-center py-3">
                <Package size={24} className="mb-2" />
                <h4 className="mb-1">{stats.disponible}</h4>
                <small>Disponible</small>
              </div>
            </div>
          </div>
        </div>

        {/* Filtros Mejorados */}
        <div className="card shadow-sm border-0 mb-4">
          <div className="card-body">
            <div className="row g-3">
              <div className="col-md-4">
                <div className="input-group">
                  <span className="input-group-text bg-success text-white">
                    <Search size={16} />
                  </span>
                  <input
                    type="text"
                    className="form-control border-success"
                    placeholder="Buscar productos o categorías..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
              </div>
              <div className="col-md-3">
                <select
                  className="form-select border-success"
                  value={filterCategoria}
                  onChange={(e) => setFilterCategoria(e.target.value)}
                >
                  <option value="">Todas las categorías</option>
                  {categoriasUnicas.map((cat) => (
                    <option key={cat} value={cat}>
                      {cat}
                    </option>
                  ))}
                </select>
              </div>
              <div className="col-md-3">
                <select
                  className="form-select border-success"
                  value={filterStock}
                  onChange={(e) => setFilterStock(e.target.value)}
                >
                  <option value="">Todo el stock</option>
                  <option value="disponible">Stock Disponible</option>
                  <option value="bajo">Stock Bajo</option>
                  <option value="sin">Sin Stock</option>
                </select>
              </div>
              <div className="col-md-2 text-center">
                <span className="badge bg-success fs-6 p-2">
                  {productosFiltrados.length} productos
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Tabla de Productos */}
        <div className="card shadow-lg border-0 rounded-3">
          <div className="card-header bg-success text-white py-3">
            <h4 className="mb-0 d-flex align-items-center">
              <Package className="me-2" /> Inventario de Productos
            </h4>
          </div>
          <div className="card-body p-0">
            <div className="table-responsive">
              <table className="table table-hover mb-0">
                <thead className="table-success">
                  <tr>
                    <th>Producto</th>
                    <th>Categoría</th>
                    <th>Precio</th>
                    <th>Stock</th>
                    <th>Proveedor</th>
                    <th>Valor Total</th>
                    <th>Estado</th>
                  </tr>
                </thead>
                <tbody>
                  {productosFiltrados.map((producto) => {
                    const valorTotal = (producto.precio * producto.stock).toFixed(2);
                    return (
                      <tr
                        key={producto.id}
                        className={
                          producto.stock === 0
                            ? "table-danger"
                            : producto.stock < 10
                            ? "table-warning"
                            : ""
                        }
                      >
                        <td>
                          <div className="d-flex align-items-center">
                            <Package size={20} className="text-success me-2" />
                            <strong>{producto.nombre}</strong>
                          </div>
                        </td>
                        <td>
                          <span className="badge bg-secondary">
                            {producto.id_categoria?.nombre || "N/A"}
                          </span>
                        </td>
                        <td className="fw-bold text-success">
                          ${parseFloat(producto.precio).toFixed(2)}
                        </td>
                        <td>
                          <div className="d-flex align-items-center">
                            <span
                              className={
                                producto.stock < 10
                                  ? "text-danger fw-bold"
                                  : "text-success fw-bold"
                              }
                            >
                              {producto.stock} unidades
                            </span>
                            {producto.stock < 10 && producto.stock > 0 && (
                              <AlertTriangle
                                size={16}
                                className="text-warning ms-2"
                              />
                            )}
                          </div>
                        </td>
                        <td>{producto.id_proveedor?.nombre || "N/A"}</td>
                        <td className="fw-bold text-primary">
                          ${valorTotal}
                        </td>
                        <td>
                          {producto.stock === 0 ? (
                            <span className="badge bg-danger">Sin Stock</span>
                          ) : producto.stock < 10 ? (
                            <span className="badge bg-warning">Stock Bajo</span>
                          ) : (
                            <span className="badge bg-success">Disponible</span>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
            {productosFiltrados.length === 0 && (
              <div className="text-center py-5">
                <Package size={64} className="text-muted mb-3" />
                <h5 className="text-muted">No se encontraron productos</h5>
                <p className="text-muted">
                  Intenta con otros términos de búsqueda o filtros
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Información de Contexto */}
        <div className="mt-3 text-center">
          <small className="text-muted">
            💡 <strong>Modo Consulta</strong> - Solo visualización de inventario
          </small>
        </div>
      </div>
    </div>
  );
}