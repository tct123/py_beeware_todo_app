import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, LEFT
from sqlalchemy import (
    Integer,
    String,
    Float,
    create_engine,
    MetaData,
    Table,
    text,
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

COLORS_DATA = {"Blue": ["#9DB2BF", "#526D82", "#27374D", "#27374D"]}


class ToDoApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.data = []
        self.gui(self)

    def gui(self, widget):
        self.main_box = toga.Box(style=Pack(direction=COLUMN,padding=5,alignment=LEFT,background_color=COLORS_DATA["Blue"][0]))
        self.buttons_box = toga.Box(style=Pack(direction=ROW,padding=5,alignment=LEFT,background_color=COLORS_DATA["Blue"][1]))
        self.todo_box = toga.Box(style=Pack(direction=COLUMN,padding=5,alignment=LEFT,background_color=COLORS_DATA["Blue"][0]))
        self.todo_container = toga.ScrollContainer(content=self.todo_box, style=Pack(flex=1))
        self.todo_text = toga.TextInput(placeholder="Task description",style=Pack(padding=5, width=300, alignment=LEFT),)
        self.add_todo = toga.Button(text="Add task",on_press=lambda widget: self.add_task(task=self.todo_text.value),style=Pack(padding=5, width=150, alignment=LEFT, flex=1))
        self.buttons_box.add(self.todo_text, self.add_todo)
        self.main_box.add(self.buttons_box, self.todo_container)
        self.main_window.content = self.main_box
        self.fill_list_from_db()
        if len(self.data) > 0:
            self.build_content()
        self.main_window.show()

    def add_task(self, task):
        self.data.append(task)
        print(self.data)
        self.save_items_to_db(task)
        self.build_task(task)

    def build_content(self):
        for item in self.data:
            self.build_task(task=item)

    def build_task(self, task):
        todo = toga.Label(text=task)
        todo_frame = toga.Box(style=Pack(direction=COLUMN,padding=5,alignment=LEFT,background_color=COLORS_DATA["Blue"][2]))
        todo_box = toga.Box(style=Pack(direction=COLUMN,padding=5,alignment=LEFT,background_color=COLORS_DATA["Blue"][1]))
        todo_box.add(todo)
        todo_frame.add(todo_box)
        self.todo_box.add(todo_frame)
        
    def save_items_to_db(self, item):
        Base = declarative_base()
        class Todos(Base):
            __tablename__ = "todos"
            id = Column(Integer, primary_key=True, autoincrement=True)
            text = Column(String, nullable=False)

        self.paths.data.mkdir(exist_ok=True, parents=True)
        path = str(self.paths.data)
        print(path)
        engine = create_engine(f"sqlite:///{path}/todos.db")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        todo = Todos(text=item)
        session.add(todo)
        session.commit()
        session.close()
    
    def fill_list_from_db(self):
        Base = declarative_base()
        class Todos(Base):
            __tablename__ = "todos"
            id = Column(Integer, primary_key=True, autoincrement=True)
            text = Column(String, nullable=False)

        self.paths.data.mkdir(exist_ok=True, parents=True)
        path = str(self.paths.data)
        print(path)
        engine = create_engine(f"sqlite:///{path}/todos.db")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        todos = session.query(Todos).all()
        for todo in todos:
            self.data.append(todo.text)

def main():
    return ToDoApp()
