#=============================== IMPORTS ZONE ===============================
from flask import render_template,request,redirect,abort,Request,url_for,jsonify
from app.app import app,SearchForm,MAX_SUGGESTION
import myLibs.debug_sys as debug_sys
import myLibs.search_engine as search_engine


#=============================== INIT ZONE ===============================
search_engine.ECO = True


#=============================== MAIN ZONE ===============================
# Display a listing of the resource.
def index():
    poke_name_form = SearchForm()
    return render_template('dashboard_fr/index.html', form = poke_name_form)


# Show the form for creating a new resource.
def create():abort(404)


# Store a newly created resource in storage.
def store(request : Request):abort(404)


# Display the specified resource.
def show(id):
    poke_name_form = SearchForm()
    poke_infos = search_engine.infos_on(id)
    debug_sys.log('INFO',str(poke_infos))
    try:
        if poke_infos['status'] == 404:
            debug_sys.log('404',f'''{poke_infos['message']} : "/{id}"''')
        return f'''404 : {poke_infos['message']}"'''
    except:
        pass
    intitule = ['Vie','Attaque','Deffense','Attaque spéciale','Deffense spéciale','Vitesse']
    stats = [{'intitule': i, 'stat': s, 'value': v} for i, s, v in zip(intitule, poke_infos['stats'].keys(), poke_infos['stats'].values())]
    return render_template('dashboard_fr/pokemon_view.html', form = poke_name_form, poke_infos = poke_infos, stats=stats)


# Show the form for editing the specified resource.
def edit(id):abort(404)


# Update the specified resource in storage.
def update(id):abort(404)

# Remove the specified resource from storage.
def destroy(id):abort(404)


def search():
    poke_name_form = SearchForm()
    if poke_name_form.validate_on_submit():
        search_result = search_engine.search(poke_name_form.recherche.data,'fr')[0]
        debug_sys.log('SEARCH',f'''{poke_name_form.recherche.data} => {search_result}''')
        return redirect(url_for('fr', id = search_result))
    else:
        abort(404)

def suggest():
    query = request.args.get('query')
    suggestions = []
    for id in search_engine.search(query,'fr')[:MAX_SUGGESTION]:
        information = search_engine.infos_on(id)
        suggestions.append((information['name']['fr'],id,information['sprites']['regular']))
    debug_sys.log('SUGGEST', f'query={query} : ' + str(suggestions))
    return jsonify(suggestions)