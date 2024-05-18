NO_PK_PROVIDED = {'pk': 'No pk provided.'}


def _object_not_exist(model):
    return {f'{model.__name__}': 'Object does not exist'}
OBJECT_NOT_EXIST = _object_not_exist