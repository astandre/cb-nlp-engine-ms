import enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ModelType(enum.Enum):
    intent = 'intent'
    entities = 'entities'


class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"<Agent {self.name}>"


class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    url = db.Column(db.Text, nullable=False)
    entity_name = db.Column(db.String(80), nullable=True)
    model_type = db.Column(
        db.Enum(ModelType),
        default=ModelType.intent,
        nullable=False
    )
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'),
                         nullable=False)
    agent = db.relationship('Agent', backref=db.backref('models', lazy=True))

    def __repr__(self):
        return f"<Model {self.name}>"


def init_database():
    exists = Agent.query.all()
    if exists is None or len(exists) == 0:
        # return
        agent = Agent(name='opencampuscursos')
        intent_model = Model(name='opencampus_intents.ftz', url='asdasd', model_type=ModelType.entities, agent=agent)
        cursos_model = Model(name='opencampus_cursos.ftz', url='asdasd', model_type=ModelType.entities,
                             entity_name="CURSOS",
                             agent=agent)

        db.session.add(agent)
        db.session.add(intent_model)
        db.session.add(cursos_model)
        db.session.commit()
