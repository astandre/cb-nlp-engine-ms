import enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ModelType(enum.Enum):
    intent = 'intent'
    entities = 'entities'


class Agent(db.Model):
    """Agent

    An Agent refers to the main o domain or purpose of the chatbot.

    Attributes:
        :param @id: Id to populate the database.
        :param @name: This name must be unique to identify the Agent.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"<Agent {self.name}>"


class Model(db.Model):
    """Model

       A Model refers to every model trained with the tool fasttext.
       These Models are specialized in  identifying intents or a certain type of entity.

       Attributes:
        :param @id: Used to populate the database

        :param @name: Unique to identify the Agent

        :param @url: Url to obtain model

        :param @entity_name: Name used to represent the entity type

        :param @model_type: If model is for entities or intents

    .. todo:: When the model is not found, make this class to download model automatically.
       """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    url = db.Column(db.Text, nullable=False)
    entity_name = db.Column(db.String(80), nullable=True)
    model_type = db.Column(
        db.Enum(ModelType),
        default=ModelType.intent,
        nullable=False
    )
    threshold = db.Column(db.Float, nullable=False, default=0.0)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'),
                         nullable=False)
    agent = db.relationship('Agent', backref=db.backref('models', lazy=True))

    def __repr__(self):
        return f"<Model {self.name}>"


def init_database():
    """
    This function is used to initially populate the database
    """
    exists = Agent.query.all()
    if exists is None or len(exists) == 0:
        agent = Agent(name='opencampuscursos')
        intent_model = Model(name='opencampus_intents.ftz',
                             url='https://drive.google.com/file/d/1ASfQkukvCVgbtoR0QI1fUEU36bG8nCgC/view?usp=sharing',
                             model_type=ModelType.intent, agent=agent,
                             threshold=0.2)
        cursos_model = Model(name='opencampus_cursos.ftz',
                             url='https://drive.google.com/file/d/1ulAokHFjdLL-bEh3iUoTyxDUsIZTO3pP/view?usp=sharing',
                             model_type=ModelType.entities,
                             entity_name="http://127.0.0.1/ockb/course/ontology/Course",
                             agent=agent, threshold=0.2)

        db.session.add(agent)
        db.session.add(intent_model)
        db.session.add(cursos_model)
        db.session.commit()
