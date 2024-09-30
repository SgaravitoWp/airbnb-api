



# class SuccessTemplate:

#     def __init__(self,
#                  message,
#                  success,
#                  status_code,
#                  data = None) -> None:
#         self.message = message
#         self.success = success
#         self.status_code = status_code
#         self.data = data



#     def  hola():
#         pass


def define_response(name):
    class NuevaClase:
        def __init__(self, mensaje):
            self.mensaje = mensaje

        def mostrar_mensaje(self):
            return self.mensaje

    NuevaClase.__name__ = nombre  # Cambiar el nombre de la clase
    return NuevaClase