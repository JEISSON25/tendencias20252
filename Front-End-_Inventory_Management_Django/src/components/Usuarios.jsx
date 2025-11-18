import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import {
  Users,
  UserPlus,
  Edit,
  Trash2,
  ArrowLeft,
  Download,
} from "lucide-react";

export default function Usuarios() {
  const navigate = useNavigate();
  const [usuarios, setUsuarios] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [empleados, setEmpleados] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [tipoUsuario, setTipoUsuario] = useState("cliente");
  const [formData, setFormData] = useState({
    nombre: "",
    correo: "",
    telefono: "",
    usuario: {
      username: "",
      password: "",
    },
  });

  useEffect(() => {
    cargarUsuarios();
  }, []);

  const cargarUsuarios = async () => {
    try {
      const [clientesRes, empleadosRes] = await Promise.all([
        api.get("/farmacia/clientes/"),
        api.get("/farmacia/empleados/"),
      ]);

      setClientes(clientesRes.data);
      setEmpleados(empleadosRes.data);
      setUsuarios([...clientesRes.data, ...empleadosRes.data]);
    } catch (error) {
      console.error("Error cargando usuarios:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (tipoUsuario === "cliente") {
        await api.post("/farmacia/clientes/", formData);
        alert("✅ Cliente creado exitosamente");
      } else {
        await api.post("/farmacia/empleados/", formData);
        alert("✅ Empleado creado exitosamente");
      }

      setShowModal(false);
      setFormData({
        nombre: "",
        correo: "",
        telefono: "",
        usuario: { username: "", password: "" },
      });
      cargarUsuarios();
    } catch (error) {
      console.error("Error creando usuario:", error);
      alert("❌ Error al crear el usuario");
    }
  };

  const handleDelete = async (id, tipo) => {
    if (window.confirm("¿Estás seguro de eliminar este usuario?")) {
      try {
        if (tipo === "cliente") {
          await api.delete(`/farmacia/clientes/${id}/`);
        } else {
          await api.delete(`/farmacia/empleados/${id}/`);
        }
        alert("✅ Usuario eliminado");
        cargarUsuarios();
      } catch (error) {
        console.error("❌ Error eliminando usuario:", error);
      }
    }
  };

  return (
    <div
      className="d-flex justify-content-center align-items-center min-vh-100 py-5"
      style={{ background: "linear-gradient(135deg, #d0f0c0, #b2dfdb)" }}
    >
      <div className="container" style={{ maxWidth: "1200px" }}>
        {/* Header */}
        <div className="d-flex justify-content-between align-items-center mb-4">
          <button
            onClick={() => navigate(-1)}
            className="btn btn-outline-success"
          >
            <ArrowLeft size={18} /> Volver
          </button>
          <button
            onClick={() => setShowModal(true)}
            className="btn btn-success"
          >
            <UserPlus size={18} /> Nuevo Usuario
          </button>
        </div>

        {/* Tabs para Clientes y Empleados */}
        <div className="card shadow-lg border-0 rounded-4">
          <div className="card-header bg-success text-white">
            <h4 className="mb-0 d-flex align-items-center">
              <Users className="me-2" /> Gestión de Usuarios
            </h4>
          </div>

          <div className="card-body">
            <ul className="nav nav-tabs mb-4">
              <li className="nav-item">
                <button
                  className="nav-link active"
                  data-bs-toggle="tab"
                  onClick={() => setUsuarios([...clientes, ...empleados])}
                >
                  Todos los Usuarios
                </button>
              </li>
              <li className="nav-item">
                <button
                  className="nav-link"
                  data-bs-toggle="tab"
                  onClick={() => setUsuarios(clientes)}
                >
                  Clientes ({clientes.length})
                </button>
              </li>
              <li className="nav-item">
                <button
                  className="nav-link"
                  data-bs-toggle="tab"
                  onClick={() => setUsuarios(empleados)}
                >
                  Empleados ({empleados.length})
                </button>
              </li>
            </ul>

            <div className="table-responsive">
              <table className="table table-hover">
                <thead className="table-success">
                  <tr>
                    <th>Tipo</th>
                    <th>Nombre</th>
                    <th>Email</th>
                    <th>Teléfono</th>
                    <th>Usuario</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {usuarios.map((user) => (
                    <tr key={user.id}>
                      <td>
                        <span
                          className={`badge ${
                            user.correo ? "bg-info" : "bg-warning"
                          }`}
                        >
                          {user.correo ? "Cliente" : "Empleado"}
                        </span>
                      </td>
                      <td className="fw-bold">{user.nombre}</td>
                      <td>{user.correo || "N/A"}</td>
                      <td>{user.telefono}</td>
                      <td>
                        <span className="fw-bold text-primary">
                          {user.usuario?.username || "N/A"}
                        </span>
                      </td>
                      <td>
                        <div className="d-flex gap-1">
                          <button className="btn btn-outline-primary btn-sm">
                            <Edit size={14} />
                          </button>
                          <button
                            onClick={() =>
                              handleDelete(
                                user.id,
                                user.correo ? "cliente" : "empleado"
                              )
                            }
                            className="btn btn-outline-danger btn-sm"
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
          </div>
        </div>

        {/* Modal para crear usuario */}
        {showModal && (
          <div
            className="modal fade show d-block"
            style={{ backgroundColor: "rgba(0,0,0,0.5)" }}
          >
            <div className="modal-dialog modal-dialog-centered">
              <div className="modal-content">
                <div className="modal-header bg-success text-white">
                  <h5 className="modal-title">Crear Nuevo Usuario</h5>
                  <button
                    type="button"
                    className="btn-close btn-close-white"
                    onClick={() => setShowModal(false)}
                  ></button>
                </div>
                <div className="modal-body">
                  <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                      <label className="form-label">Tipo de Usuario</label>
                      <select
                        className="form-select"
                        value={tipoUsuario}
                        onChange={(e) => setTipoUsuario(e.target.value)}
                      >
                        <option value="cliente">Cliente</option>
                        <option value="empleado">Empleado</option>
                      </select>
                    </div>

                    <div className="mb-3">
                      <label className="form-label">Nombre Completo</label>
                      <input
                        type="text"
                        className="form-control"
                        value={formData.nombre}
                        onChange={(e) =>
                          setFormData({ ...formData, nombre: e.target.value })
                        }
                        required
                      />
                    </div>

                    {tipoUsuario === "cliente" && (
                      <>
                        <div className="mb-3">
                          <label className="form-label">
                            Correo Electrónico
                          </label>
                          <input
                            type="email"
                            className="form-control"
                            value={formData.correo}
                            onChange={(e) =>
                              setFormData({
                                ...formData,
                                correo: e.target.value,
                              })
                            }
                            required
                          />
                        </div>
                        <div className="mb-3">
                          <label className="form-label">Teléfono</label>
                          <input
                            type="text"
                            className="form-control"
                            value={formData.telefono}
                            onChange={(e) =>
                              setFormData({
                                ...formData,
                                telefono: e.target.value,
                              })
                            }
                            required
                          />
                        </div>
                      </>
                    )}

                    {tipoUsuario === "empleado" && (
                      <div className="mb-3">
                        <label className="form-label">Teléfono</label>
                        <input
                          type="text"
                          className="form-control"
                          value={formData.telefono}
                          onChange={(e) =>
                            setFormData({
                              ...formData,
                              telefono: e.target.value,
                            })
                          }
                          required
                        />
                      </div>
                    )}

                    <div className="mb-3">
                      <label className="form-label">Nombre de Usuario</label>
                      <input
                        type="text"
                        className="form-control"
                        value={formData.usuario.username}
                        onChange={(e) =>
                          setFormData({
                            ...formData,
                            usuario: {
                              ...formData.usuario,
                              username: e.target.value,
                            },
                          })
                        }
                        required
                      />
                    </div>

                    <div className="mb-3">
                      <label className="form-label">Contraseña</label>
                      <input
                        type="password"
                        className="form-control"
                        value={formData.usuario.password}
                        onChange={(e) =>
                          setFormData({
                            ...formData,
                            usuario: {
                              ...formData.usuario,
                              password: e.target.value,
                            },
                          })
                        }
                        required
                      />
                    </div>

                    <div className="d-flex justify-content-end gap-2">
                      <button
                        type="button"
                        className="btn btn-secondary"
                        onClick={() => setShowModal(false)}
                      >
                        Cancelar
                      </button>
                      <button type="submit" className="btn btn-success">
                        Crear Usuario
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
