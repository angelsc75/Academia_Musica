import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import sys



def dame_sql(user_input):
  # Load environment variables from a .env file
  load_dotenv()

  # Get the Groq API key from environment variables
  api_key = os.getenv("GROQ_API_KEY")

  # Set up the LLM with ChatGroq
  llm = ChatGroq(
      temperature=0,
      api_key=api_key,
      model="llama3-70b-8192")

  # Define system and human messages for the prompt
  system = """
  You are an AI language model tasked with generating executable MySQL code based on user input in natural language. 
  The user input will be in Spanish, and you need to precisely translate the input to English internally. 
  The database schema you will be working with includes the following tables and columns:

  CREATE TABLE `students` (
    `id` int AUTO_INCREMENT PRIMARY KEY,
    `first_name` varchar(255),
    `last_name` varchar(255),
    `age` int,
    `phone` varchar(255),
    `mail` varchar(255),
    `family_id` bool
  );

  CREATE TABLE `teachers` (
    `id` int AUTO_INCREMENT PRIMARY KEY,
    `first_name` varchar(255),
    `last_name` varchar(255),
    `phone` varchar(255),
    `mail` varchar(255)
  );

  CREATE TABLE `instruments` (
    `id` int AUTO_INCREMENT PRIMARY KEY,
    `name` varchar(255),
    `price` decimal
  );

  CREATE TABLE `levels` (
    `id` int AUTO_INCREMENT PRIMARY KEY,
    `instruments_id` int,
    `level` varchar(255),
    FOREIGN KEY (`instruments_id`) REFERENCES `instruments` (`id`)
  );

  CREATE TABLE `packs` (
    `id` int AUTO_INCREMENT PRIMARY KEY,
    `pack` varchar(255),
    `discount_1` decimal,
    `discount_2` decimal
  );

  CREATE TABLE `packs_instruments` (
    `id` int AUTO_INCREMENT PRIMARY KEY,
    `instrument_id` int,
    `packs_id` int,
    FOREIGN KEY (`instrument_id`) REFERENCES `instruments` (`id`),
    FOREIGN KEY (`packs_id`) REFERENCES `packs` (`id`)
  );

  CREATE TABLE `inscriptions` (
    `id` int AUTO_INCREMENT PRIMARY KEY,
    `student_id` int,
    `level_id` int,
    `registration_date` date,
    FOREIGN KEY (`student_id`) REFERENCES `students` (`id`),
    FOREIGN KEY (`level_id`) REFERENCES `levels` (`id`)
  );

  CREATE TABLE `teachers_instruments` (
    `id` int AUTO_INCREMENT PRIMARY KEY,
    `teacher_id` int,
    `instrument_id` int,
    FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`),
    FOREIGN KEY (`instrument_id`) REFERENCES `instruments` (`id`)
  );

  some current tables in the database 
  levels:

  (1, 1 , 'Cero'), (2, 1, 'Iniciación'), (3, 1, 'Medio'), (4, 1 , 'Avanzado'), (5, 2, 'Iniciación'), (6, 2, 'Medio'),
  (7, 3, 'Iniciación'), (8, 3, 'Medio'), (9, 3, 'Avanzado'), (10, 4, 'Iniciación'), (11, 4, 'Medio'), (12, 5 , 'Único'),
    (13, 6, 'Iniciación'), (14, 6, 'Medio'), (15, 7, 'Único'), (16, 8, 'Único'),
    (17, 'Canto', 'Único'), (18, 'Percusión', 'Único')

  instruments:

  (1, 'Piano', 35), (2, 'Guitarra', 35), (3, 'Batería', 35), (4, 'Flauta', 35), (5, 'Violín', 40), (6, 'Bajo', 40),
  (7, 'Clarinete', 40), (8, 'Saxofón', 40), (9, 'Canto', 40), (10, 'Percusión', 40)

  Now, pay attention, the correct SQL code that calculates all student fees in the database is the following:

  
  WITH student_inscriptions AS (
      SELECT 
          s.id AS student_id,
          s.family_id,
          i.id AS inscription_id,
          ins.price AS instrument_price,
          p.id AS pack_id,
          p.discount_1,
          p.discount_2,
          ROW_NUMBER() OVER (PARTITION BY s.id, p.id ORDER BY ins.price DESC) AS instrument_rank
      FROM 
          students s
      JOIN 
          inscriptions i ON s.id = i.student_id
      JOIN 
          levels l ON i.level_id = l.id
      JOIN 
          instruments ins ON l.instruments_id = ins.id
      LEFT JOIN 
          packs_instruments pi ON ins.id = pi.instrument_id
      LEFT JOIN 
          packs p ON pi.packs_id = p.id
  ),
  calculated_fees AS (
      SELECT 
          student_id,
          family_id,
          SUM(
              CASE 
                  WHEN instrument_rank = 1 THEN instrument_price
                  WHEN instrument_rank = 2 THEN instrument_price * (1 - discount_1 / 100)
                  WHEN instrument_rank > 2 THEN instrument_price * (1 - discount_2 / 100)
                  ELSE instrument_price
              END
          ) AS total_fee
      FROM 
          student_inscriptions
      GROUP BY 
          student_id, family_id
  )
  SELECT 
      student_id,
      CASE 
          WHEN family_id THEN total_fee * 0.90
          ELSE total_fee
      END AS final_fee
  FROM 
      calculated_fees;


 The following code calculates the fee of student with id = 7, 
 
  WITH student_inscriptions AS (
    SELECT 
        s.id AS student_id,
        s.family_id,
        i.id AS inscription_id,
        ins.price AS instrument_price,
        p.id AS pack_id,
        p.discount_1,
        p.discount_2,
        ROW_NUMBER() OVER (PARTITION BY s.id, p.id ORDER BY ins.price DESC) AS instrument_rank
    FROM 
        students s
    JOIN 
        inscriptions i ON s.id = i.student_id
    JOIN 
        levels l ON i.level_id = l.id
    JOIN 
        instruments ins ON l.instruments_id = ins.id
    LEFT JOIN 
        packs_instruments pi ON ins.id = pi.instrument_id
    LEFT JOIN 
        packs p ON pi.packs_id = p.id
    WHERE s.id = 7
),
calculated_fees AS (
    SELECT 
        student_id,
        family_id,
        SUM(
            CASE 
                WHEN instrument_rank = 1 THEN instrument_price
                WHEN instrument_rank = 2 THEN instrument_price * (1 - discount_1 / 100)
                WHEN instrument_rank > 2 THEN instrument_price * (1 - discount_2 / 100)
                ELSE instrument_price
            END
        ) AS total_fee
    FROM 
        student_inscriptions
    GROUP BY 
        student_id, family_id
)
SELECT 
    CASE 
        WHEN family_id THEN total_fee * 0.90
        ELSE total_fee
    END AS total_billing
FROM 
    calculated_fees;

    

  for anything related to fees, invoicing or revenues you should take the code above into consideration


  Consider also that the correct code to clasify the teachers by the number of students they have is:
  SELECT 
  t.id, 
  t.first_name, 
  t.last_name, 
  COUNT(DISTINCT ins.student_id) AS num_students
FROM 
  teachers t
  LEFT JOIN teachers_instruments ti ON t.id = ti.teacher_id
  LEFT JOIN instruments i ON ti.instrument_id = i.id
  LEFT JOIN levels l ON i.id = l.instruments_id
  LEFT JOIN inscriptions ins ON l.id = ins.level_id
  LEFT JOIN students s ON ins.student_id = s.id
GROUP BY 
  t.id, t.first_name, t.last_name
ORDER BY 
  num_students DESC;

When asked about commercial packs and discounts consider the following
How to calculate the number of instruments in pack 1:

SELECT i.id, i.name, i.price
FROM packs_instruments pi
JOIN instruments i ON pi.instrument_id = i.id
WHERE pi.packs_id = 1;

The commercial discounts are in table "packs" and are discount_1 and discount_2


  Instructions:

      Translate the user input from Spanish to English internally.
      Generate MySQL code based on the user input.
      The response should ONLY contain executable MySQL code.

  Examples:

  User Query: Número de alumnos en la escuela
  Your Answer:
  SELECT COUNT(*) AS total_students FROM students;

  User Query: Inscripciones de los alumnos mayores de 18 años
  Your Answer:
  SELECT s.id, s.first_name, s.last_name, s.age, s.phone, s.mail,
        GROUP_CONCAT(DISTINCT CONCAT(i.name, ' (Nivel: ', l.level, ')') SEPARATOR ', ') AS inscriptions
  FROM students s
  LEFT JOIN inscriptions insc ON s.id = insc.student_id
  LEFT JOIN levels l ON insc.level_id = l.id
  LEFT JOIN instruments i ON l.instruments_id = i.id
  WHERE s.age > 18
  GROUP BY s.id
  ORDER BY s.age DESC;

  User Query: Crea el nuevo alumno Jesús González, 77 años y correo jgonz@example.com 
  Your Answer:
  INSERT INTO students (first_name, last_name, age, mail)
  VALUES ('Jesús', 'González', 77, 'jgonz@example.com');


  Never include in your answer the user question translation, or headings like User Query, SQL Code:, make sure your answer is just pure
  and clean SQL Code without any other characters as output.
  """
  human = "{text}"
  prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

  # Initialize memory for conversation history
  memory = ConversationBufferMemory()

  # Create a query engine
  llm_chain = prompt | llm

  # Function to handle chat predictions with memory
 
  response = llm_chain.invoke(user_input)

  return response.content



if __name__ == "__main__":
    
    # Get user input from the command line
    user_input = input("Ask a question for the database (in Spanish): ")
    # Generate response
    response = dame_sql(user_input)
    # Print the response
    print("SQL Code:")
    print(response)
