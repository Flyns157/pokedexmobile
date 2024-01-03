from app.app import app


def resource(path: str, controller):
    @app.route(f'{path}')
    def index(): controller.index()
    @app.route(f'{path}/<int:id>')
    def show(id): controller.show(id)
    @app.route(f'{path}/create', methods=['GET', 'POST'])
    def create(): controller.create()
    @app.route(f'{path}/<int:id>/edit', methods=['GET', 'POST'])
    def editedit(id): controller.edit(id)
    @app.route(f'{path}/<int:id>/update', methods=['GET', 'POST'])
    def update(id): controller.update(id)
    @app.route(f'{path}/<int:id>/delete', methods=['GET', 'POST'])
    def delete(id): controller.delete(id)
