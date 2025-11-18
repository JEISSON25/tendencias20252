import { useState, useEffect, useCallback, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import {
  ArrowLeft,
  ShoppingCart,
  Trash2,
  Save,
  Plus,
  Minus,
  Search,
  User,
  Package,
} from "lucide-react";

export default function RegistrarVenta() {
  const navigate = useNavigate();
  const [clientes, setClientes] = useState([]);
  const [productos, setProductos] = useState([]);
  const [venta, setVenta] = useState({
    id_cliente: "",
    detalles: [],
  });
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [empleadoId, setEmpleadoId] = useState(null);
  const [userName, setUserName] = useState("");
  const [userId, setUserId] = useState(null);

  // 🔄 Cálculos derivados
  const total = useMemo(() => 
    venta.detalles.reduce((sum, detalle) => sum + detalle.subtotal, 0), 
    [venta.detalles]
  );

  const totalItems = useMemo(() => 
    venta.detalles.reduce((sum, detalle) => sum + detalle.cantidad, 0), 
    [venta.detalles]
  );

  const clienteSeleccionado = useMemo(() => 
    clientes.find((c) => c.id == venta.id_cliente), 
    [clientes, venta.id_cliente]
  );

  const productosFiltrados = useMemo(() => 
    searchTerm
      ? productos.filter((producto) =>
          producto.nombre.toLowerCase().includes(searchTerm.toLowerCase())
        )
      : productos,
    [productos, searchTerm]
  );

  // 🔧 Obtener información del usuario desde el token
  const obtenerUsuarioDesdeToken = useCallback(() => {
    const token = localStorage.getItem("access");
    if (!token) return null;
    
    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      console.log("🔐 Payload del token:", payload);
      return payload;
    } catch (error) {
      console.error("Error decodificando token:", error);
      return null;
    }
  }, []);

  // 🔍 Buscar empleado por usuario - CORREGIDO
  const buscarEmpleadoPorUsuario = useCallback(async (userPayload) => {
    try {
      console.log("🔍 Buscando empleado para user_id:", userPayload.user_id);
      
      const empleadosRes = await api.get("/farmacia/empleados/");
      console.log("📋 Todos los empleados:", empleadosRes.data);
      
      // Buscar empleado que coincida con el user_id
      const empleadoEncontrado = empleadosRes.data.find((emp) => {
        console.log("🔎 Comparando:", {
          empleadoUsuario: emp.usuario,
          userPayloadId: userPayload.user_id,
          tipos: {
            empleadoUsuarioType: typeof emp.usuario,
            userPayloadIdType: typeof userPayload.user_id
          }
        });
        
        // CORRECCIÓN: Comparar como números
        return parseInt(emp.usuario) === parseInt(userPayload.user_id);
      });

      if (empleadoEncontrado) {
        console.log("✅ Empleado encontrado:", empleadoEncontrado);
        setEmpleadoId(empleadoEncontrado.id);
        return empleadoEncontrado;
      } else {
        console.warn("⚠️ No se encontró empleado, usando user_id directamente");
        // Si no encuentra empleado, usar el user_id como fallback
        setEmpleadoId(userPayload.user_id);
        return null;
      }
    } catch (error) {
      console.error("❌ Error obteniendo empleados, usando user_id:", error);
      // En caso de error, usar el user_id del token
      setEmpleadoId(userPayload.user_id);
      return null;
    }
  }, []);

  // 📥 Carga de datos iniciales - MEJORADO
  useEffect(() => {
    const cargarDatos = async () => {
      try {
        setLoading(true);

        const userPayload = obtenerUsuarioDesdeToken();
        if (userPayload) {
          setUserName(userPayload.username || "Empleado");
          setUserId(userPayload.user_id);
          
          // Intentar buscar empleado, si falla usar user_id directamente
          await buscarEmpleadoPorUsuario(userPayload);
        }

        // Cargar datos esenciales
        const [clientesRes, productosRes] = await Promise.all([
          api.get("/farmacia/clientes/"),
          api.get("/farmacia/productos/"),
        ]);

        setClientes(clientesRes.data);
        setProductos(productosRes.data);
      } catch (error) {
        console.error("Error cargando datos:", error);
        alert("Error al cargar datos iniciales");
      } finally {
        setLoading(false);
      }
    };

    cargarDatos();
  }, [obtenerUsuarioDesdeToken, buscarEmpleadoPorUsuario]);

  // 🛒 Funciones de gestión de productos
  const agregarProducto = useCallback((producto) => {
    if (producto.stock <= 0) {
      alert("❌ Este producto no tiene stock disponible");
      return;
    }

    setVenta(prevVenta => {
      const existeIndex = prevVenta.detalles.findIndex(
        (d) => d.id_producto === producto.id
      );

      if (existeIndex !== -1) {
        const nuevosDetalles = [...prevVenta.detalles];
        nuevosDetalles[existeIndex].cantidad += 1;
        nuevosDetalles[existeIndex].subtotal = 
          nuevosDetalles[existeIndex].cantidad * nuevosDetalles[existeIndex].precio_unitario;
        
        return { ...prevVenta, detalles: nuevosDetalles };
      } else {
        const nuevoDetalle = {
          id_producto: producto.id,
          nombre: producto.nombre,
          cantidad: 1,
          precio_unitario: parseFloat(producto.precio),
          subtotal: parseFloat(producto.precio),
        };

        return {
          ...prevVenta,
          detalles: [...prevVenta.detalles, nuevoDetalle],
        };
      }
    });
  }, []);

  const actualizarCantidad = useCallback((index, nuevaCantidad) => {
    if (nuevaCantidad < 1) {
      eliminarProducto(index);
      return;
    }

    setVenta(prevVenta => {
      const detalles = [...prevVenta.detalles];
      const producto = productos.find((p) => p.id === detalles[index].id_producto);

      if (producto && nuevaCantidad > producto.stock) {
        alert(`❌ Stock insuficiente. Disponible: ${producto.stock}`);
        return prevVenta;
      }

      const precioUnitario = detalles[index].precio_unitario;
      detalles[index] = {
        ...detalles[index],
        cantidad: nuevaCantidad,
        subtotal: nuevaCantidad * precioUnitario,
      };

      return { ...prevVenta, detalles };
    });
  }, [productos]);

  const incrementarCantidad = useCallback((index) => {
    actualizarCantidad(index, venta.detalles[index].cantidad + 1);
  }, [venta.detalles, actualizarCantidad]);

  const decrementarCantidad = useCallback((index) => {
    actualizarCantidad(index, venta.detalles[index].cantidad - 1);
  }, [venta.detalles, actualizarCantidad]);

  const eliminarProducto = useCallback((index) => {
    setVenta(prevVenta => ({
      ...prevVenta,
      detalles: prevVenta.detalles.filter((_, i) => i !== index)
    }));
  }, []);

  // ✅ Validaciones MEJORADAS - No bloquea por empleado
  const validarVenta = useCallback(() => {
    if (!venta.id_cliente) {
      alert("❌ Selecciona un cliente");
      return false;
    }

    if (venta.detalles.length === 0) {
      alert("❌ Agrega al menos un producto a la venta");
      return false;
    }

    // Validar stock
    for (const detalle of venta.detalles) {
      const producto = productos.find((p) => p.id === detalle.id_producto);
      if (!producto) {
        alert(`❌ Producto no encontrado: ${detalle.nombre}`);
        return false;
      }
      if (detalle.cantidad > producto.stock) {
        alert(`❌ Stock insuficiente para ${producto.nombre}. Disponible: ${producto.stock}`);
        return false;
      }
    }

    return true;
  }, [venta, productos]);

  // 💾 Guardar venta - CON ALTERNATIVAS
  const guardarVenta = async () => {
    if (!validarVenta()) return;

    setLoading(true);

    try {
      // Preparar datos para el backend
      const facturaData = {
        id_cliente: parseInt(venta.id_cliente),
        id_empleado: empleadoId || userId, // Usar empleadoId o userId como fallback
        detalles: venta.detalles.map((detalle) => ({
          id_producto: detalle.id_producto,
          cantidad: detalle.cantidad,
        })),
      };

      console.log("📤 Enviando datos de venta:", {
        ...facturaData,
        empleadoUsado: empleadoId ? "empleadoId" : "userId",
        valor: empleadoId || userId
      });

      const response = await api.post("/farmacia/facturasventa/", facturaData);

      console.log("✅ Venta registrada exitosamente:", response.data);
      alert("✅ Venta registrada correctamente");
      navigate("/empleado");
    } catch (error) {
      console.error("❌ Error al registrar venta:", error);
      manejarErrorVenta(error);
    } finally {
      setLoading(false);
    }
  };

  const manejarErrorVenta = (error) => {
    let mensajeError = "Error al registrar la venta";

    if (error.response?.data) {
      const errorData = error.response.data;
      console.error("🔍 Detalles del error del backend:", errorData);
      
      if (errorData.id_empleado) {
        mensajeError = `❌ Error en empleado: ${
          Array.isArray(errorData.id_empleado)
            ? errorData.id_empleado.join(", ")
            : errorData.id_empleado
        }`;
        
        // Información adicional para debugging
        mensajeError += `\n\n🔧 Información de depuración:`;
        mensajeError += `\n• Empleado ID enviado: ${empleadoId}`;
        mensajeError += `\n• User ID: ${userId}`;
        mensajeError += `\n• Usuario: ${userName}`;
      } else if (errorData.id_cliente) {
        mensajeError = `❌ Error en cliente: ${errorData.id_cliente}`;
      } else if (errorData.detalles) {
        mensajeError = `❌ Error en detalles: ${JSON.stringify(errorData.detalles)}`;
      } else if (errorData.detail) {
        mensajeError = `❌ Error: ${errorData.detail}`;
      }
    }

    alert(mensajeError);
  };

  // 🎨 Componentes reutilizables - SIN RESTRICCIONES DE EMPLEADO
  const ProductoItem = ({ producto }) => (
    <button
      type="button"
      className={`btn text-start p-3 border-0 ${
        producto.stock <= 0
          ? "bg-light text-muted"
          : "bg-success bg-opacity-10 text-success"
      }`}
      onClick={() => agregarProducto(producto)}
      disabled={producto.stock <= 0}
    >
      <div className="d-flex justify-content-between align-items-start w-100">
        <div className="text-start">
          <div className="fw-bold">{producto.nombre}</div>
          <small>${parseFloat(producto.precio).toFixed(2)}</small>
        </div>
        <span className={`badge ${producto.stock <= 0 ? "bg-danger" : "bg-success"}`}>
          {producto.stock <= 0 ? "Sin stock" : producto.stock}
        </span>
      </div>
    </button>
  );

  const DetalleVentaRow = ({ detalle, index }) => (
    <tr>
      <td className="fw-bold">{detalle.nombre}</td>
      <td>${detalle.precio_unitario.toFixed(2)}</td>
      <td>
        <div className="d-flex align-items-center gap-2">
          <button
            className="btn btn-outline-secondary btn-sm"
            onClick={() => decrementarCantidad(index)}
          >
            <Minus size={12} />
          </button>
          <span className="fw-bold mx-2">{detalle.cantidad}</span>
          <button
            className="btn btn-outline-secondary btn-sm"
            onClick={() => incrementarCantidad(index)}
          >
            <Plus size={12} />
          </button>
        </div>
      </td>
      <td className="fw-bold text-success">${detalle.subtotal.toFixed(2)}</td>
      <td>
        <button
          className="btn btn-outline-danger btn-sm"
          onClick={() => eliminarProducto(index)}
        >
          <Trash2 size={14} />
        </button>
      </td>
    </tr>
  );

  // 🎯 Renderizado condicional
  if (loading && productos.length === 0) {
    return (
      <div
        className="min-vh-100 d-flex justify-content-center align-items-center"
        style={{ background: "linear-gradient(135deg, #d0f0c0, #b2dfdb)" }}
      >
        <div className="text-center">
          <div
            className="spinner-border text-success mb-3"
            style={{ width: "3rem", height: "3rem" }}
          >
            <span className="visually-hidden">Cargando...</span>
          </div>
          <h5 className="text-success">Cargando datos...</h5>
        </div>
      </div>
    );
  }

  return (
    <div
      className="min-vh-100"
      style={{ background: "linear-gradient(135deg, #d0f0c0, #b2dfdb)" }}
    >
      {/* Navbar */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-success shadow-sm">
        <div className="container">
          <span className="navbar-brand fw-bold fs-4">🛒 Registrar Venta</span>
          <div className="d-flex align-items-center gap-2">
            {userName && (
              <span className="text-light me-2">
                <User size={16} className="me-1" />
                {userName} 
                {empleadoId && ` (EmpID: ${empleadoId})`}
                {!empleadoId && userId && ` (UserID: ${userId})`}
              </span>
            )}
            <button
              onClick={() => navigate(-1)}
              className="btn btn-outline-light btn-sm"
            >
              <ArrowLeft size={16} /> Volver
            </button>
          </div>
        </div>
      </nav>

      <div className="container py-4">
        <div className="text-center mb-4">
          <h1 className="fw-bold text-success mb-2">Registrar Nueva Venta</h1>
          <p className="text-muted">Complete la información de la venta</p>
        </div>

        {/* Información del usuario */}
        <div className="alert alert-info text-center">
          <strong>👤 Usuario:</strong> {userName} | 
          <strong> ID:</strong> {empleadoId ? `Empleado ${empleadoId}` : `Usuario ${userId}`}
        </div>

        <div className="row g-4">
          {/* Panel izquierdo - Cliente y Productos */}
          <div className="col-lg-4">
            <div className="card border-0 shadow-sm rounded-3">
              <div className="card-header bg-success text-white py-3">
                <h5 className="mb-0 d-flex align-items-center">
                  <User className="me-2" size={20} />
                  Información de Venta
                </h5>
              </div>
              <div className="card-body">
                <div className="mb-4">
                  <label className="form-label fw-semibold">Cliente *</label>
                  <select
                    className="form-select"
                    value={venta.id_cliente}
                    onChange={(e) => setVenta(prev => ({ ...prev, id_cliente: e.target.value }))}
                    required
                  >
                    <option value="">Selecciona un cliente</option>
                    {clientes.map((cliente) => (
                      <option key={cliente.id} value={cliente.id}>
                        {cliente.nombre} - {cliente.correo || cliente.telefono}
                      </option>
                    ))}
                  </select>
                  {clienteSeleccionado && (
                    <div className="mt-2 p-2 bg-success bg-opacity-10 rounded">
                      <small className="text-success">
                        ✅ Cliente seleccionado: <strong>{clienteSeleccionado.nombre}</strong>
                      </small>
                    </div>
                  )}
                </div>

                <div className="mb-3">
                  <label className="form-label fw-semibold">Buscar Productos</label>
                  <div className="input-group">
                    <span className="input-group-text bg-light">
                      <Search size={16} />
                    </span>
                    <input
                      type="text"
                      className="form-control"
                      placeholder="Nombre del producto..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                    />
                  </div>
                </div>

                <div>
                  <label className="form-label fw-semibold d-flex align-items-center">
                    <Package className="me-2" size={16} />
                    Productos Disponibles ({productosFiltrados.length})
                  </label>
                  <div style={{ maxHeight: "50vh", overflowY: "auto" }} className="d-grid gap-2">
                    {productosFiltrados.map((producto) => (
                      <ProductoItem key={producto.id} producto={producto} />
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Panel derecho - Detalles de la Venta */}
          <div className="col-lg-8">
            <div className="card border-0 shadow-sm rounded-3 h-100">
              <div className="card-header bg-success text-white py-3">
                <div className="d-flex justify-content-between align-items-center">
                  <h5 className="mb-0 d-flex align-items-center">
                    <ShoppingCart className="me-2" size={20} />
                    Detalles de la Venta
                  </h5>
                  <span className="badge bg-light text-success fs-6">
                    ${total.toFixed(2)}
                  </span>
                </div>
              </div>

              <div className="card-body d-flex flex-column">
                {venta.detalles.length === 0 ? (
                  <div className="text-center py-5 my-auto">
                    <ShoppingCart size={64} className="text-muted mb-3" />
                    <p className="text-muted fs-5">No hay productos en la venta</p>
                    <small className="text-muted">Selecciona productos del panel izquierdo</small>
                  </div>
                ) : (
                  <>
                    <div className="table-responsive flex-grow-1">
                      <table className="table table-hover align-middle">
                        <thead className="table-success">
                          <tr>
                            <th>Producto</th>
                            <th>Precio Unit.</th>
                            <th width="140">Cantidad</th>
                            <th>Subtotal</th>
                            <th width="80">Acción</th>
                          </tr>
                        </thead>
                        <tbody>
                          {venta.detalles.map((detalle, index) => (
                            <DetalleVentaRow key={index} detalle={detalle} index={index} />
                          ))}
                        </tbody>
                      </table>
                    </div>

                    <div className="mt-auto pt-4 border-top">
                      <div className="row align-items-center">
                        <div className="col-md-6">
                          <div className="text-muted">
                            <small className="d-block">Productos: {venta.detalles.length}</small>
                            <small className="d-block">Items totales: {totalItems}</small>
                            {clienteSeleccionado && (
                              <small className="d-block text-success">Cliente: {clienteSeleccionado.nombre}</small>
                            )}
                            <small className="d-block text-info">
                              Vendedor: {empleadoId ? `Empleado ${empleadoId}` : `Usuario ${userId}`}
                            </small>
                          </div>
                        </div>
                        <div className="col-md-6 text-end">
                          <h4 className="text-success mb-3">Total: ${total.toFixed(2)}</h4>
                          <button
                            className="btn btn-success btn-lg px-4"
                            onClick={guardarVenta}
                            disabled={loading || venta.detalles.length === 0}
                          >
                            {loading ? (
                              <>
                                <div className="spinner-border spinner-border-sm me-2" />
                                Procesando...
                              </>
                            ) : (
                              <>
                                <Save size={18} className="me-2" />
                                Finalizar Venta
                              </>
                            )}
                          </button>
                        </div>
                      </div>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}