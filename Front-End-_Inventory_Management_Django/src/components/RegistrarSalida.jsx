// RegistrarSalida.jsx - VERSIÓN CORREGIDA
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { ArrowLeft, Save } from "lucide-react";

export default function RegistrarSalida() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    tipo: "salida",
    id_producto: "",
    cantidad: "",
    id_cliente: "",
    responsable: ""
  });
  const [productos, setProductos] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const cargarDatos = async () => {
      try {
        // Obtener ID del usuario actual desde el token
        const token = localStorage.getItem("access");
        let userId = "";
        if (token) {
          const payload = JSON.parse(atob(token.split(".")[1]));
          userId = payload.user_id;
          setFormData(prev => ({ ...prev, responsable: userId }));
        }

        const [prodRes, cliRes] = await Promise.all([
          api.get("/farmacia/productos/"),
          api.get("/farmacia/clientes/")
        ]);

        setProductos(prodRes.data);
        setClientes(cliRes.data);

      } catch (error) {
        console.error("Error al cargar datos:", error);
        alert("Error al cargar productos o clientes");
      }
    };

    cargarDatos();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.id_producto || !formData.cantidad || !formData.id_cliente) {
      alert("Completa todos los campos obligatorios");
      return;
    }

    // Validar stock disponible
    const productoSeleccionado = productos.find(p => p.id == formData.id_producto);
    if (productoSeleccionado && productoSeleccionado.stock < parseInt(formData.cantidad)) {
      alert(`Stock insuficiente. Disponible: ${productoSeleccionado.stock}`);
      return;
    }

    setLoading(true);

    try {
      const movimientoData = {
        tipo: "salida",
        cantidad: parseInt(formData.cantidad),
        id_producto: parseInt(formData.id_producto),
        id_cliente: parseInt(formData.id_cliente),
        responsable: formData.responsable ? parseInt(formData.responsable) : null,
      };

      await api.post("/farmacia/movimientos/", movimientoData);

      alert("✅ Salida registrada correctamente");
      navigate("/empleado/movimientos");
    } catch (error) {
      console.error("Error al registrar salida:", error);
      const msg = error.response?.data?.detail || 
                  error.response?.data?.non_field_errors?.[0] || 
                  "Error al registrar la salida";
      alert(`❌ Error: ${msg}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-vh-100" style={{ background: "linear-gradient(135deg, #d0f0c0, #b2dfdb)" }}>
      {/* Navbar */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
        <div className="container">
          <span className="navbar-brand fw-bold fs-4 d-flex align-items-center">
            📤 Registrar Salida
          </span>
          <div className="d-flex align-items-center">
            <button onClick={() => navigate(-1)} className="btn btn-outline-light btn-sm me-2">
              <ArrowLeft size={16} /> Volver
            </button>
          </div>
        </div>
      </nav>

      {/* Contenido Principal */}
      <div className="container py-5">
        
        {/* Header */}
        <div className="text-center mb-5">
          <h1 className="fw-bold text-primary mb-3">Registrar Salida de Inventario</h1>
          <p className="text-muted fs-5">
            Registre la salida de productos del inventario
          </p>
        </div>

        {/* Formulario */}
        <div className="row justify-content-center">
          <div className="col-md-8">
            <div className="card border-0 shadow-sm hover-lift rounded-4">
              <div className="card-header bg-primary text-white py-3">
                <h5 className="mb-0">Información de la Salida</h5>
              </div>
              <div className="card-body p-4">
                <form onSubmit={handleSubmit}>
                  <div className="row g-3">
                    
                    {/* Producto */}
                    <div className="col-md-6">
                      <label className="form-label fw-semibold">Producto *</label>
                      <select
                        name="id_producto"
                        value={formData.id_producto}
                        onChange={handleChange}
                        className="form-select"
                        required
                      >
                        <option value="">Selecciona un producto</option>
                        {productos.map((p) => (
                          <option key={p.id} value={p.id}>
                            {p.nombre} (Stock: {p.stock})
                          </option>
                        ))}
                      </select>
                    </div>

                    {/* Cantidad */}
                    <div className="col-md-3">
                      <label className="form-label fw-semibold">Cantidad *</label>
                      <input
                        type="number"
                        name="cantidad"
                        value={formData.cantidad}
                        onChange={handleChange}
                        className="form-control"
                        min="1"
                        placeholder="Ej: 5"
                        required
                      />
                    </div>

                    {/* Cliente */}
                    <div className="col-md-3">
                      <label className="form-label fw-semibold">Cliente *</label>
                      <select
                        name="id_cliente"
                        value={formData.id_cliente}
                        onChange={handleChange}
                        className="form-select"
                        required
                      >
                        <option value="">Selecciona cliente</option>
                        {clientes.map((cli) => (
                          <option key={cli.id} value={cli.id}>
                            {cli.nombre}
                          </option>
                        ))}
                      </select>
                    </div>

                  </div>

                  {/* Botón Guardar */}
                  <div className="mt-4 text-end">
                    <button
                      type="submit"
                      className="btn btn-primary btn-lg"
                      disabled={loading}
                    >
                      {loading ? (
                        <>
                          <div className="spinner-border spinner-border-sm me-2" role="status"></div>
                          Guardando...
                        </>
                      ) : (
                        <>
                          <Save size={18} className="me-2" />
                          Guardar Salida
                        </>
                      )}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}