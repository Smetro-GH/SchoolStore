from website import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Asegurarse de que el directorio instance existe
    if not os.path.exists('instance'):
        os.makedirs('instance')
    
    # Ejecutar la aplicación
    app.run(debug=True, host='0.0.0.0', port=5000)

    