from flask import Flask, request, render_template_string
from VIRTUAL import AsistenteVirtualSalud

app = Flask(__name__)
asistente = AsistenteVirtualSalud()

HTML_PAGE = """
<!DOCTYPE html>
<html lang=\"es\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>Asistente Virtual de Salud</title>
  <style>
    body {
      font-family: 'Open Sans', sans-serif;
      background-color: #f4f6f8;
      margin: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }

    .chat-container {
      background-color: #fff;
      width: 100%;
      max-width: 400px;
      border-radius: 16px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    .chat-header {
      background-color: #4a90e2;
      color: white;
      padding: 16px;
      font-size: 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .chat-messages {
      flex-grow: 1;
      padding: 16px;
      overflow-y: auto;
    }

    .message {
      margin-bottom: 12px;
      max-width: 80%;
      padding: 10px 14px;
      border-radius: 12px;
      line-height: 1.4;
    }

    .bot-message {
      background-color: #e0f0ff;
      align-self: flex-start;
    }

    .user-message {
      background-color: #d1f5d3;
      align-self: flex-end;
    }

    .chat-input {
      display: flex;
      padding: 12px;
      border-top: 1px solid #ccc;
      background-color: #fff;
    }

    .chat-input input {
      flex-grow: 1;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 20px;
      outline: none;
      margin-right: 8px;
    }

    .chat-input button {
      background-color: #4a90e2;
      border: none;
      color: white;
      padding: 10px 16px;
      border-radius: 20px;
      cursor: pointer;
    }

    .chat-input button:hover {
      background-color: #3a78c2;
    }

    .quick-replies {
      display: flex;
      gap: 8px;
      padding: 0 16px 16px;
      flex-wrap: wrap;
    }

    .quick-reply {
      background-color: #e6eaf1;
      border: none;
      border-radius: 16px;
      padding: 6px 12px;
      cursor: pointer;
      font-size: 14px;
    }

    .quick-reply:hover {
      background-color: #d1d9e6;
    }
  </style>
</head>
<body>
  <div class=\"chat-container\">
    <div class=\"chat-header\">
      <span>🩺 Asistente Virtual de Salud</span>
      <span style=\"font-size: 12px; color: #d4fbd7;\">🟢 En línea</span>
    </div>

    <div class=\"chat-messages\">
      <div class=\"message bot-message\">¡Hola, soy tu asistente médico virtual! ¿En qué puedo ayudarte hoy?</div>
      {% if resultado %}
        <div class=\"message bot-message\"><strong>Condiciones posibles:</strong> {{ resultado.condiciones }}</div>
        <div class=\"message bot-message\"><strong>Recomendaciones:</strong>
          <ul>
            {% for rec in resultado.recomendaciones %}
              <li>{{ rec }}</li>
            {% endfor %}
          </ul>
        </div>
      {% endif %}
    </div>

    <form method=\"POST\">
      <div class=\"chat-input\">
        <input type=\"text\" name=\"sintomas\" placeholder=\"Ej. fiebre, tos, dolor de cabeza\" required />
        <button type=\"submit\">➤</button>
      </div>
    </form>
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        sintomas = request.form['sintomas'].split(',')
        condiciones = asistente.analizar_sintomas(sintomas)
        recomendaciones = asistente.generar_recomendaciones(condiciones)
        resultado = {"condiciones": ", ".join(condiciones), "recomendaciones": recomendaciones}
    return render_template_string(HTML_PAGE, resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)