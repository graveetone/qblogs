from wtforms import Form, StringField, TextAreaField

class PostForm(Form):
    title = StringField("Назва")
    text = TextAreaField("Текст")
    tags = StringField("Теги(через пробіл)")
