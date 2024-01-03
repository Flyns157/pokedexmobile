from app.app import app


def resource(path: str, controller):
    @app.route(f'{path}', methods=['GET'])
    def index(): controller.index()
    @app.route(f'{path}/<int:id>', methods=['GET'])
    def show(id): controller.show(id)
    @app.route(f'{path}/create', methods=['GET'])
    def create(): controller.create()
    @app.route(f'{path}/<int:id>/edit', methods=['GET'])
    def editedit(id): controller.edit(id)
    @app.route(f'{path}/<int:id>/update', methods=['POST'])
    def update(id): controller.update(id)
    @app.route(f'{path}/<int:id>/delete', methods=['POST'])
    def delete(id): controller.delete(id)
