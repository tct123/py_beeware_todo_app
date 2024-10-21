import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, LEFT
from sqlalchemy import Integer, String, Float, create_engine, MetaData, Table, text, create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

COLORS_DATA = {"Blue": ["#9DB2BF", "#526D82", "#27374D", "#27374D"]}


class ToDoApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.data = []
        self.gui(self)

    def gui(self, widget):
        self.main_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=5,
                alignment=LEFT,
                background_color=COLORS_DATA["Blue"][0],
            )
        )

        self.buttons_box = toga.Box(
            style=Pack(
                direction=ROW,
                padding=5,
                alignment=LEFT,
                background_color=COLORS_DATA["Blue"][1],
            )
        )

        self.todo_text = toga.TextInput(
            placeholder="Task description",
            style=Pack(padding=5, width=300, alignment=LEFT),
        )
        self.add_todo = toga.Button(
            text="Add task",
            on_press=self.add_task,
            style=Pack(padding=5, width=150, alignment=LEFT),
        )
        self.buttons_box.add(self.todo_text, self.add_todo)
        self.main_box.add(self.buttons_box)

        self.main_window.content = self.main_box
        self.main_window.show()

    def add_task(self, widget):
        todo = toga.Label(text=self.todo_text.value)
        todo_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=5,
                alignment=LEFT,
                background_color=COLORS_DATA["Blue"][1],
            )
        )
        self.data.append({
            'todo': todo,
            'todo_box': todo_box
        })
        print(self.data)
        todo_box.add(todo)
        self.save_items_to_db(self.todo_text.value)
        self.main_box.add(todo_box)


    def save_items_to_db(self, item):
        Base = declarative_base()
        
        class Todos(Base):
            __tablename__ = 'todos'
            id = Column(Integer, primary_key=True, autoincrement=True)
            text = Column(String, nullable=False)
        
        print(self.paths.data)
        self.paths.data.mkdir(exist_ok=True, parents=True)
        path = str(self.paths.data)
        engine = create_engine(f'sqlite:///{path}/todos.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        todo = Todos(text=item)
        session.add(todo)
        session.commit()
        session.close()



def main():
    return ToDoApp()

