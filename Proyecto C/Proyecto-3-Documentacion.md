# Proyecto 3: Abordaje Ético mediante Modelos de Lenguaje Natural

**INSTITUTO TECNOLOGICO DE MEXICO**  
**CAMPUS MORELIA**  
**INGENIERIA EN SISTEMAS COMPUTACIONALES**  
**Nombre del estudiante:** Luis Martín Maya Villalpando  
**Materia:** Inteligencia Artificial
**Profesor: Jesus Eduardo Alcaraz Chavez**
**Fecha:** {date}

---

## Objetivo del Proyecto

Este proyecto tiene como finalidad explorar dos dilemas éticos contemporáneos —el aborto y la eutanasia— utilizando tecnologías de lenguaje natural como Ollama. Se busca integrar el análisis ético con herramientas de inteligencia artificial, generando tanto un documento estructurado como un video explicativo. El proyecto incluye el uso de **embeddings** y **fine-tuning** para enriquecer las respuestas del modelo ante preguntas complejas en contextos sensibles.

---

## Marco Teórico

### 🔹 Modelos de Lenguaje Natural

Los **modelos de lenguaje natural** (LLMs, por sus siglas en inglés) son sistemas de inteligencia artificial entrenados con grandes cantidades de texto para comprender y generar lenguaje humano. Modelos como **LLaMA**, **Mistral**, **GPT**, entre otros, permiten tareas como responder preguntas, generar texto, resumir información o analizar argumentos éticos.

### 🔹 Fine-Tuning

El **fine-tuning** es una técnica que permite personalizar un modelo de lenguaje ya preentrenado para tareas específicas. En este proyecto, se plantea ajustar un modelo general para que:

- Conozca en profundidad los temas de aborto y eutanasia.
- Aprenda a responder respetando principios éticos y filosóficos.
- Sea más sensible al contexto moral, legal y humano de cada caso.

Este proceso implica exponer al modelo a ejemplos relevantes y ajustar sus pesos internos para que sus respuestas se alineen con el dominio deseado.

### 🔹 Embeddings

Los **embeddings** son representaciones numéricas del texto que permiten a un modelo “entender” relaciones semánticas entre conceptos. Por ejemplo:

- "interrupción del embarazo" y "terminación del embarazo" tendrán embeddings cercanos.
- "muerte digna" y "eutanasia pasiva" pueden relacionarse por proximidad semántica.

En este proyecto, los embeddings permiten que el modelo busque respuestas en documentos cargados, sin necesidad de entrenamiento adicional completo (enfoque RAG: _Retrieval-Augmented Generation_).

### 🔹 Ollama

**Ollama** es una herramienta que facilita la ejecución de modelos de lenguaje grandes en entornos locales. Algunas ventajas:

- Soporta modelos como LLaMA3, Mistral o Gemma.
- Permite el uso de fine-tuning e integración con frameworks como Anything LLM.
- Es ideal para tareas privadas o educativas, sin depender de servidores externos.

Con Ollama, entrenaremos localmente un modelo que pueda comprender mejor el lenguaje moral y bioético de los documentos utilizados.

---

## Herramientas Tecnológicas Utilizadas

- **Modelo base:** Mistral o LLaMA3, gestionado desde Ollama.
- **Framework:** Anything LLM para orquestación del conocimiento.
- **Técnicas aplicadas:**
  - Generación de embeddings a partir de documentos base (.pdf, .md).
  - Fine-tuning temático con corpus personalizado de bioética.
  - Prompting ético específico para temas sensibles.

---

## Tema Central 1:

### “La autonomía personal frente al inicio de la vida: el dilema del aborto en contextos éticos y tecnológicos”

- A continucacion se muestra las respuestas que dio el modelo ya entrenado, hacia algunos de los cuestionamientos

3. ¿Qué principios éticos (utilitarismo, deontología, ética del cuidado) pueden respaldar o rechazar el aborto inducido?
   ![Imagen 1](img/Pregunta-3.png)
4. ¿Puede una inteligencia artificial participar de forma ética en decisiones sobre aborto?
   ![Imagen 2](img/Pregunta-1.png)

5. ¿Qué riesgos éticos implica delegar información médica sensible a sistemas automatizados?
   ![Imagen 3](img/Pregunta-2.png)

-Podemos observar entonces que dado a las respuestas, el entrenamiento ha sido algo bueno dado que las respuestas que genera se encuentran dentro del contexto dado
sin embargo son un poco generales podemos notar entonces tambien que no toma ninguna postura, si no que tiene uns postura neutral, en la mayoria de los casos la busqueda que hacia sobre los dicumentos con los que se entreno eran del 40 al 60 porciento.

#### Implementación en el modelo:

- Documentos cargados con información legal, filosófica y médica sobre aborto.
- Se utilizaron embeddings para alimentar el modelo con respuestas basadas en datos reales.
- El fine-tuning permite que el modelo entienda el lenguaje técnico y ético del debate.

---

## Tema Central 2:

### “Eutanasia y dignidad humana: decisiones de vida o muerte en la era de la inteligencia artificial”

#### Preguntas guía:

- A continucacion se muestra las respuestas que dio el modelo ya entrenado, hacia algunos de los cuestionamientos

3. ¿Qué papel podrían (o no deberían) tener los sistemas de inteligencia artificial en este tipo de decisiones?
   ![Imagen 4](img/Pregunta-4.png)
4. ¿Qué sucede cuando el deseo de morir entra en conflicto con creencias religiosas, leyes o protocolos médicos?
   ![Imagen 5](img/Pregunta-5.png)
5. ¿Se puede hablar de una “muerte digna” sin considerar el contexto emocional y humano?
   ![Imagen 5](img/Pregunta-6.png)

-Podemos observar entonces que dado a las respuestas, el entrenamiento ha sido algo bueno dado que las respuestas que genera se encuentran dentro del contexto dado
sin embargo son un poco generales podemos notar entonces tambien que no toma ninguna postura, si no que tiene uns postura neutral, en la mayoria de los casos la busqueda que hacia sobre los dicumentos con los que se entreno eran del 40 al 60 porciento.

#### Implementación en el modelo:

- Se usaron documentos ético-legales sobre eutanasia y dignidad humana.
- El modelo responde teniendo en cuenta factores humanos, emocionales y culturales.
- El fine-tuning reforzó principios bioéticos clave para evitar sesgos inadecuados.

---

## 📽️ Resultados Esperados del Video

- Presentación visual del uso de Ollama, embeddings y fine-tuning.
- Demostración de respuestas del modelo a preguntas éticas complejas.
- Reflexión crítica sobre el uso responsable de IA en contextos humanos.

**Link Video:** https://itecm-my.sharepoint.com/:v:/g/personal/l20121013_morelia_tecnm_mx/EUsIKAVoFzJKnkZKWrUUvf0BcBiv4ayBZbC-0oWjEaz_yg?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=qH0smG

---

## Conclusión

Este proyecto demuestra cómo los modelos de lenguaje, al ser ajustados correctamente, pueden participar en discusiones éticas complejas, aportando claridad y contexto. La integración de IA en estos temas debe hacerse con responsabilidad, considerando no solo la precisión técnica, sino también la sensibilidad moral que implican decisiones como el aborto o la eutanasia.

---
