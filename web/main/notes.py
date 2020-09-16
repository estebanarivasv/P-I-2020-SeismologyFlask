"""
RUTA
"""
def sensores():
    form = UserToEditForm()   # FIlter form
    url = current_app.config["API_URL"] + "/users"
    query = makeRequest("GET", url, authenticated_user=True)
    # Cargamos los usuarios en el formulario
    data = {}
    if form.validate_on_submit():
        if form.yearFrom.data != None:
            data["year"] = form.yearFrom.data
    json.dumps(data)
    query = makeRequest("GET", url, authenticated_user=True, data=data)
    if query.status_code == 200:
        sensors = json.loads(query.text)["sensors"]
        return render_template("..", sensors=sensors, form=form)


"""
FORMULARIOS
"""
class ProjectFilterForm():
    name = StringField("name", [
        validators.optional()
    ])
    yearFrom = DatetimeField("from year", [
        validators.optional()
    ],
    format="%Y")
    page = HiddenField("page")
    submit = SubmitField()

"""
BACKEND PAGINATION RESULTS
"""
return jsonify({
    'projects': [project.to_json() for project in projects.items],
    'total_projects': projects.total,
    'total_pages'
})