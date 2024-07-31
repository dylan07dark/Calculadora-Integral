from flask import Flask, render_template, request, jsonify
from sympy import Symbol, sympify, latex, integrate
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular_indefinida', methods=['POST'])
def calcular_indefinida():
    x = Symbol('x')
    y1 = request.form['ecuacion']
    try:
        y1 = sympify(y1)
        resultado = y1.integrate(x)
        procedimiento = fr"Integral indefinida de f(x): \( \int {latex(y1)} \, dx \)<br>Antiderivada: \( {latex(resultado)} + C \)"
        return jsonify({
            'procedimiento': procedimiento,
            'resultado': f"{latex(resultado)} + C",
        })
    except Exception as e:
        return jsonify({
            'error': f"Error: {str(e)}"
        })

@app.route('/calcular_definida', methods=['POST'])
def calcular_definida():
    x = Symbol('x')
    y1 = request.form['ecuacion_definida']
    limite_inferior = request.form['limite_inferior']
    limite_superior = request.form['limite_superior']
    
    try:
        y1 = sympify(y1)
        limite_inferior = float(limite_inferior)
        limite_superior = float(limite_superior)
        resultado = y1.integrate((x, limite_inferior, limite_superior))
        procedimiento = fr"Integral definida de f(x): \( \int_{{{limite_inferior}}}^{{{limite_superior}}} {latex(y1)} \, dx \)<br>Procedimiento:<br>\[ {latex(y1.integrate(x))} \]<br>Resultado: \( {latex(resultado)} \)"
        return jsonify({
            'resultado': latex(resultado),
            'procedimiento': procedimiento
        })
    except Exception as e:
        return jsonify({
            'error': f"Error: {str(e)}"
        })

@app.route('/graficar_volumen', methods=['POST'])
def graficar_volumen():
    x = Symbol('x')
    f1 = request.form['primera_expresion']
    f2 = request.form['segunda_expresion']
    limite_inferior = float(request.form['limite_inferior_vol'])
    limite_superior = float(request.form['limite_superior_vol'])

    try:
        f1 = sympify(f1)
        f2 = sympify(f2)
        x_vals = np.linspace(limite_inferior, limite_superior, 400)
        y_vals_f1 = np.array([float(f1.evalf(subs={x: val})) for val in x_vals])
        y_vals_f2 = np.array([float(f2.evalf(subs={x: val})) for val in x_vals])

        plt.figure(figsize=(8, 6))
        plt.fill_between(x_vals, y_vals_f1, y_vals_f2, where=(y_vals_f1 > y_vals_f2), color='skyblue', alpha=0.4)
        plt.fill_between(x_vals, y_vals_f1, y_vals_f2, where=(y_vals_f1 < y_vals_f2), color='salmon', alpha=0.4)
        plt.plot(x_vals, y_vals_f1, label='f1(x)')
        plt.plot(x_vals, y_vals_f2, label='f2(x)')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Área entre dos curvas')
        plt.legend()
        plt.grid(True)

        img = io.BytesIO()
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

        return jsonify({
            'volumen_img': img_base64
        })
    except Exception as e:
        return jsonify({
            'error': f"Error: {str(e)}"
        })

@app.route('/calcular_area', methods=['POST'])
def calcular_area():
    x = Symbol('x')
    f = request.form['ecuacion_area']
    limite_inferior = float(request.form['limite_inferior_area'])
    limite_superior = float(request.form['limite_superior_area'])

    try:
        f = sympify(f)
        x_vals = np.linspace(limite_inferior, limite_superior, 400)
        y_vals = np.array([float(f.evalf(subs={x: val})) for val in x_vals])

        area = float(f.integrate((x, limite_inferior, limite_superior)))
        plt.figure(figsize=(8, 6))
        plt.fill_between(x_vals, y_vals, color='skyblue', alpha=0.4)
        plt.plot(x_vals, y_vals, label='f(x)')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Área bajo la curva')
        plt.legend()
        plt.grid(True)

        img = io.BytesIO()
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

        return jsonify({
            'area_img': img_base64,
            'area_result': latex(area)
        })
    except Exception as e:
        return jsonify({
            'error': f"Error: {str(e)}"
        })

@app.route('/calcular_longitud_arco', methods=['POST'])
def calcular_longitud_arco():
    try:
        # Obtén los datos del formulario
        ecuacion = request.form.get('ecuacion_longitud')
        limite_inferior = float(request.form.get('limite_inferior_arco'))
        limite_superior = float(request.form.get('limite_superior_arco'))
        
        # Validar que los datos sean correctos
        if not ecuacion or limite_inferior is None or limite_superior is None:
            return jsonify({'error': 'Datos de entrada no válidos'}), 400

        # Crear un rango de valores x
        x = np.linspace(limite_inferior, limite_superior, 400)
        # Evaluar la ecuación para obtener los valores y
        y = eval(ecuacion)  # Asegúrate de que esto sea seguro en tu entorno
        
        # Calcular la longitud del arco
        dx = x[1] - x[0]
        longitud = np.sum(np.sqrt(1 + np.gradient(y, dx)**2) * dx)
        
        # Crear la gráfica
        fig, ax = plt.subplots()
        ax.plot(x, y, label=f'Longitud del Arco: {longitud:.2f}')
        ax.set_title('Longitud del Arco')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.legend()
        
        # Convertir la gráfica a imagen base64
        img = io.BytesIO()
        plt.savefig(img, format='png')
        plt.close(fig)
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
        
        return jsonify({'longitud_arco_img': img_base64})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
