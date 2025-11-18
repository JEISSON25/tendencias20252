// src/components/admin/GestionMovimientos.jsx
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  Download,
  Search,
  Filter,
  Package,
  User,
  Truck,
  Calendar,
  Plus,
  Edit,
  Trash2,
  BarChart3
} from "lucide-react";
import api from "../services/api";

export default function GestionMovimientos() {
  const navigate = useNavigate();
  const [movimientos, setMovimientos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [filterTipo, setFilterTipo] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    tipo: "entrada",
    id_producto: "",
    cantidad: "",
    id_proveedor: "",
    id_cliente: "",
    responsable: ""
  });
  const [productos, setProductos] = useState([]);
  const [proveedores, setProveedores] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [empleados, setEmpleados] = useState([]);
  const [movimientoEdit, setMovimientoEdit] = useState(null);
  const [stats, setStats] = useState({
    total: 0,
    entradas: 0,
    salidas: 0,
    valorTotalEntradas: 0,
    valorTotalSalidas: 0
  });

  useEffect(() => {
    cargarDatos();
  }, []);

  const cargarDatos = async () => {
    try {
      setLoading(true);

      const [movRes, prodRes, provRes, cliRes, empRes] = await Promise.all([
        api.get("/farmacia/movimientos/"),
        api.get("/farmacia/productos/"),
        api.get("/farmacia/proveedores/"),
        api.get("/farmacia/clientes/"),
        api.get("/farmacia/empleados/")
      ]);

      setMovimientos(movRes.data);
      setProductos(prodRes.data);
      setProveedores(provRes.data);
      setClientes(cliRes.data);
      setEmpleados(empRes.data);
      calcularEstadisticas(movRes.data, prodRes.data);
    } catch (error) {
      console.error("Error cargando datos:", error);
      alert("Error al cargar los datos");
    } finally {
      setLoading(false);
    }
  };

  const calcularEstadisticas = (movimientosData, productosData) => {
    const total = movimientosData.length;
    const entradas = movimientosData.filter(m => m.tipo === "entrada").length;
    const salidas = movimientosData.filter(m => m.tipo === "salida").length;
    
    // Calcular valores totales
    const valorTotalEntradas = movimientosData
      .filter(m => m.tipo === "entrada")
      .reduce((sum, mov) => {
        const producto = productosData.find(p => p.id === mov.id_producto);
        return sum + (producto ? producto.precio * mov.cantidad : 0);
      }, 0);

    const valorTotalSalidas = movimientosData
      .filter(m => m.tipo === "salida")
      .reduce((sum, mov) => {
        const producto = productosData.find(p => p.id === mov.id_producto);
        return sum + (producto ? producto.precio * mov.cantidad : 0);
      }, 0);

    setStats({ total, entradas, salidas, valorTotalEntradas, valorTotalSalidas });
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
      ...(name === "tipo" && {
        id_proveedor: value === "entrada" ? "" : prev.id_proveedor,
        id_cliente: value === "salida" ? "" : prev.id_cliente
      })
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Validaciones
      if (!formData.id_producto || !formData.cantidad || !formData.responsable) {
        alert("Completa los campos obligatorios");
        return;
      }

      if (formData.tipo === "entrada" && !formData.id_proveedor) {
        alert("Para entradas debe seleccionar un proveedor");
        return;
      }

      if (formData.tipo === "salida" && !formData.id_cliente) {
        alert("Para salidas debe seleccionar un cliente");
        return;
      }

      const movimientoData = {
        tipo: formData.tipo,
        cantidad: parseInt(formData.cantidad),
        id_producto: parseInt(formData.id_producto),
        id_proveedor: formData.id_proveedor ? parseInt(formData.id_proveedor) : null,
        id_cliente: formData.id_cliente ? parseInt(formData.id_cliente) : null,
        responsable: parseInt(formData.responsable),
      };

      if (movimientoEdit) {
        await api.patch(`/farmacia/movimientos/${movimientoEdit.id}/`, movimientoData);
        alert("✅ Movimiento actualizado correctamente");
      } else {
        await api.post("/farmacia/movimientos/", movimientoData);
        alert("✅ Movimiento registrado correctamente");
      }

      resetForm();
      cargarDatos();
    } catch (error) {
      console.error("Error guardando movimiento:", error);
      const errorMsg = error.response?.data?.detail || "Error al guardar movimiento";
      alert(`❌ Error: ${errorMsg}`);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm("¿Estás seguro de eliminar este movimiento?")) {
      try {
        await api.delete(`/farmacia/movimientos/${id}/`);
        alert("✅ Movimiento eliminado correctamente");
        cargarDatos();
      } catch (error) {
        console.error("Error eliminando movimiento:", error);
        alert("Error al eliminar el movimiento");
      }
    }
  };

  const descargarPDF = async (movimientoId = null) => {
    try {
      let url;
      if (movimientoId) {
        url = `/farmacia/movimientos/${movimientoId}/pdf/`;
      } else {
        url = "/farmacia/movimientos/all_pdf/";
      }

      const response = await api.get(url, { responseType: "blob" });
      const blob = new Blob([response.data], { type: "application/pdf" });
      const urlWindow = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = urlWindow;
      link.setAttribute("download", movimientoId ? `movimiento_${movimientoId}.pdf` : "todos_movimientos.pdf");
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(urlWindow);
    } catch (error) {
      console.error("Error al descargar PDF:", error);
      alert("Error al descargar el PDF");
    }
  };

  const resetForm = () => {
    setFormData({
      tipo: "entrada",
      id_producto: "",
      cantidad: "",
      id_proveedor: "",
      id_cliente: "",
      responsable: ""
    });
    setMovimientoEdit(null);
    setShowForm(false);
  };

  const editMovimiento = (movimiento) => {
    setMovimientoEdit(movimiento);
    setFormData({
      tipo: movimiento.tipo,
      id_producto: movimiento.id_producto,
      cantidad: movimiento.cantidad,
      id_proveedor: movimiento.id_proveedor || "",
      id_cliente: movimiento.id_cliente || "",
      responsable: movimiento.responsable || ""
    });
    setShowForm(true);
  };

  // Filtrar movimientos
  const movimientosFiltrados = movimientos.filter((movimiento) => {
    const matchesSearch =
      movimiento.producto_nombre?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      movimiento.proveedor_nombre?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      movimiento.cliente_nombre?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      movimiento.responsable_nombre?.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesTipo = !filterTipo || movimiento.tipo === filterTipo;

    return matchesSearch && matchesTipo;
  });

  const getBadgeVariant = (tipo) => {
    return tipo === "entrada" ? "success" : "warning";
  };

  const getIcon = (tipo) => {
    return tipo === "entrada" ? <Truck size={16} /> : <Package size={16} />;
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
          <button onClick={() => navigate("/admin")} className="btn btn-outline-success">
            <ArrowLeft size={18} /> Volver al Dashboard
          </button>
          <h1 className="text-success d-flex align-items-center">
            <Package className="me-2" /> Gestión de Movimientos
          </h1>
          <div className="d-flex gap-2">
            <button onClick={() => setShowForm(true)} className="btn btn-success">
              <Plus size={18} /> Nuevo Movimiento
            </button>
            <button onClick={() => descargarPDF()} className="btn btn-outline-success">
              <Download size={18} /> PDF
            </button>
          </div>
        </div>

        {/* Estadísticas Avanzadas */}
        <div className="row mb-4">
          <div className="col-md-3">
            <div className="card bg-success text-white shadow-sm border-0">
              <div className="card-body text-center py-3">
                <BarChart3 size={24} className="mb-2" />
                <h4 className="mb-1">{stats.total}</h4>
                <small>Total Movimientos</small>
              </div>
            </div>
          </div>
          <div className="col-md-2">
            <div className="card bg-primary text-white shadow-sm border-0">
              <div className="card-body text-center py-3">
                <Truck size={24} className="mb-2" />
                <h4 className="mb-1">{stats.entradas}</h4>
                <small>Entradas</small>
              </div>
            </div>
          </div>
          <div className="col-md-2">
            <div className="card bg-warning text-dark shadow-sm border-0">
              <div className="card-body text-center py-3">
                <Package size={24} className="mb-2" />
                <h4 className="mb-1">{stats.salidas}</h4>
                <small>Salidas</small>
              </div>
            </div>
          </div>
          <div className="col-md-2">
            <div className="card bg-info text-white shadow-sm border-0">
              <div className="card-body text-center py-3">
                <BarChart3 size={24} className="mb-2" />
                <h4 className="mb-1">${stats.valorTotalEntradas.toFixed(2)}</h4>
                <small>Valor Entradas</small>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card bg-danger text-white shadow-sm border-0">
              <div className="card-body text-center py-3">
                <BarChart3 size={24} className="mb-2" />
                <h4 className="mb-1">${stats.valorTotalSalidas.toFixed(2)}</h4>
                <small>Valor Salidas</small>
              </div>
            </div>
          </div>
        </div>

        {/* Formulario de Movimiento */}
        {showForm && (
          <div className="card shadow-lg border-0 mb-4">
            <div className="card-header bg-success text-white py-3">
              <h5 className="mb-0">
                {movimientoEdit ? 'Editar Movimiento' : 'Registrar Nuevo Movimiento'}
              </h5>
            </div>
            <div className="card-body">
              <form onSubmit={handleSubmit}>
                <div className="row g-3">
                  <div className="col-md-2">
                    <label className="form-label fw-semibold">Tipo *</label>
                    <select
                      name="tipo"
                      value={formData.tipo}
                      onChange={handleInputChange}
                      className="form-select border-success"
                      required
                    >
                      <option value="entrada">Entrada</option>
                      <option value="salida">Salida</option>
                    </select>
                  </div>

                  <div className="col-md-3">
                    <label className="form-label fw-semibold">Producto *</label>
                    <select
                      name="id_producto"
                      value={formData.id_producto}
                      onChange={handleInputChange}
                      className="form-select border-success"
                      required
                    >
                      <option value="">Seleccionar producto</option>
                      {productos.map((producto) => (
                        <option key={producto.id} value={producto.id}>
                          {producto.nombre} (Stock: {producto.stock})
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="col-md-2">
                    <label className="form-label fw-semibold">Cantidad *</label>
                    <input
                      type="number"
                      name="cantidad"
                      value={formData.cantidad}
                      onChange={handleInputChange}
                      className="form-control border-success"
                      min="1"
                      required
                    />
                  </div>

                  <div className="col-md-3">
                    <label className="form-label fw-semibold">Responsable *</label>
                    <select
                      name="responsable"
                      value={formData.responsable}
                      onChange={handleInputChange}
                      className="form-select border-success"
                      required
                    >
                      <option value="">Seleccionar responsable</option>
                      {empleados.map((emp) => (
                        <option key={emp.id} value={emp.id}>
                          {emp.nombre}
                        </option>
                      ))}
                    </select>
                  </div>

                  {formData.tipo === "entrada" ? (
                    <div className="col-md-2">
                      <label className="form-label fw-semibold">Proveedor *</label>
                      <select
                        name="id_proveedor"
                        value={formData.id_proveedor}
                        onChange={handleInputChange}
                        className="form-select border-success"
                        required={formData.tipo === "entrada"}
                      >
                        <option value="">Seleccionar proveedor</option>
                        {proveedores.map((prov) => (
                          <option key={prov.id} value={prov.id}>
                            {prov.nombre}
                          </option>
                        ))}
                      </select>
                    </div>
                  ) : (
                    <div className="col-md-2">
                      <label className="form-label fw-semibold">Cliente *</label>
                      <select
                        name="id_cliente"
                        value={formData.id_cliente}
                        onChange={handleInputChange}
                        className="form-select border-success"
                        required={formData.tipo === "salida"}
                      >
                        <option value="">Seleccionar cliente</option>
                        {clientes.map((cli) => (
                          <option key={cli.id} value={cli.id}>
                            {cli.nombre}
                          </option>
                        ))}
                      </select>
                    </div>
                  )}
                </div>

                <div className="mt-3 d-flex gap-2">
                  <button type="submit" className="btn btn-success">
                    <Plus size={18} /> {movimientoEdit ? 'Actualizar' : 'Registrar'} Movimiento
                  </button>
                  <button type="button" className="btn btn-outline-secondary" onClick={resetForm}>
                    Cancelar
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Filtros y Búsqueda */}
        <div className="card shadow-sm border-0 mb-4">
          <div className="card-body">
            <div className="row g-3">
              <div className="col-md-6">
                <div className="input-group">
                  <span className="input-group-text bg-success text-white">
                    <Search size={16} />
                  </span>
                  <input
                    type="text"
                    className="form-control border-success"
                    placeholder="Buscar por producto, proveedor, cliente o responsable..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
              </div>
              <div className="col-md-4">
                <div className="input-group">
                  <span className="input-group-text bg-success text-white">
                    <Filter size={16} />
                  </span>
                  <select
                    className="form-select border-success"
                    value={filterTipo}
                    onChange={(e) => setFilterTipo(e.target.value)}
                  >
                    <option value="">Todos los tipos</option>
                    <option value="entrada">Entradas</option>
                    <option value="salida">Salidas</option>
                  </select>
                </div>
              </div>
              <div className="col-md-2 text-center">
                <span className="badge bg-success fs-6 p-2">
                  {movimientosFiltrados.length} registros
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Tabla de Movimientos */}
        <div className="card shadow-lg border-0 rounded-3">
          <div className="card-header bg-success text-white py-3">
            <h4 className="mb-0 d-flex align-items-center">
              <Package className="me-2" /> Historial de Movimientos
            </h4>
          </div>
          <div className="card-body p-0">
            <div className="table-responsive">
              <table className="table table-hover mb-0">
                <thead className="table-success">
                  <tr>
                    <th>ID</th>
                    <th>Tipo</th>
                    <th>Producto</th>
                    <th>Cantidad</th>
                    <th>Proveedor/Cliente</th>
                    <th>Responsable</th>
                    <th>Fecha</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {movimientosFiltrados.map((movimiento) => (
                    <tr key={movimiento.id}>
                      <td className="fw-bold">#{movimiento.id}</td>
                      <td>
                        <span className={`badge bg-${getBadgeVariant(movimiento.tipo)} d-flex align-items-center`}>
                          {getIcon(movimiento.tipo)}
                          <span className="ms-1 text-capitalize">{movimiento.tipo}</span>
                        </span>
                      </td>
                      <td className="fw-bold">{movimiento.producto_nombre || "N/A"}</td>
                      <td>
                        <span className={`fw-bold ${movimiento.tipo === "entrada" ? "text-success" : "text-warning"}`}>
                          {movimiento.tipo === "entrada" ? "+" : "-"}
                          {movimiento.cantidad}
                        </span>
                      </td>
                      <td>
                        {movimiento.tipo === "entrada" ? (
                          <span className="text-success">
                            <Truck size={14} className="me-1" />
                            {movimiento.proveedor_nombre || "N/A"}
                          </span>
                        ) : (
                          <span className="text-primary">
                            <User size={14} className="me-1" />
                            {movimiento.cliente_nombre || "N/A"}
                          </span>
                        )}
                      </td>
                      <td>{movimiento.responsable_nombre || "N/A"}</td>
                      <td>
                        <small className="text-muted d-flex align-items-center">
                          <Calendar size={12} className="me-1" />
                          {new Date(movimiento.fecha).toLocaleDateString("es-ES")}
                        </small>
                      </td>
                      <td>
                        <div className="d-flex gap-1">
                          <button
                            onClick={() => editMovimiento(movimiento)}
                            className="btn btn-outline-primary btn-sm"
                            title="Editar"
                          >
                            <Edit size={14} />
                          </button>
                          <button
                            onClick={() => descargarPDF(movimiento.id)}
                            className="btn btn-outline-success btn-sm"
                            title="Descargar PDF"
                          >
                            <Download size={14} />
                          </button>
                          <button
                            onClick={() => handleDelete(movimiento.id)}
                            className="btn btn-outline-danger btn-sm"
                            title="Eliminar"
                          >
                            <Trash2 size={14} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {movimientosFiltrados.length === 0 && (
              <div className="text-center py-5">
                <Package size={64} className="text-muted mb-3" />
                <h5 className="text-muted">No se encontraron movimientos</h5>
                <p className="text-muted">No hay movimientos que coincidan con los filtros</p>
              </div>
            )}
          </div>
        </div>

        {/* Información de Contexto */}
        <div className="mt-3 text-center">
          <small className="text-muted">
            💡 <strong>Modo Administrador</strong> - Gestión completa de movimientos (CRUD)
          </small>
        </div>
      </div>
    </div>
  );
}