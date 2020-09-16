from flask_wtf import FlaskForm
import wtforms as wtf

class TablePagination(FlaskForm):
    first_page = wtf.SubmitField(label="<<")
    first_page_num = wtf.HiddenField()
    prev_page = wtf.SubmitField(label="<")
    prev_page_num = wtf.HiddenField()
    next_page = wtf.SubmitField(label=">")
    next_page_num = wtf.HiddenField()
    last_page = wtf.SubmitField(label=">>")
    last_page_num = wtf.HiddenField()


