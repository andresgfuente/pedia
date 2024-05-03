import streamlit as st
import random
#As Langchain team has been working aggresively on improving the tool, we can see a lot of changes happening every weeek,
#As a part of it, the below import has been depreciated
#from langchain.llms import OpenAI

import time
import boto3
import json
import botocore.config
#When deployed on huggingface spaces, this values has to be passed using Variables & Secrets setting, as shown in the video :)
#import os
#os.environ["OPENAI_API_KEY"] = "sk-werwerwerrtertertwkFJwtwetwteWSig4ZY9AT"

#Function to return the response

frases_simpaticas = [
    "La vida es como una caja de chocolates, pero sin las calorías.",
    "Si te caes siete veces, levántate ocho. O mejor aún, consigue un cojín más cómodo.",
    "La sonrisa es el idioma universal, pero no olvides que el café también ayuda.",
    "La paciencia es una virtud, pero también lo es saber cuándo pedir pizza.",
    "No te preocupes por el mañana, a menos que seas un aspirador robótico.",
    "No importa cuán lento vayas, siempre estás adelantando a los que están en el sofá.",
    "La vida es como un videojuego, pero sin los botones de reinicio.",
    "No todo el que divaga está perdido, a menos que haya olvidado su GPS.",
    "Si la vida te da limones, haz limonada. Si te da sandía, invita a tus amigos a una fiesta.",
    "La felicidad está en las pequeñas cosas, como encontrar dinero en un abrigo viejo o que el semáforo cambie a verde justo cuando llegas.",
    "No soy perezoso, solo estoy en modo de ahorro de energía.",
    "No se puede comprar la felicidad, pero sí puedes comprar helado, que es casi lo mismo.",
    "La mente es como un paracaídas, funciona mejor cuando está abierta, pero también es útil tener un buen seguro.",
    "El dinero no puede comprar el amor, pero sí puede comprar una pizza, que es bastante parecido.",
    "La mejor manera de olvidar tus problemas es recordar que hay alguien por ahí con problemas peores. Y si no los hay, siempre puedes mirar Twitter."
]

def load_answer(question):
    prompt_text = f"""Human: Responde la siguiente pregunta: {question}.
    Assistant:
    """
    body = {
        "prompt": prompt_text,
        "max_tokens_to_sample": 2048,
        "temperature": 0.1,
        "top_k":250,
        "top_p": 0.2,
        "stop_sequences":["\n\nHuman:"]
    }
    body_titan= {
            "inputText": prompt_text,
            "textGenerationConfig": {
                "maxTokenCount": 4096,
                "stopSequences": [],
                "temperature": 0,
                "topP": 1
            }
        }

    # "text-davinci-003" model is depreciated, so using the latest one https://platform.openai.com/docs/deprecations
    bedrock=boto3.client("bedrock-runtime",region_name='us-east-1')
    response = bedrock.invoke_model(body=json.dumps(body),modelId="anthropic.claude-v2:1")   #anthropic.claude-v2:1     amazon.titan-text-express-v1
    response_content = response.get('body').read().decode('utf-8')
    response_data = json.loads(response_content)
    #response_data=response_data['results'][0]['outputText']
    respuesta= response_data["completion"].strip()
    #llm = OpenAI(model_name="gpt-3.5-turbo-instruct",temperature=0)

    #Last week langchain has recommended to use invoke function for the below please :)
    return respuesta

usuarios_permitidos = ['andresg','valeriar','sergioab']

def validar_usuario(username):
    if username in usuarios_permitidos:
        return True
    else:
        return False
def crear_sliders():
    st.sidebar.subheader("Configuración de Parámetros")
    st.session_state['temperature']  = st.sidebar.slider("Creatividad", min_value=0.0, max_value=1.0, step=0.1, value=0.1)
    st.session_state['longitud']  = st.sidebar.slider("Longitud de Respuesta", min_value=0, max_value=300, step=10, value=100)

def get_text():
    input_text = st.text_input("En que puedo ayudarte? ", key="input")
    return input_text    
    
if 'username' not in st.session_state:
    st.session_state['username'] ='' 
if 'respuesta' not in st.session_state:
    st.session_state['respuesta']=None

st.set_page_config(page_title="Itaupedia", page_icon=':robot:')
st.header('Bienvenidos a Itaupedia!')
#st.markdown("<h2 style='color:black;'>Bienvenidos a Itaupedia!</h2>", unsafe_allow_html=True)
#st.markdown("<h6 style='color:black;'>Itaupedia es un chatbot interno diseñado para facilitar el acceso y la búsqueda de información dentro de la organización. Alimentado por una amplia base de datos de documentos internos, Itaupedia puede responder preguntas sobre políticas, procedimientos, y cualquier otro tipo de información relevante para los empleados.</h6>", unsafe_allow_html=True)


st.sidebar.title('Ingrese su nombre de Usuario')
st.session_state['username']=st.sidebar.text_input('Username:',  type='default')
validado=False
if st.sidebar.button("Validar Usuario"):
        if validar_usuario(st.session_state['username'].lower()):
            st.sidebar.success('Usuario Validado Correctamente')
            validado=True
            #st.write(f"Bienvenido, {st.session_state['username']}!")        
        else:
            st.sidebar.error('Error en el ingreso del Nombre de Usuario')               
if validado:
    st.write('Bienvenido',st.session_state['username'])
user_input=get_text()

respondido=False
submit = st.button('Enviar pregunta')
if submit and validar_usuario(st.session_state['username']):
    frase_aleatoria = random.choice(frases_simpaticas)
    with st.spinner("📢"+frase_aleatoria):
        response = load_answer(user_input)
        st.subheader("Respuesta:")
        st.write(response)
        respondido=True
elif  not submit:
    pass
elif validar_usuario(st.session_state['username'])==False: # If username isn't defined yet
    st.warning("Por favor valide que se haya ingresado correctamente su usuario o que no este vacio el campo de Username.")
elif validar_usuario==False:
    st.write('Error en el ingreso del Nombre de Usuario')
else:
    st.write('Error en el ingreso del Nombre de Usuario')

def boton_carita(emocion, descripcion):
    if st.button(emocion):
        st.write(descripcion)
            

resultado=None
if respondido:
    time.sleep(5)
    st.subheader("Encuesta de satisfacción")
    st.write("Por favor, indique su grado de acuerdo con la siguiente afirmación:")
    col1, col2, col3 = st.columns(3)
    with col1:
        resultado=boton_carita("😊", "Ha sido de mucha ayuda.")

    with col2:
        resultado=boton_carita("😐", "Es aceptable.")
        
    with col3:
        resultado=boton_carita("😠", "No es satisfactorio.")

if resultado is not None:
    st.write("¡Gracias por tu feedback!")

    # Llamar a las funciones de los botones y colocarlos en las columnas respectivas
